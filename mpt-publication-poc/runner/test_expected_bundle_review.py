"""Authored only / NOT_RUN. Approval mocks below test plumbing, never human evidence."""
import copy
import inspect
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
import expected_bundle_emitter as emitter
import frozen_bundle_compare as comparator
import snapshot_oracle as oracle
from expected_bounds import Budgets, parse, canonical, guard
from expected_admission import AdmissionAdapter, AdmissionReceipt, AdmissionBlocked
from expected_wire_review import scalar, table


class SimulationAdmission(AdmissionAdapter):
    """TEST DOUBLE ONLY: never a signature, filesystem or module verification backend."""
    def __init__(self, denial=None, mutated=False):
        self.denial = denial
        self.mutated = mutated

    def authorize(self, *, phase, raw, binding, approval, budgets):
        if self.denial:
            raise AdmissionBlocked("SIMULATED rejection: " + self.denial)
        return AdmissionReceipt(phase, emitter.digest(canonical(binding, budgets)),
                                emitter.digest(raw), "SIMULATION-NOT-EVIDENCE")

    def recheck(self, receipt):
        if self.mutated:
            raise AdmissionBlocked("SIMULATED expected file identity mutation")



class ExpectedBundleReview(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent
        names = {"schema": root / "snapshot_schema.json",
                 "template": root / "expected-bundle.template.json",
                 "oracle": root / "snapshot_oracle.py",
                 "emitter": root / "expected_bundle_emitter.py",
                 "interpretations": root.parent / "SNAPSHOT-INTERPRETATION-REVIEW.md",
                 "vectors": root / "snapshot_compound_vectors.json"}
        self.sources = {k: p.read_bytes() for k, p in names.items()}
        self.template = emitter.decode(self.sources["template"])
        self.budgets = Budgets()
        self.generated = emitter.decode(self.generate(
            sources=self.sources, interpretations=emitter.RULES,
            generation={"environment": "UNIT-TEST-SIMULATION", "run_id": "SIMULATED"}))
        self.calls = 0


    def generate(self, **kwargs):
        return emitter.generate_expected(admission=SimulationAdmission(), budgets=self.budgets, **kwargs)

    def compare(self, raw, *, binding, approval, observe, admission=None, budgets=None):
        return comparator.compare_frozen(
            raw, binding=binding, approval=approval, observe=observe,
            schema_bytes=self.sources["schema"], template_bytes=self.sources["template"],
            admission=admission or SimulationAdmission(), budgets=budgets or self.budgets)

    def simulated_review(self, bundle):
        # Only an in-memory mock for negative admission tests, not a freeze API.
        review = {"reviewer": "TEST-DOUBLE", "decision_id": "SIMULATED-NOT-APPROVAL",
                  "timestamp": "SIMULATED"}
        bundle["state"] = "REVIEWED_FROZEN"
        bundle["review"] = review
        raw = emitter.canonical(bundle)
        binding = dict(bundle_sha256=emitter.digest(raw),
                       manifest_sha256=emitter.digest(b"SIMULATED-MANIFEST"),
                       capsule_sha256=emitter.digest(b"SIMULATED-CAPSULE"),
                       sources=self.generated["sources"],
                       required_slot_ids=self.template["completeness"]["required_slot_ids"],
                       interpretations=emitter.RULES, bundle_path="/SIMULATED/expected.json")
        approval = dict(review, state="APPROVED", binding=copy.deepcopy(binding),
                        signature="TEST-DOUBLE-NOT-A-SIGNATURE")
        return raw, binding, approval

    def observe(self):
        self.calls += 1
        return copy.deepcopy(self.generated["records"])

    def reject(self, raw, binding, approval):
        with self.assertRaises((ValueError, TypeError, KeyError)):
            self.compare(raw, binding=binding, approval=approval,
                                      observe=self.observe)
        self.assertEqual(self.calls, 0)

    def test_inventory_and_all_slots(self):
        self.assertEqual(self.generated["state"], "EXPECTED_UNVERIFIED")
        self.assertIsNone(self.generated["review"])
        self.assertEqual(len(self.generated["records"]), 428)
        self.assertEqual({r["id"] for r in self.generated["records"]},
                         set(self.template["completeness"]["required_slot_ids"]))
        for record in self.generated["records"]:
            comparator.record_check(record)
        # Requires an explicit selection; no interpretation default.
        with self.assertRaises(ValueError):
            self.generate(sources=self.sources, interpretations={},
                                      generation={"environment": "SIM", "run_id": "SIM"})

    def test_incomplete_duplicate_bytes_length_digest_and_identity(self):
        mutations = [
            lambda b: b["records"].pop(),
            lambda b: b["records"].append(copy.deepcopy(b["records"][0])),
            lambda b: b["records"][0].pop("length"),
            lambda b: b["records"].__setitem__(1, copy.deepcopy(b["records"][0])),
            lambda b: b["records"][0].__setitem__("hex", "00"),
            lambda b: b["records"][0].__setitem__("length", -1),
            lambda b: b["records"][0].__setitem__("sha256", "UNRESOLVED"),
            lambda b: b["sources"].__setitem__("schema", emitter.digest(b"drift")),
            lambda b: b["sources"].__setitem__("oracle", emitter.digest(b"drift")),
            lambda b: b["interpretations"].__setitem__("SNAP-P01", "PENDING_HUMAN_APPROVAL"),
            lambda b: b.__setitem__("spec", "UNKNOWN"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                bundle = copy.deepcopy(self.generated)
                mutate(bundle)
                self.reject(*self.simulated_review(bundle))

    def test_not_frozen_and_missing_approval(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        self.reject(raw, binding, None)
        bundle = emitter.decode(raw)
        bundle["state"] = "EXPECTED_UNVERIFIED"
        raw = emitter.canonical(bundle)
        binding["bundle_sha256"] = emitter.digest(raw)
        approval["binding"] = copy.deepcopy(binding)
        self.reject(raw, binding, approval)

    def test_external_hashes_and_authentication(self):
        for key in ("manifest_sha256", "capsule_sha256", "bundle_sha256"):
            raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
            binding[key] = emitter.digest(b"DRIFT")
            self.reject(raw, binding, approval)
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        with self.assertRaises(ValueError):
            self.compare(raw, binding=binding, approval=approval,
                                      admission=SimulationAdmission(denial="false authority"), observe=self.observe)
        self.assertEqual(self.calls, 0)

    def test_each_slot_comparison(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        for index, record in enumerate(self.generated["records"]):
            with self.subTest(slot=record["id"]):
                observed = copy.deepcopy(self.generated["records"])
                observed[index]["error"] = "SIMULATED-SUT-ERROR"
                result = self.compare(
                    raw, binding=binding, approval=approval,
                    observe=lambda: observed)
                self.assertTrue(any(d.get("id") == record["id"] and d.get("field") == "error"
                                    for d in result["differences"]))

    def test_divergences_not_short_circuited(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        observed = self.observe()
        observed[0]["hex"] = "00"
        observed[1]["length"] = -1
        observed[2]["error"] = "ValueError"
        observed.pop()
        result = self.compare(raw, binding=binding, approval=approval,
                                           observe=lambda: observed)
        self.assertGreaterEqual(len(result["differences"]), 4)

    def test_emitter_cannot_read_observed(self):
        source = inspect.getsource(emitter)
        for forbidden in ("snapshot_codec", "snapshot_reference", "test_snapshot", "open(",
                          "read_bytes(", "read_text(", "__import__"):
            self.assertNotIn(forbidden, source)
        with patch("builtins.open", side_effect=AssertionError("file access forbidden")):
            self.generate(sources=self.sources, interpretations=emitter.RULES,
                                      generation={"environment": "SIM", "run_id": "SIM"})
        sources = dict(self.sources, OBSERVED=b"forbidden")
        with self.assertRaises(ValueError):
            self.generate(sources=sources, interpretations=emitter.RULES,
                                      generation={"environment": "SIM", "run_id": "SIM"})

    def test_scalar_controls(self):
        self.assertNotEqual(oracle.scalar_fixture("jsonb", None),
                            oracle.part("J", oracle.json_fixture(None)))
        self.assertNotEqual(oracle.scalar_fixture("numeric", Decimal("1.0")),
                            oracle.scalar_fixture("numeric", Decimal("1.00")))
        self.assertNotEqual(oracle.scalar_fixture("text", "\u00e9"),
                            oracle.scalar_fixture("text", "e\u0301"))
        self.assertEqual(oracle.scalar_fixture("bytea", b"\x00\xff").hex(),
                         "59000000000000000200ff")
        self.assertEqual(oracle.scalar_fixture("timestamp with time zone", {"micros": -1}).hex(),
                         "5a00000000000000022d31")
        self.assertNotEqual(oracle.scalar_fixture("timestamp with time zone", {"micros": 1}),
                            oracle.scalar_fixture("timestamp with time zone", {"micros": 2}))
        self.assertEqual(oracle.scalar_fixture("jsonb", {"a": [None, False]}).hex(),
                         "4a000000000000002f6f00000000000000266b000000000000000161"
                         "6100000000000000136e000000000000000062000000000000000130")
        for invalid in ({"micros": True}, {"micros": 1.0}, {"micros": 2**63-1},
                        {"micros": -2**63}, "infinity", "2026-01-01"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                oracle.scalar_fixture("timestamp with time zone", invalid)

    def test_partition_metadata_envelope_and_pk_controls(self):
        records = {r["id"]: bytes.fromhex(r["hex"]) for r in self.generated["records"]}
        self.assertNotEqual(records["MULTI@1/position/P-A"], records["MULTI@1/position/P-B"])
        for fixture in ("EMPTY@1", "TYPED@1", "MULTI@1"):
            metadata = b"".join(records[fixture + "/table/" + n] for n in sorted(
                ("publication_barrier", "publication_batch", "publication_cut", "public_projection")))
            self.assertEqual(records[fixture + "/metadata"], metadata)
            envelope = oracle.part("v", "MPT-SNAPSHOT@1/ENVELOPE")
            for layer in ("persisted", "published", "metadata"):
                envelope += oracle.part("h", oracle.sha(records[fixture + "/" + layer]))
            envelope += (oracle.part("m", bytes(32)) + oracle.part("c", bytes.fromhex("11"*32))
                         + oracle.part("r", "VECTOR-ONLY"))
            self.assertEqual(records[fixture + "/envelope"], envelope)
        keys = [oracle.part("k", oracle.scalar_fixture("text", k)) for k in ("aa", "b", "a")]
        self.assertEqual(sorted(keys), [keys[2], keys[1], keys[0]])

    def test_disabled_and_external_rejections_before_observe(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        with self.assertRaises(ValueError):
            comparator.compare_frozen(
                raw, binding=binding, approval=approval, observe=self.observe,
                schema_bytes=self.sources["schema"], template_bytes=self.sources["template"],
                budgets=self.budgets)
        for failure in ("bad-signature", "wrong-role", "same-author-and-reviewer", "expired",
                        "revoked", "wrong-scope", "path-replaced", "symlink", "reparse",
                        "hardlink", "different-loaded-module", "different-runtime"):
            with self.subTest(failure=failure), self.assertRaises(AdmissionBlocked):
                self.compare(raw, binding=binding, approval=approval, observe=self.observe,
                             admission=SimulationAdmission(denial=failure))
        self.assertEqual(self.calls, 0)

    def test_canonical_order_and_post_freeze_bytes(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        self.reject(raw + b" ", binding, approval)
        bundle = copy.deepcopy(self.generated)
        bundle["records"].reverse()
        self.reject(*self.simulated_review(bundle))
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        # Rebind an intentionally noncanonical whitespace form to reach canonical check.
        raw += b" "
        binding["bundle_sha256"] = emitter.digest(raw)
        approval["binding"] = copy.deepcopy(binding)
        self.reject(raw, binding, approval)

    def test_semantically_wrong_frame_with_consistent_hash(self):
        bundle = copy.deepcopy(self.generated)
        record = next(r for r in bundle["records"] if r["id"] == "TYPED@1/scalar/position/0/position_id")
        # Existing observed values are not used: change only the declared frame tag.
        record["hex"] = "59" + record["hex"][2:]
        record["sha256"] = emitter.digest(bytes.fromhex(record["hex"]))
        self.reject(*self.simulated_review(bundle))
        self.assertEqual(self.calls, 0)

    def test_expected_immutability_after_observer(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        before = bytes(raw)
        with self.assertRaises(AdmissionBlocked):
            self.compare(raw, binding=binding, approval=approval, observe=self.observe,
                         admission=SimulationAdmission(mutated=True))
        self.assertEqual(raw, before)
        self.assertEqual(self.calls, 1)

    def test_limits_abort_without_result(self):
        with self.assertRaises(ValueError):
            parse(b"[" * 33 + b"]" * 33, self.budgets)
        with self.assertRaises(ValueError):
            guard(Decimal("1e129"), self.budgets)
        with self.assertRaises(ValueError):
            canonical({"x": "large"}, Budgets(output_bytes=8))
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        with self.assertRaises(ValueError):
            self.compare(raw, binding=binding, approval=approval,
                         observe=lambda: [None] * 857)
        with self.assertRaises(ValueError):
            self.compare(raw, binding=binding, approval=approval,
                         observe=lambda: [], budgets=Budgets(diagnostics=1))
        self.assertEqual(self.calls, 0)

    def test_honest_counters(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        observed = copy.deepcopy(self.generated["records"][:-1])
        observed.append(copy.deepcopy(observed[0]))
        result = self.compare(raw, binding=binding, approval=approval, observe=lambda: observed)
        self.assertEqual(result["required_slots"], 428)
        self.assertEqual(result["observed_slots"], 428)
        self.assertEqual(result["missing_slots"], 1)
        self.assertEqual(result["invalid_slots"], 2)
        self.assertEqual(result["extra_slots"], 0)
        self.assertEqual(result["matched_slots"], 426)
        self.assertNotIn("compared_slots", result)

    def test_manual_wire_rejection_oracle(self):
        # Hand-authored literals, not generated by emitter or SUT.
        with self.assertRaises(ValueError):
            scalar(bytes.fromhex("59000000000000000141"),
                   {"type": "text", "nullable": False}, self.budgets)
        with self.assertRaises(ValueError):
            scalar(bytes.fromhex("4e0000000000000000"),
                   {"type": "text", "nullable": False}, self.budgets)
        with self.assertRaises(ValueError):
            scalar(bytes.fromhex("5a00000000000000022d30"),
                   {"type": "timestamp with time zone", "nullable": False}, self.budgets)

    def test_partition_descriptor_and_link_tampering(self):
        for slot, old, new in (
                ("MULTI@1/partition-table/P-A/position", b"P-A", b"P-Z"),
                ("EMPTY@1/table/publication_domain", b"domain_id", b"domain_iz"),
                ("TYPED@1/scalar/position/0/position_id", b"SYNTH-A", b"SYNTH-Z")):
            with self.subTest(slot=slot):
                bundle = copy.deepcopy(self.generated)
                record = next(r for r in bundle["records"] if r["id"] == slot)
                wire = bytes.fromhex(record["hex"])
                self.assertIn(old, wire)
                wire = wire.replace(old, new, 1)
                record.update(hex=wire.hex(), length=len(wire), sha256=emitter.digest(wire))
                self.reject(*self.simulated_review(bundle))

    def test_wrong_admission_receipt_and_legacy_true_callback(self):
        class WrongReceipt(SimulationAdmission):
            def authorize(self, **kwargs):
                receipt = super().authorize(**kwargs)
                return AdmissionReceipt("WRONG-PHASE", receipt.binding_sha256,
                                        receipt.raw_sha256, receipt.evidence_id)
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        with self.assertRaises(AdmissionBlocked):
            self.compare(raw, binding=binding, approval=approval, observe=self.observe,
                         admission=WrongReceipt())
        with self.assertRaises(AdmissionBlocked):
            self.compare(raw, binding=binding, approval=approval, observe=self.observe,
                         admission=lambda _: True)
        self.assertEqual(self.calls, 0)

    def test_legacy_keyword_and_generation_defaults_rejected(self):
        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        with self.assertRaises(TypeError):
            comparator.compare_frozen(
                raw, binding=binding, approval=approval, observe=self.observe,
                schema_bytes=self.sources["schema"], template_bytes=self.sources["template"],
                budgets=self.budgets, authenticate=lambda _: True)
        with patch.object(emitter, "streams", side_effect=AssertionError("generation reached")):
            with self.assertRaises(ValueError):
                emitter.generate_expected(sources=self.sources, interpretations=emitter.RULES,
                                          generation={"environment": "SIM", "run_id": "SIM"})
        self.assertEqual(self.calls, 0)

    def test_abort_paths_never_publish_report(self):
        class RecordingAdmission(SimulationAdmission):
            checks = 0

            def recheck(self, receipt):
                self.checks += 1
                super().recheck(receipt)

        def broken_observer():
            raise ValueError("SIMULATED observer failure")

        raw, binding, approval = self.simulated_review(copy.deepcopy(self.generated))
        cases = (
            (broken_observer, RecordingAdmission(), self.budgets),
            (lambda: [], RecordingAdmission(), Budgets(diagnostics=1)),
            (self.observe, RecordingAdmission(mutated=True), self.budgets),
        )
        for observer, adapter, limits in cases:
            sentinel = object()
            report = sentinel
            with self.subTest(observer=observer), self.assertRaises(ValueError):
                report = self.compare(raw, binding=binding, approval=approval, observe=observer,
                                      admission=adapter, budgets=limits)
            self.assertIs(report, sentinel)
            self.assertEqual(adapter.checks, 1)
