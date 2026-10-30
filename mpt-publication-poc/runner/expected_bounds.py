"""Proposed bounded parsing/serialization. NOT_RUN; no OS containment claim."""
import json
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Budgets:
    # Proposed ceilings; constructing these does not authorize any execution.
    input_bytes: int = 8388608
    source_bytes: int = 1048576
    output_bytes: int = 8388608
    wire_bytes: int = 1048576
    scalar_bytes: int = 4096
    depth: int = 32
    nodes: int = 100000
    records: int = 856
    diagnostics: int = 4096
    text_chars: int = 2097152
    decimal_digits: int = 128
    decimal_exponent: int = 128

    def check(self):
        for name, ceiling in Budgets().__dict__.items():
            value = getattr(self, name)
            if type(value) is not int or not 0 < value <= ceiling:
                raise ValueError("unapproved or invalid budget")


def guard(value, limits, depth=0, counter=None):
    if counter is None:
        limits.check()
        counter = [0, 0]
    counter[0] += 1
    if depth > limits.depth or counter[0] > limits.nodes:
        raise ValueError("structure budget")
    if type(value) is str:
        counter[1] += len(value) * 4
        if len(value) > limits.text_chars:
            raise ValueError("text budget")
    elif type(value) is bytes:
        counter[1] += len(value)
        if len(value) > limits.wire_bytes:
            raise ValueError("bytes budget")
    elif type(value) is Decimal:
        if not value.is_finite():
            raise ValueError("finite decimal required")
        digits = value.as_tuple()
        if len(digits.digits) > limits.decimal_digits or abs(digits.exponent) > limits.decimal_exponent:
            raise ValueError("decimal budget")
    elif type(value) in (list, tuple, dict):
        if len(value) > limits.nodes:
            raise ValueError("container budget")
        items = value.items() if type(value) is dict else ((None, v) for v in value)
        for key, child in items:
            if key is not None:
                if type(key) is not str:
                    raise ValueError("string key required")
                guard(key, limits, depth + 1, counter)
            guard(child, limits, depth + 1, counter)
    elif value is not None and type(value) not in (bool, int):
        raise ValueError("unsupported bounded value")
    elif type(value) is int and value.bit_length() > 256:
        raise ValueError("integer budget")
    if counter[1] > limits.input_bytes:
        raise ValueError("total input budget")


def _unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out


def parse(raw, limits):
    limits.check()
    if type(raw) is not bytes or len(raw) > limits.input_bytes:
        raise ValueError("input budget")
    # Scan ASCII structural characters before json.loads allocations. JSON grammar
    # and UTF8 validation remain json.loads responsibilities.
    depth = nodes = token = 0
    quoted = escaped = False
    for byte in raw:
        if quoted:
            token += 1
            if token > limits.text_chars * 6:
                raise ValueError("JSON string budget")
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted, token = True, 0
            nodes += 1
        elif byte in (91, 123):
            depth += 1
            nodes += 1
        elif byte in (93, 125):
            depth -= 1
            if depth < 0:
                raise ValueError("JSON bracket balance")
        elif byte in (44, 58):
            nodes += 1
        if depth > limits.depth or nodes > limits.nodes:
            raise ValueError("JSON structure budget")

    def integer(text):
        if len(text) > 78:
            raise ValueError("JSON integer budget")
        return int(text)

    def forbidden(_):
        raise ValueError("JSON float/nonfinite forbidden")

    value = json.loads(raw, object_pairs_hook=_unique, parse_int=integer,
                       parse_float=forbidden, parse_constant=forbidden)
    guard(value, limits)
    return value


def canonical(value, limits):
    guard(value, limits)
    # Preflight a conservative escaped-size bound before encoder allocations.
    def estimate(v):
        if type(v) is str:
            return 2 + sum(12 if ord(c) > 65535 else 6 if ord(c) > 127 or ord(c) < 32
                           else 2 if c in ('"', '\\') else 1 for c in v)
        if type(v) is list:
            return 2 + sum(1 + estimate(x) for x in v)
        if type(v) is dict:
            return 2 + sum(2 + estimate(k) + estimate(x) for k, x in v.items())
        if v is None or type(v) is bool:
            return 5
        if type(v) is int:
            return 80
        raise ValueError("unsupported canonical value")
    if estimate(value) > limits.output_bytes:
        raise ValueError("output preflight budget")
    out = bytearray()
    encoder = json.JSONEncoder(sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
    for chunk in encoder.iterencode(value):
        if len(out) + len(chunk) > limits.output_bytes:
            raise ValueError("output budget")
        out.extend(chunk.encode("ascii"))
    return bytes(out)
