"""Candidate fake-transport controls. NOT_RUN; no SQL is sent or database opened.
Connected DDL/privilege/concurrent-writer cases remain documentary, not simulated proof.
"""
import unittest
from types import SimpleNamespace
import snapshot_collector as sut


def limits():
    return {key: 1000 for key in sut.BOUNDS}


class Cursor:
    description = ("value",)
    def __init__(self, rows):
        self.rows = list(rows)


class Guard:
    def __init__(self, rows=()):
        self.rows = rows
        self.calls = []
        self.failure = None
    def execute(self, raw, query, params, **bounds):
        self.calls.append(("execute", bounds))
        return Cursor(self.rows)
    def fetch(self, cursor, **bounds):
        self.calls.append(("fetch", bounds))
        if self.failure:
            raise self.failure
        return [cursor.rows.pop(0)] if cursor.rows else []
    def close_cursor(self, cursor, **bounds):
        self.calls.append(("cursor_close", bounds))
    def rollback(self, raw, **bounds):
        self.calls.append(("rollback", bounds))
    def close(self, raw, **bounds):
        self.calls.append(("close", bounds))


class CollectorControls(unittest.TestCase):
    def test_disabled_never_touches_connection(self):
        class Untouchable:
            def __getattribute__(self, name):
                raise AssertionError(name)
        with self.assertRaises(sut.CollectionBlocked):
            sut.collect(Untouchable(),schema_bytes=b"",manifest_bytes=b"",
                        approval_bytes=b"",independently_approved_config_sha256="")

    def test_type_precision_and_width_boundaries(self):
        for typ,value in [("numeric",1.5),("bigint",True),("boolean",1),
                          ("text",b"a"),("bytea",3),("unknown","x"),
                          ("timestamp with time zone","1.1"),("xid8","01")]:
            with self.subTest(typ=typ):
                with self.assertRaises(sut.CollectionBlocked):
                    sut.convert({"type":typ,"nullable":False},value)
        with self.assertRaises(sut.CollectionBlocked):
            sut.convert({"type":"text","nullable":False},None)
        self.assertEqual(str(sut.convert({"type":"numeric","nullable":False},"1.00")), "1.00")
        caps = limits()
        caps["max_json_depth"] = 1
        caps["max_decimal_chars"] = 4
        for typ, value in [("numeric", "12345"), ("jsonb", "[[0]]"), ("jsonb", "1e9999")]:
            with self.assertRaises(sut.CollectionBlocked):
                sut.convert({"type": typ, "nullable": False}, value, caps)

    def test_each_budget_boundary(self):
        settings = limits()
        settings["max_bytes_per_value"] = 10
        settings["max_bytes_per_row"] = 19
        budget = sut.Budget(settings, clock=lambda: 0)
        self.assertEqual(budget.row(("a",)),19)
        with self.assertRaises(sut.CollectionBlocked):
            budget.row(("aa",))
        with self.assertRaises(sut.CollectionBlocked):
            budget.row(("a","a"))
        budget.relation(1000)
        with self.assertRaises(sut.CollectionBlocked):
            budget.relation(1)
        with self.assertRaises(sut.CollectionBlocked):
            sut.Budget(settings,clock=lambda:0).relation(1001)
        settings["max_memory_bytes"] = 1
        with self.assertRaises(sut.CollectionBlocked):
            sut.Budget(settings,clock=lambda:0).memory(["a"])
        now = [0]
        budget = sut.Budget(limits(),clock=lambda:now[0])
        now[0] = 1
        with self.assertRaises(sut.CollectionBlocked):
            budget.remaining_ms()

    def test_bounded_fetch_row_and_buffer_overflow(self):
        raw = SimpleNamespace(autocommit=True, info=SimpleNamespace(transaction_status=0))
        for rows,cap in [([(1,),(2,)],1),([("x"*1001,)],10)]:
            guard = Guard(rows)
            conn = sut.BoundedConnection(raw,guard,sut.Budget(limits(),clock=lambda:0))
            with self.assertRaises(sut.CollectionBlocked):
                conn.execute("DOCUMENTARY QUERY",row_cap=cap)
            self.assertEqual(guard.calls[-1][0],"cursor_close")

    def test_cancel_loss_and_cleanup_preserve_original(self):
        raw = SimpleNamespace(autocommit=True,info=SimpleNamespace(transaction_status=0))
        for original in (KeyboardInterrupt(),TimeoutError(),ConnectionError()):
            guard = Guard()
            guard.failure = original
            conn = sut.BoundedConnection(raw,guard,sut.Budget(limits(),clock=lambda:0))
            with self.assertRaises(type(original)) as found:
                conn.execute("DOCUMENTARY QUERY")
            self.assertIs(found.exception,original)
            self.assertEqual(guard.calls[-1][0],"cursor_close")
        class BrokenCleanup(Guard):
            def rollback(self, raw, **bounds):
                self.calls.append(("rollback", bounds))
                raise ConnectionError("rollback")
            def close(self, raw, **bounds):
                self.calls.append(("close", bounds))
                raise OSError("close")
        guard = BrokenCleanup()
        original = ValueError("primary")
        sut.finish(raw,guard,100,original)
        self.assertEqual(len(original.cleanup_errors),2)
        self.assertEqual([n for n,_ in guard.calls],["rollback","close"])
        with self.assertRaises(sut.CollectionBlocked):
            sut.finish(raw,guard,100,None)
