"""Future isolated connected harness. MATERIALIZED_NOT_RUN; no driver import/connect/main.
prepare() creates a plan only. dispatch() is blocked by the concrete candidate admission.
Credentials/connections remain external. No destructive setup/teardown or process actions.
"""
import hashlib
import json
import re
from dataclasses import dataclass
from snapshot_transport_candidate import PsycopgIncrementalCandidate, TransportBlocked


class HarnessBlocked(ValueError):
    pass


@dataclass(frozen=True)
class CasePlan:
    case_id: str
    manifest_sha256: str
    environment_sha256: str
    scenario_sha256: str
    configuration_sha256: str
    checkpoints: tuple
    expected: str


def prepare(config_bytes, *, independently_approved_sha256, manifest_bytes,
            environment_bytes, scenarios_bytes, case_id):
    digest = lambda b: hashlib.sha256(b).hexdigest()
    if digest(config_bytes) != independently_approved_sha256:
        raise HarnessBlocked("configuration identity mismatch")
    cfg = json.loads(config_bytes)
    for flag in ("execution_authorized", "isolated_environment_approved", "credentials_external",
                 "fixture_authorized", "cleanup_plan_approved", "independent_oracle_reviewed"):
        if cfg.get(flag) is not True:
            raise HarnessBlocked("missing approval: " + flag)
    for name, value in (("manifest_sha256", manifest_bytes), ("environment_sha256", environment_bytes),
                        ("scenarios_sha256", scenarios_bytes)):
        if cfg.get(name) != digest(value):
            raise HarnessBlocked("unapproved " + name)
    for name in ("driver_build", "libpq_build", "postgres_build", "environment_identity",
                 "fixture_identity", "reviewer_identity"):
        if type(cfg.get(name)) is not str or cfg[name] in ("", "UNRESOLVED"):
            raise HarnessBlocked("unresolved " + name)
    if cfg.get("reader_role") != "mpt_snapshot_reader":
        raise HarnessBlocked("dedicated reader required")
    if any(k in cfg for k in ("dsn", "host", "password", "credentials", "token")):
        raise HarnessBlocked("credentials/endpoints forbidden in candidate configuration")
    for name in ("transport_sha256", "isolation_evidence_sha256", "oracle_sha256"):
        if type(cfg.get(name)) is not str or re.fullmatch("[0-9a-f]{64}", cfg[name]) is None:
            raise HarnessBlocked("unresolved " + name)
    catalog = json.loads(scenarios_bytes)
    if catalog.get("contract") != "MPT-CONNECTED-CANDIDATE@1":
        raise HarnessBlocked("unknown scenario contract")
    matches = [c for c in catalog["cases"] if c["id"] == case_id]
    if len(matches) != 1:
        raise HarnessBlocked("unknown/duplicate scenario")
    return CasePlan(case_id, digest(manifest_bytes), digest(environment_bytes),
                    digest(scenarios_bytes), digest(config_bytes),
                    ("C0 approved fixture ready", "C1 observer MVCC established",
                     "C2 controlled concurrent action/fault", "C3 complete observation or rejection",
                     "C4 rollback/close/evidence"), matches[0]["oracle"])


def dispatch(plan, external_session_provider=None):
    # Call the concrete class method; an injected provider cannot self-certify admission.
    PsycopgIncrementalCandidate.admission(None)
    raise HarnessBlocked("connected scheduling requires separately reviewed implementation")


def evidence_template(plan):
    return {"case_id": plan.case_id, "manifest_sha256": plan.manifest_sha256,
            "environment_sha256": plan.environment_sha256,
            "scenarios_sha256": plan.scenario_sha256,
            "configuration_sha256": plan.configuration_sha256,
            "status": "MATERIALIZED_NOT_RUN", "observations": [],
            "required": ["checkpoint sequence and transaction/snapshot identities",
                         "independent before/after rows and all layer digests",
                         "actual exception class/SQLSTATE, primary and cleanup errors",
                         "role/ACL/schema/view observations",
                         "native memory/buffer high-water and monotonic deadline evidence",
                         "connection termination or quarantine evidence"],
            "result": "UNRESOLVED"}
