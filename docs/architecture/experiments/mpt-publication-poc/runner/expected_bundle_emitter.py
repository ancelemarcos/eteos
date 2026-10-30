"""Candidate 0.16. Pure independent generation; NOT_RUN, no filesystem or SUT access."""
import hashlib
import json
from decimal import Decimal
import snapshot_oracle as oracle
from expected_bounds import Budgets, guard, parse, canonical as bounded_canonical
from expected_admission import require_admission

RULES = {f"SNAP-P0{i}": f"candidate-0.15/P0{i}" for i in range(1, 6)}
SOURCE_NAMES = {"schema", "template", "oracle", "emitter", "interpretations", "vectors"}


def canonical(value, limits=None):
    return bounded_canonical(value, limits or Budgets())


def digest(value):
    return hashlib.sha256(value).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def decode(value):
    return parse(value, Budgets())


def recipe(name, schemas):
    rows = {n: [] for n in schemas}
    view = []
    if name == "TYPED@1":
        rows = oracle.populated_fixture(schemas)
        view = [dict(position_id="SYNTH-A", version=1, lifecycle="OPEN_DECLARED",
                     side="LONG", remaining_quantity=1, average_entry_price=Decimal("1.00"),
                     domain_id="SYNTH-A", ordinal=1)]
    elif name == "MULTI@1":
        rows["position_guard"] = [
            dict(position_id="P-B", pending_close_command=None),
            dict(position_id="P-A", pending_close_command="C-1")]
        rows["publication_domain"] = [dict(domain_id="D", policy_version="1")]
    elif name != "EMPTY@1":
        raise ValueError("unknown independent recipe")
    return rows, view


def streams(schemas, limits):
    guard(schemas, limits)
    result = {}
    for fixture in ("EMPTY@1", "TYPED@1", "MULTI@1"):
        rows, view = recipe(fixture, schemas)
        guard(rows, limits)
        guard(view, limits)
        snapshot = oracle.fixture_snapshot(schemas, rows, view)
        prefix = fixture + "/"
        for name, schema in schemas.items():
            result[prefix + "table/" + name] = snapshot["normal"]["mpt_poc." + name]
            keyed = []
            for row in rows[name]:
                values = {c["name"]: oracle.scalar_fixture(c["type"], row[c["name"]])
                          for c in schema["columns"]}
                key = oracle.part("k", b"".join(values[k] for k in schema["pk"]))
                keyed.append((key, values))
            for index, (_, values) in enumerate(sorted(keyed, key=lambda item: item[0])):
                stem = name + "/" + str(index)
                result[prefix + "row/" + stem] = oracle.part(
                    "r", b"".join(values[c["name"]] for c in schema["columns"]))
                for c in schema["columns"]:
                    result[prefix + "scalar/" + stem + "/" + c["name"]] = values[c["name"]]
        for position, tables in snapshot["position_tables"].items():
            for qualified, value in tables.items():
                result[prefix + "partition-table/" + position + "/" + qualified.split(".", 1)[1]] = value
        for position, value in snapshot["positions"].items():
            result[prefix + "position/" + position] = value
        for qualified, value in snapshot["global_tables"].items():
            result[prefix + "global-table/" + qualified.split(".", 1)[1]] = value
        for layer in ("persisted", "global", "metadata", "published", "envelope"):
            result[prefix + layer] = snapshot[layer]
    return result


def generate_expected(*, sources, interpretations, generation, admission=None,
                      approval=None, budgets=None):
    """Caller supplies authenticated source bytes; never accepts paths or observed data.
    Source-byte/load binding of Python modules requires external isolation and review.
    No approval or freeze operation exists here.
    """
    if budgets is None:
        raise ValueError("explicit externally approved budget required")
    budgets.check()
    if type(sources) is not dict:
        raise ValueError("source mapping required")
    if set(sources) != SOURCE_NAMES or any(type(v) is not bytes for v in sources.values()):
        raise ValueError("exact source byte inventory required; observed input forbidden")
    if any(len(v) > budgets.source_bytes for v in sources.values()) or sum(
            len(v) for v in sources.values()) > budgets.input_bytes:
        raise ValueError("source byte budget")
    generation_binding = {"sources": {k: digest(v) for k, v in sources.items()},
                          "interpretations": interpretations, "generation": generation,
                          "budgets": budgets.__dict__}
    receipt = require_admission(admission, phase="GENERATE_EXPECTED", raw=b"",
                                binding=generation_binding, approval=approval, budgets=budgets)
    if interpretations != RULES:
        raise ValueError("explicit candidate interpretation selection required")
    if set(generation) != {"environment", "run_id"} or any(
            type(v) is not str or not v or v == "UNRESOLVED" for v in generation.values()):
        raise ValueError("generation provenance required")
    schema = parse(sources["schema"], budgets)
    template = parse(sources["template"], budgets)
    if schema["contract"] != "MPT-SNAPSHOT@1":
        raise ValueError("contract")
    tables = schema["tables"]
    if len(tables) != 30 or sum(len(t["columns"]) for t in tables.values()) != 191:
        raise ValueError("schema inventory")
    for name, table in tables.items():
        if len(name) > 128 or len(table["columns"]) > 32:
            raise ValueError("schema dimension budget")
        names = [c["name"] for c in table["columns"]]
        if len(set(names)) != len(names) or not table["pk"] or not set(table["pk"]) <= set(names):
            raise ValueError("schema column/PK identity")
        if any(len(c["name"]) > 128 or len(c["type"]) > 32 or
               type(c["nullable"]) is not bool for c in table["columns"]):
            raise ValueError("schema column budget")
    if digest(sources["schema"]) != template["schema_sha256"]:
        raise ValueError("schema drift")
    if digest(sources["oracle"]) != template["source_recipe_sha256"]:
        raise ValueError("recipe drift")
    if digest(sources["vectors"]) != template["source_vectors_sha256"]:
        raise ValueError("vector drift")
    values = streams(schema["tables"], budgets)
    if sum(len(v) for v in values.values()) * 2 > budgets.output_bytes:
        raise ValueError("hex output budget")
    if any(len(v) > budgets.wire_bytes for v in values.values()):
        raise ValueError("wire output budget")
    ids = template["completeness"]["required_slot_ids"]
    if len(values) != 428 or len(ids) != 428 or len(set(ids)) != 428 or set(values) != set(ids):
        raise ValueError("independent inventory differs from 428-slot template")
    records = [{"id": key, "hex": values[key].hex(), "length": len(values[key]),
                "sha256": digest(values[key]), "error": None} for key in sorted(values)]
    output = canonical({
        "spec": "MPT-FROZEN-COMPARE@1", "contract": schema["contract"],
        "bundle_id": "CANDIDATE-0.16-EXPECTED@1", "state": "EXPECTED_UNVERIFIED",
        "sources": {k: digest(v) for k, v in sources.items()},
        "interpretations": interpretations, "generation": generation,
        "review": None, "records": records}, budgets)
    admission.recheck(receipt)
    return output
