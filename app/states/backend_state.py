import reflex as rx
import os
import logging
import time


# Safe data boundaries — these are the ONLY fields that would ever be
# synchronized to a backend. Sensitive content (raw resume bytes, secrets,
# auth tokens, server URLs) is explicitly excluded.
SAFE_REGISTRATION_FIELDS: list[str] = [
    "full_name",
    "email",
    "phone",
    "career_stage",
]
SAFE_INTAKE_FIELDS: list[str] = [
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
]
SAFE_RESUME_METADATA_FIELDS: list[str] = [
    "resume_filename",
    "resume_size",
]
SAFE_BOOKING_FIELDS: list[str] = [
    "session_type",
    "booking_confirmed",
]


# Cache the backend readiness check so we don't ping MongoDB on every render.
# (cached_result, cached_label, cache_expiry_epoch)
_BACKEND_CACHE: dict[str, float | bool | str] = {
    "ready": False,
    "label": "",
    "expires_at": 0.0,
}
_BACKEND_CACHE_TTL_SECONDS: float = 60.0


def _is_safe_mongo_uri(uri: str) -> bool:
    """Lightweight, non-logging validation of a MongoDB URI shape."""
    if not uri or not isinstance(uri, str):
        return False
    uri_l = uri.strip().lower()
    if not (
        uri_l.startswith("mongodb://") or uri_l.startswith("mongodb+srv://")
    ):
        return False
    # Reject obviously local/unreachable targets so we don't even attempt
    # a network call against a service that is not provisioned in the sandbox.
    local_hosts = ("localhost", "127.0.0.1", "0.0.0.0", "::1")
    for host in local_hosts:
        if f"@{host}" in uri_l or f"//{host}" in uri_l:
            return False
    return True


def _try_mongo_ping() -> bool:
    """Attempt a short, safe PyMongo ping. Returns True only on success.

    Never raises. Never logs the URI or credentials. All failures (missing
    URI, malformed URI, DNS failure, connection refused, auth error,
    timeout, unexpected exception) return False so the UI gracefully
    falls back to local-only storage messaging.
    """
    uri = os.getenv("MONGODB_URI", "")
    if not _is_safe_mongo_uri(uri):
        return False
    try:
        from pymongo import MongoClient
        from pymongo.errors import PyMongoError

        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=1500,
            connectTimeoutMS=1500,
            socketTimeoutMS=1500,
            appname="pathwise-readiness-check",
        )
        try:
            result = client.admin.command("ping")
            return bool(result and result.get("ok") == 1)
        except PyMongoError:
            # Don't log the exception payload because some PyMongo errors
            # echo the connection string. Just record a generic message.
            logging.exception("Unexpected error")
            logging.warning(
                "Pathwise: MongoDB readiness ping failed; "
                "falling back to browser-local storage."
            )
            return False
        finally:
            try:
                client.close()
            except Exception:
                logging.exception("Unexpected error")
    except Exception:
        logging.exception("Unexpected error")
        logging.warning(
            "Pathwise: MongoDB readiness check could not run; "
            "falling back to browser-local storage."
        )
        return False


def _detect_backend_ready() -> tuple[bool, str]:
    """Detect (server-side only) whether a secure backend is configured.

    Returns (ready, provider_label). Never returns or exposes the actual
    credential values — only a boolean and a generic provider label that
    is safe to render in the UI. Results are cached briefly so this is
    cheap to call from computed vars.
    """
    try:
        now = time.monotonic()
        if now < float(_BACKEND_CACHE.get("expires_at", 0.0)):
            return (
                bool(_BACKEND_CACHE.get("ready", False)),
                str(_BACKEND_CACHE.get("label", "")),
            )

        ready = False
        label = ""

        firebase_keys = [
            "FIREBASE_SERVICE_ACCOUNT_JSON",
            "GOOGLE_APPLICATION_CREDENTIALS",
            "FIREBASE_PROJECT_ID",
        ]
        if any(os.getenv(k) for k in firebase_keys):
            ready, label = True, "Firebase"
        elif os.getenv("MONGODB_URI"):
            # Only mark MongoDB ready if a short, safe ping actually succeeds.
            if _try_mongo_ping():
                ready, label = True, "MongoDB"
            else:
                ready, label = False, ""
        elif any(os.getenv(k) for k in ("DATABASE_URL", "POSTGRES_URL")):
            ready, label = True, "Secure database"

        _BACKEND_CACHE["ready"] = ready
        _BACKEND_CACHE["label"] = label
        _BACKEND_CACHE["expires_at"] = now + _BACKEND_CACHE_TTL_SECONDS
        return ready, label
    except Exception:
        logging.exception("Unexpected error")
        logging.warning(
            "Pathwise: backend readiness detection failed; "
            "falling back to browser-local storage."
        )
        return False, ""


class BackendState(rx.State):
    """Exposes only safe, non-sensitive backend status to the frontend."""

    @rx.var
    def backend_ready(self) -> bool:
        ready, _ = _detect_backend_ready()
        return ready

    @rx.var
    def backend_provider(self) -> str:
        _, label = _detect_backend_ready()
        return label

    @rx.var
    def storage_mode_label(self) -> str:
        ready, label = _detect_backend_ready()
        if ready:
            return f"Secure cloud sync • {label}"
        return "Saved on this browser only"

    @rx.var
    def storage_mode_description(self) -> str:
        ready, label = _detect_backend_ready()
        if ready:
            return (
                f"Your registration, intake answers, resume metadata, and booking are securely "
                f"synced to {label}. Sensitive credentials never leave the server."
            )
        return (
            "Cloud sync isn't enabled yet, so your registration, intake answers, resume "
            "metadata, session selection, and booking confirmation are saved privately in "
            "this browser on this device only. Use the same device and browser to return — "
            "details won't transfer elsewhere until secure cloud storage is turned on."
        )

    @rx.var
    def storage_short_label(self) -> str:
        ready, _ = _detect_backend_ready()
        if ready:
            return "Synced securely"
        return "Saved on this device"

    @rx.var
    def storage_inline_notice(self) -> str:
        ready, _ = _detect_backend_ready()
        if ready:
            return "Your details are securely synced to your private account."
        return (
            "Heads up: your details are saved only in this browser on this device. "
            "Use the same browser to come back — they won't sync elsewhere yet."
        )