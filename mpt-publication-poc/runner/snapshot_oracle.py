"""Independent documentary fixture construction. NOT_RUN; human review pending.
Source: FULL-SNAPSHOT-CONTRACT and SNAP-P01..05, never encoder outputs.
Scope: typed fixture tables and every snapshot layer; no database/FK-validity claim.
Derived hashes are only future comparisons, not precomputed evidence or approvals.
"""
import hashlib
import struct
from decimal import Decimal


def numeric_payload(value):
    if type(value) is not Decimal or not value.is_finite():
        raise ValueError("finite Decimal fixture required")
    fixed = format(value, "f")
    negative = fixed.startswith("-")
    unsigned = fixed.lstrip("-")
    integer, dot, fraction = unsigned.partition(".")
    coefficient = (integer + fraction).lstrip("0") or "0"
    if negative and coefficient != "0":
        coefficient = "-" + coefficient
    return coefficient + ":" + str(len(fraction))


def json_fixture(value):
    if value is None:
        return part("n", b"")
    if type(value) is bool:
        return part("b", "1" if value else "0")
    if type(value) is str:
        return part("s", value)
    if type(value) is Decimal:
        return part("d", numeric_payload(value))
    if type(value) is list:
        return part("a", b"".join(json_fixture(v) for v in value))
    if type(value) is dict and all(type(k) is str for k in value):
        return part("o", b"".join(part("k", k) + json_fixture(value[k])
                    for k in sorted(value, key=lambda x: x.encode("utf-8"))))
    raise ValueError("unsupported JSON fixture")


def scalar_fixture(typ, value):
    if typ not in ("text", "boolean", "integer", "bigint", "xid8", "numeric",
                   "jsonb", "bytea", "timestamp with time zone"):
        raise ValueError("unknown fixture type")
    if value is None:
        return part("N", b"")
    if typ == "text" and type(value) is str:
        return part("T", value)
    if typ == "boolean" and type(value) is bool:
        return part("B", "1" if value else "0")
    if typ in ("integer", "bigint", "xid8") and type(value) is int:
        bounds = {"integer": (-2147483648, 2147483647),
                  "bigint": (-9223372036854775808, 9223372036854775807),
                  "xid8": (0, 18446744073709551615)}
        low, high = bounds[typ]
        if not low <= value <= high:
            raise ValueError("integer fixture range")
        return part("X" if typ == "xid8" else "I", str(value))
    if typ == "numeric":
        return part("D", numeric_payload(value))
    if typ == "bytea" and type(value) is bytes:
        return part("Y", value)
    if typ == "jsonb":
        return part("J", json_fixture(value))
    if typ == "timestamp with time zone" and type(value) is dict and set(value) == {"micros"}:
        micros = value["micros"]
        if type(micros) is not int or not -9223372036854775808 < micros < 9223372036854775807:
            raise ValueError("timestamp wire range, not PostgreSQL validity")
        return part("Z", str(micros))
    raise ValueError("wrong fixture type")


def part(tag, payload):
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    return bytes([ord(tag)]) + struct.pack(">Q", len(payload)) + payload


def sha(value):
    return hashlib.sha256(value).digest()


def relation(name, schema, rows, version="MPT-SNAPSHOT@1", position=None):
    fields = []
    for column in schema["columns"]:
        fields.extend([part("c", column["name"]), part("t", column["type"]),
                       part("b", "1" if column["nullable"] else "0")])
    fields.append(part("p", b"".join(part("c", k) for k in schema["pk"])))
    keyed = []
    for row in rows:
        if set(row) != {c["name"] for c in schema["columns"]}:
            raise ValueError("fixture field inventory mismatch")
        values = {}
        for column in schema["columns"]:
            value = row[column["name"]]
            if value is None and (not column["nullable"] or column["name"] in schema["pk"]):
                raise ValueError("NULL in required fixture column")
            values[column["name"]] = scalar_fixture(column["type"], value)
        key = part("k", b"".join(values[k] for k in schema["pk"]))
        body = part("r", b"".join(values[c["name"]] for c in schema["columns"]))
        keyed.append((key, body))
    if len({key for key, _ in keyed}) != len(keyed):
        raise ValueError("duplicate fixture primary key")
    prefix = part("v", version)
    if position is not None:
        prefix += part("p", position)
    return (prefix + part("t", name) + part("s", b"".join(fields)) +
            part("c", str(len(rows))) + part("r", b"".join(v for _, v in sorted(keyed))))


