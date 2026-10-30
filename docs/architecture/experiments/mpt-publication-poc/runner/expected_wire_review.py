"""Independent structural wire checks. NOT_RUN; no emitter/oracle/SUT/parser imports."""
import hashlib
import re

TAGS = {"text": b"T", "boolean": b"B", "integer": b"I", "bigint": b"I",
        "xid8": b"X", "numeric": b"D", "bytea": b"Y",
        "timestamp with time zone": b"Z", "jsonb": b"J"}
VERSION = b"MPT-SNAPSHOT@1"


def frames(raw, limits):
    if type(raw) is not bytes or len(raw) > limits.wire_bytes:
        raise ValueError("wire budget")
    offset = 0
    result = []
    while offset < len(raw):
        if len(result) >= limits.nodes or len(raw) - offset < 9:
            raise ValueError("frame boundary/count")
        length = int.from_bytes(raw[offset+1:offset+9], "big")
        end = offset + 9 + length
        if end > len(raw):
            raise ValueError("frame length")
        result.append((raw[offset:offset+1], raw[offset+9:end], raw[offset:end]))
        offset = end
    return result


def one(raw, limits):
    parts = frames(raw, limits)
    if len(parts) != 1:
        raise ValueError("one frame required")
    return parts[0]


def decimal_payload(payload, limits):
    if len(payload) > limits.decimal_digits + 8 or re.fullmatch(
            rb"(?:0|-?[1-9][0-9]*):(?:0|[1-9][0-9]*)", payload) is None:
        raise ValueError("decimal syntax")
    coefficient, scale = payload.split(b":")
    if len(coefficient.lstrip(b"-")) > limits.decimal_digits or int(scale) > limits.decimal_exponent:
        raise ValueError("decimal budget")


def json_node(raw, limits, depth=0, count=None):
    count = [0] if count is None else count
    count[0] += 1
    if depth > min(16, limits.depth) or count[0] > min(1024, limits.nodes):
        raise ValueError("JSON wire budget")
    tag, payload, _ = one(raw, limits)
    if tag == b"n" and payload == b"":
        return
    if tag == b"b" and payload in (b"0", b"1"):
        return
    if tag == b"s":
        payload.decode("utf-8")
        return
    if tag == b"d":
        decimal_payload(payload, limits)
        return
    children = frames(payload, limits)
    if tag == b"a":
        for child in children:
            json_node(child[2], limits, depth + 1, count)
        return
    if tag == b"o" and len(children) % 2 == 0:
        keys = []
        for i in range(0, len(children), 2):
            key, value = children[i:i+2]
            if key[0] != b"k":
                raise ValueError("JSON key tag")
            key[1].decode("utf-8")
            keys.append(key[1])
            json_node(value[2], limits, depth + 1, count)
        if keys != sorted(set(keys)):
            raise ValueError("JSON key order/duplicate")
        return
    raise ValueError("JSON node tag/value")


def scalar(raw, column, limits):
    if len(raw) > limits.scalar_bytes:
        raise ValueError("scalar budget")
    tag, payload, _ = one(raw, limits)
    if tag == b"N":
        if payload or not column["nullable"]:
            raise ValueError("NULL semantic")
        return
    typ = column["type"]
    if tag != TAGS.get(typ):
        raise ValueError("SQL type/tag")
    if typ == "text":
        payload.decode("utf-8")
    elif typ == "boolean":
        if payload not in (b"0", b"1"):
            raise ValueError("bool")
    elif typ in ("integer", "bigint", "xid8", "timestamp with time zone"):
        if len(payload) > 20 or re.fullmatch(rb"(?:0|-?[1-9][0-9]*)", payload) is None:
            raise ValueError("integer syntax")
        value = int(payload)
        low, high = {"integer": (-2**31, 2**31-1), "bigint": (-2**63, 2**63-1),
                     "xid8": (0, 2**64-1),
                     "timestamp with time zone": (-2**63+1, 2**63-2)}[typ]
        if not low <= value <= high:
            raise ValueError("wire integer range, not PostgreSQL finite dates")
    elif typ == "numeric":
        decimal_payload(payload, limits)
    elif typ == "jsonb":
        json_node(payload, limits)


