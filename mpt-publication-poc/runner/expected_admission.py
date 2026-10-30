"""Disabled external admission boundary. No keys, authority, filesystem or runtime adapter."""
from dataclasses import dataclass
from hashlib import sha256
from expected_bounds import canonical


class AdmissionBlocked(ValueError):
    pass


@dataclass(frozen=True)
class AdmissionReceipt:
    phase: str
    binding_sha256: str
    raw_sha256: str
    evidence_id: str


class AdmissionAdapter:
    """Future independently approved host must implement BOTH operations.

    authorize must authenticate signature, reviewer role/separation/scope, validity and
    revocation from pinned offline policy; verify budget approval, stable-handle path/
    file identity and actual loaded module/runtime identities against signed inventory.
    Never create this receipt from candidate claims or a bool callback.

    recheck must verify retained file identity/bytes, loaded identity and immutability
    after observation. No concrete approving implementation is included.
    """
    def authorize(self, *, phase, raw, binding, approval, budgets):
        raise AdmissionBlocked("external authority/loader/monitor implementation pending")

    def recheck(self, receipt):
        raise AdmissionBlocked("external immutable-handle recheck pending")


def require_admission(adapter, *, phase, raw, binding, approval, budgets):
    if not isinstance(adapter, AdmissionAdapter):
        raise AdmissionBlocked("disabled: approved external admission adapter required")
    budgets.check()
    bound = sha256(canonical(binding, budgets)).hexdigest()
    receipt = adapter.authorize(phase=phase, raw=raw, binding=binding,
                                approval=approval, budgets=budgets)
    if sha256(canonical(binding, budgets)).hexdigest() != bound:
        raise AdmissionBlocked("binding mutated during admission")
    if type(receipt) is not AdmissionReceipt or (
            receipt.phase != phase or receipt.binding_sha256 != bound or
            receipt.raw_sha256 != sha256(raw).hexdigest() or
            type(receipt.evidence_id) is not str or not receipt.evidence_id or
            receipt.evidence_id == "UNRESOLVED"):
        raise AdmissionBlocked("invalid external admission receipt")
    # Structural receipt checks are NOT signature authentication or loaded-byte proof.
    return receipt
