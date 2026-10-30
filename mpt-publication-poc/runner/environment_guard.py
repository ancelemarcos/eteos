"""Candidate preflight 0.7. NOT_RUN. This module is authored, never imported in this task."""
import hashlib
import json
import platform
import re
import subprocess
import importlib.metadata
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.7"

FREEZE_KEYS = ("approval_identity", "controller_identity", "controller_permissions_sha256",
               "process_isolation_identity", "process_isolation_evidence_sha256",
               "supervisor_policy_sha256", "collector_authorization_sha256",
               "signature_policy_identity", "clock_evidence_sha256")


def verify_freeze(config):
    # Approved config hash is verified before this function. No self-generated approvals.
    freeze = config.get("freeze")
    require(isinstance(freeze,dict) and set(freeze)==set(FREEZE_KEYS),
            "freeze checklist incomplete")
    for key,value in freeze.items():
        require(isinstance(value,str) and value.strip() not in ("","UNRESOLVED","PENDING"),
                "freeze field unresolved: "+key)
        if key.endswith("_sha256"):
            require(re.fullmatch(r"[0-9a-f]{64}",value) is not None,
                    "invalid approved evidence hash: "+key)
    require(freeze["signature_policy_identity"]=="ED25519-RAW-JSON-V1",
            "unsupported signature policy")
    return freeze


class PreflightBlocked(RuntimeError):
    pass


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise PreflightBlocked(message)


