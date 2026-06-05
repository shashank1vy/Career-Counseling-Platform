import os
import json
import logging
import time
import threading

_firebase_lock = threading.Lock()
_firebase_state: dict = {
    "initialized": False,
    "ready": False,
    "client": None,
    "checked_at": 0.0,
    "error": "",
}
_HEALTH_TTL_SECONDS = 60.0


def _load_service_account() -> dict | None:
    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        if not data.get("project_id"):
            return None
        return data
    except Exception:
        logging.exception(
            "Pathwise: failed to parse FIREBASE_SERVICE_ACCOUNT_JSON"
        )
        return None


def _initialize() -> None:
    """Initialize firebase_admin app once. Never raises."""
    if _firebase_state["initialized"]:
        return
    _firebase_state["initialized"] = True
    service_account = _load_service_account()
    if not service_account:
        _firebase_state["ready"] = False
        _firebase_state["error"] = "missing_credentials"
        return
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credentials.Certificate(service_account)
            )
        client = firestore.client()
        # Health check - short write/read
        doc = client.collection("_pathwise_health").document("connectivity")
        doc.set({"status": "ok"}, merge=True)
        snap = doc.get()
        if snap.exists:
            _firebase_state["client"] = client
            _firebase_state["ready"] = True
            _firebase_state["checked_at"] = time.monotonic()
            _firebase_state["error"] = ""
        else:
            _firebase_state["ready"] = False
            _firebase_state["error"] = "health_check_failed"
    except Exception:
        logging.exception("Pathwise: Firebase initialization failed")
        _firebase_state["ready"] = False
        _firebase_state["error"] = "init_failed"


def get_client():
    """Return Firestore client if ready, else None. Never raises."""
    with _firebase_lock:
        if not _firebase_state["initialized"]:
            _initialize()
        if not _firebase_state["ready"]:
            return None
        # Refresh health check periodically
        now = time.monotonic()
        if (
            now - float(_firebase_state.get("checked_at", 0.0))
            > _HEALTH_TTL_SECONDS
        ):
            try:
                client = _firebase_state["client"]
                doc = client.collection("_pathwise_health").document(
                    "connectivity"
                )
                doc.set({"status": "ok"}, merge=True)
                _firebase_state["checked_at"] = now
            except Exception:
                logging.exception("Pathwise: Firebase health refresh failed")
                _firebase_state["ready"] = False
                _firebase_state["client"] = None
                return None
        return _firebase_state["client"]


def is_ready() -> bool:
    return get_client() is not None


def save_user_record(email: str, record: dict) -> bool:
    """Safely persist a sanitized record. Returns True on success."""
    if not email:
        return False
    client = get_client()
    if client is None:
        return False
    try:
        safe = _sanitize(record)
        safe["updated_at"] = time.time()
        client.collection("pathwise_users").document(email.lower().strip()).set(
            safe, merge=True
        )
        return True
    except Exception:
        logging.exception("Pathwise: Firestore write failed")
        return False


def fetch_user_record(email: str) -> dict | None:
    if not email:
        return None
    client = get_client()
    if client is None:
        return None
    try:
        snap = (
            client.collection("pathwise_users")
            .document(email.lower().strip())
            .get()
        )
        if snap.exists:
            data = snap.to_dict() or {}
            return _sanitize(data)
        return None
    except Exception:
        logging.exception("Pathwise: Firestore read failed")
        return None


# Whitelist of safe fields - never include raw file content, credentials, tokens.
_SAFE_FIELDS = {
    "full_name",
    "email",
    "phone",
    "career_stage",
    "current_role",
    "experience_level",
    "education_level",
    "institution",
    "field_of_study",
    "skills",
    "interests",
    "target_roles",
    "challenges",
    "guidance_areas",
    "career_objective",
    "intake_submitted",
    "resume_filename",
    "resume_size",
    "session_type",
    "booking_confirmed",
    "updated_at",
}


def _sanitize(record: dict) -> dict:
    out: dict = {}
    for k, v in record.items():
        if k in _SAFE_FIELDS:
            out[k] = v
    return out