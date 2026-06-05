import reflex as rx
import os
import logging


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


def _detect_backend_ready() -> tuple[bool, str]:
    """Detect (server-side only) whether a secure backend is configured.

    Returns (ready, provider_label). Never returns or exposes the actual
    credential values — only a boolean and a generic provider label that
    is safe to render in the UI.
    """
    try:
        firebase_keys = [
            "FIREBASE_SERVICE_ACCOUNT_JSON",
            "GOOGLE_APPLICATION_CREDENTIALS",
            "FIREBASE_PROJECT_ID",
        ]
        if any(os.getenv(k) for k in firebase_keys):
            return True, "Firebase"
        db_keys = ["DATABASE_URL", "POSTGRES_URL"]
        if any(os.getenv(k) for k in db_keys):
            return True, "Secure database"
        return False, ""
    except Exception as e:
        logging.exception(f"Error detecting backend readiness: {e}")
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