def verify_files(package, config_path, approved_config_sha, config):
    require(sha(config_path) == approved_config_sha, "configuration differs from independently approved hash")
    verify_freeze(config)
    manifest = package / "MANIFEST.md"
    require(sha(manifest) == config["manifest_sha256"], "manifest differs from approved hash")
    text = manifest.read_text(encoding="utf-8")
    inventory = text.split("<!-- ARTIFACTS-BEGIN -->")[1].split("<!-- ARTIFACTS-END -->")[0]
    entries = re.findall(r"^\| ([^|]+?) \| ([0-9a-f]{64}) \|$", inventory, re.M)
    require(bool(entries), "missing artifact inventory")
    expected = {}
    for relative, digest in entries:
        relative = relative.strip()
        target = (package / relative).resolve()
        require(target.is_relative_to(package.resolve()), "manifest path escapes package")
        require(relative not in expected, "duplicate manifest path")
        require(sha(target) == digest, "artifact hash mismatch: " + relative)
        expected[relative] = digest
    actual = {p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file()
              and p.name != "MANIFEST.md" and "__pycache__" not in p.parts}
    require(set(expected) == actual, "unlisted or missing package artifacts")
    head = subprocess.run(["git", "-C", str(package), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    require(head == config["git_head"], "checkout HEAD mismatch")
    require(platform.python_version() == config["python_version"], "Python version mismatch")
    dependencies = sorted((d.metadata["Name"].lower(),d.version) for d in importlib.metadata.distributions())
    dependencies_hash = hashlib.sha256(json.dumps(dependencies,separators=(",",":")).encode()).hexdigest()
    require(dependencies_hash == config["installed_dependencies_sha256"], "installed dependency inventory mismatch")
    require(config["policy_identity"] == "MPT-POC-0.7", "unapproved policy identity")
    return {"head": head, "manifest_sha256": sha(manifest), "configuration_sha256": sha(config_path),
            "artifact_hashes": expected, "runner_version": VERSION, "package": str(package.resolve()),
            "policy_identity":config["policy_identity"],"dependencies":dependencies,
            "installed_dependencies_sha256":dependencies_hash}


def verify_attestation(config):
    # Requires a separately approved collector, signer and dependency freeze.
    # No example attestation/signature is fabricated or shipped.
    import cryptography
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    require(cryptography.__version__ == config["cryptography_version"], "signature verifier version mismatch")
    proof = Path(config["attestation_path"])
    public_key = Path(config["attestation_public_key_path"])
    signature = Path(config["attestation_signature_path"])
    require(sha(proof) == config["attestation_sha256"], "attestation hash mismatch")
    require(sha(public_key) == config["attestation_public_key_sha256"], "unapproved collector key")
    require(sha(signature) == config["attestation_signature_sha256"], "signature hash mismatch")
    Ed25519PublicKey.from_public_bytes(public_key.read_bytes()).verify(signature.read_bytes(), proof.read_bytes())
    data = json.loads(proof.read_text(encoding="utf-8"))
    # Signed capture includes raw image/container inspect outputs and a DB identity binding.
    image, container = data["image_inspect"][0], data["container_inspect"][0]
    require(config["image_digest"] in image["RepoDigests"], "digest absent from signed image inspection")
    require(container["Image"] == image["Id"], "container/image mismatch")
    require(container["Id"] == config["container_id"], "container identity mismatch")
    require(container["State"]["Running"] is True, "attested container was not running")
    require(image["Architecture"] == config["architecture"], "image architecture mismatch")
    require(data["postgres_system_identifier"] == config["postgres_system_identifier"], "cluster binding mismatch")
    require(data["captured_at_utc"] == config["attestation_captured_at_utc"], "unapproved evidence capture")
    require(config["collector_identity"] not in ("UNRESOLVED",""), "collector identity unresolved")
    require(data["collector_identity"] == config["collector_identity"], "collector identity mismatch")
    require(data["policy_identity"] == config["policy_identity"], "collector policy mismatch")
    freeze = verify_freeze(config)
    require(data.get("freeze")==freeze, "signed freeze evidence differs from approval")
    max_age = config["attestation_max_age_seconds"]
    skew = config["attestation_clock_skew_seconds"]
    require(type(max_age) is int and max_age>0, "approved freshness window unresolved")
    require(type(skew) is int and 0<=skew<max_age, "approved clock tolerance unresolved")
    captured = datetime.fromisoformat(data["captured_at_utc"].replace("Z","+00:00"))
    require(captured.tzinfo is not None, "attestation timestamp must be timezone aware")
    verified_at = datetime.now(timezone.utc)
    age = (verified_at-captured).total_seconds()
    require(-skew<=age<=max_age, "external evidence stale or in the future")
    return {"attestation_sha256": sha(proof), "signer_sha256": sha(public_key),
            "signature_verified": True, "image_digest": config["image_digest"],
            "container_id": container["Id"], "captured_at_utc": data["captured_at_utc"],
            "collector_identity":data["collector_identity"],
            "attestation_verified_at_utc":verified_at.isoformat(),"attestation_age_seconds":age,
            "observed_freeze":data["freeze"]}


def verify_server(conn, config, driver_version):
    require(driver_version == config["driver_version"], "driver version mismatch")
    names = ("server_version", "server_version_num", "transaction_isolation",
             "default_transaction_isolation", "fsync", "synchronous_commit",
             "server_encoding", "TimeZone", "max_connections")
    actual = {name: conn.execute("SELECT current_setting(%s)", (name,)).fetchone()[0] for name in names}
    require(actual == config["server_settings"], "observed PostgreSQL settings mismatch")
    require(actual["transaction_isolation"] == "read committed", "READ COMMITTED required")
    system_id = conn.execute("SELECT system_identifier::text FROM pg_control_system()").fetchone()[0]
    require(system_id == config["postgres_system_identifier"], "connected cluster differs from signed evidence")
    extensions = conn.execute("SELECT extname,extversion FROM pg_extension ORDER BY extname").fetchall()
    require([list(row) for row in extensions] == config["extensions"], "extension inventory mismatch")
    return {"server_settings": actual, "postgres_system_identifier": system_id,
            "python_version": platform.python_version(), "driver_version": driver_version,
            "runtime_machine": platform.machine(),"extensions":extensions}


def verify_privileges(conn, config, role):
    # No passwords, connection strings, role config or collector secrets are queried/logged.
    identity = conn.execute("SELECT session_user::text,current_user::text").fetchone()
    require(identity[1] == "mpt_"+role, "wrong effective test role")
    memberships = conn.execute("""SELECT rolname,rolsuper,rolcreaterole,rolcreatedb,rolreplication,rolbypassrls
        FROM pg_roles WHERE rolname=session_user OR pg_has_role(session_user,oid,'MEMBER')
        ORDER BY rolname""").fetchall()
    if role != "owner":
        require(not any(any(row[1:]) for row in memberships), "privileged runtime membership")
        require(not any(row[0].startswith("mpt_") and row[0] not in (identity[0],"mpt_"+role)
                        for row in memberships), "cross-role membership")
    columns = conn.execute("""SELECT c.relname,a.attname,
        has_column_privilege(current_user,c.oid,a.attnum,'INSERT'),
        has_column_privilege(current_user,c.oid,a.attnum,'UPDATE'),
        has_table_privilege(current_user,c.oid,'DELETE'),
        has_table_privilege(current_user,c.oid,'TRUNCATE'),pg_get_userbyid(c.relowner)
        FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
        JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum>0 AND NOT a.attisdropped
        WHERE n.nspname='mpt_poc' AND c.relkind IN ('r','v')
        ORDER BY c.relname,a.attnum""").fetchall()
    functions = conn.execute("""SELECT p.oid::regprocedure::text,
        has_function_privilege(current_user,p.oid,'EXECUTE'),p.prosecdef,p.proconfig,
        pg_get_userbyid(p.proowner) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE n.nspname='mpt_poc' ORDER BY p.oid::regprocedure::text""").fetchall()
    if role == "writer":
        require(not any(row[0] in ("notification","outbox_event") and row[1] in
            ("delivery_status","dispatch_status","lease_token","lease_until_observed")
            and any(row[2:6]) for row in columns), "writer delivery privilege bypass")
    controller = conn.execute("""SELECT
        pg_has_role(current_user,'pg_signal_backend','USAGE'),
        pg_has_role(current_user,'pg_read_all_stats','USAGE'),
        has_function_privilege(current_user,'pg_control_system()','EXECUTE'),
        has_schema_privilege(current_user,'mpt_poc','CREATE'),
        has_database_privilege(current_user,current_database(),'CREATE')""").fetchone()
    observed = {"identity":identity,"memberships":memberships,"columns":columns,"functions":functions,
                "controller_capabilities":controller}
    digest = hashlib.sha256(json.dumps(observed,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    require(digest == config["privilege_inventory_sha256"][role], "effective privilege inventory mismatch")
    return {"effective_privileges":observed,"privilege_inventory_sha256":digest}
