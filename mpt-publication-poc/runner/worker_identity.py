"""H01-CTRL@1 consistency validators only. NOT_RUN. No OS, I/O, spawn, kill or restart API."""
from dataclasses import dataclass, replace
import re


def nonempty(value):
    return type(value) is str and bool(value) and value.strip()==value


def sha(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}",value) is not None


@dataclass(frozen=True)
class Identity:
    run_id: str
    sandbox_id: str
    supervisor_id: str
    generation: int
    creation_identity: str
    executable_sha256: str
    configuration_sha256: str
    manifest_sha256: str
    ipc_nonce: str


@dataclass(frozen=True)
class Binding:
    identity: Identity
    capability: object  # opaque IN-MEMORY consistency token, never an OS handle or PID


def validate_identity(expected, observed, retained_capability, presented_capability):
    if type(expected) is not Identity or type(observed) is not Identity:
        raise ValueError("typed identities required")
    if any(type(getattr(expected,key)) is not type(getattr(observed,key))
           for key in Identity.__dataclass_fields__):
        raise ValueError("identity field type mismatch")
    if retained_capability is None or presented_capability is not retained_capability:
        raise ValueError("capability identity mismatch")
    for value in (expected.run_id,expected.sandbox_id,expected.supervisor_id,
                  expected.creation_identity,expected.ipc_nonce):
        if not nonempty(value):
            raise ValueError("missing identity")
    if type(expected.generation) is not int or expected.generation<1:
        raise ValueError("invalid generation")
    if not all(sha(v) for v in (expected.executable_sha256,expected.configuration_sha256,
                               expected.manifest_sha256)):
        raise ValueError("invalid artifact identity")
    if expected!=observed:
        raise ValueError("child/run/sandbox identity mismatch")
    return Binding(expected,retained_capability)


def validate_restart(previous, replacement):
    for bound in (previous,replacement):
        if type(bound) is not Binding:
            raise ValueError("typed binding required")
        validate_identity(bound.identity,bound.identity,bound.capability,bound.capability)
    old,new=previous.identity,replacement.identity
    if (old.run_id,old.sandbox_id,old.supervisor_id,old.executable_sha256,
        old.configuration_sha256,old.manifest_sha256)!=(new.run_id,new.sandbox_id,new.supervisor_id,
        new.executable_sha256,new.configuration_sha256,new.manifest_sha256):
        raise ValueError("restart changed run/artifact binding")
    if new.generation!=old.generation+1 or new.creation_identity==old.creation_identity:
        raise ValueError("restart must have fresh creation identity/generation")
    if new.ipc_nonce==old.ipc_nonce or previous.capability is replacement.capability:
        raise ValueError("restart reused nonce/capability")
    return replacement


@dataclass(frozen=True)
class CheckState:
    binding: Binding
    operation_id: str
    next_sequence: int = 1
    phase: str = "IDENTITY_CONFIRMED"


FIELDS=frozenset(("run_id","sandbox_id","supervisor_id","generation","creation_identity",
                  "ipc_nonce","sequence","phase","operation_id","transaction_outcome",
                  "full_rows_sha256"))


def validate_checkpoint(state, message, observed, presented_capability, encoded_size,
                        max_message_bytes, now_tick, deadline_tick):
    """Caller supplies actual measured size/time. This is not authentication or an IPC reader."""
    if type(state) is not CheckState or type(state.binding) is not Binding:
        raise ValueError("typed checkpoint state required")
    if type(state.next_sequence) is not int or state.next_sequence<1 or type(state.phase) is not str:
        raise ValueError("invalid checkpoint state")
    validate_identity(state.binding.identity,observed,state.binding.capability,presented_capability)
    if type(message) is not dict or set(message)!=FIELDS:
        raise ValueError("unknown/missing IPC fields")
    if (type(encoded_size) is not int or type(max_message_bytes) is not int
            or not 0<encoded_size<=max_message_bytes):
        raise ValueError("invalid/oversize IPC frame")
    if any(type(t) is not int for t in (now_tick,deadline_tick)) or not 0<=now_tick<deadline_tick:
        raise ValueError("expired/invalid monotonic deadline")
    identity=state.binding.identity
    for key in ("run_id","sandbox_id","supervisor_id","generation","creation_identity","ipc_nonce"):
        if type(message[key]) is not type(getattr(identity,key)) or message[key]!=getattr(identity,key):
            raise ValueError("IPC identity mismatch")
    if (not nonempty(state.operation_id) or message["operation_id"]!=state.operation_id
            or type(message["sequence"]) is not int or message["sequence"]!=state.next_sequence):
        raise ValueError("IPC operation/sequence mismatch")
    if not sha(message["full_rows_sha256"]):
        raise ValueError("invalid complete-state hash")
    transitions={
        "IDENTITY_CONFIRMED":{"BEFORE_COMMIT":"OPEN","AFTER_COMMIT":"COMMITTED"},
        "BEFORE_COMMIT":{"EXIT_CONFIRMED":"ROLLED_BACK"},
        "AFTER_COMMIT":{"EXIT_CONFIRMED":"COMMITTED"},
        "EXIT_CONFIRMED":{},
    }
    phase=message["phase"]
    allowed=transitions.get(state.phase,{})
    if type(phase) is not str or phase not in allowed or message["transaction_outcome"]!=allowed[phase]:
        raise ValueError("unexpected/unknown transaction checkpoint")
    # EXIT_CONFIRMED must be supplied by independently verified supervisor/DB observer.
    # Pure equality cannot establish that a child died or that rollback actually completed.
    return replace(state,next_sequence=state.next_sequence+1,phase=phase)
