"""Non-operational worker controller interface, candidate 0.7.
No OS process primitives, database connections or executable entry point.
Every lifecycle method rejects unconditionally, including with approved-looking inputs.
"""
from dataclasses import dataclass
from typing import Literal


BLOCKED_SCENARIOS = {
    "PROCESS-WORKER-BEFORE-COMMIT": "isolated child supervisor/IPC not implemented or approved",
    "PROCESS-WORKER-AFTER-COMMIT": "isolated child supervisor/IPC not implemented or approved",
    "COMPOUND-MEMBER-SEAM": "member checkpoint decision pending; no approved SQL injection seam",
}


class ControllerUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class ChildEvidence:
    # Future output of spawn only; never an accepted target selector.
    pid: int
    creation_identity: str
    handle_evidence_id: str  # opaque audit ID; never an address or reusable OS handle
    supervisor_instance: str
    executable_sha256: str
    configuration_sha256: str
    isolation_evidence_sha256: str


@dataclass(frozen=True)
class Checkpoint:
    phase: Literal["BEFORE_COMMIT", "AFTER_COMMIT", "EXIT_CONFIRMED", "RESTART_CONFIRMED"]
    supervisor_instance: str
    child_creation_identity: str
    operation_id: str
    ipc_nonce: str
    sequence: int
    transaction_outcome: Literal["OPEN", "COMMITTED", "ROLLED_BACK", "UNKNOWN"]
    full_rows_sha256: str  # future canonical snapshot encoder must be independently frozen


class IsolatedWorkerController:
    """Interface only. No method accepts a PID, executable, shell command or target handle."""

    def start_authorized_child(self):
        raise ControllerUnavailable("BLOCKING_EXECUTION_REVIEW: supervisor implementation absent")

    def await_checkpoint(self):
        raise ControllerUnavailable("BLOCKING_EXECUTION_REVIEW: authenticated IPC absent")

    def terminate_owned_child(self):
        raise ControllerUnavailable("BLOCKING_EXECUTION_REVIEW: owned-child capability absent")

    def confirm_exit(self):
        raise ControllerUnavailable("BLOCKING_EXECUTION_REVIEW: OS exit observer absent")

    def restart_owned_child(self):
        raise ControllerUnavailable("BLOCKING_EXECUTION_REVIEW: isolated restart absent")