def row(raw, schema, limits):
    tag, payload, _ = one(raw, limits)
    if tag != b"r":
        raise ValueError("row tag")
    values = frames(payload, limits)
    if len(values) != len(schema["columns"]):
        raise ValueError("row field count")
    for value, column in zip(values, schema["columns"]):
        scalar(value[2], column, limits)
    mapping = {c["name"]: v for c, v in zip(schema["columns"], values)}
    if any(mapping[k][0] == b"N" for k in schema["pk"]):
        raise ValueError("NULL PK")
    pk = b"".join(mapping[k][2] for k in schema["pk"])
    key = b"k" + len(pk).to_bytes(8, "big") + pk
    return key, mapping


def table(raw, name, schema, version, position, limits):
    parts = frames(raw, limits)
    tags = [b"v"] + ([b"p"] if position is not None else []) + [b"t", b"s", b"c", b"r"]
    if [p[0] for p in parts] != tags or parts[0][1] != version:
        raise ValueError("table framing/version")
    if position is not None:
        if parts[1][1] != position.encode("utf-8"):
            raise ValueError("partition identity")
        parts = [parts[0]] + parts[2:]
    if parts[1][1] != ("mpt_poc." + name).encode("utf-8"):
        raise ValueError("qualified table identity")
    descriptor = frames(parts[2][1], limits)
    expected = []
    for c in schema["columns"]:
        expected.extend([(b"c", c["name"].encode()), (b"t", c["type"].encode()),
                         (b"b", b"1" if c["nullable"] else b"0")])
    if len(descriptor) != len(expected) + 1 or [(t, p) for t, p, _ in descriptor[:-1]] != expected:
        raise ValueError("schema descriptor")
    if descriptor[-1][0] != b"p" or [(t, p.decode("utf-8")) for t, p, _ in frames(
            descriptor[-1][1], limits)] != [(b"c", k) for k in schema["pk"]]:
        raise ValueError("schema PK")
    rows = frames(parts[4][1], limits)
    if len(rows) > 3 or parts[3][1] != str(len(rows)).encode("ascii"):
        raise ValueError("row count")
    parsed = [row(r[2], schema, limits) for r in rows]
    keys = [k for k, _ in parsed]
    if keys != sorted(set(keys)):
        raise ValueError("PK order/duplicate")
    return [r[2] for r in rows], parsed


