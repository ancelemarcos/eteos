"""Independent reference parser. NOT_RUN. Does not import or call snapshot_codec."""
import re


def frames(data):
    if type(data) is not bytes:
        raise ValueError("bytes required")
    result=[]
    cursor=0
    while cursor<len(data):
        start=cursor
        if len(data)-cursor<9:
            raise ValueError("truncated header")
        tag=data[cursor:cursor+1].decode("ascii")
        length=int.from_bytes(data[cursor+1:cursor+9],"big")
        cursor+=9
        end=cursor+length
        if end>len(data):
            raise ValueError("truncated payload")
        result.append((tag,data[cursor:end],data[start:end]))
        cursor=end
    return result


def integer(payload, unsigned=False):
    s=payload.decode("ascii")
    pattern=r"(0|[1-9][0-9]*)" if unsigned else r"(0|-?[1-9][0-9]*)"
    if re.fullmatch(pattern,s) is None:
        raise ValueError("noncanonical integer")
    return int(s)


def number(payload):
    pieces=payload.split(b":")
    if len(pieces)!=2:
        raise ValueError("numeric needs coefficient:scale")
    return (integer(pieces[0]),integer(pieces[1],True))


def json_node(tag,payload):
    if tag=="n" and payload==b"":
        return ("json-null",)
    if tag=="b" and payload in (b"0",b"1"):
        return ("json-bool",payload==b"1")
    if tag=="s":
        return ("json-string",payload.decode("utf-8"))
    if tag=="d":
        return ("json-number",)+number(payload)
    if tag=="a":
        return ("json-array",tuple(json_node(t,p) for t,p,_ in frames(payload)))
    if tag=="o":
        pairs=frames(payload)
        if len(pairs)%2:
            raise ValueError("unpaired object member")
        output=[]
        previous=None
        for index in range(0,len(pairs),2):
            key,value=pairs[index:index+2]
            if key[0]!="k" or (previous is not None and key[1]<=previous):
                raise ValueError("unordered/duplicate object key")
            previous=key[1]
            output.append((key[1].decode("utf-8"),json_node(value[0],value[1])))
        return ("json-object",tuple(output))
    raise ValueError("invalid JSON node")


def scalar(data):
    nodes=frames(data)
    if len(nodes)!=1:
        raise ValueError("exactly one scalar required")
    tag,payload,_=nodes[0]
    if tag=="N" and not payload:
        return ("sql-null",)
    if tag=="T":
        return ("text",payload.decode("utf-8"))
    if tag=="B" and payload in (b"0",b"1"):
        return ("boolean",payload==b"1")
    if tag in ("I","X","Z"):
        value=integer(payload,tag=="X")
        if tag=="X" and value>=2**64:
            raise ValueError("xid8 overflow")
        if tag=="I" and not -2**63<=value<2**63:
            raise ValueError("bigint overflow")
        if tag=="Z" and not -2**63<value<2**63-1:
            raise ValueError("invalid/nonfinite timestamp")
        return ({"I":"integer","X":"xid8","Z":"timestamp-micros"}[tag],value)
    if tag=="D":
        return ("numeric",)+number(payload)
    if tag=="Y":
        return ("bytes-hex",payload.hex())
    if tag=="J":
        children=frames(payload)
        if len(children)!=1:
            raise ValueError("one JSONB value required")
        return ("jsonb",json_node(children[0][0],children[0][1]))
    raise ValueError("invalid scalar")


