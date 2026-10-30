"""Candidate 0.16. Frozen-data-only comparison; NOT_RUN. No SUT/emitter import."""
import hashlib
import json
import re
from expected_bounds import Budgets, guard, parse, canonical
from expected_admission import require_admission
from expected_wire_review import validate_slots

HEX64 = re.compile(r"[0-9a-f]{64}")
RULES = {f"SNAP-P0{i}": f"candidate-0.15/P0{i}" for i in range(1, 6)}


def sha(value):
    return hashlib.sha256(value).hexdigest()


def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def record_check(record, limits=None):
    limits = limits or Budgets()
    guard(record, limits)
    if type(record) is not dict:
        raise ValueError("record object")
    if set(record) != {"id", "hex", "length", "sha256", "error"}:
        raise ValueError("record fields")
    if type(record["id"]) is not str:
        raise ValueError("record ID")
    # All 428 snapshot slots are successful-byte expectations. Negative controls
    # are source tests, never substituted error records for missing snapshot bytes.
    if record["error"] is not None:
        raise ValueError("snapshot slot requires bytes, not an error")
    h = record["hex"]
    if type(h) is str and len(h) > limits.wire_bytes * 2:
        raise ValueError("record wire budget")
    if type(h) is not str or re.fullmatch(r"(?:[0-9a-f]{2})*", h) is None:
        raise ValueError("canonical hex required")
    raw = bytes.fromhex(h)
    if type(record["length"]) is not int or record["length"] != len(raw):
        raise ValueError("length mismatch")
    if record["sha256"] != sha(raw):
        raise ValueError("digest mismatch")


def _validate_claims(raw, *, binding, approval, limits):
    """Pure claim checks after external admission; not an authority or observer API."""
    if type(raw) is not bytes or len(raw) > 8388608:
        raise ValueError("input bound")
    required = {"bundle_sha256", "manifest_sha256", "capsule_sha256", "sources",
                "required_slot_ids", "interpretations", "bundle_path"}
    if type(binding) is not dict or set(binding) != required:
        raise ValueError("trusted binding required")
    for k in ("bundle_sha256", "manifest_sha256", "capsule_sha256"):
        if type(binding[k]) is not str or HEX64.fullmatch(binding[k]) is None:
            raise ValueError("unresolved external hash")
    if sha(raw) != binding["bundle_sha256"]:
        raise ValueError("bundle hash drift")
    if not binding["bundle_path"] or binding["bundle_path"] == "UNRESOLVED":
        raise ValueError("explicit external read-only path required")
    if type(approval) is not dict or set(approval) != {
            "reviewer", "decision_id", "timestamp", "state", "binding", "signature"}:
        raise ValueError("external approval required")
    if any(type(approval[k]) is not str or not approval[k] or approval[k] == "UNRESOLVED"
           for k in ("reviewer", "decision_id", "timestamp", "signature")):
        raise ValueError("review identity")
    if approval["state"] != "APPROVED" or approval["binding"] != binding:
        raise ValueError("external approval drift")
    bundle = parse(raw, limits)
    if canonical(bundle, limits) != raw:
        raise ValueError("noncanonical JSON")
    if set(bundle) != {"spec", "contract", "bundle_id", "state", "sources",
                       "interpretations", "generation", "review", "records"}:
        raise ValueError("bundle fields")
    if (bundle["spec"] != "MPT-FROZEN-COMPARE@1" or
            bundle["contract"] != "MPT-SNAPSHOT@1" or
            bundle["bundle_id"] != "CANDIDATE-0.16-EXPECTED@1" or
            bundle["state"] != "REVIEWED_FROZEN"):
        raise ValueError("version or freeze state")
    if set(binding["sources"]) != {"schema", "template", "oracle", "emitter",
                                   "interpretations", "vectors"}:
        raise ValueError("source inventory")
    if any(type(v) is not str or HEX64.fullmatch(v) is None for v in binding["sources"].values()):
        raise ValueError("source hash")
    if bundle["sources"] != binding["sources"]:
        raise ValueError("schema/recipe/source drift")
    if bundle["interpretations"] != RULES or binding["interpretations"] != RULES:
        raise ValueError("pending or divergent interpretation")
    if bundle["review"] != {k: approval[k] for k in ("reviewer", "decision_id", "timestamp")}:
        raise ValueError("human review mismatch")
    if set(bundle["generation"]) != {"environment", "run_id"} or any(
            type(v) is not str or not v or v == "UNRESOLVED" for v in bundle["generation"].values()):
        raise ValueError("generation provenance")
    ids = binding["required_slot_ids"]
    if len(ids) != 428 or len(set(ids)) != 428:
        raise ValueError("trusted inventory must identify all 428 slots")
    records = bundle["records"]
    if type(records) is not list or len(records) != 428:
        raise ValueError("incomplete bundle")
    found = {}
    for record in records:
        record_check(record, limits)
        if record["id"] in found:
            raise ValueError("duplicate slot")
        found[record["id"]] = record
    if set(found) != set(ids):
        raise ValueError("missing/extra slot")
    if list(found) != sorted(ids):
        raise ValueError("noncanonical record order")
    return found