def validate_slots(records, schema, specs, limits):
    """Validate bytes against supplied hash-bound schema/template and cross-layer links.
    This validates structure/consistency, not independent human truth of fixture values.
    """
    tables = schema["tables"]
    if schema["contract"] != "MPT-SNAPSHOT@1" or len(tables) != 30 or sum(
            len(t["columns"]) for t in tables.values()) != 191:
        raise ValueError("schema inventory")
    expected_ids = sorted(specs)
    if len(expected_ids) != 428 or list(records) != expected_ids:
        raise ValueError("exact slot order")
    data = {}
    total = 0
    for key, record in records.items():
        if type(record["hex"]) is not str or len(record["hex"]) > 2 * limits.wire_bytes:
            raise ValueError("wire hex bound")
        total += len(record["hex"]) // 2
        if total > limits.input_bytes:
            raise ValueError("total wire budget")
        data[key] = bytes.fromhex(record["hex"])
    parsed_tables = {}
    for key in expected_ids:
        spec = specs[key]
        fixture, layer = key.split("/")[:2]
        if spec["id"] != key or spec["fixture_id"] != fixture or spec["layer"] != layer:
            raise ValueError("ID/spec mismatch")
        if layer in ("table", "partition-table", "global-table"):
            name = spec["table"]
            position = spec.get("position") if layer == "partition-table" else None
            suffix = {"table": b"", "partition-table": b"/POSITION", "global-table": b"/GLOBAL"}[layer]
            parsed_tables[key] = table(data[key], name, tables[name], VERSION + suffix, position, limits)
        elif layer == "scalar":
            col = next(c for c in tables[spec["table"]]["columns"] if c["name"] == spec["column"])
            scalar(data[key], col, limits)
        elif layer == "row":
            row(data[key], tables[spec["table"]], limits)
    scoped = {n for n, t in tables.items() if any(c["name"] == "position_id" for c in t["columns"])}
    for key, (rows, parsed) in parsed_tables.items():
        spec = specs[key]
        prefix, name, layer = spec["fixture_id"] + "/", spec["table"], spec["layer"]
        normal_key = prefix + "table/" + name
        if layer == "table":
            if len(rows) != spec["row_count"]:
                raise ValueError("fixture row count")
            for i, (wire, (_, mapping)) in enumerate(zip(rows, parsed)):
                if data[prefix + "row/" + name + "/" + str(i)] != wire:
                    raise ValueError("row/table link")
                for c, value in mapping.items():
                    if data[prefix + "scalar/" + name + "/" + str(i) + "/" + c] != value[2]:
                        raise ValueError("scalar/row link")
        else:
            normal_rows, normal_parsed = parsed_tables[normal_key]
            if layer == "global-table":
                if name in scoped or rows != normal_rows:
                    raise ValueError("global membership")
            else:
                selected = [r for r, (_, m) in zip(normal_rows, normal_parsed)
                            if m["position_id"][1] == spec["position"].encode()]
                if name not in scoped or rows != selected:
                    raise ValueError("partition membership")
    view = {"pk": ["position_id"], "columns": [
        {"name": n, "type": t, "nullable": False} for n, t in (
            ("position_id", "text"), ("version", "bigint"), ("lifecycle", "text"),
            ("side", "text"), ("remaining_quantity", "bigint"), ("average_entry_price", "numeric"),
            ("domain_id", "text"), ("ordinal", "bigint"))]}
    for key in expected_ids:
        spec = specs[key]
        prefix, layer = spec["fixture_id"] + "/", spec["layer"]
        if layer == "published":
            rows, _ = table(data[key], "published_positions", view, VERSION + b"/PUBLISHED", None, limits)
            if len(rows) != (1 if spec["fixture_id"] == "TYPED@1" else 0):
                raise ValueError("view recipe count")
        elif layer == "metadata":
            names = sorted(("publication_barrier", "publication_batch", "publication_cut", "public_projection"))
            # All components already independently parsed; bounded input sum precedes join.
            if data[key] != b"".join(data[prefix + "table/" + n] for n in names):
                raise ValueError("metadata full-stream order")
        elif layer in ("persisted", "global", "position"):
            parts = frames(data[key], limits)
            expected = [(b"v", VERSION + b"/" + layer.upper().encode())]
            if layer == "position":
                expected.append((b"p", spec["position"].encode()))
            names = sorted(tables if layer == "persisted" else scoped if layer == "position"
                           else set(tables) - scoped)
            for n in names:
                child = prefix + (("table/" + n) if layer == "persisted" else
                                  ("global-table/" + n) if layer == "global" else
                                  ("partition-table/" + spec["position"] + "/" + n))
                expected.extend([(b"t", ("mpt_poc." + n).encode()),
                                 (b"h", hashlib.sha256(data[child]).digest())])
            if [(t, p) for t, p, _ in parts] != expected:
                raise ValueError("aggregate membership/digest")
        elif layer == "envelope":
            expected = [(b"v", VERSION + b"/ENVELOPE")]
            expected += [(b"h", hashlib.sha256(data[prefix + n]).digest())
                         for n in ("persisted", "published", "metadata")]
            expected += [(b"m", bytes(32)), (b"c", bytes.fromhex("11"*32)), (b"r", b"VECTOR-ONLY")]
            if [(t, p) for t, p, _ in frames(data[key], limits)] != expected:
                raise ValueError("envelope recipe")
