"""Candidate tests ONLY. NOT_RUN. No database, main, runner integration or approvals.
Expected streams come from independent snapshot_oracle or literal hand-derived hex.
Round-trip assertions are supplementary, never substitutes for independent equality.
"""
import json
import unittest
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from pathlib import Path
import snapshot_codec as sut
import snapshot_reference as ref
import snapshot_oracle as oracle


class CodecConformance(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(Path(__file__).with_name("snapshot_schema.json").read_text("utf-8"))

    def test_scalar_bytes_and_decoding(self):
        cases = [
            ("text", "", "540000000000000000", ("text", "")),
            ("text", "\u00e9", "540000000000000002c3a9", ("text", "\u00e9")),
            ("text", "e\u0301", "54000000000000000365cc81", ("text", "e\u0301")),
            ("text", None, "4e0000000000000000", ("sql-null",)),
            ("boolean", False, "42000000000000000130", ("boolean", False)),
            ("numeric", Decimal("1.00"), "4400000000000000053130303a32", ("numeric", 100, 2)),
            ("bytea", bytes.fromhex("00ff"), "59000000000000000200ff", ("bytes-hex", "00ff")),
            ("timestamp with time zone", sut.TimestampMicros(-1),
             "5a00000000000000022d31", ("timestamp-micros", -1))]
        for typ, value, literal, decoded in cases:
            with self.subTest(typ=typ, literal=literal):
                expected = bytes.fromhex(literal)
                self.assertEqual(sut.scalar(typ, value), expected)
                self.assertEqual(ref.scalar(expected), decoded)

    def test_nested_json_independent_bytes(self):
        expected = (oracle.part("J", oracle.part("o", oracle.part("k", "a") +
                    oracle.part("a", oracle.part("n", b"") + oracle.part("b", "0")))))
        self.assertEqual(len(expected), 56)
        self.assertEqual(sut.scalar("jsonb", sut.parse_stored_jsonb('{"a":[null,false]}')), expected)
        array_value = ("json-array", (("json-null",), ("json-bool", False)))
        object_value = ("json-object", (("a", array_value),))
        self.assertEqual(ref.scalar(expected), ("jsonb", object_value))

    def test_empty_multirow_order_and_corruption(self):
        schema = self.doc["tables"]["publication_domain"]
        for rows, length in [([], 200), ([{"domain_id": k, "policy_version": "1"}
                                        for k in ("aa", "b", "a")], 288)]:
            expected = oracle.relation("mpt_poc.publication_domain", schema, rows)
            self.assertEqual(len(expected), length)
            self.assertEqual(sut.table_bytes("mpt_poc.publication_domain", schema, rows), expected)
            decoded = ref.table(expected)
            restored = [dict(zip([c["name"] for c in schema["columns"]],
                                [v[1] for v in row])) for row in decoded["rows"]]
            self.assertEqual(sut.table_bytes("mpt_poc.publication_domain", schema, restored), expected)
            self.assertEqual(sut.table_bytes("mpt_poc.publication_domain", schema, list(reversed(rows))), expected)
            for bad in (expected[:-1], expected + b"x", b"?" + expected[1:]):
                with self.assertRaises(ValueError):
                    ref.table(bad)

    def test_complete_empty_and_multiple_partitions(self):
        for multiple in (False, True):
            rows = {n: [] for n in self.doc["tables"]}
            if multiple:
                rows["position_guard"] = [{"position_id": "P-B", "pending_close_command": None},
                                           {"position_id": "P-A", "pending_close_command": "C-1"}]
                rows["publication_domain"] = [{"domain_id": "D", "policy_version": "1"}]
            expected = oracle.fixture_snapshot(self.doc["tables"], rows)
            actual = sut.snapshot(self.doc, rows, [], "00"*32, "11"*32, "VECTOR-ONLY")
            self.assertEqual(actual["table_sha256"], {n: oracle.sha(v).hex() for n,v in expected["normal"].items()})
            for key, stream in [("persisted_sha256","persisted"), ("published_sha256","published"),
                                ("publication_metadata_sha256","metadata"),
                                ("envelope_sha256","envelope"), ("global_partition_sha256","global")]:
                self.assertEqual(actual[key], oracle.sha(expected[stream]).hex())
            self.assertEqual(actual["position_sha256"], {p: oracle.sha(v).hex()
                                                        for p,v in expected["positions"].items()})
            for p, tables in expected["position_tables"].items():
                for name, wire in tables.items():
                    n = name.split(".")[1]
                    self.assertEqual(sut.table_bytes(name, self.doc["tables"][n],
                        [r for r in rows[n] if r["position_id"] == p], sut.VERSION+"/POSITION", p), wire)
                self.assertEqual(ref.aggregate(expected["positions"][p], tables)["position"], p)
            ref.aggregate(expected["persisted"], expected["normal"])
            ref.aggregate(expected["global"], expected["global_tables"])
            self.assertEqual(ref.envelope(expected["envelope"])["run_id"], "VECTOR-ONLY")
            self.assertEqual(len(expected["envelope"]), 257)
            names = ("publication_barrier","publication_batch","publication_cut","public_projection")
            self.assertEqual(len(ref.metadata(expected["metadata"],
                {"mpt_poc."+n:self.doc["tables"][n] for n in names})), 4)
            with self.assertRaises(ValueError):
                ref.envelope(expected["envelope"][:-1])
            with self.assertRaises(ValueError):
                ref.aggregate(expected["persisted"], [])
            with self.assertRaises(ValueError):
                ref.metadata(expected["metadata"] + expected["metadata"], {})

    def test_rejections(self):
        for typ,value in [("unknown",None),("bigint",True),("numeric",1.0),
                          ("numeric",Decimal("NaN")),("numeric",Decimal("Infinity")),
                          ("timestamp with time zone",sut.TimestampMicros(2**63-1)),
                          ("timestamp with time zone",sut.TimestampMicros(-2**63))]:
            with self.assertRaises(ValueError):
                sut.scalar(typ,value)
        for raw in ('{"a":1,"a":2}', '{"a":NaN}'):
            with self.assertRaises(ValueError):
                sut.parse_stored_jsonb(raw)
        for malformed in (b"N"+bytes(7), b"N"+bytes(7)+b"\x01",
                          oracle.part("Q", b""), oracle.part("I", "01"),
                          oracle.part("D", "1:-1")):
            with self.assertRaises(ValueError):
                ref.scalar(malformed)
        schema = self.doc["tables"]["publication_domain"]
        for rows in ([{"domain_id":None,"policy_version":"1"}], [{"domain_id":"a"}],
                     [{"domain_id":"a","policy_version":"1","extra":"x"}],
                     [{"domain_id":"a","policy_version":"1"}]*2):
            with self.assertRaises(ValueError):
                sut.table_bytes("mpt_poc.publication_domain",schema,rows)
        with self.assertRaises(ValueError):
            sut.table_bytes("mpt_poc.publication_domain",schema,[],version="unknown")
        with self.assertRaises(ValueError):
            sut.descriptor({**schema, "extra": True})
        with self.assertRaises(ValueError):
            sut.snapshot({**self.doc, "extra": True}, {}, [], "00"*32, "11"*32, "VECTOR-ONLY")
        with self.assertRaises(UnicodeError):
            sut.scalar("text","\ud800")

    def test_fully_populated_typed_snapshot(self):
        rows = oracle.populated_fixture(self.doc["tables"])
        published = [{"position_id":"SYNTH-A", "version":1, "lifecycle":"OPEN_DECLARED",
                      "side":"LONG", "remaining_quantity":1, "average_entry_price":Decimal("1.00"),
                      "domain_id":"SYNTH-A", "ordinal":1}]
        expected = oracle.fixture_snapshot(self.doc["tables"], rows, published)
        actual_rows = {}
        for name, schema in self.doc["tables"].items():
            actual_rows[name] = []
            for row in rows[name]:
                converted = dict(row)
                for column in schema["columns"]:
                    value = row[column["name"]]
                    if value is not None and column["type"] == "jsonb":
                        converted[column["name"]] = sut.Jsonb(value)
                    elif value is not None and column["type"] == "timestamp with time zone":
                        converted[column["name"]] = sut.TimestampMicros(value["micros"])
                actual_rows[name].append(converted)
            wire = sut.table_bytes("mpt_poc."+name, schema, actual_rows[name])
            self.assertEqual(wire, expected["normal"]["mpt_poc."+name])
            self.assertEqual(len(ref.table(wire)["rows"]), 1)
        actual = sut.snapshot(self.doc, actual_rows, published, "00"*32, "11"*32, "VECTOR-ONLY")
        for key, stream in [("persisted_sha256","persisted"), ("published_sha256","published"),
                            ("publication_metadata_sha256","metadata"), ("envelope_sha256","envelope"),
                            ("global_partition_sha256","global")]:
            self.assertEqual(actual[key], oracle.sha(expected[stream]).hex())
        self.assertEqual(actual["position_sha256"],
                         {p:oracle.sha(v).hex() for p,v in expected["positions"].items()})
        records = oracle.layer_records(expected)
        self.assertEqual(records["envelope"]["length"], 257)
        self.assertTrue(all(r["reviewer"] == "PENDING_HUMAN_APPROVAL" for r in records.values()))

    def test_oracle_negative_typed_values(self):
        for typ,value in [("numeric",Decimal("NaN")),("numeric",1.0),
                          ("integer",True),("jsonb",1.0),("unknown",None),
                          ("timestamp with time zone",{"micros":9223372036854775807})]:
            with self.assertRaises(ValueError):
                oracle.scalar_fixture(typ,value)
        with self.assertRaises(UnicodeError):
            oracle.scalar_fixture("text","\ud800")
        self.assertNotEqual(oracle.scalar_fixture("numeric",Decimal("1.0")),
                            oracle.scalar_fixture("numeric",Decimal("1.00")))

    def test_python_time_domain_without_postgresql_claim(self):
        epoch_hex = "5a000000000000000130"
        expected = bytes.fromhex(epoch_hex)
        offset_epoch = datetime(1970, 1, 1, 1, tzinfo=timezone(timedelta(hours=1)))
        self.assertEqual(sut.scalar("timestamp with time zone", offset_epoch), expected)
        self.assertEqual(oracle.scalar_fixture("timestamp with time zone", {"micros": 0}), expected)
        self.assertEqual(ref.scalar(expected), ("timestamp-micros", 0))
        with self.assertRaises(ValueError):
            sut.scalar("timestamp with time zone", datetime(1970, 1, 1))
        with self.assertRaises(OverflowError):
            sut.scalar("timestamp with time zone",
                       datetime(1, 1, 1, tzinfo=timezone(timedelta(hours=1))))
        micros = 253402300800000000  # Wire-only year-10000 boundary, no DB validity assertion.
        self.assertEqual(sut.scalar("timestamp with time zone", sut.TimestampMicros(micros)),
                         oracle.scalar_fixture("timestamp with time zone", {"micros": micros}))
