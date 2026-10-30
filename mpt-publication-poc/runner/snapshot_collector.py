"""Disabled-by-default MVCC candidate. NOT_RUN. No connect(), DSN, main or runner integration."""
import hashlib
import json
import re
import sys
from time import monotonic
from decimal import Decimal
from snapshot_codec import TABLES, Jsonb, TimestampMicros, parse_stored_jsonb, descriptor

class CollectionBlocked(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise CollectionBlocked(reason)


def quoted(name):
    # Only previously frozen identifiers may reach this helper.
    require(type(name) is str and name.replace("_","").isalnum(), "invalid identifier")
    return '"'+name+'"'


def projection(column):
    n=quoted(column["name"])
    typ=column["type"]
    if typ in ("numeric","jsonb","xid8"):
        return n+"::text"
    if typ=="timestamp with time zone":
        return "(extract(epoch from "+n+")*1000000)::text"
    return n


def convert(column, value, limits=None):
    if value is None:
        require(column["nullable"], "unexpected NULL")
        return None
    typ = column["type"]
    if typ in ("numeric", "jsonb", "xid8", "timestamp with time zone"):
        require(type(value) is str, "exact projected text required")
    if typ == "numeric":
        if limits is not None:
            require(len(value) <= limits["max_decimal_chars"], "numeric text cap")
        require(re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", value) is not None,
                "noncanonical/nonfinite stored numeric")
        return Decimal(value)
    if typ == "jsonb":
        if limits is not None:
            depth, in_string, escaped = 0, False, False
            for ch in value:
                if in_string:
                    if escaped:
                        escaped = False
                    elif ch == chr(92):
                        escaped = True
                    elif ch == '"':
                        in_string = False
                elif ch == '"':
                    in_string = True
                elif ch in "[{":
                    depth += 1
                    require(depth <= limits["max_json_depth"], "JSON depth cap")
                elif ch in "]}":
                    depth -= 1
        result = parse_stored_jsonb(value)
        if limits is not None:
            def inspect(node):
                if type(node) is Decimal:
                    _, digits, exponent = node.as_tuple()
                    require(len(digits) + abs(exponent) <= limits["max_decimal_chars"],
                            "JSON decimal expansion cap")
                elif type(node) is list:
                    for item in node:
                        inspect(item)
                elif type(node) is dict:
                    for item in node.values():
                        inspect(item)
            inspect(result.value)
        return result
    if typ == "xid8":
        require(re.fullmatch(r"0|[1-9][0-9]*", value) is not None, "invalid xid8")
        result = int(value)
        require(result < 2**64, "xid8 overflow")
        return result
    if typ == "timestamp with time zone":
        require(re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", value) is not None,
                "invalid timestamp text")
        result = Decimal(value)
        require(result == result.to_integral_value(), "fractional microseconds")
        micros = int(result)
        require(-2**63 < micros < 2**63-1, "timestamp wire overflow")
        return TimestampMicros(micros)
    if typ in ("integer", "bigint"):
        bits = 32 if typ == "integer" else 64
        require(type(value) is int and -2**(bits-1) <= value < 2**(bits-1),
                "integer type/range")
    elif typ == "boolean":
        require(type(value) is bool, "boolean required")
    elif typ == "text":
        require(type(value) is str, "text required")
        value.encode("utf-8", errors="strict")
    elif typ == "bytea":
        require(type(value) is bytes, "exact bytes required")
    else:
        raise CollectionBlocked("unknown column type")
    return value


BOUNDS = ("statement_timeout_ms", "lock_timeout_ms", "max_rows_per_table",
          "max_bytes_per_value", "max_bytes_per_row", "max_bytes_per_table",
          "max_bytes_total", "max_buffer_bytes", "max_memory_bytes",
          "total_timeout_ms", "cleanup_timeout_ms", "max_catalog_rows",
          "max_json_depth", "max_decimal_chars", "max_bytes_per_batch", "call_timeout_ms")


def value_size(value):
    # Transport accounting includes a type/null marker and 64-bit length per value.
    if value is None:
        return 9
    if type(value) is bytes:
        return 9 + len(value)
    if type(value) is str:
        return 9 + len(value.encode("utf-8", errors="strict"))
    if type(value) is bool:
        return 10
    if type(value) is int:
        return 9 + len(str(value))
    raise CollectionBlocked("unexpected raw driver type")


class Budget:
    def __init__(self, approval, clock=monotonic):
        self.limits = approval
        self.clock = clock
        self.deadline = clock() + approval["total_timeout_ms"] / 1000
        self.total = 0

    def remaining_ms(self):
        value = int((self.deadline - self.clock()) * 1000)
        require(value > 0, "total collection deadline exceeded")
        return value

    def row(self, row):
        self.remaining_ms()
        sizes = [value_size(v) for v in row]
        require(all(n <= self.limits["max_bytes_per_value"] for n in sizes),
                "value byte cap exceeded")
        size = 9 + sum(sizes)
        require(size <= self.limits["max_bytes_per_row"], "row byte cap exceeded")
        return size

    def relation(self, size):
        require(size <= self.limits["max_bytes_per_table"], "table byte cap exceeded")
        require(self.total + size <= self.limits["max_bytes_total"], "total byte cap exceeded")
        self.total += size

    def memory(self, value):
        # Retained Python graph only; native driver buffers require the external guard.
        seen = set()
        def size(obj):
            if id(obj) in seen:
                return 0
            seen.add(id(obj))
            amount = sys.getsizeof(obj)
            if isinstance(obj, dict):
                amount += sum(size(k) + size(v) for k, v in obj.items())
            elif isinstance(obj, (list, tuple)):
                amount += sum(size(v) for v in obj)
            elif type(obj) in (Jsonb, TimestampMicros):
                amount += size(obj.value)
            require(amount <= self.limits["max_memory_bytes"], "retained memory cap exceeded")
            return amount
        return size(value)


class BoundedResult:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows

    def fetchone(self):
        require(len(self.rows) == 1, "exactly one result row required")
        return self.rows[0]


class BoundedConnection:
    """External guard must enforce deadlines/native buffers BEFORE allocation or blocking.
    No concrete guard is supplied or implicitly trusted by this candidate.
    """
    def __init__(self, raw, guard, budget):
        self.raw, self.guard, self.budget = raw, guard, budget
        self.autocommit, self.info = raw.autocommit, raw.info

    def execute(self, query, params=None, *, row_cap=None):
        cap = self.budget.limits["max_catalog_rows"] if row_cap is None else row_cap
        remaining = min(self.budget.remaining_ms(), self.budget.limits["statement_timeout_ms"],
                        self.budget.limits["call_timeout_ms"])
        cursor = self.guard.execute(self.raw, query, params, timeout_ms=remaining,
                                    max_buffer_bytes=self.budget.limits["max_buffer_bytes"],
                                    max_memory_bytes=self.budget.limits["max_memory_bytes"])
        rows, size = [], 0
        try:
            if cursor.description is not None:
                while True:
                    self.budget.remaining_ms()
                    batch = self.guard.fetch(cursor, count=1,
                                             timeout_ms=min(self.budget.remaining_ms(),
                                                            self.budget.limits["call_timeout_ms"]),
                                             max_buffer_bytes=self.budget.limits["max_buffer_bytes"],
                                             max_memory_bytes=self.budget.limits["max_memory_bytes"])
                    require(type(batch) is list and len(batch) <= 1, "invalid bounded fetch")
                    if not batch:
                        break
                    require(type(batch[0]) in (tuple, list), "invalid row")
                    require(len(rows) < cap, "row cap exceeded")
                    batch_bytes = self.budget.row(batch[0])
                    require(batch_bytes <= self.budget.limits["max_bytes_per_batch"],
                            "batch byte cap exceeded")
                    size += batch_bytes
                    require(size <= self.budget.limits["max_buffer_bytes"], "result buffer cap exceeded")
                    rows.append(batch[0])
                    self.budget.memory(rows)
            self.budget.remaining_ms()
            return BoundedResult(rows)
        finally:
            original = sys.exception()
            try:
                self.guard.close_cursor(cursor, timeout_ms=self.budget.limits["cleanup_timeout_ms"])
            except BaseException as cleanup:
                if original is not None:
                    original.add_note("cursor cleanup failed: " + type(cleanup).__name__)
                    original.cursor_cleanup_error = cleanup
                else:
                    raise


def finish(raw, guard, cleanup_timeout_ms, original):
    errors = []
    for method in ("rollback", "close"):
        try:
            getattr(guard, method)(raw, timeout_ms=cleanup_timeout_ms)
        except BaseException as error:
            errors.append(error)
    if errors:
        if original is not None:
            original.cleanup_errors = tuple(errors)
            original.add_note("cleanup failed: " + ", ".join(type(e).__name__ for e in errors))
        else:
            error = CollectionBlocked("cleanup failed; result suppressed")
            error.cleanup_errors = tuple(errors)
            raise error from errors[0]


def collect(conn, *, schema_bytes, manifest_bytes, approval_bytes,
            independently_approved_config_sha256, transport_guard=None, enabled=False):
    """Takes ownership of an ALREADY OPEN, dedicated psycopg-compatible idle connection.
    Caller must separately verify signed provenance/package and grant execution authorization.
    No SQL at all unless enabled=True AND approval bytes match independent hash/authority.
    Returns supplied-data objects and provenance, NOT canonical bytes/hashes or a PASS verdict.
    """
    require(enabled is True,"collector disabled")
    config_hash=hashlib.sha256(approval_bytes).hexdigest()
    require(config_hash==independently_approved_config_sha256,"unapproved configuration")
    approval=json.loads(approval_bytes)
    require(approval.get("collector_authorized") is True,"collection not authorized")
    require(approval.get("ddl_quiescence_approved") is True,"DDL quiescence not approved")
    require(approval.get("contract")=="MPT-SNAPSHOT@1","contract/version mismatch")
    require(hashlib.sha256(schema_bytes).hexdigest()==approval["schema_sha256"],"schema hash mismatch")
    require(hashlib.sha256(manifest_bytes).hexdigest()==approval["manifest_sha256"],"manifest hash mismatch")
    doc=json.loads(schema_bytes)
    require(type(doc) is dict and set(doc) == {"contract", "tables"},
            "unknown/missing schema document field")
    require(doc.get("contract")=="MPT-SNAPSHOT@1" and set(doc["tables"])==TABLES,"inventory mismatch")
    for key in BOUNDS:
        require(type(approval[key]) is int and approval[key]>0,"unresolved bound: "+key)
    for key in ("database","role","login","server_version","server_version_num","run_id","viewdef_sha256"):
        require(type(approval[key]) is str and approval[key] not in ("","UNRESOLVED"),"unresolved "+key)
    require(sum(len(t["columns"]) for t in doc["tables"].values()) == 191, "field count mismatch")
    for table in doc["tables"].values():
        descriptor(table)
    require(approval["role"] == "mpt_snapshot_reader" and approval["login"] == approval["role"],
            "dedicated direct login required; no SET ROLE")
    for key in ("transport_guard_sha256", "privilege_review_sha256"):
        require(type(approval.get(key)) is str and
                re.fullmatch("[0-9a-f]{64}", approval[key]) is not None, "unresolved " + key)
    require(approval.get("privilege_quiescence_approved") is True, "privilege quiescence required")
    require(type(approval.get("approved_extensions")) is list, "extension inventory unresolved")
    require(transport_guard is not None, "independent bounded transport guard required")
    require(transport_guard.artifact_sha256 == approval["transport_guard_sha256"],
            "transport guard identity mismatch")
    transport_guard.admission()  # Must refuse before touching conn if native guarantees are unresolved.
    # Guard verification is external independent evidence, not this self-reported hash.
    raw = conn
    budget = Budget(approval)
    conn = BoundedConnection(raw, transport_guard, budget)
    # All preceding refusals leave caller's connection untouched. From here ownership transfers.
    try:
        require(conn.autocommit is True and conn.info.transaction_status==0,
                "dedicated idle autocommit connection required")
        conn.execute("BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY")
        conn.execute("SET LOCAL search_path=pg_catalog")
        conn.execute("SET LOCAL row_security=off")
        require(conn.execute("SELECT current_setting('search_path')").fetchone()[0] == "pg_catalog",
                "unexpected search_path")
        require(conn.execute("SELECT count(*) FROM pg_auth_members WHERE member = "
                             "(SELECT oid FROM pg_roles WHERE rolname=session_user)").fetchone()[0] == 0,
                "role memberships forbidden, including SET ROLE paths")
        extensions = conn.execute("SELECT extname,extversion FROM pg_extension ORDER BY extname").fetchall()
        require([list(row) for row in extensions] == approval["approved_extensions"],
                "extension inventory drift")
        require(conn.execute("""SELECT count(*) FROM pg_namespace
            WHERE has_schema_privilege(current_user,oid,'CREATE')
               OR nspowner=(SELECT oid FROM pg_roles WHERE rolname=session_user)""").fetchone()[0] == 0,
                "schema creation/ownership anywhere forbidden")
        require(not any(conn.execute("""SELECT
            has_database_privilege(current_user,current_database(),'CREATE'),
            has_database_privilege(current_user,current_database(),'TEMP'),
            (SELECT datdba=(SELECT oid FROM pg_roles WHERE rolname=session_user)
             FROM pg_database WHERE datname=current_database())""").fetchone()),
                "database creation/temp/ownership forbidden")
        require(conn.execute("""SELECT count(*) FROM pg_class c JOIN pg_namespace n
            ON n.oid=c.relnamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema')
            AND c.relkind IN ('r','p','v','m','f','S') AND
            (c.relowner=(SELECT oid FROM pg_roles WHERE rolname=session_user) OR c.relrowsecurity
             OR (c.relkind <> 'S' AND
                (has_table_privilege(current_user,c.oid,'INSERT,UPDATE,DELETE,TRUNCATE,TRIGGER,REFERENCES')
                 OR has_any_column_privilege(current_user,c.oid,'INSERT,UPDATE,REFERENCES')))
             OR (c.relkind='S' AND has_sequence_privilege(current_user,c.oid,'USAGE,UPDATE')))""").fetchone()[0] == 0,
                "cross-schema ownership/RLS/mutation privileges")
        require(conn.execute("""SELECT count(*) FROM pg_proc p JOIN pg_namespace n
            ON n.oid=p.pronamespace WHERE has_function_privilege(current_user,p.oid,'EXECUTE')
            AND (p.prosecdef OR n.nspname NOT IN ('pg_catalog','information_schema'))""").fetchone()[0] == 0,
                "callable privileged/custom function")

        require(conn.execute("SELECT pg_catalog.pg_my_temp_schema()").fetchone()[0]==0,
                "collector connection must have no temporary namespace")
        conn.execute("SET LOCAL TIME ZONE 'UTC'")
        conn.execute("SELECT set_config('statement_timeout',%s,true)",(str(approval["statement_timeout_ms"]),))
        conn.execute("SELECT set_config('lock_timeout',%s,true)",(str(approval["lock_timeout_ms"]),))
        observed=conn.execute("""SELECT current_database(),session_user::text,current_user::text,
            current_setting('server_version'),current_setting('server_version_num'),
            current_setting('transaction_isolation'),current_setting('transaction_read_only')""").fetchone()
        require(tuple(observed)==(approval["database"],approval["login"],approval["role"],
                approval["server_version"],approval["server_version_num"],"repeatable read","on"),
                "environment/identity/isolation mismatch")
        dangerous=conn.execute("""SELECT count(*) FROM pg_roles WHERE
            (rolname IN (session_user,current_user) OR pg_has_role(session_user,oid,'MEMBER'))
            AND (rolsuper OR rolcreaterole OR rolcreatedb OR rolreplication OR rolbypassrls)""").fetchone()[0]
        require(dangerous==0,"privileged collector login or inheritance")
        require(not any(conn.execute("""SELECT has_schema_privilege(current_user,'mpt_poc','CREATE'),
            has_database_privilege(current_user,current_database(),'CREATE')""").fetchone()),
            "collector must not create objects")
        unsafe=conn.execute("""SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='mpt_poc' AND c.relkind IN ('r','v') AND
            (pg_has_role(session_user,c.relowner,'MEMBER') OR c.relrowsecurity OR
             has_table_privilege(current_user,c.oid,'INSERT,UPDATE,DELETE,TRUNCATE,TRIGGER')
             OR has_any_column_privilege(current_user,c.oid,'INSERT,UPDATE'))""").fetchone()[0]
        require(unsafe==0,"collector has mutating/owner privileges or RLS")
        callable_functions=conn.execute("""SELECT count(*) FROM pg_proc p JOIN pg_namespace n
            ON n.oid=p.pronamespace WHERE n.nspname='mpt_poc'
            AND has_function_privilege(current_user,p.oid,'EXECUTE')""").fetchone()[0]
        require(callable_functions==0,"collector must not call application functions")
        # Bind the complete reviewed security catalog, not just application-schema grants.
        # Each row is JSON text so ACL arrays and NULL remain deterministic driver scalars.
        security_queries = {
            "roles": "SELECT row_to_json(x)::text FROM (SELECT oid,rolname,rolsuper,rolinherit,"
                     "rolcreaterole,rolcreatedb,rolcanlogin,rolreplication,rolbypassrls,"
                     "rolconfig FROM pg_roles ORDER BY oid) x",
            "memberships": "SELECT row_to_json(x)::text FROM (SELECT * FROM pg_auth_members "
                           "ORDER BY roleid,member,grantor) x",
            "schemas": "SELECT row_to_json(x)::text FROM (SELECT oid,nspname,nspowner,nspacl "
                       "FROM pg_namespace ORDER BY oid) x",
            "relations": "SELECT row_to_json(x)::text FROM (SELECT oid,relnamespace,relname,relowner,"
                         "relkind,relacl,relrowsecurity,relforcerowsecurity FROM pg_class ORDER BY oid) x",
            "columns": "SELECT row_to_json(x)::text FROM (SELECT attrelid,attnum,attname,attacl "
                       "FROM pg_attribute WHERE attnum>0 AND NOT attisdropped ORDER BY attrelid,attnum) x",
            "functions": "SELECT row_to_json(x)::text FROM (SELECT oid,pronamespace,proname,proowner,"
                         "proacl,prosecdef,proleakproof,proconfig,prolang,proargtypes::text "
                         "FROM pg_proc ORDER BY oid) x",
            "databases": "SELECT row_to_json(x)::text FROM (SELECT oid,datname,datdba,datacl "
                         "FROM pg_database ORDER BY oid) x",
            "defaults": "SELECT row_to_json(x)::text FROM (SELECT * FROM pg_default_acl ORDER BY oid) x",
            "extensions": "SELECT row_to_json(x)::text FROM (SELECT oid,extname,extowner,extnamespace,"
                          "extversion FROM pg_extension ORDER BY oid) x",
        }
        security = {}
        for label, query in security_queries.items():
            security[label] = conn.execute(query).fetchall()
            budget.memory(security)
        security_bytes = json.dumps(security, sort_keys=True, ensure_ascii=True,
                                    separators=(",", ":")).encode("ascii")
        require(hashlib.sha256(security_bytes).hexdigest() == approval["privilege_review_sha256"],
                "security catalog differs from independently reviewed environment")
        del security, security_bytes
        # SHARE-read relation locks prevent DDL drift during catalog/data observations.
        lock_names=sorted(TABLES|{"published_positions"})
        conn.execute("LOCK TABLE "+",".join('mpt_poc.'+quoted(n) for n in lock_names)+" IN ACCESS SHARE MODE")
        relations=conn.execute("""SELECT c.relname,c.relkind FROM pg_class c JOIN pg_namespace n
            ON n.oid=c.relnamespace WHERE n.nspname='mpt_poc'
            AND c.relkind IN ('r','p','f','v','m') ORDER BY c.relname""").fetchall()
        require(dict(relations)=={**{n:"r" for n in TABLES},"published_positions":"v"},
                "unexpected relation inventory")
        for table in sorted(TABLES):
            expected=doc["tables"][table]
            cols=conn.execute("""SELECT a.attname,format_type(a.atttypid,a.atttypmod),NOT a.attnotnull
                FROM pg_attribute a WHERE a.attrelid=%s::regclass AND a.attnum>0
                AND NOT a.attisdropped ORDER BY a.attnum""",("mpt_poc."+table,)).fetchall()
            require([tuple(r) for r in cols]==[(c["name"],c["type"],c["nullable"])
                    for c in expected["columns"]],"column/type/nullability/order mismatch: "+table)
            pk=conn.execute("""SELECT a.attname FROM pg_index i
                CROSS JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum,ord)
                JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.attnum
                WHERE i.indrelid=%s::regclass AND i.indisprimary ORDER BY k.ord""",
                ("mpt_poc."+table,)).fetchall()
            require([r[0] for r in pk]==expected["pk"],"primary key mismatch: "+table)
        viewdef=conn.execute("SELECT pg_get_viewdef('mpt_poc.published_positions'::regclass,true)").fetchone()[0]
        require(hashlib.sha256(viewdef.encode("utf-8")).hexdigest()==approval["viewdef_sha256"],
                "view definition differs from independently approved version")
        view_names=("position_id","version","lifecycle","side","remaining_quantity","average_entry_price",
                    "domain_id","ordinal")
        view_types=("text","bigint","text","text","bigint","numeric","text","bigint")
        view_columns=[{"name":n,"type":t,"nullable":False} for n,t in zip(view_names,view_types)]
        vcols=conn.execute("""SELECT a.attname,format_type(a.atttypid,a.atttypmod)
            FROM pg_attribute a WHERE a.attrelid='mpt_poc.published_positions'::regclass
            AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum""").fetchall()
        require([tuple(r) for r in vcols]==list(zip(view_names,view_types)),"view shape mismatch")
        snapshot_id=conn.execute("SELECT pg_current_snapshot()::text").fetchone()[0]
        collected = {}
        def read(table, columns, keys):
            name = "mpt_poc." + quoted(table)
            count = conn.execute("SELECT count(*) FROM " + name).fetchone()[0]
            require(type(count) is int and 0 <= count <= approval["max_rows_per_table"],
                    "invalid/over-limit complete row count")
            query = "SELECT " + ",".join(projection(c) for c in columns) + " FROM " + name
            raw_rows = conn.execute(query, row_cap=approval["max_rows_per_table"]).fetchall()
            require(len(raw_rows) == count, "incomplete or duplicate transport result")
            converted, table_size, seen_keys = [], 0, set()
            for row in raw_rows:
                require(len(row) == len(columns), "row width mismatch")
                table_size += budget.row(row)
                require(table_size <= approval["max_bytes_per_table"], "table byte cap exceeded")
                require(budget.total + table_size <= approval["max_bytes_total"], "total byte cap exceeded")
                converted_row = {c["name"]: convert(c, value, approval) for c, value in zip(columns, row)}
                key = tuple(converted_row[k] for k in keys)
                require(None not in key and key not in seen_keys, "NULL/duplicate primary key")
                seen_keys.add(key)
                converted.append(converted_row)
                budget.memory((collected, raw_rows, converted))
            budget.relation(table_size)
            budget.remaining_ms()
            collected[table] = converted
            return converted
        tables = {n: read(n, doc["tables"][n]["columns"], doc["tables"][n]["pk"])
                  for n in sorted(TABLES)}
        published = read("published_positions", view_columns, ["position_id"])
        budget.remaining_ms()
        conn.execute("ROLLBACK")  # read-only snapshot closed; no partial result escapes on error
        return {"tables":tables,"published_rows":published,"provenance":{
            "mvcc_snapshot":snapshot_id,"observed_environment":list(observed),
            "run_id":approval["run_id"],"manifest_sha256":approval["manifest_sha256"],
            "configuration_sha256":config_hash,"schema_sha256":approval["schema_sha256"],
            "viewdef_sha256":approval["viewdef_sha256"],"status":"COLLECTED_NOT_VALIDATED"}}
    finally:
        finish(raw, transport_guard, approval["cleanup_timeout_ms"], sys.exception())
