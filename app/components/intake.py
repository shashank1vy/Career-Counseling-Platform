import reflex as rx
from app.states.app_state import AppState, UPLOAD_ID
from app.components.storage_status import storage_inline_notice


INPUT_CLS = (
    "w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl "
    "hover:border-indigo-300 focus:ring-2 focus:ring-indigo-900/15 "
    "focus:border-indigo-700 outline-none transition-all duration-200 "
    "text-slate-900 placeholder-slate-400 text-sm shadow-sm"
)

GUIDANCE_OPTIONS = [
    ("Resume review", "file-text"),
    ("Interview prep", "messages-square"),
    ("Career switch", "shuffle"),
    ("Skill roadmap", "map"),
    ("Salary negotiation", "badge-dollar-sign"),
    ("LinkedIn profile", "linkedin"),
    ("Job search strategy", "search"),
    ("Networking", "users"),
]


def section_header(
    icon: str, title: str, subtitle: str, step: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-5 w-5 text-indigo-900"),
                class_name="h-10 w-10 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.h3(
                    title,
                    class_name="text-base font-semibold text-slate-900 tracking-tight",
                ),
                rx.el.p(subtitle, class_name="text-xs text-slate-500 mt-0.5"),
                class_name="ml-3",
            ),
            class_name="flex items-center",
        ),
        rx.cond(
            step != "",
            rx.el.span(
                step,
                class_name="text-[10px] font-bold uppercase tracking-widest text-indigo-700 bg-indigo-50/60 border border-indigo-100 px-2.5 py-1 rounded-full",
            ),
            rx.fragment(),
        ),
        class_name="flex items-center justify-between mb-5",
    )


def field_label(text: str, required: bool = False) -> rx.Component:
    return rx.el.label(
        text,
        rx.cond(
            required,
            rx.el.span(" *", class_name="text-rose-600"),
            rx.fragment(),
        ),
        class_name="block text-sm font-semibold text-slate-800 mb-1.5 tracking-tight",
    )


def field_error(key: str) -> rx.Component:
    msg = AppState.intake_errors[key].to(str)
    return rx.cond(
        AppState.intake_errors.contains(key),
        rx.el.p(
            rx.icon("circle-alert", class_name="h-3.5 w-3.5 mr-1 inline"),
            msg,
            class_name="text-xs text-rose-700 mt-1.5 flex items-center font-medium",
        ),
        rx.fragment(),
    )


def text_input(name: str, placeholder: str, default: str = "") -> rx.Component:
    return rx.el.input(
        name=name,
        type="text",
        placeholder=placeholder,
        default_value=default,
        class_name=INPUT_CLS,
    )


def select_input(
    name: str, options: list[tuple[str, str]], default_value
) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Select an option", value="default", disabled=True),
            rx.foreach(
                options,
                lambda o: rx.el.option(o[1], value=o[0]),
            ),
            name=name,
            default_value=rx.cond(
                default_value != "", default_value, "default"
            ),
            key=default_value,
            class_name="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl hover:border-indigo-300 focus:ring-2 focus:ring-indigo-900/15 focus:border-indigo-700 outline-none transition-all duration-200 text-slate-900 placeholder-slate-400 text-sm shadow-sm appearance-none cursor-pointer pr-10",
        ),
        rx.icon(
            "chevron-down",
            class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500 pointer-events-none",
        ),
        class_name="relative",
    )


def textarea_input(
    name: str, placeholder: str, rows: int = 3, default: str = ""
) -> rx.Component:
    return rx.el.textarea(
        name=name,
        placeholder=placeholder,
        rows=rows,
        default_value=default,
        class_name=INPUT_CLS + " resize-none",
    )


def guidance_chip(item: tuple[str, str]) -> rx.Component:
    label = item[0]
    icon_name = item[1]
    selected = AppState.guidance_areas.contains(label)
    return rx.el.button(
        rx.icon(icon_name, class_name="h-4 w-4 mr-1.5"),
        label,
        rx.cond(
            selected,
            rx.icon("check", class_name="h-3.5 w-3.5 ml-1.5"),
            rx.fragment(),
        ),
        type="button",
        on_click=lambda: AppState.toggle_guidance(label),
        class_name=rx.cond(
            selected,
            "flex items-center px-3.5 py-2 text-sm font-semibold rounded-xl border transition-all bg-indigo-900 text-white border-indigo-900 shadow-sm shadow-indigo-100 ring-2 ring-indigo-300/30 active:scale-[0.99]",
            "flex items-center px-3.5 py-2 text-sm font-medium rounded-xl border transition-all bg-white text-slate-700 border-slate-200 hover:border-indigo-300 hover:text-indigo-900 hover:bg-indigo-50/30 active:scale-[0.99]",
        ),
    )


