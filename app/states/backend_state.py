import reflex as rx
import logging
from app.states.firebase_client import is_ready as _firebase_is_ready


# Safe data boundaries — these are the ONLY fields that are ever
# synchronized to Firestore. Sensitive content (raw resume bytes, secrets,
# auth tokens, service account JSON) is explicitly excluded.
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
    """Detect (server-side only) whether Firebase Firestore is configured
    and reachable. Never exposes credential values — only a boolean and
    a generic provider label that's safe to render in the UI.
    """
    try:
        if _firebase_is_ready():
            return True, "Firebase Firestore"
        return False, ""
    except Exception:
        logging.exception(
            "Pathwise: Firebase readiness detection failed; "
            "falling back to cookie-only storage."
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
        return "Cookie-only draft mode"

    @rx.var
    def storage_mode_description(self) -> str:
        ready, label = _detect_backend_ready()
        if ready:
            return (
                f"Your completed registration, intake answers, resume metadata, and "
                f"booking confirmation are securely persisted to {label}. Drafts and "
                f"in-progress journey data stay in your browser cookies until you "
                f"complete each step. Raw resume contents and credentials never leave "
                f"the server."
            )
        return (
            "Firebase cloud sync isn't available right now, so your registration, "
            "intake answers, resume metadata, session selection, and booking "
            "confirmation are stored only in this browser's cookies on this device. "
            "Return in the same browser to pick up where you left off — your data "
            "won't transfer elsewhere until cloud sync is restored."
        )

    @rx.var
    def storage_short_label(self) -> str:
        ready, _ = _detect_backend_ready()
        if ready:
            return "Synced to Firebase"
        return "Cookie-only draft"

    @rx.var
    def storage_inline_notice(self) -> str:
        ready, _ = _detect_backend_ready()
        if ready:
            return (
                "Completed steps are securely synced to Firebase Firestore; "
                "drafts stay in this browser's cookies."
            )
        return (
            "Heads up: Firebase sync is unavailable, so your details are saved "
            "only in this browser's cookies on this device. Use the same "
            "browser to come back — they won't sync elsewhere until cloud "
            "storage is reconnected."
        )