def validate_frozen(raw, *, binding, approval, schema_bytes, template_bytes,
                    admission=None, budgets=None):
    if budgets is None:
        raise ValueError("explicit externally approved budget required")
    budgets.check()
    if type(raw) is not bytes or len(raw) > budgets.input_bytes:
        raise ValueError("input budget")
    for source in (schema_bytes, template_bytes):
        if type(source) is not bytes or len(source) > budgets.source_bytes:
            raise ValueError("source budget")
    receipt = require_admission(admission, phase="COMPARE_FROZEN", raw=raw,
                                binding=binding, approval=approval, budgets=budgets)
    found = _validate_claims(raw, binding=binding, approval=approval, limits=budgets)
    if sha(schema_bytes) != binding["sources"]["schema"] or sha(template_bytes) != binding["sources"]["template"]:
        raise ValueError("supplied schema/template drift")
    schema, template = parse(schema_bytes, budgets), parse(template_bytes, budgets)
    specs = template["records"]
    if len(specs) != 428 or len({s["id"] for s in specs}) != 428:
        raise ValueError("template duplicate/incomplete")
    if set(template["completeness"]["required_slot_ids"]) != set(found):
        raise ValueError("template identity")
    validate_slots(found, schema, {s["id"]: s for s in specs}, budgets)
    return found, receipt


def compare_frozen(raw, *, binding, approval, schema_bytes, template_bytes, observe,
                   admission=None, budgets=None):
    expected, receipt = validate_frozen(
        raw, binding=binding, approval=approval, schema_bytes=schema_bytes,
        template_bytes=template_bytes, admission=admission, budgets=budgets)
    before = sha(raw)
    try:
        observed = observe()
        if type(observed) is not list or len(observed) > budgets.records:
            raise ValueError("observed count budget")
        guard(observed, budgets)
        differences, indexed, counts, invalid = [], {}, {}, set()

        def report(item):
            if len(differences) >= budgets.diagnostics:
                raise ValueError("diagnostic budget; comparison aborted")
            differences.append(item)

        for index, record in enumerate(observed):
            if type(record) is not dict or type(record.get("id")) is not str:
                invalid.add(index)
                report({"kind": "malformed", "index": index})
                continue
            key = record["id"]
            counts[key] = counts.get(key, 0) + 1
            if key in indexed:
                invalid.update((index, indexed[key][0]))
                report({"kind": "duplicate", "id": key, "index": index})
                continue
            indexed[key] = (index, record)
            try:
                record_check(record, budgets)
            except (ValueError, TypeError, KeyError):
                invalid.add(index)
                report({"kind": "invalid-observed", "id": key, "index": index})
        matched = 0
        for key in sorted(set(expected) | set(indexed)):
            if key not in expected or key not in indexed:
                report({"id": key, "kind": "extra" if key not in expected else "missing"})
                continue
            index, record = indexed[key]
            equal = True
            for field in ("hex", "length", "sha256", "error"):
                if record.get(field) != expected[key][field]:
                    equal = False
                    # Full bytes remain in immutable observed evidence. Diagnostics
                    # identify every differing field without copying unbounded payloads.
                    report({"id": key, "field": field, "kind": "different"})
            if equal and index not in invalid and counts[key] == 1:
                matched += 1
        result = {"report_spec": "MPT-FROZEN-COMPARISON-REPORT@2",
                  "state": "COMPARISON_ONLY", "differences": differences,
                  "expected_bundle_sha256": before, "required_slots": len(expected),
                  "observed_slots": len(observed), "matched_slots": matched,
                  "missing_slots": len(set(expected) - set(indexed)),
                  "extra_slots": len(set(indexed) - set(expected)), "invalid_slots": len(invalid)}
        canonical(result, budgets)
        if sha(raw) != before:
            raise ValueError("expected input mutated")
    finally:
        admission.recheck(receipt)
    return result