def table(data):
    """Decode table wire format independently; return ordered schema, keys and typed values."""
    nodes=frames(data)
    if len(nodes) not in (5,6) or nodes[0][0]!="v":
        raise ValueError("invalid table framing")
    version=nodes.pop(0)[1].decode("utf-8")
    if version not in ("MPT-SNAPSHOT@1","MPT-SNAPSHOT@1/POSITION",
                       "MPT-SNAPSHOT@1/GLOBAL","MPT-SNAPSHOT@1/PUBLISHED"):
        raise ValueError("unknown table version")
    position=None
    if nodes[0][0]=="p":
        position=nodes.pop(0)[1].decode("utf-8")
    if (position is not None)!=(version=="MPT-SNAPSHOT@1/POSITION"):
        raise ValueError("invalid partition identity")
    if position=="":
        raise ValueError("empty position identity")
    if [t for t,_,_ in nodes]!=["t","s","c","r"]:
        raise ValueError("invalid table field order")
    name=nodes[0][1].decode("utf-8")
    desc=frames(nodes[1][1])
    if not desc or desc[-1][0]!="p" or (len(desc)-1)%3:
        raise ValueError("invalid descriptor")
    columns=[]
    for offset in range(0,len(desc)-1,3):
        n,t,nullable=desc[offset:offset+3]
        if (n[0],t[0],nullable[0])!=("c","t","b") or nullable[1] not in (b"0",b"1"):
            raise ValueError("invalid column descriptor")
        columns.append((n[1].decode("utf-8"),t[1].decode("utf-8"),nullable[1]==b"1"))
    keys=frames(desc[-1][1])
    if not keys or any(t!="c" for t,_,_ in keys):
        raise ValueError("invalid primary key")
    pk=[p.decode("utf-8") for _,p,_ in keys]
    names=[c[0] for c in columns]
    if len(set(names))!=len(names) or len(set(pk))!=len(pk) or not set(pk)<=set(names):
        raise ValueError("schema duplicates/unknown key")
    count=integer(nodes[2][1],True)
    rows=frames(nodes[3][1])
    if len(rows)!=count:
        raise ValueError("row count mismatch")
    decoded=[]
    previous=None
    expected={"text":"text","boolean":"boolean","integer":"integer","bigint":"integer",
              "xid8":"xid8","numeric":"numeric","bytea":"bytes-hex",
              "timestamp with time zone":"timestamp-micros","jsonb":"jsonb"}
    if any(typ not in expected for _,typ,_ in columns):
        raise ValueError("unknown descriptor type")
    for tag,payload,_ in rows:
        fields=frames(payload)
        if tag!="r" or len(fields)!=len(columns):
            raise ValueError("wrong row width")
        values=[scalar(raw) for _,_,raw in fields]
        for (col,typ,nullable),value in zip(columns,values):
            if value[0]=="sql-null":
                if not nullable or col in pk:
                    raise ValueError("NULL forbidden")
            elif typ not in expected or value[0]!=expected[typ]:
                raise ValueError("wrong column type")
            elif typ in ("integer","bigint"):
                bits=32 if typ=="integer" else 64
                if not -2**(bits-1)<=value[1]<2**(bits-1):
                    raise ValueError("integer overflow")
            elif typ=="timestamp with time zone" and not -2**63<value[1]<2**63-1:
                raise ValueError("invalid/nonfinite timestamp")
        key_payload=b"".join(fields[names.index(k)][2] for k in pk)
        # Independent length header construction; never call the encoder.
        key=b"k"+len(key_payload).to_bytes(8,"big")+key_payload
        if previous is not None and key<=previous:
            raise ValueError("noncanonical row order/duplicate key")
        previous=key
        decoded.append(values)
    return {"version":version,"position":position,"name":name,"columns":columns,"pk":pk,"rows":decoded}


def aggregate(data, expected_names):
    """Independent aggregate decoder; no encoder calls or inferred table inventory."""
    nodes = frames(data)
    if not nodes or nodes[0][0] != "v":
        raise ValueError("missing aggregate version")
    version = nodes.pop(0)[1].decode("utf-8")
    if version not in ("MPT-SNAPSHOT@1/PERSISTED", "MPT-SNAPSHOT@1/GLOBAL",
                       "MPT-SNAPSHOT@1/POSITION"):
        raise ValueError("unknown aggregate version")
    position = None
    if version.endswith("/POSITION"):
        if not nodes or nodes[0][0] != "p" or not nodes[0][1]:
            raise ValueError("missing position")
        position = nodes.pop(0)[1].decode("utf-8")
    if len(nodes) % 2:
        raise ValueError("incomplete aggregate")
    pairs = {}
    previous = None
    for i in range(0, len(nodes), 2):
        name, digest = nodes[i:i+2]
        if name[0] != "t" or digest[0] != "h" or len(digest[1]) != 32:
            raise ValueError("invalid aggregate member")
        if previous is not None and name[1] <= previous:
            raise ValueError("unordered/duplicate aggregate name")
        previous = name[1]
        pairs[name[1].decode("utf-8")] = digest[1].hex()
    if set(pairs) != set(expected_names):
        raise ValueError("aggregate inventory mismatch")
    return {"version": version, "position": position, "digests": pairs}


def envelope(data):
    nodes = frames(data)
    if [t for t, _, _ in nodes] != ["v", "h", "h", "h", "m", "c", "r"]:
        raise ValueError("invalid envelope fields")
    if nodes[0][1] != b"MPT-SNAPSHOT@1/ENVELOPE":
        raise ValueError("unknown envelope version")
    if any(len(p) != 32 for _, p, _ in nodes[1:6]) or not nodes[6][1]:
        raise ValueError("invalid envelope digest/run identity")
    return {"digests": [p.hex() for _, p, _ in nodes[1:6]],
            "run_id": nodes[6][1].decode("utf-8")}


def metadata(data, expected_schemas):
    # Each normal table stream has exactly five top-level frames.
    nodes = frames(data)
    if len(nodes) != 5 * len(expected_schemas):
        raise ValueError("metadata inventory/width")
    decoded = []
    for i, name in enumerate(sorted(expected_schemas, key=lambda n: n.encode("utf-8"))):
        raw = b"".join(n[2] for n in nodes[i*5:i*5+5])
        value = table(raw)
        expected = expected_schemas[name]
        if (value["version"] != "MPT-SNAPSHOT@1" or value["name"] != name or
            value["columns"] != [(c["name"], c["type"], c["nullable"])
                                 for c in expected["columns"]] or value["pk"] != expected["pk"]):
            raise ValueError("metadata schema/order/version mismatch")
        decoded.append(value)
    return decoded
