"""MPT-SNAPSHOT@1 candidate encoder. NOT_RUN. Pure supplied-data operations; no DB collector."""
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

VERSION = "MPT-SNAPSHOT@1"
TABLES = frozenset("access_audit assessment_attempt assessment_result batch_recovery_audit command_receipt delivery_audit domain_resolution_policy notification notification_decision outbox_event personal_journal_entry plan plan_revision position position_event position_guard position_revision public_projection publication_barrier publication_batch publication_cut publication_domain publication_member recipient_guard send_authorization synthetic_destination_call synthetic_destination_receipt t4_operation_receipt worker_lease worker_lease_audit".split())


@dataclass(frozen=True)
class Jsonb:
    value: object  # parsed stored JSONB, Decimal numbers; NOT a Python float


@dataclass(frozen=True)
class TimestampMicros:
    value: int  # exact stored UTC microseconds, supports outside datetime's year range


def frame(tag, payload):
    if type(tag) is not str or len(tag)!=1 or not tag.isascii() or type(payload) is not bytes:
        raise ValueError("invalid frame")
    return tag.encode("ascii")+len(payload).to_bytes(8,"big")+payload


def text_frame(tag, value):
    if type(value) is not str:
        raise ValueError("text required")
    return frame(tag,value.encode("utf-8",errors="strict"))


def decimal_bytes(value):
    if type(value) is not Decimal or not value.is_finite():
        raise ValueError("finite exact Decimal required")
    sign,digits,exponent = value.as_tuple()
    coefficient = "".join(str(d) for d in digits).lstrip("0") or "0"
    if exponent>0:
        coefficient = coefficient+"0"*exponent if coefficient!="0" else "0"
    scale = max(-exponent,0)
    if sign and coefficient!="0":
        coefficient = "-"+coefficient
    return (coefficient+":"+str(scale)).encode("ascii")


def json_value(value):
    if value is None:
        return frame("n",b"")
    if type(value) is bool:
        return frame("b",b"1" if value else b"0")
    if type(value) is str:
        return text_frame("s",value)
    if type(value) is Decimal:
        return frame("d",decimal_bytes(value))
    if type(value) is int:
        return frame("d",decimal_bytes(Decimal(value)))
    if type(value) is list:
        return frame("a",b"".join(json_value(x) for x in value))
    if type(value) is dict and all(type(k) is str for k in value):
        return frame("o",b"".join(text_frame("k",k)+json_value(value[k])
                                 for k in sorted(value,key=lambda s:s.encode("utf-8"))))
    raise ValueError("unsupported JSONB value; floats forbidden")