def resume_section() -> rx.Component:
    return rx.el.div(
        section_header(
            "file-up",
            "Resume / CV",
            "Optional but highly recommended — helps your counsellor prep.",
            "Module 06",
        ),
        rx.cond(
            AppState.resume_filename != "",
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-text",
                        class_name="h-5 w-5 text-emerald-700",
                    ),
                    class_name="h-10 w-10 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        AppState.resume_filename,
                        class_name="text-sm font-semibold text-slate-900 truncate",
                    ),
                    rx.el.p(
                        AppState.resume_size_label,
                        class_name="text-xs text-slate-500 mt-0.5",
                    ),
                    class_name="flex-1 min-w-0 ml-3",
                ),
                rx.el.div(
                    rx.icon("circle-check", class_name="h-3.5 w-3.5 mr-1"),
                    "Uploaded",
                    class_name="flex items-center text-[11px] font-bold text-emerald-800 bg-emerald-50 border border-emerald-200/60 px-2.5 py-1 rounded-full",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4"),
                    type="button",
                    on_click=AppState.clear_resume,
                    class_name="ml-2 p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-all",
                ),
                class_name="flex items-center gap-1 p-4 bg-emerald-50/30 border border-emerald-200/70 rounded-xl",
            ),
            rx.upload.root(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload",
                            class_name="h-6 w-6 text-indigo-900",
                        ),
                        class_name="h-12 w-12 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-3",
                    ),
                    rx.el.p(
                        "Drop your resume or click to browse",
                        class_name="text-sm font-semibold text-slate-800",
                    ),
                    rx.el.p(
                        "PDF, DOC, or DOCX • up to 5 MB",
                        class_name="text-xs text-slate-500 mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center py-8 px-4 text-center",
                ),
                id=UPLOAD_ID,
                accept={
                    "application/pdf": [".pdf"],
                    "application/msword": [".doc"],
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                        ".docx"
                    ],
                },
                multiple=False,
                max_files=1,
                max_size=5 * 1024 * 1024,
                on_drop=AppState.handle_resume_upload(
                    rx.upload_files(upload_id=UPLOAD_ID)
                ),
                class_name="border-2 border-dashed border-slate-300 rounded-xl bg-slate-50/40 hover:border-indigo-400 hover:bg-indigo-50/20 transition-all cursor-pointer",
            ),
        ),
        rx.cond(
            AppState.resume_error != "",
            rx.el.p(
                rx.icon("circle-alert", class_name="h-3.5 w-3.5 mr-1 inline"),
                AppState.resume_error,
                class_name="text-xs text-rose-700 mt-2 flex items-center font-medium",
            ),
            rx.fragment(),
        ),
        class_name="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm",
    )


