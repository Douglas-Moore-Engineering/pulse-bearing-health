"""Offline integrity checks; authentic cloud approval/enforcement remains external."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def verify_bundle(root, manifest_bytes, approval, *, now=None):
    """Check a reference bundle against a separately supplied trusted approval.

    The caller owns approval authentication. This helper never deploys or grants
    site authority. A locally edited JSON approval is not authentic cloud consent.
    """
    now = now or datetime.now(timezone.utc)
    manifest = json.loads(manifest_bytes)
    if manifest.get("scope") != "offline-reference":
        raise ValueError("Only offline-reference bundles are supported")
    if not isinstance(approval, dict) or approval.get("revoked") is not False:
        raise ValueError("Missing or revoked approval")
    if approval.get("manifest_sha256") != hashlib.sha256(manifest_bytes).hexdigest():
        raise ValueError("Approval does not bind manifest bytes")
    if approval.get("target") != manifest.get("target") or manifest.get("target") != "local":
        raise ValueError("Target mismatch")
    if not approval.get("actor") or approval.get("scope") != "offline-reference":
        raise ValueError("Approval actor/scope missing")
    try:
        issued = datetime.fromisoformat(approval["issued_at"])
        expires = datetime.fromisoformat(approval["expires_at"])
        if issued.tzinfo is None or expires.tzinfo is None or not issued <= now < expires:
            raise ValueError("Approval not currently valid")
    except (KeyError, TypeError) as exc:
        raise ValueError("Approval timestamps missing") from exc
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("Empty artifact manifest")
    root = Path(root).resolve()
    for name, expected in artifacts.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or path == root or not path.is_file():
            raise ValueError("Artifact outside bundle or missing")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Artifact digest mismatch")
    return manifest
