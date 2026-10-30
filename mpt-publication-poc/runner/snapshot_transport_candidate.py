"""Psycopg 3 candidate boundary. MATERIALIZED_NOT_RUN; permanently disarmed in this revision.
No psycopg import, connect, DSN or driver operation at import. No capability is self-certified.
"""
from dataclasses import dataclass


class TransportBlocked(ValueError):
    pass


@dataclass(frozen=True)
class SelectPlan:
    sql: str
    params: tuple
    cursor_name: str
    fetch_rows: int
    max_column_bytes: int
    max_row_bytes: int
    max_batch_bytes: int
    timeout_ms: int


class PsycopgIncrementalCandidate:
    artifact_sha256 = "UNRESOLVED"
    # This source cannot be armed by a boolean, hash, subclass capability claim or config.
    # A separately reviewed implementation revision must supply the missing guarantees.
    def admission(self):
        raise TransportBlocked(
            "UNRESOLVED: native single-field/buffer allocation and hard call/cancel/cleanup "
            "bounds are not established for the pinned psycopg/libpq build")

    def plan_select(self, sql, params, *, cursor_name, limits):
        if type(sql) is not str or not sql.startswith("SELECT ") or ";" in sql:
            raise TransportBlocked("single reviewed SELECT required")
        if type(params) is not tuple or type(cursor_name) is not str or not cursor_name.isidentifier():
            raise TransportBlocked("invalid immutable parameters/cursor identity")
        keys = ("fetch_rows", "max_bytes_per_value", "max_bytes_per_row",
                "max_bytes_per_batch", "call_timeout_ms")
        if any(type(limits.get(k)) is not int or limits[k] <= 0 for k in keys):
            raise TransportBlocked("UNRESOLVED incremental limits")
        if not (limits["max_bytes_per_value"] <= limits["max_bytes_per_row"]
                <= limits["max_bytes_per_batch"]):
            raise TransportBlocked("inconsistent limits")
        return SelectPlan(sql, params, cursor_name, *(limits[k] for k in keys))

    def execute(self, raw, query, params=None, **bounds):
        self.admission()

    def fetch(self, cursor, *, count, **bounds):
        self.admission()

    def cancel(self, raw, **bounds):
        self.admission()

    def close_cursor(self, cursor, **bounds):
        self.admission()

    def rollback(self, raw, **bounds):
        self.admission()

    def close(self, raw, **bounds):
        self.admission()


def future_psycopg_read_recipe(plan):
    """Declarative API mapping only; no connection access or query execution.
    Transaction/control statements require a different bounded path, also unresolved.
    """
    return {
        "declare": "raw.cursor(name=plan.cursor_name, withhold=False)",
        "execute": "server_cursor.execute(plan.sql, plan.params)",
        "fetch": "server_cursor.fetchmany(plan.fetch_rows)",
        "close": "server_cursor.close()",
        "cancel": "raw.cancel_safe(timeout=approved_seconds), availability/version unresolved",
        "limitations": ("fetch row count does not bound one column's native allocation",
                        "cancel request does not prove query termination or rollback",
                        "network/cleanup deadlines require independent enforceable mechanism"),
        "status": "DOCUMENTED",
    }
