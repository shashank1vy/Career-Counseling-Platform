import reflex as rx
import json
import logging
from app.states.firebase_client import (
    save_user_record as _firebase_save,
    fetch_user_record as _firebase_fetch,
)

UPLOAD_ID = "resume_upload"


class AppState(rx.State):
    current_step: str = "landing"
    session_type: str = "discovery"
    booking_confirmed: bool = False

    full_name: str = ""
    email: str = ""
    phone: str = ""
    career_stage: str = ""

    name_error: str = ""
    email_error: str = ""
    phone_error: str = ""
    stage_error: str = ""

    registered: bool = False

    # Intake
    current_role: str = ""
    experience_level: str = ""
    education_level: str = ""
    institution: str = ""
    field_of_study: str = ""
    skills: str = ""
    interests: str = ""
    target_roles: str = ""
    challenges: str = ""
    guidance_areas: list[str] = []
    career_objective: str = ""
    intake_submitted: bool = False
    intake_errors: dict[str, str] = {}

    # Resume
    resume_filename: str = ""
    resume_size: int = 0
    resume_error: str = ""

    # Career Paths exploration data
    career_path_filter: str = "all"

    @rx.event
    def set_career_path_filter(self, filter_val: str):
        self.career_path_filter = filter_val

    career_paths: list[dict[str, str]] = [
        {
            "title": "Technology & Engineering",
            "icon": "cpu",
            "color_theme": "blue",
            "desc": "Software engineering, DevOps, cloud architecture, and data engineering pathways.",
            "roles": "Frontend Developer, Backend Engineer, Cloud Architect, Data Engineer",
            "trend_label": "🔥 Hot market",
            "trend_key": "hot",
            "key_skills": "System Design, Kubernetes, Python, React, AWS",
        },
        {
            "title": "Product & Creative Design",
            "icon": "palette",
            "color_theme": "rose",
            "desc": "Product management, user research, UI/UX design, and creative direction.",
            "roles": "Product Manager, UX Designer, UX Researcher, Creative Director",
            "trend_label": "📈 Rising",
            "trend_key": "rising",
            "key_skills": "User Research, Wireframing, Product Strategy, Figma, A/B Testing",
        },
        {
            "title": "Data Science & AI",
            "icon": "brain-circuit",
            "color_theme": "sage",
            "desc": "Artificial intelligence, machine learning, deep data science, and business analytics.",
            "roles": "ML Engineer, Data Scientist, BI Specialist, Analytics Lead",
            "trend_label": "🔥 Hot market",
            "trend_key": "hot",
            "key_skills": "PyTorch, LLMs, SQL, Vector Databases, Spark",
        },
        {
            "title": "Business & Growth Strategy",
            "icon": "trending-up",
            "color_theme": "amber",
            "desc": "Management consulting, operations strategy, business development, and product marketing.",
            "roles": "Management Consultant, Operations Lead, Growth Marketer, Business Analyst",
            "trend_label": "✓ Steady",
            "trend_key": "steady",
            "key_skills": "Financial Modeling, SEO, CRM, Market Research, Agile",
        },
    ]

    @rx.var
    def filtered_career_paths(self) -> list[dict[str, str]]:
        if self.career_path_filter == "all":
            return self.career_paths
        return [
            p
            for p in self.career_paths
            if p.get("trend_key") == self.career_path_filter
        ]

    # Persistence (browser-local; survives reloads using cookies for transient/session state)
    accounts_json: str = rx.Cookie(name="pathwise_accounts")
    current_user_email: str = rx.LocalStorage("", name="pathwise_current_user")

    # Login
    login_email: str = ""
    login_phone: str = ""
    login_email_error: str = ""
    login_phone_error: str = ""
    login_general_error: str = ""

    @rx.var
    def is_logged_in(self) -> bool:
        return self.current_user_email != ""

    @rx.var
    def has_saved_account(self) -> bool:
        try:
            data = json.loads(self.accounts_json or "{}")
            return len(data) > 0
        except Exception:
            logging.exception("Unexpected error")
            return False

    def _load_accounts(self) -> dict:
        try:
            return json.loads(self.accounts_json or "{}")
        except Exception:
            logging.exception("Unexpected error")
            return {}

    def _save_accounts(self, accounts: dict) -> None:
        self.accounts_json = json.dumps(accounts)

    def _current_record(self) -> dict:
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "career_stage": self.career_stage,
            "current_role": self.current_role,
            "experience_level": self.experience_level,
            "education_level": self.education_level,
            "institution": self.institution,
            "field_of_study": self.field_of_study,
            "skills": self.skills,
            "interests": self.interests,
            "target_roles": self.target_roles,
            "challenges": self.challenges,
            "guidance_areas": list(self.guidance_areas),
            "career_objective": self.career_objective,
            "intake_submitted": self.intake_submitted,
            "resume_filename": self.resume_filename,
            "resume_size": self.resume_size,
            "session_type": self.session_type,
            "booking_confirmed": self.booking_confirmed,
        }

    def _persist_current(self, sync_cloud: bool = False) -> None:
        if not self.email:
            return
        accounts = self._load_accounts()
        key = self.email.lower().strip()
        existing = accounts.get(key, {})
        existing.update(self._current_record())
        accounts[key] = existing
        self._save_accounts(accounts)
        self.current_user_email = key
        if sync_cloud:
            try:
                _firebase_save(key, existing)
            except Exception:
                logging.exception(
                    "Pathwise: Firestore sync failed; cookie state preserved."
                )

    def _hydrate_from(self, record: dict) -> None:
        self.full_name = record.get("full_name", "")
        self.email = record.get("email", "")
        self.phone = record.get("phone", "")
        self.career_stage = record.get("career_stage", "")
        self.current_role = record.get("current_role", "")
        self.experience_level = record.get("experience_level", "")
        self.education_level = record.get("education_level", "")
        self.institution = record.get("institution", "")
        self.field_of_study = record.get("field_of_study", "")
        self.skills = record.get("skills", "")
        self.interests = record.get("interests", "")
        self.target_roles = record.get("target_roles", "")
        self.challenges = record.get("challenges", "")
        self.guidance_areas = list(record.get("guidance_areas", []))
        self.career_objective = record.get("career_objective", "")
        self.intake_submitted = record.get("intake_submitted", False)
        self.resume_filename = record.get("resume_filename", "")
        self.resume_size = record.get("resume_size", 0)
        self.session_type = record.get("session_type", "discovery")
        self.booking_confirmed = record.get("booking_confirmed", False)
        self.registered = True

    @rx.var
    def progress_percent(self) -> int:
        steps = {
            "landing": 0,
            "register": 25,
            "intake": 50,
            "review": 75,
            "booking": 90,
            "done": 100,
        }
        return steps.get(self.current_step, 0)

    @rx.var
    def session_label(self) -> str:
        m = {
            "discovery": "Discovery Session (30 min)",
            "deep_dive": "Deep Dive Session (60 min)",
            "mock_interview": "Mock Interview (45 min)",
            "resume_clinic": "Resume Clinic (45 min)",
        }
        return m.get(self.session_type, "Discovery Session (30 min)")

    @rx.var
    def calendly_url(self) -> str:
        import os
        from urllib.parse import (
            urlparse,
            urlunparse,
            parse_qsl,
            urlencode,
        )

        DEFAULT_URL = "https://calendly.com/pathwise-careers/discovery-30min"

        # Resolve the configured base URL, validating it is a trusted
        # calendly.com URL. Fall back safely if anything is off.
        env_url = os.getenv("CALENDLY_DISCOVERY_URL", "").strip()
        base_url = DEFAULT_URL
        if env_url:
            try:
                parsed_env = urlparse(env_url)
                if (
                    parsed_env.scheme in {"http", "https"}
                    and parsed_env.netloc
                    and parsed_env.netloc.lower().endswith("calendly.com")
                ):
                    base_url = env_url
            except Exception:
                logging.exception(
                    "Pathwise: failed to parse CALENDLY_DISCOVERY_URL; "
                    "using default Calendly URL."
                )
                base_url = DEFAULT_URL

        # Resolve the campaign tag from current state at runtime.
        stage_value = (self.career_stage or "").strip()
        utm_campaign = stage_value if stage_value else "general"

        embed_params: dict[str, str] = {
            "embed_type": "Inline",
            "embed_domain": "pathwise.app",
            "hide_gdpr_banner": "1",
            "utm_source": "pathwise_app",
            "utm_medium": "booking_flow",
            "utm_campaign": utm_campaign,
        }

        try:
            parsed = urlparse(base_url)
            # Re-validate after the env parse in case base_url was tampered.
            if not (
                parsed.scheme in {"http", "https"}
                and parsed.netloc
                and parsed.netloc.lower().endswith("calendly.com")
            ):
                parsed = urlparse(DEFAULT_URL)

            existing_params = dict(
                parse_qsl(parsed.query, keep_blank_values=False)
            )
            # Our embed/UTM values always take precedence so they reflect
            # the live career stage and embedding configuration.
            existing_params.update(embed_params)
            new_query = urlencode(existing_params, doseq=False)
            return urlunparse(
                (
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment,
                )
            )
        except Exception:
            logging.exception(
                "Pathwise: failed to assemble Calendly URL; using safe fallback."
            )
            fallback_query = urlencode(embed_params, doseq=False)
            return f"{DEFAULT_URL}?{fallback_query}"

    @rx.var
    def first_name(self) -> str:
        parts = self.full_name.strip().split(" ")
        return parts[0] if parts and parts[0] else "there"

    @rx.var
    def stage_label(self) -> str:
        m = {
            "fresher": "Fresher / Student",
            "early_career": "Early-career professional (1–5 yrs)",
            "switcher": "Mid-career switcher",
            "senior": "Senior professional",
        }
        return m.get(self.career_stage, "Not specified")

    @rx.var
    def skills_list(self) -> list[str]:
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    @rx.var
    def interests_list(self) -> list[str]:
        return [s.strip() for s in self.interests.split(",") if s.strip()]

    @rx.var
    def target_roles_list(self) -> list[str]:
        return [s.strip() for s in self.target_roles.split(",") if s.strip()]

    @rx.var
    def resume_size_label(self) -> str:
        if self.resume_size <= 0:
            return ""
        kb = self.resume_size / 1024
        if kb < 1024:
            return f"{kb:.1f} KB"
        return f"{kb / 1024:.2f} MB"

    @rx.event
    def go_to_register(self, stage: str = ""):
        if stage:
            self.career_stage = stage
        self.current_step = "register"

    @rx.event
    def go_to_login(self):
        self.login_email_error = ""
        self.login_phone_error = ""
        self.login_general_error = ""
        self.current_step = "login"

    @rx.event
    def go_to_landing(self):
        self.current_step = "landing"

    @rx.event
    def go_to_intake(self):
        self.current_step = "intake"

    @rx.event
    def go_to_review(self):
        self.current_step = "review"

    @rx.event
    def go_to_booking(self):
        self.current_step = "booking"

    @rx.event
    def set_stage(self, v: str):
        self.career_stage = v
        self.stage_error = ""

    @rx.event
    def submit_registration(self, form_data: dict):
        name = form_data.get("full_name", "").strip()
        email = form_data.get("email", "").strip()
        phone = form_data.get("phone", "").strip()
        stage = form_data.get("career_stage", "").strip()

        valid = True
        if len(name) < 2:
            self.name_error = "Please enter your full name (min 2 characters)."
            valid = False
        else:
            self.name_error = ""

        if "@" not in email or "." not in email or len(email) < 5:
            self.email_error = "Please enter a valid email address."
            valid = False
        else:
            self.email_error = ""

        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) < 7:
            self.phone_error = "Please enter a valid phone number."
            valid = False
        else:
            self.phone_error = ""

        if not stage or stage == "default":
            self.stage_error = "Please select your career stage."
            valid = False
        else:
            self.stage_error = ""

        if not valid:
            return

        self.full_name = name
        self.email = email
        self.phone = phone
        self.career_stage = stage
        self.registered = True
        # Hydrate from existing saved account (cookies first, then Firebase)
        accounts = self._load_accounts()
        existing = accounts.get(email.lower())
        cloud_record = None
        try:
            cloud_record = _firebase_fetch(email.lower())
        except Exception:
            logging.exception(
                "Pathwise: Firestore fetch failed during registration."
            )
        merged = {}
        if cloud_record:
            merged.update(cloud_record)
        if existing:
            merged.update(existing)
        if merged:
            merged.update(
                {
                    "full_name": name,
                    "email": email,
                    "phone": phone,
                    "career_stage": stage,
                }
            )
            self._hydrate_from(merged)
        self._persist_current(sync_cloud=True)
        self.current_step = "intake"
        return rx.toast.success(
            f"Welcome, {name.split()[0]}! Saved to this browser on this device."
        )

    @rx.event
    def submit_login(self, form_data: dict):
        email = form_data.get("login_email", "").strip().lower()
        phone = form_data.get("login_phone", "").strip()

        self.login_email_error = ""
        self.login_phone_error = ""
        self.login_general_error = ""

        if not email or "." not in email or len(email) < 5:
            self.login_email_error = "Enter the email you registered with."
            return

        accounts = self._load_accounts()
        record = accounts.get(email)
        if not record:
            try:
                cloud_record = _firebase_fetch(email)
            except Exception:
                logging.exception(
                    "Pathwise: Firestore fetch failed during login."
                )
                cloud_record = None
            if cloud_record:
                record = cloud_record
                accounts[email] = record
                self._save_accounts(accounts)
            else:
                self.login_general_error = (
                    "No account found for that email. Try signing up instead."
                )
                return

        # Optional phone match — if provided, must match saved phone
        if phone:
            saved_digits = "".join(
                c for c in record.get("phone", "") if c.isdigit()
            )
            entered_digits = "".join(c for c in phone if c.isdigit())
            if (
                saved_digits
                and entered_digits
                and saved_digits[-7:] != entered_digits[-7:]
            ):
                self.login_phone_error = (
                    "Phone number doesn't match our records."
                )
                return

        self._hydrate_from(record)
        self.current_user_email = email
        # Resume where the user left off
        if self.booking_confirmed:
            self.current_step = "done"
        elif self.intake_submitted:
            self.current_step = "review"
        elif self.registered:
            self.current_step = "intake"
        else:
            self.current_step = "register"
        return rx.toast.success(
            f"Welcome back, {AppState.first_name}! Picking up where you left off."
        )

    @rx.event
    def logout(self):
        self.current_user_email = ""
        self.full_name = ""
        self.email = ""
        self.phone = ""
        self.career_stage = ""
        self.current_role = ""
        self.experience_level = ""
        self.education_level = ""
        self.institution = ""
        self.field_of_study = ""
        self.skills = ""
        self.interests = ""
        self.target_roles = ""
        self.challenges = ""
        self.guidance_areas = []
        self.career_objective = ""
        self.intake_submitted = False
        self.resume_filename = ""
        self.resume_size = 0
        self.session_type = "discovery"
        self.booking_confirmed = False
        self.registered = False
        self.current_step = "landing"
        return rx.toast.info(
            "Signed out — your saved details remain on this device."
        )

    @rx.event
    def toggle_guidance(self, area: str):
        if area in self.guidance_areas:
            self.guidance_areas = [a for a in self.guidance_areas if a != area]
        else:
            self.guidance_areas = [*self.guidance_areas, area]

    @rx.event
    async def handle_resume_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        try:
            data = await file.read()
            allowed = (".pdf", ".doc", ".docx")
            lower = file.name.lower()
            if not lower.endswith(allowed):
                self.resume_error = "Only PDF, DOC, or DOCX files are accepted."
                return
            if len(data) > 5 * 1024 * 1024:
                self.resume_error = (
                    "File too large — please keep it under 5 MB."
                )
                return
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            path = upload_dir / file.name
            with path.open("wb") as f:
                f.write(data)
            self.resume_filename = file.name
            self.resume_size = len(data)
            self.resume_error = ""
            self._persist_current(sync_cloud=True)
            return rx.toast.success(
                f"Resume uploaded & saved locally: {file.name}"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error: {e}")
            self.resume_error = "Something went wrong uploading your resume."

    @rx.event
    def clear_resume(self):
        self.resume_filename = ""
        self.resume_size = 0
        self.resume_error = ""
        return rx.clear_selected_files(UPLOAD_ID)

    @rx.event
    def submit_intake(self, form_data: dict):
        errors: dict[str, str] = {}

        current_role = form_data.get("current_role", "").strip()
        experience = form_data.get("experience_level", "").strip()
        education = form_data.get("education_level", "").strip()
        institution = form_data.get("institution", "").strip()
        field = form_data.get("field_of_study", "").strip()
        skills = form_data.get("skills", "").strip()
        interests = form_data.get("interests", "").strip()
        targets = form_data.get("target_roles", "").strip()
        challenges = form_data.get("challenges", "").strip()
        objective = form_data.get("career_objective", "").strip()

        if not experience or experience == "default":
            errors["experience_level"] = "Please select your experience level."
        if not education or education == "default":
            errors["education_level"] = "Please select your education level."
        if len(skills) < 2:
            errors["skills"] = "Add at least one skill."
        if len(targets) < 2:
            errors["target_roles"] = "Tell us at least one target role."
        if len(objective) < 10:
            errors["career_objective"] = (
                "Please write a short objective (min 10 chars)."
            )
        if not self.guidance_areas:
            errors["guidance_areas"] = (
                "Pick at least one area where you'd like guidance."
            )

        self.intake_errors = errors
        if errors:
            return rx.toast.error("Please fix the highlighted fields.")

        self.current_role = current_role
        self.experience_level = experience
        self.education_level = education
        self.institution = institution
        self.field_of_study = field
        self.skills = skills
        self.interests = interests
        self.target_roles = targets
        self.challenges = challenges
        self.career_objective = objective
        self.intake_submitted = True
        self._persist_current(sync_cloud=True)
        self.current_step = "review"
        return rx.toast.success("Intake saved — review your details next.")

    @rx.event
    def reset_intake(self):
        self.current_role = ""
        self.experience_level = ""
        self.education_level = ""
        self.institution = ""
        self.field_of_study = ""
        self.skills = ""
        self.interests = ""
        self.target_roles = ""
        self.challenges = ""
        self.guidance_areas = []
        self.career_objective = ""
        self.intake_submitted = False
        self.intake_errors = {}
        self.resume_filename = ""
        self.resume_size = 0
        self.resume_error = ""
        return rx.toast.info("Intake cleared.")

    @rx.event
    def edit_intake(self):
        self.current_step = "intake"

    @rx.event
    def confirm_and_book(self):
        self.current_step = "booking"
        self._persist_current(sync_cloud=True)
        return rx.toast.success("Great! Let's get your session booked.")

    @rx.event
    def select_session_type(self, value: str):
        self.session_type = value
        self._persist_current(sync_cloud=True)

    @rx.event
    def confirm_booking(self):
        self.booking_confirmed = True
        self.current_step = "done"
        self._persist_current(sync_cloud=True)
        return rx.toast.success("Booked! Confirmation saved securely.")

    @rx.event
    def restart_journey(self):
        self.booking_confirmed = False
        self.current_step = "landing"
        return rx.toast.info("Welcome back!")