def aggregate_stream(version, streams, position=None):
    result = part("v", version)
    if position is not None:
        result += part("p", position)
    for name in sorted(streams, key=lambda n: n.encode("utf-8")):
        result += part("t", name) + part("h", sha(streams[name]))
    return result


def fixture_snapshot(schemas, rows, published_rows=()):
    """Fixed synthetic provenance; supplied typed published rows. No collection authority."""
    version = "MPT-SNAPSHOT@1"
    normal = {"mpt_poc." + n: relation("mpt_poc." + n, s, rows[n])
              for n, s in schemas.items()}
    scoped = {n for n, s in schemas.items() if "position_id" in [c["name"] for c in s["columns"]]}
    position_streams = {}
    position_tables = {}
    for position in sorted({r["position_id"] for n in scoped for r in rows[n]}):
        streams = {"mpt_poc." + n: relation("mpt_poc." + n, schemas[n],
                   [r for r in rows[n] if r["position_id"] == position],
                   version + "/POSITION", position) for n in scoped}
        position_tables[position] = streams
        position_streams[position] = aggregate_stream(version + "/POSITION", streams, position)
    global_tables = {"mpt_poc." + n: relation("mpt_poc." + n, s, rows[n], version + "/GLOBAL")
                     for n, s in schemas.items() if n not in scoped}
    global_stream = aggregate_stream(version + "/GLOBAL", global_tables)
    persisted = aggregate_stream(version + "/PERSISTED", normal)
    metadata_names = ("publication_barrier", "publication_batch", "publication_cut", "public_projection")
    metadata_bytes = b"".join(normal["mpt_poc." + n] for n in sorted(metadata_names))
    view_schema = {"pk": ["position_id"], "columns": [
        {"name": n, "type": t, "nullable": False} for n, t in [
            ("position_id", "text"), ("version", "bigint"), ("lifecycle", "text"),
            ("side", "text"), ("remaining_quantity", "bigint"), ("average_entry_price", "numeric"),
            ("domain_id", "text"), ("ordinal", "bigint")]]}
    published = relation("mpt_poc.published_positions", view_schema, published_rows, version + "/PUBLISHED")
    envelope_bytes = (part("v", version + "/ENVELOPE") + part("h", sha(persisted)) +
                      part("h", sha(published)) + part("h", sha(metadata_bytes)) +
                      part("m", bytes(32)) + part("c", bytes.fromhex("11" * 32)) +
                      part("r", "VECTOR-ONLY"))
    return {"normal": normal, "position_tables": position_tables,
            "positions": position_streams, "global": global_stream,
            "global_tables": global_tables, "persisted": persisted,
            "metadata": metadata_bytes, "published": published, "envelope": envelope_bytes}

def populated_fixture(schemas):
    """One explicit typed row per table; all declared fields included. Wire-only, not FK-valid."""
    values = {"text": "SYNTH-A", "boolean": False, "integer": 1, "bigint": 1,
              "xid8": 1, "numeric": Decimal("1.00"), "bytea": bytes.fromhex("00ff"),
              "timestamp with time zone": {"micros": -1},
              "jsonb": {"a": [None, False, Decimal("1.00"), "\u00e9"]}}
    return {name: [{c["name"]: None if c["nullable"] and c["name"] not in s["pk"]
                    else values[c["type"]] for c in s["columns"]}]
            for name, s in schemas.items()}


def layer_records(snapshot):
    """Future reviewable bytes/length/SHA records, NOT executed or frozen by this source."""
    streams = {}
    for name, value in snapshot["normal"].items():
        streams["table:" + name] = value
    for position, tables in snapshot["position_tables"].items():
        for name, value in tables.items():
            streams["position-table:" + position + ":" + name] = value
    for position, value in snapshot["positions"].items():
        streams["position:" + position] = value
    for name, value in snapshot["global_tables"].items():
        streams["global-table:" + name] = value
    for name in ("global", "persisted", "metadata", "published", "envelope"):
        streams[name] = snapshot[name]
    return {name: {"hex": value.hex(), "length": len(value), "sha256": sha(value).hex(),
                   "source": "independent SNAP-P01..05 fixture derivation",
                   "reviewer": "PENDING_HUMAN_APPROVAL"}
            for name, value in streams.items()}
