"""Phase 1: Analytics data capture foundation.

Provides a safe, Firebase-backed analytics event persistence layer.

Safety guarantees:
- Never raises into the user experience; all errors are logged and swallowed.
- Silently falls back to a no-op when Firebase is unavailable.
- Strict allow-list sanitization of metadata; sensitive data is dropped.
- Never persists credentials, secrets, tokens, raw uploaded file contents,
  service account JSON, cookies, or browser internals.
"""

import logging
import time
import uuid
from datetime import datetime, timezone

from app.states.firebase_client import get_client


# Strict allow-list of metadata keys that are safe to persist alongside
# analytics events. Any key not in this set is silently dropped.
_SAFE_METADATA_KEYS: set[str] = {
    "career_stage",
    "stage",
    "session_type",
    "guidance_area",
    "guidance_count",
    "career_path_filter",
    "from_step",
    "to_step",
    "duration_ms",
    "duration_seconds",
    "page",
    "step",
    "intake_submitted",
    "booking_confirmed",
    "registered",
    "is_logged_in",
    "has_resume",
    "resume_size_bucket",
    "education_level",
    "experience_level",
    "target_role_count",
    "skill_count",
    "interest_count",
    "filter_value",
    "button_id",
    "cta_id",
    "form_id",
    "field_id",
    "validation_failed_fields",
    "error_code",
    "outcome",
    "source",
    "referrer_kind",
    "device_kind",
}

# Keys that are always blocked, even if present in the safe list elsewhere.
# These are the obvious sensitive surfaces we never want to log.
_BLOCKED_KEYS: set[str] = {
    "password",
    "token",
    "auth",
    "auth_token",
    "secret",
    "api_key",
    "service_account",
    "cookie",
    "cookies",
    "session",
    "credential",
    "credentials",
    "raw",
    "file",
    "file_bytes",
    "file_data",
    "resume_bytes",
    "resume_data",
    "resume_content",
    "user_agent",
    "ip",
    "ip_address",
    "fingerprint",
    "device_id",
    "phone",
    "email",
    "full_name",
    "name",
}

_MAX_STRING_LEN = 200
_MAX_LIST_LEN = 25
_MAX_METADATA_KEYS = 20


def _sanitize_value(value):
    """Sanitize a single value: clamp strings/lists, allow primitives only."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        # Guard against absurdly large numbers (which usually indicate bugs).
        try:
            if abs(value) > 1e15:
                return None
            return value
        except Exception:
            logging.exception("Unexpected error")
            return None
    if isinstance(value, str):
        v = value.strip()
        if len(v) > _MAX_STRING_LEN:
            v = v[:_MAX_STRING_LEN]
        return v
    if isinstance(value, (list, tuple)):
        out = []
        for item in list(value)[:_MAX_LIST_LEN]:
            sv = _sanitize_value(item)
            if sv is not None:
                out.append(sv)
        return out
    # Drop dicts, bytes, and any other complex/unknown types.
    return None


def _sanitize_metadata(metadata: dict | None) -> dict:
    """Apply allow-list + block-list + value sanitization."""
    if not metadata or not isinstance(metadata, dict):
        return {}
    out: dict = {}
    for k, v in metadata.items():
        if not isinstance(k, str):
            continue
        key = k.strip().lower()
        if not key or len(key) > 64:
            continue
        if key in _BLOCKED_KEYS:
            continue
        if key not in _SAFE_METADATA_KEYS:
            continue
        sv = _sanitize_value(v)
        if sv is None:
            continue
        out[key] = sv
        if len(out) >= _MAX_METADATA_KEYS:
            break
    return out


def _coerce_str(value, max_len: int = _MAX_STRING_LEN) -> str:
    if not isinstance(value, str):
        return ""
    v = value.strip()
    if len(v) > max_len:
        v = v[:max_len]
    return v


def _hash_email(email: str) -> str:
    """Stable, non-reversible identifier for grouping events by account
    without storing the raw email address as the primary key."""
    if not email:
        return ""
    try:
        import hashlib

        return hashlib.sha256(
            email.lower().strip().encode("utf-8")
        ).hexdigest()[:32]
    except Exception:
        logging.exception("Pathwise analytics: email hashing failed")
        return ""


def new_session_id() -> str:
    """Generate a fresh anonymous session identifier."""
    try:
        return uuid.uuid4().hex
    except Exception:
        logging.exception("Pathwise analytics: failed to generate session id")
        # Time-based fallback so we never return an empty session id.
        return f"sess-{int(time.time() * 1000)}"


def log_event(
    event_name: str,
    *,
    session_id: str = "",
    user_email: str = "",
    journey_step: str = "",
    metadata: dict | None = None,
) -> bool:
    """Persist a single analytics event to Firebase. Never raises.

    Returns True if successfully written, False otherwise (including when
    Firebase is unavailable).
    """
    try:
        name = _coerce_str(event_name, max_len=80)
        if not name:
            return False

        client = get_client()
        if client is None:
            return False

        sid = _coerce_str(session_id, max_len=64)
        step = _coerce_str(journey_step, max_len=40)
        email_lc = _coerce_str(user_email, max_len=200).lower()
        user_hash = _hash_email(email_lc) if email_lc else ""

        now = datetime.now(timezone.utc)
        payload: dict = {
            "event": name,
            "session_id": sid,
            "user_hash": user_hash,
            "journey_step": step,
            "timestamp_utc": now.isoformat(),
            "timestamp_epoch_ms": int(now.timestamp() * 1000),
            "metadata": _sanitize_metadata(metadata),
        }
        # Keep raw email only if present so per-user reporting is possible;
        # this matches what the existing form-sync layer already persists.
        if email_lc:
            payload["user_email"] = email_lc

        try:
            client.collection("pathwise_analytics_events").add(payload)
            return True
        except Exception:
            logging.exception(
                "Pathwise analytics: Firestore write failed for event '%s'",
                name,
            )
            return False
    except Exception:
        # Belt-and-braces: absolutely never raise from this function.
        logging.exception("Pathwise analytics: unexpected error in log_event")
        return False