def parse_stored_jsonb(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:
                raise ValueError("duplicate key: input must be stored JSONB representation")
            result[key]=value
        return result
    def invalid(value):
        raise ValueError("nonfinite JSON token")
    return Jsonb(json.loads(raw,parse_int=Decimal,parse_float=Decimal,
                           parse_constant=invalid,object_pairs_hook=pairs))


def scalar(sql_type, value):
    if sql_type not in {"text", "boolean", "integer", "bigint", "xid8", "numeric",
                        "bytea", "timestamp with time zone", "jsonb"}:
        raise ValueError("unknown SQL type")
    if value is None:
        return frame("N",b"")
    if sql_type=="text":
        return text_frame("T",value)
    if sql_type=="boolean":
        if type(value) is not bool:
            raise ValueError("boolean required")
        return frame("B",b"1" if value else b"0")
    if sql_type in ("integer","bigint","xid8"):
        if type(value) is not int:
            raise ValueError("exact integer required")
        lo,hi = {"integer":(-2**31,2**31-1),"bigint":(-2**63,2**63-1),"xid8":(0,2**64-1)}[sql_type]
        if not lo<=value<=hi:
            raise ValueError("integer out of range")
        return frame("X" if sql_type=="xid8" else "I",str(value).encode("ascii"))
    if sql_type=="numeric":
        return frame("D",decimal_bytes(value))
    if sql_type=="bytea":
        if type(value) is not bytes:
            raise ValueError("bytea requires bytes")
        return frame("Y",value)
    if sql_type=="timestamp with time zone":
        if type(value) is TimestampMicros and type(value.value) is int:
            micros=value.value
        elif type(value) is datetime and value.tzinfo is not None and value.utcoffset() is not None:
            delta=value.astimezone(timezone.utc)-datetime(1970,1,1,tzinfo=timezone.utc)
            micros=(delta.days*86400+delta.seconds)*1000000+delta.microseconds
        else:
            raise ValueError("aware datetime or exact stored TimestampMicros required")
        if not -2**63<micros<2**63-1:
            raise ValueError("invalid/nonfinite stored timestamp")
        return frame("Z",str(micros).encode("ascii"))
    if sql_type=="jsonb" and type(value) is Jsonb:
        return frame("J",json_value(value.value))
    raise ValueError("unsupported SQL type/value")


def descriptor(schema):
    if type(schema) is not dict or set(schema) != {"columns", "pk"}:
        raise ValueError("unknown/missing schema field")
    if type(schema["columns"]) is not list or type(schema["pk"]) is not list:
        raise ValueError("schema lists required")
    if any(type(c) is not dict or set(c) != {"name", "type", "nullable"}
           or type(c["name"]) is not str or not c["name"] for c in schema["columns"]):
        raise ValueError("unknown/missing column metadata")
    cols=schema["columns"]
    names=[c["name"] for c in cols]
    if len(names)!=len(set(names)) or not schema["pk"] or not set(schema["pk"])<=set(names):
        raise ValueError("invalid schema identity")
    if len(schema["pk"])!=len(set(schema["pk"])):
        raise ValueError("duplicate primary key column")
    allowed={"text","boolean","integer","bigint","xid8","numeric","bytea",
             "timestamp with time zone","jsonb"}
    if any(c["type"] not in allowed or type(c["nullable"]) is not bool for c in cols):
        raise ValueError("invalid column metadata")
    return frame("s",b"".join(text_frame("c",c["name"])+text_frame("t",c["type"])
        +frame("b",b"1" if c["nullable"] else b"0") for c in cols)
        +frame("p",b"".join(text_frame("c",key) for key in schema["pk"])))


def rows_bytes(schema, rows):
    names=[c["name"] for c in schema["columns"]]
    ordered=[]
    for row in rows:
        if type(row) is not dict or set(row)!=set(names):
            raise ValueError("row columns differ from schema")
        values={}
        for c in schema["columns"]:
            if row[c["name"]] is None and (not c["nullable"] or c["name"] in schema["pk"]):
                raise ValueError("null in required column")
            values[c["name"]]=scalar(c["type"],row[c["name"]])
        key=frame("k",b"".join(values[k] for k in schema["pk"]))
        ordered.append((key,frame("r",b"".join(values[n] for n in names))))
    ordered.sort(key=lambda pair:pair[0])
    if any(a[0]==b[0] for a,b in zip(ordered,ordered[1:])):
        raise ValueError("duplicate primary key")
    return b"".join(row for _,row in ordered)


def table_bytes(name, schema, rows, version=VERSION, position=None):
    if version not in (VERSION,VERSION+"/POSITION",VERSION+"/GLOBAL",VERSION+"/PUBLISHED"):
        raise ValueError("unknown table version")
    if (position is not None)!=(version==VERSION+"/POSITION"):
        raise ValueError("invalid partition identity")
    if position is not None and (type(position) is not str or not position):
        raise ValueError("empty/invalid position identity")
    prefix=text_frame("v",version)
    if position is not None:
        prefix+=text_frame("p",position)
    return (prefix+text_frame("t",name)+descriptor(schema)
            +text_frame("c",str(len(rows)))+frame("r",rows_bytes(schema,rows)))


def digest(data):
    return hashlib.sha256(data).digest()


def combined(version, pairs, position=None):
    if version not in (VERSION+"/PERSISTED", VERSION+"/POSITION", VERSION+"/GLOBAL"):
        raise ValueError("unknown aggregate version")
    if (position is not None) != (version == VERSION+"/POSITION"):
        raise ValueError("invalid aggregate partition")
    if position is not None and (type(position) is not str or not position):
        raise ValueError("empty aggregate partition")
    if type(pairs) is not dict or any(type(n) is not str or not n or
                                     type(h) is not bytes or len(h) != 32
                                     for n, h in pairs.items()):
        raise ValueError("invalid aggregate digest")
    payload=text_frame("v",version)
    if position is not None:
        payload+=text_frame("p",position)
    return digest(payload+b"".join(text_frame("t",n)+frame("h",h)
                                  for n,h in sorted(pairs.items())))


def snapshot(schema_document, tables, published_rows, manifest_sha256, config_sha256, run_id):
    """No collection: caller must supply one independently attested complete MVCC snapshot."""
    if type(schema_document) is not dict or set(schema_document) != {"contract", "tables"}:
        raise ValueError("unknown/missing schema document field")
    schemas=schema_document["tables"]
    if schema_document["contract"]!=VERSION or set(schemas)!=TABLES or set(tables)!=TABLES:
        raise ValueError("wrong schema/table inventory")
    if any(type(rows) is not list for rows in tables.values()):
        raise ValueError("materialized table row lists required")
    for supplied_hash in (manifest_sha256,config_sha256):
        if type(supplied_hash) is not str or re.fullmatch("[0-9a-f]{64}",supplied_hash) is None:
            raise ValueError("invalid provenance hash")
    if type(run_id) is not str or not run_id:
        raise ValueError("run identity required")
    canonical={n:table_bytes("mpt_poc."+n,schemas[n],tables[n]) for n in sorted(schemas)}
    hashes={"mpt_poc."+n:digest(data) for n,data in canonical.items()}
    persisted=combined(VERSION+"/PERSISTED",hashes)
    scoped={n for n,s in schemas.items() if any(c["name"]=="position_id" for c in s["columns"])}
    positions=sorted({row["position_id"] for n in scoped for row in tables[n]})
    aggregates={}
    for position in positions:
        subset={"mpt_poc."+n:digest(table_bytes("mpt_poc."+n,schemas[n],
                    [r for r in tables[n] if r["position_id"]==position],VERSION+"/POSITION",position))
                for n in scoped}
        aggregates[position]=combined(VERSION+"/POSITION",subset,position).hex()
    global_tables={"mpt_poc."+n:digest(table_bytes("mpt_poc."+n,schemas[n],tables[n],VERSION+"/GLOBAL"))
                   for n in schemas if n not in scoped}
    view_names=("position_id","version","lifecycle","side","remaining_quantity","average_entry_price",
                "domain_id","ordinal")
    view_types=("text","bigint","text","text","bigint","numeric","text","bigint")
    view_schema={"columns":[{"name":n,"type":t,"nullable":False} for n,t in zip(view_names,view_types)],
                 "pk":["position_id"]}
    published=digest(table_bytes("mpt_poc.published_positions",view_schema,published_rows,
                                 VERSION+"/PUBLISHED"))
    metadata=b"".join(canonical[n] for n in sorted(
        ("publication_barrier","publication_cut","publication_batch","public_projection")))
    envelope=digest(text_frame("v",VERSION+"/ENVELOPE")+frame("h",persisted)+frame("h",published)
        +frame("h",digest(metadata))+frame("m",bytes.fromhex(manifest_sha256))
        +frame("c",bytes.fromhex(config_sha256))+text_frame("r",run_id))
    return {"contract":VERSION,"table_sha256":{n:h.hex() for n,h in hashes.items()},
            "persisted_sha256":persisted.hex(),"position_sha256":aggregates,
            "global_partition_sha256":combined(VERSION+"/GLOBAL",global_tables).hex(),
            "published_sha256":published.hex(),"publication_metadata_sha256":digest(metadata).hex(),
            "envelope_sha256":envelope.hex()}
