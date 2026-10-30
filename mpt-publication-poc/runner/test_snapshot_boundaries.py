"""Nonexecuted admission/plan tests. Fake objects cannot prove driver guarantees."""
import hashlib
import json
import unittest
from pathlib import Path
from snapshot_transport_candidate import PsycopgIncrementalCandidate, TransportBlocked
from connected_snapshot_harness import prepare, dispatch, HarnessBlocked, CasePlan


class InertBoundaries(unittest.TestCase):
    def test_no_driver_operation_even_if_cancellation_is_ignored(self):
        class NeverTouch:
            def __getattribute__(self, key):
                raise AssertionError("driver touched: " + key)
        adapter = PsycopgIncrementalCandidate()
        for operation in ("execute", "fetch", "cancel", "rollback", "close", "close_cursor"):
            with self.subTest(operation=operation):
                with self.assertRaises(TransportBlocked):
                    if operation == "execute":
                        adapter.execute(NeverTouch(), "SELECT 1")
                    elif operation == "fetch":
                        adapter.fetch(NeverTouch(), count=1)
                    else:
                        getattr(adapter, operation)(NeverTouch())

    def test_incremental_plan_requires_resolved_consistent_limits(self):
        adapter = PsycopgIncrementalCandidate()
        limits = {"fetch_rows": 1, "max_bytes_per_value": 16, "max_bytes_per_row": 32,
                  "max_bytes_per_batch": 64, "call_timeout_ms": 100}
        plan = adapter.plan_select("SELECT 1", (), cursor_name="review_cursor", limits=limits)
        self.assertEqual(plan.fetch_rows, 1)
        for bad in ({**limits, "call_timeout_ms": "UNRESOLVED"},
                    {**limits, "max_bytes_per_row": 1}, {**limits, "fetch_rows": True}):
            with self.assertRaises(TransportBlocked):
                adapter.plan_select("SELECT 1", (), cursor_name="review_cursor", limits=bad)

    def test_false_connected_approval_refuses_before_provider(self):
        cfg = Path(__file__).with_name("connected-approval.example.json").read_bytes()
        with self.assertRaises(HarnessBlocked):
            prepare(cfg, independently_approved_sha256=hashlib.sha256(cfg).hexdigest(),
                    manifest_bytes=b"", environment_bytes=b"", scenarios_bytes=b"", case_id="MVCC-UPDATE")

    def test_even_forged_plan_cannot_activate_dispatch(self):
        plan = CasePlan("MVCC-UPDATE", "0"*64, "0"*64, "0"*64, "0"*64, (), "A")
        with self.assertRaises(TransportBlocked):
            dispatch(plan, external_session_provider=lambda: self.fail("provider called"))