def intake_form() -> rx.Component:
    return rx.el.form(
        # Current role
        rx.el.div(
            section_header(
                "briefcase",
                "Your current situation",
                "Where are you right now?",
                "Module 01",
            ),
            rx.el.div(
                field_label("Current role / status"),
                text_input(
                    "current_role",
                    "e.g. Software Engineer at Acme, or Final-year student",
                    AppState.current_role,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                field_label("Experience level", required=True),
                select_input(
                    "experience_level",
                    [
                        ("none", "No experience yet (Fresher)"),
                        ("intern", "Internship experience"),
                        ("0_1", "0–1 year"),
                        ("1_3", "1–3 years"),
                        ("3_5", "3–5 years"),
                        ("5_10", "5–10 years"),
                        ("10_plus", "10+ years"),
                    ],
                    AppState.experience_level,
                ),
                field_error("experience_level"),
                class_name="mb-4",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Education
        rx.el.div(
            section_header(
                "graduation-cap",
                "Education",
                "Tell us about your background.",
                "Module 02",
            ),
            rx.el.div(
                field_label("Highest qualification", required=True),
                select_input(
                    "education_level",
                    [
                        ("high_school", "High School"),
                        ("diploma", "Diploma"),
                        ("bachelors", "Bachelor's degree"),
                        ("masters", "Master's degree"),
                        ("phd", "PhD / Doctorate"),
                        ("other", "Other"),
                    ],
                    AppState.education_level,
                ),
                field_error("education_level"),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    field_label("Institution"),
                    text_input(
                        "institution",
                        "e.g. IIT Bombay",
                        AppState.institution,
                    ),
                ),
                rx.el.div(
                    field_label("Field of study"),
                    text_input(
                        "field_of_study",
                        "e.g. Computer Science",
                        AppState.field_of_study,
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Skills & interests
        rx.el.div(
            section_header(
                "sparkles",
                "Skills & interests",
                "What you bring and what you love.",
                "Module 03",
            ),
            rx.el.div(
                field_label("Top skills", required=True),
                text_input(
                    "skills",
                    "Python, Data analysis, Public speaking",
                    AppState.skills,
                ),
                rx.el.p(
                    "Separate skills with commas.",
                    class_name="text-xs text-slate-500 mt-1.5",
                ),
                field_error("skills"),
                class_name="mb-4",
            ),
            rx.el.div(
                field_label("Interests"),
                text_input(
                    "interests",
                    "Product, AI, Design, Climate tech",
                    AppState.interests,
                ),
                rx.el.p(
                    "Separate interests with commas.",
                    class_name="text-xs text-slate-500 mt-1.5",
                ),
                class_name="",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Targets & challenges
        rx.el.div(
            section_header(
                "target",
                "Goals & challenges",
                "Where you want to go and what's in the way.",
                "Module 04",
            ),
            rx.el.div(
                field_label("Target roles or industries", required=True),
                text_input(
                    "target_roles",
                    "Product Manager, Data Scientist, UX Designer",
                    AppState.target_roles,
                ),
                rx.el.p(
                    "Separate with commas.",
                    class_name="text-xs text-slate-500 mt-1.5",
                ),
                field_error("target_roles"),
                class_name="mb-4",
            ),
            rx.el.div(
                field_label("Biggest challenges right now"),
                textarea_input(
                    "challenges",
                    "e.g. Not getting interview calls, unsure how to switch domains, feeling stuck in current role…",
                    3,
                    AppState.challenges,
                ),
                class_name="",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Guidance areas
        rx.el.div(
            section_header(
                "compass",
                "Where do you want guidance?",
                "Pick all that apply — your counsellor will focus here.",
                "Module 05",
            ),
            rx.el.div(
                rx.foreach(GUIDANCE_OPTIONS, guidance_chip),
                class_name="flex flex-wrap gap-2",
            ),
            field_error("guidance_areas"),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Career objective
        rx.el.div(
            section_header(
                "flag",
                "Career objective",
                "A short statement of where you want to be.",
                "Module 07",
            ),
            rx.el.div(
                field_label("In a few sentences…", required=True),
                textarea_input(
                    "career_objective",
                    "e.g. I want to transition into a Product Management role at a mid-sized SaaS company within the next 6–9 months.",
                    4,
                    AppState.career_objective,
                ),
                field_error("career_objective"),
                class_name="",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
        ),
        # Resume
        resume_section(),
        # Actions
        rx.el.div(
            rx.el.button(
                rx.icon("rotate-ccw", class_name="h-4 w-4 mr-1.5"),
                "Reset",
                type="button",
                on_click=AppState.reset_intake,
                class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-slate-400 active:scale-[0.99] transition-all duration-200 focus:ring-2 focus:ring-slate-300/30 focus:outline-none",
            ),
            rx.el.button(
                rx.icon("save", class_name="h-4 w-4 mr-2"),
                "Save & review",
                rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                type="submit",
                class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-indigo-900 hover:bg-indigo-950 active:scale-[0.99] rounded-xl transition-all duration-200 shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
            ),
            class_name="flex flex-col sm:flex-row gap-3 mt-6",
        ),
        on_submit=AppState.submit_intake,
        reset_on_submit=False,
    )


def intake_placeholder() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back",
                on_click=AppState.go_to_landing,
                class_name="flex items-center text-sm font-semibold text-slate-600 hover:text-indigo-900 mb-6 transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "MODULE 02 • GUIDED INTAKE",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.icon(
                        "clipboard-list",
                        class_name="h-5 w-5 text-indigo-900",
                    ),
                    class_name="h-11 w-11 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Hi ",
                    AppState.first_name,
                    " — let's understand your goals",
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Take a few minutes to share your background. The more we know, the more tailored your session will be.",
                    class_name="text-sm text-slate-600 mt-2 max-w-2xl",
                ),
                class_name="mb-6",
            ),
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            intake_form(),
            class_name="max-w-3xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-10 flex justify-center",
    )