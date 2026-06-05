import reflex as rx
from app.states.app_state import AppState


def feature_card(
    icon: str,
    title: str,
    desc: str,
    step_num: str = "",
    accent_color: str = "indigo",
) -> rx.Component:
    icon_color = rx.match(
        accent_color,
        ("emerald", "text-emerald-700"),
        ("amber", "text-amber-700"),
        ("rose", "text-rose-700"),
        "text-indigo-900",
    )
    bg_color = rx.match(
        accent_color,
        ("emerald", "bg-emerald-50 border-emerald-100"),
        ("amber", "bg-amber-50 border-amber-100"),
        ("rose", "bg-rose-50 border-rose-100"),
        "bg-indigo-50 border-indigo-100",
    )
    badge_color = rx.match(
        accent_color,
        ("emerald", "text-emerald-700 bg-emerald-50/70 border-emerald-100"),
        ("amber", "text-amber-700 bg-amber-50/70 border-amber-100"),
        ("rose", "text-rose-700 bg-rose-50/70 border-rose-100"),
        "text-indigo-700 bg-indigo-50/60 border-indigo-100",
    )
    hover_color = rx.match(
        accent_color,
        ("emerald", "hover:border-emerald-300 hover:shadow-emerald-50"),
        ("amber", "hover:border-amber-300 hover:shadow-amber-50"),
        ("rose", "hover:border-rose-300 hover:shadow-rose-50"),
        "hover:border-indigo-300 hover:shadow-indigo-50",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-5 w-5 {icon_color}"),
                class_name=f"h-11 w-11 rounded-2xl flex items-center justify-center border {bg_color}",
            ),
            rx.cond(
                step_num != "",
                rx.el.span(
                    step_num,
                    class_name=f"text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full border {badge_color}",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.h3(
            title, class_name="text-base font-semibold text-slate-900 mb-2"
        ),
        rx.el.p(desc, class_name="text-xs text-slate-600 leading-relaxed"),
        class_name=f"bg-white rounded-2xl border border-slate-200/70 p-6 hover:shadow-md hover:-translate-y-0.5 active:scale-[0.99] transition-academic animate-fade-in-up {hover_color}",
    )


def benefit_card(
    icon: str, title: str, desc: str, color_theme: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon,
                class_name=rx.match(
                    color_theme,
                    ("sage", "h-5 w-5 text-emerald-700"),
                    ("amber", "h-5 w-5 text-amber-700"),
                    ("rose", "h-5 w-5 text-rose-700"),
                    "h-5 w-5 text-indigo-900",
                ),
            ),
            class_name=rx.match(
                color_theme,
                (
                    "sage",
                    "h-11 w-11 rounded-2xl bg-emerald-50 flex items-center justify-center mb-4 border border-emerald-100",
                ),
                (
                    "amber",
                    "h-11 w-11 rounded-2xl bg-amber-50 flex items-center justify-center mb-4 border border-amber-100",
                ),
                (
                    "rose",
                    "h-11 w-11 rounded-2xl bg-rose-50 flex items-center justify-center mb-4 border border-rose-100",
                ),
                "h-11 w-11 rounded-2xl bg-indigo-50 flex items-center justify-center mb-4 border border-indigo-100",
            ),
        ),
        rx.el.h3(
            title, class_name="text-base font-semibold text-slate-900 mb-2"
        ),
        rx.el.p(desc, class_name="text-xs text-slate-600 leading-relaxed"),
        class_name="bg-white rounded-2xl border border-slate-200/70 p-6 hover:border-indigo-300 hover:shadow-md hover:-translate-y-0.5 active:scale-[0.99] transition-academic animate-fade-in-up h-full",
    )


def outcome_item(icon: str, text: str) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-emerald-700"),
            class_name="h-8 w-8 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0",
        ),
        rx.el.span(
            text,
            class_name="text-sm text-slate-700 ml-3 leading-relaxed font-medium",
        ),
        class_name="flex items-start py-2.5",
    )


def mentor_card(mentor: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={mentor['seed']}",
                class_name="h-14 w-14 rounded-full bg-indigo-50 border border-indigo-100",
            ),
            rx.el.div(
                rx.icon(
                    "badge-check", class_name="h-3.5 w-3.5 text-indigo-900"
                ),
                class_name="h-6 w-6 rounded-full bg-white border border-indigo-100 flex items-center justify-center -ml-3 mt-9 shadow-sm",
            ),
            class_name="flex items-end mb-4",
        ),
        rx.el.h4(
            mentor["name"],
            class_name="text-sm font-bold text-slate-900",
        ),
        rx.el.p(
            mentor["title"],
            class_name="text-xs text-slate-600 mt-0.5",
        ),
        rx.el.div(
            rx.foreach(
                mentor["expertise"].split(","),
                lambda s: rx.el.span(
                    s.strip(),
                    class_name="text-[10px] font-semibold text-indigo-800 bg-indigo-50 border border-indigo-100/80 px-2 py-0.5 rounded-full",
                ),
            ),
            class_name="flex flex-wrap gap-1 mt-3",
        ),
        rx.el.div(
            rx.icon("star", class_name="h-3.5 w-3.5 text-amber-600"),
            rx.el.span(
                mentor["rating"],
                class_name="text-xs font-bold text-slate-800 ml-1",
            ),
            rx.el.span(
                f" • {mentor['sessions']} sessions",
                class_name="text-xs text-slate-500 ml-1",
            ),
            class_name="flex items-center mt-3 pt-3 border-t border-slate-100",
        ),
        class_name="bg-white rounded-2xl border border-slate-200/70 p-5 hover:border-indigo-200 hover:shadow-sm transition-all duration-300",
    )


def testimonial_card(t: dict[str, str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("quote", class_name="h-5 w-5 text-indigo-300"),
            class_name="mb-3",
        ),
        rx.el.p(
            t["quote"],
            class_name="text-sm text-slate-700 leading-relaxed italic",
        ),
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={t['seed']}",
                class_name="h-9 w-9 rounded-full bg-indigo-50 border border-indigo-100",
            ),
            rx.el.div(
                rx.el.p(
                    t["name"],
                    class_name="text-xs font-bold text-slate-900",
                ),
                rx.el.p(
                    t["role"],
                    class_name="text-[11px] text-slate-500 mt-0.5",
                ),
                class_name="ml-3",
            ),
            class_name="flex items-center mt-5 pt-5 border-t border-slate-100",
        ),
        class_name="bg-white rounded-2xl border border-slate-200/70 p-6 hover:border-indigo-200 hover:shadow-sm transition-all duration-300",
    )


def faq_item(question: str, answer: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "circle-help",
                class_name="h-4 w-4 text-indigo-900 shrink-0 mt-0.5",
            ),
            rx.el.h4(
                question,
                class_name="text-sm font-bold text-slate-900 ml-2",
            ),
            class_name="flex items-start mb-2",
        ),
        rx.el.p(
            answer,
            class_name="text-xs text-slate-600 leading-relaxed ml-6",
        ),
        class_name="p-5 bg-white border border-slate-200/60 rounded-2xl hover:border-indigo-200 hover:shadow-sm transition-all",
    )


def audience_card(
    icon: str,
    title: str,
    desc: str,
    badge: str,
    stage: str,
    curriculum: list[str],
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    icon,
                    class_name=rx.match(
                        stage,
                        ("fresher", "h-5 w-5 text-emerald-700"),
                        ("early_career", "h-5 w-5 text-indigo-900"),
                        "h-5 w-5 text-amber-700",
                    ),
                ),
                class_name=rx.match(
                    stage,
                    (
                        "fresher",
                        "h-11 w-11 rounded-2xl bg-emerald-50 flex items-center justify-center border border-emerald-100",
                    ),
                    (
                        "early_career",
                        "h-11 w-11 rounded-2xl bg-indigo-50 flex items-center justify-center border border-indigo-100",
                    ),
                    "h-11 w-11 rounded-2xl bg-amber-50 flex items-center justify-center border border-amber-100",
                ),
            ),
            rx.el.span(
                badge,
                class_name=rx.match(
                    stage,
                    (
                        "fresher",
                        "text-[11px] font-bold text-emerald-800 bg-emerald-50 border border-emerald-100/80 px-2.5 py-1 rounded-full w-fit",
                    ),
                    (
                        "early_career",
                        "text-[11px] font-bold text-indigo-800 bg-indigo-50 border border-indigo-100/80 px-2.5 py-1 rounded-full w-fit",
                    ),
                    "text-[11px] font-bold text-amber-800 bg-amber-50 border border-amber-100/80 px-2.5 py-1 rounded-full w-fit",
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.h3(
            title, class_name="text-base font-semibold text-slate-900 mb-2"
        ),
        rx.el.p(desc, class_name="text-xs text-slate-600 leading-relaxed mb-4"),
        rx.el.div(
            rx.el.p(
                "Curriculum highlights",
                class_name="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2",
            ),
            rx.el.ul(
                rx.foreach(
                    curriculum,
                    lambda c: rx.el.li(
                        rx.icon(
                            "check",
                            class_name=rx.match(
                                stage,
                                ("fresher", "h-3.5 w-3.5 text-emerald-700"),
                                ("early_career", "h-3.5 w-3.5 text-indigo-900"),
                                "h-3.5 w-3.5 text-amber-700",
                            ),
                        ),
                        rx.el.span(
                            c,
                            class_name="text-xs text-slate-700 ml-2 font-medium",
                        ),
                        class_name="flex items-center py-1",
                    ),
                ),
            ),
            class_name="mb-4 pb-4 border-b border-slate-100",
        ),
        rx.el.button(
            "Begin counselling",
            rx.icon(
                "arrow-right",
                class_name=rx.match(
                    stage,
                    ("fresher", "h-3.5 w-3.5 ml-1.5 text-emerald-700"),
                    ("early_career", "h-3.5 w-3.5 ml-1.5 text-indigo-900"),
                    "h-3.5 w-3.5 ml-1.5 text-amber-700",
                ),
            ),
            on_click=lambda: AppState.go_to_register(stage),
            class_name=rx.match(
                stage,
                (
                    "fresher",
                    "flex items-center text-xs font-bold text-emerald-700 hover:text-emerald-800 transition-colors",
                ),
                (
                    "early_career",
                    "flex items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
                ),
                "flex items-center text-xs font-bold text-amber-700 hover:text-amber-800 transition-colors",
            ),
        ),
        class_name=rx.match(
            stage,
            (
                "fresher",
                "bg-white rounded-2xl border border-slate-200/70 p-6 hover:border-emerald-300 hover:shadow-md transition-all duration-300",
            ),
            (
                "early_career",
                "bg-white rounded-2xl border border-slate-200/70 p-6 hover:border-indigo-300 hover:shadow-md transition-all duration-300",
            ),
            "bg-white rounded-2xl border border-slate-200/70 p-6 hover:border-amber-300 hover:shadow-md transition-all duration-300",
        ),
    )


def stat(value: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            value,
            class_name="text-2xl sm:text-3xl font-extrabold text-indigo-900 tracking-tight",
        ),
        rx.el.p(label, class_name="text-xs font-semibold text-slate-500 mt-1"),
    )


def trust_logo(name: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-4 w-4 text-slate-500"),
        rx.el.span(
            name,
            class_name="text-xs font-bold text-slate-600 ml-1.5 tracking-wide",
        ),
        class_name="flex items-center px-4 py-2 bg-white border border-slate-200/70 rounded-xl",
    )


def filter_tab(label: str, key_val: str) -> rx.Component:
    is_selected = AppState.career_path_filter == key_val
    return rx.el.button(
        label,
        on_click=lambda: AppState.set_career_path_filter(key_val),
        type="button",
        class_name=rx.cond(
            is_selected,
            "px-4 py-2 text-xs sm:text-sm font-bold rounded-xl transition-academic bg-indigo-900 text-white shadow-md scale-105 ring-2 ring-indigo-200",
            "px-4 py-2 text-xs sm:text-sm font-semibold rounded-xl transition-academic text-slate-600 bg-white border border-slate-200/70 hover:bg-slate-50 hover:text-slate-900 hover:border-slate-300 hover:scale-102 active:scale-95",
        ),
    )


def career_path_card(path: dict[str, str]) -> rx.Component:
    theme_color = path["color_theme"]
    icon_wrap = rx.match(
        theme_color,
        (
            "blue",
            "h-11 w-11 rounded-2xl bg-indigo-50 flex items-center justify-center border border-indigo-100 shrink-0 transition-academic group-hover:scale-110",
        ),
        (
            "rose",
            "h-11 w-11 rounded-2xl bg-rose-50 flex items-center justify-center border border-rose-100 shrink-0 transition-academic group-hover:scale-110",
        ),
        (
            "sage",
            "h-11 w-11 rounded-2xl bg-emerald-50 flex items-center justify-center border border-emerald-100 shrink-0 transition-academic group-hover:scale-110",
        ),
        "h-11 w-11 rounded-2xl bg-amber-50 flex items-center justify-center border border-amber-100 shrink-0 transition-academic group-hover:scale-110",
    )
    icon_color = rx.match(
        theme_color,
        ("blue", "h-5 w-5 text-indigo-900"),
        ("rose", "h-5 w-5 text-rose-700"),
        ("sage", "h-5 w-5 text-emerald-700"),
        "h-5 w-5 text-amber-700",
    )
    trend_badge = rx.match(
        path["trend_key"],
        (
            "hot",
            "text-[11px] font-bold text-rose-800 bg-rose-50 border border-rose-200/70 px-2.5 py-1 rounded-full w-fit flex items-center gap-1 animate-pulse-gentle",
        ),
        (
            "rising",
            "text-[11px] font-bold text-indigo-800 bg-indigo-50 border border-indigo-200/70 px-2.5 py-1 rounded-full w-fit flex items-center gap-1 animate-pulse-gentle",
        ),
        "text-[11px] font-bold text-emerald-800 bg-emerald-50 border border-emerald-200/70 px-2.5 py-1 rounded-full w-fit flex items-center gap-1 animate-pulse-gentle",
    )
    role_chip = rx.match(
        theme_color,
        (
            "blue",
            "text-xs font-semibold text-indigo-900 bg-indigo-50/70 border border-indigo-100/70 px-2.5 py-1 rounded-xl transition-all hover:bg-indigo-100",
        ),
        (
            "rose",
            "text-xs font-semibold text-rose-800 bg-rose-50/70 border border-rose-100/70 px-2.5 py-1 rounded-xl transition-all hover:bg-rose-100",
        ),
        (
            "sage",
            "text-xs font-semibold text-emerald-800 bg-emerald-50/70 border border-emerald-100/70 px-2.5 py-1 rounded-xl transition-all hover:bg-emerald-100",
        ),
        "text-xs font-semibold text-amber-800 bg-amber-50/70 border border-amber-100/70 px-2.5 py-1 rounded-xl transition-all hover:bg-amber-100",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(path["icon"], class_name=icon_color),
                    class_name=icon_wrap,
                ),
                rx.el.span(path["trend_label"], class_name=trend_badge),
                class_name="flex items-center justify-between w-full mb-4",
            ),
            rx.el.div(
                rx.el.h3(
                    path["title"],
                    class_name="text-base font-bold text-slate-900 group-hover:text-indigo-900 transition-colors",
                ),
                rx.el.p(
                    path["desc"],
                    class_name="text-xs text-slate-600 mt-1.5 leading-relaxed",
                ),
                class_name="w-full",
            ),
            class_name="w-full",
        ),
        # Stats row
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="h-3.5 w-3.5 text-slate-500"),
                rx.el.span(
                    path["learners"],
                    class_name="text-[11px] font-semibold text-slate-700 ml-1",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(class_name="h-3 w-px bg-slate-200"),
            rx.el.div(
                rx.icon("clock", class_name="h-3.5 w-3.5 text-slate-500"),
                rx.el.span(
                    path["duration"],
                    class_name="text-[11px] font-semibold text-slate-700 ml-1",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(class_name="h-3 w-px bg-slate-200"),
            rx.el.div(
                rx.icon(
                    "trending-up",
                    class_name="h-3.5 w-3.5 text-emerald-700",
                ),
                rx.el.span(
                    path["growth"],
                    class_name="text-[11px] font-semibold text-emerald-800 ml-1",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center gap-3 mt-4 pt-4 border-t border-slate-100",
        ),
        # Key Skills Section
        rx.el.div(
            rx.el.p(
                "Key skills in demand",
                class_name="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    path["key_skills"].split(","),
                    lambda skill: rx.el.span(
                        skill.strip(),
                        class_name="text-xs font-semibold text-slate-700 bg-slate-50 border border-slate-200/70 px-2.5 py-0.5 rounded-xl",
                    ),
                ),
                class_name="flex flex-wrap gap-1.5",
            ),
            class_name="mt-4 pt-4 border-t border-slate-100",
        ),
        # Roles Section
        rx.el.div(
            rx.el.p(
                "Sample roles you can pursue",
                class_name="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    path["roles"].split(","),
                    lambda role: rx.el.span(
                        role.strip(),
                        class_name=role_chip,
                    ),
                ),
                class_name="flex flex-wrap gap-1.5",
            ),
            class_name="mt-4 pt-4 border-t border-slate-100",
        ),
        # CTA
        rx.el.button(
            "Get guided in this path",
            rx.icon(
                "arrow-right",
                class_name="h-3.5 w-3.5 ml-1.5 transition-academic group-hover:translate-x-1",
            ),
            on_click=lambda: AppState.go_to_register(""),
            class_name="mt-5 flex items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
        ),
        class_name="bg-white rounded-2xl border border-slate-200/70 p-6 hover:shadow-lg hover:border-indigo-300 hover:-translate-y-0.5 active:scale-[0.99] transition-academic flex flex-col justify-between group animate-fade-in-up",
    )


MENTORS: list[dict[str, str]] = [
    {
        "name": "Dr. Anika Rao",
        "title": "Ex-Google • PhD, Carnegie Mellon",
        "expertise": "Software, System Design, ML",
        "rating": "4.9",
        "sessions": "320",
        "seed": "anika_rao_mentor",
    },
    {
        "name": "Marcus Chen",
        "title": "Senior PM, ex-Microsoft & Stripe",
        "expertise": "Product, Strategy, Growth",
        "rating": "4.9",
        "sessions": "412",
        "seed": "marcus_chen_mentor",
    },
    {
        "name": "Priya Iyer",
        "title": "Lead Data Scientist, FinTech",
        "expertise": "Data Science, AI, Analytics",
        "rating": "4.8",
        "sessions": "275",
        "seed": "priya_iyer_mentor",
    },
    {
        "name": "Daniel Okafor",
        "title": "UX Director • Adobe alum",
        "expertise": "Design, UX Research, Portfolio",
        "rating": "4.9",
        "sessions": "198",
        "seed": "daniel_okafor_mentor",
    },
]


TESTIMONIALS: list[dict[str, str]] = [
    {
        "quote": "Pathwise helped me transition from civil engineering into a data analyst role at a Series B startup — in under four months. The roadmap was brutally clear and motivating.",
        "name": "Sneha M.",
        "role": "Career switcher → Data Analyst",
        "seed": "testimonial_sneha",
    },
    {
        "quote": "As a final-year student, I had no idea what I actually wanted. My counsellor helped me narrow down to product management and prep for top-tier interviews.",
        "name": "Arjun T.",
        "role": "Student → Associate PM",
        "seed": "testimonial_arjun",
    },
    {
        "quote": "I'd been stuck at the same level for three years. One deep-dive session reframed how I positioned my work — landed a senior role with a 38% raise.",
        "name": "Rebecca L.",
        "role": "Engineer → Senior Engineer",
        "seed": "testimonial_rebecca",
    },
]


LEARNING_OUTCOMES: list[tuple[str, str]] = [
    (
        "compass",
        "A clear, written career direction tailored to your strengths and life context.",
    ),
    (
        "route",
        "A 30-60-90 day action plan with concrete weekly milestones.",
    ),
    (
        "file-text",
        "An ATS-optimized resume and LinkedIn rewrite playbook you can apply right away.",
    ),
    (
        "messages-square",
        "Interview frameworks (STAR, CIRCLE, system design) practiced with feedback.",
    ),
    (
        "book-open",
        "A curated reading and course list mapped to your target roles.",
    ),
    (
        "shield-check",
        "Confidence — backed by data, mentor experience, and a community of peers.",
    ),
]


def landing() -> rx.Component:
    return rx.el.div(
        # Hero
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "graduation-cap",
                            class_name="h-3.5 w-3.5 text-indigo-900",
                        ),
                        rx.el.span(
                            "Pathwise Academy • Career Counselling Studio",
                            class_name="text-xs font-bold text-slate-800 ml-1.5 tracking-wide",
                        ),
                        class_name="inline-flex items-center bg-white/80 border border-indigo-100/80 px-3.5 py-1.5 rounded-full mb-4 shadow-sm",
                    ),
                    # Prominent Hero Announcement Banner (High Contrast, Responsive, Pulsing Animation)
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "gift",
                                    class_name="h-4 w-4 text-emerald-700 animate-bounce",
                                ),
                                rx.el.span(
                                    "FREE GIFT",
                                    class_name="text-[10px] sm:text-[11px] font-black uppercase tracking-widest text-emerald-800",
                                ),
                                class_name="inline-flex items-center gap-1.5 bg-emerald-100/90 px-3 py-1 rounded-full border border-emerald-300 shadow-sm shrink-0",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Limited Time Benefit:",
                                    class_name="text-xs sm:text-sm font-bold text-indigo-900 uppercase tracking-wider block sm:inline",
                                ),
                                rx.el.span(
                                    "Free 30 mins Discovery Session with Industry Expert",
                                    class_name="text-sm sm:text-base md:text-lg font-black text-slate-900 ml-0 sm:ml-2 mt-1 sm:mt-0 block sm:inline leading-tight tracking-tight",
                                ),
                                class_name="flex-1 text-center sm:text-left",
                            ),
                            class_name="flex flex-col sm:flex-row items-center gap-3 w-full",
                        ),
                        rx.el.div(
                            rx.icon(
                                "sparkles",
                                class_name="h-5 w-5 text-indigo-900 animate-pulse-gentle hidden md:block shrink-0",
                            ),
                            class_name="shrink-0",
                        ),
                        class_name="w-full max-w-4xl mx-auto flex items-center justify-between bg-gradient-to-r from-amber-50 via-indigo-50 to-emerald-50 border-2 border-indigo-400 p-4 sm:p-5 md:p-6 rounded-3xl mb-8 shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 animate-pulse-gentle relative overflow-hidden ring-4 ring-indigo-200/50",
                    ),
                    rx.el.h1(
                        "Learn the path. ",
                        rx.el.span(
                            "Walk it with confidence.",
                            class_name="text-indigo-900",
                        ),
                        class_name="text-4xl sm:text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.1]",
                    ),
                    rx.el.p(
                        "A scholarly, mentor-led approach to career guidance. We pair you with vetted counsellors and a structured curriculum so you don't just plan a career — you build the discipline to thrive in it.",
                        class_name="text-sm sm:text-base text-slate-600 mt-6 max-w-2xl mx-auto leading-relaxed",
                    ),
                    # Highlighting the same offer next to calls-to-action as a strong CTA strip
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "gift",
                                    class_name="h-4 w-4 text-emerald-700 mr-2 animate-bounce",
                                ),
                                rx.el.span(
                                    "GUARANTEED COMPLIMENTARY OFFER",
                                    class_name="text-[10px] font-extrabold uppercase tracking-widest text-emerald-800 bg-emerald-100 border border-emerald-300 px-2 py-0.5 rounded-md mr-3 shrink-0",
                                ),
                                rx.el.span(
                                    "Free 30 mins Discovery Session with Industry Expert is instantly credited upon signup",
                                    class_name="text-xs sm:text-sm font-extrabold text-slate-900 tracking-tight",
                                ),
                                class_name="flex flex-col sm:flex-row items-center justify-center text-center gap-2 sm:gap-0 p-3.5 bg-gradient-to-r from-emerald-50/90 via-white to-emerald-50/90 border border-emerald-300/80 rounded-2xl shadow-sm",
                            ),
                            class_name="max-w-2xl mx-auto w-full",
                        ),
                        class_name="mt-8 flex justify-center w-full px-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon(
                                "graduation-cap", class_name="h-4 w-4 mr-2"
                            ),
                            "Begin counselling",
                            rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                            on_click=lambda: AppState.go_to_register(""),
                            class_name="flex items-center bg-indigo-900 text-white px-6 py-3 rounded-xl hover:bg-indigo-950 hover:shadow-lg hover:shadow-indigo-100 active:scale-[0.98] transition-all font-semibold",
                        ),
                        rx.el.button(
                            rx.icon("log-in", class_name="h-4 w-4 mr-2"),
                            "Sign in",
                            on_click=AppState.go_to_login,
                            class_name="flex items-center text-slate-700 px-6 py-3 rounded-xl hover:bg-slate-50 transition-all font-semibold border border-slate-200/80 bg-white",
                        ),
                        class_name="flex flex-col sm:flex-row gap-3 justify-center mt-4",
                    ),
                    rx.cond(
                        AppState.has_saved_account,
                        rx.el.div(
                            rx.icon(
                                "hard-drive",
                                class_name="h-3.5 w-3.5 text-indigo-900",
                            ),
                            rx.el.span(
                                "We found saved details from a previous session on this device.",
                                class_name="text-xs font-medium text-slate-700 ml-1.5",
                            ),
                            rx.el.button(
                                "Resume",
                                on_click=AppState.go_to_login,
                                class_name="text-xs font-bold text-indigo-900 hover:text-indigo-950 ml-2 underline underline-offset-2",
                            ),
                            class_name="inline-flex items-center bg-indigo-50/60 border border-indigo-100/60 px-3.5 py-2 rounded-2xl mt-5 shadow-sm",
                        ),
                        rx.fragment(),
                    ),
                    # Trust signals strip
                    rx.el.div(
                        rx.el.p(
                            "Counsellors who've shaped careers at",
                            class_name="text-[11px] font-bold uppercase tracking-widest text-slate-500 text-center mb-4",
                        ),
                        rx.el.div(
                            trust_logo("Google", "search"),
                            trust_logo("Microsoft", "square"),
                            trust_logo("Stripe", "credit-card"),
                            trust_logo("Adobe", "palette"),
                            trust_logo("Amazon", "package"),
                            trust_logo("Meta", "infinity"),
                            class_name="flex flex-wrap items-center justify-center gap-2",
                        ),
                        class_name="mt-12",
                    ),
                    # Stats
                    rx.el.div(
                        stat("12,000+", "Sessions completed"),
                        rx.el.div(
                            class_name="h-8 w-px bg-slate-200 hidden sm:block"
                        ),
                        stat("4.9 / 5", "Mentor rating"),
                        rx.el.div(
                            class_name="h-8 w-px bg-slate-200 hidden sm:block"
                        ),
                        stat("85%", "Reach goals in 90 days"),
                        rx.el.div(
                            class_name="h-8 w-px bg-slate-200 hidden sm:block"
                        ),
                        stat("60+", "Career domains"),
                        class_name="flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 mt-10 pt-8 border-t border-slate-200/60",
                    ),
                    class_name="text-center max-w-4xl mx-auto",
                ),
                class_name="relative",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-14 sm:py-20 bg-gradient-to-b from-indigo-50/40 via-white to-white border-b border-slate-200/40",
        ),
        # Audience (Who we help — curriculum styled)
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "FOR EVERY STAGE",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "Counselling tracks designed for where you are.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Each track has its own curriculum, mentor matching rules, and outcome milestones — so you get guidance that fits your reality.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    audience_card(
                        "graduation-cap",
                        "Freshers & Students",
                        "Just stepping into the workforce? Discover roles that match your strengths and build a launch plan that works.",
                        "Starting out",
                        "fresher",
                        [
                            "Strengths & interest mapping",
                            "First-resume bootcamp",
                            "Internship & entry-role strategy",
                            "Mock HR + technical screens",
                        ],
                    ),
                    audience_card(
                        "book-open",
                        "Higher-Study Strategy",
                        "Planning a Master's, MBA, or PhD? Optimize your academic application, research statement, and university shortlists.",
                        "Academic Bound",
                        "fresher",
                        [
                            "Statement of Purpose (SOP) critique",
                            "Academic CV & credentials audit",
                            "Research or thesis proposal planning",
                            "Letter of Recommendation prep",
                        ],
                    ),
                    audience_card(
                        "trending-up",
                        "Early-Career Pros",
                        "1–5 years in? Get strategic guidance on growth, skill gaps, and how to land the next big opportunity.",
                        "Growing",
                        "early_career",
                        [
                            "Growth narrative & positioning",
                            "Skill-gap audit and roadmap",
                            "Senior-level interview prep",
                            "Compensation negotiation",
                        ],
                    ),
                    audience_card(
                        "target",
                        "Active Interview-Ready Seekers",
                        "Have an upcoming round? Go through specialized mock trials, stress-tests, and live calibration sessions.",
                        "Interview Sprint",
                        "early_career",
                        [
                            "STAR & behavioral deep-dives",
                            "Live system design dry runs",
                            "Industry-specific technical mocks",
                            "Post-interview feedback loop",
                        ],
                    ),
                    audience_card(
                        "shuffle",
                        "Role Switchers",
                        "Ready for a pivot? Map a clear, confident transition into a new domain or industry — without starting over.",
                        "Pivoting",
                        "switcher",
                        [
                            "Transferable-skill translation",
                            "Targeted upskilling plan",
                            "Bridge-role identification",
                            "Story-driven resume rewrite",
                        ],
                    ),
                    audience_card(
                        "rotate-ccw",
                        "Career Returners",
                        "Returning to work after a career break? Reframe your timeline, bridge the gap, and relaunch with confidence.",
                        "Relaunching",
                        "switcher",
                        [
                            "Break gap positioning playbook",
                            "Skills refreshing recommendations",
                            "Returnship programs routing",
                            "Confidence & brand rebuilding",
                        ],
                    ),
                    audience_card(
                        "award",
                        "Leadership Track",
                        "Targeting a Director, VP, Staff Engineer, or Executive role? Refine your strategic influence and organizational design.",
                        "Executive Path",
                        "senior",
                        [
                            "Strategic influence framework",
                            "Organizational impact alignment",
                            "Executive presence masterclass",
                            "360 peer feedback planning",
                        ],
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-white border-b border-slate-200/60",
        ),
        # Explore career paths (richer educational treatment)
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "CAREER PATH LIBRARY",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "Explore the paths our counsellors specialize in.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Each path is a structured learning track — mapped to live market demand, validated by domain mentors, and refreshed every quarter.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-8",
                ),
                rx.el.div(
                    filter_tab("All paths", "all"),
                    filter_tab("Hot market", "hot"),
                    filter_tab("Rising", "rising"),
                    filter_tab("Steady", "steady"),
                    class_name="flex flex-wrap justify-center items-center gap-2 mb-10 bg-white p-2 rounded-2xl border border-slate-200/70 max-w-md mx-auto shadow-sm",
                ),
                rx.el.div(
                    rx.foreach(
                        AppState.filtered_career_paths, career_path_card
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-slate-50/70 border-b border-slate-200/60",
        ),
        # How it works (curriculum-styled)
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "THE PATHWISE METHOD",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "A simple, structured path to clarity.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Seven cohesive milestones — an academic, step-by-step career readiness journey designed by educators and domain experts.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    feature_card(
                        "user-plus",
                        "Register your profile",
                        "Tell us who you are and where you are in your career — takes under a minute and helps us pre-match a counsellor.",
                        "Step 01",
                        "indigo",
                    ),
                    feature_card(
                        "clipboard-list",
                        "Complete a guided intake",
                        "Walk through a structured questionnaire on goals, skills, and challenges. Your answers shape your personalized session.",
                        "Step 02",
                        "indigo",
                    ),
                    feature_card(
                        "calendar-check",
                        "Meet your counsellor 1:1",
                        "Pick a slot, join a focused video session, and walk away with a written action plan you can start that same week.",
                        "Step 03",
                        "indigo",
                    ),
                    feature_card(
                        "bar-chart-3",
                        "Comprehensive Assessment Plan",
                        "Receive an exhaustive diagnostic evaluation of your technical skills, soft skill capabilities, and target academic readiness metrics.",
                        "Step 04",
                        "emerald",
                    ),
                    feature_card(
                        "book-open",
                        "Grooming & Upskilling Period",
                        "Engage in a 3–9 month structured roadmap tailored to your specific readiness levels, featuring deep skill building and mentoring reviews.",
                        "Step 05",
                        "amber",
                    ),
                    feature_card(
                        "send",
                        "Interview Lineup",
                        "Gain exclusive fast-track entries, direct applications, and live calibration mocks with top-tier partnered companies and universities.",
                        "Step 06",
                        "rose",
                    ),
                    feature_card(
                        "trophy",
                        "Final Selection & Alumni Network",
                        "Transition smoothly into your dream offer, secure final advisory reviews, and secure lifelong integration within our expert alumni community.",
                        "Step 07",
                        "emerald",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
                id="how",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-white border-b border-slate-200/60",
        ),
        # Learning outcomes
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "WHAT YOU'LL TAKE AWAY",
                            class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                        ),
                        rx.el.h2(
                            "Learning outcomes from every counselling track.",
                            class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                        ),
                        rx.el.p(
                            "Pathwise sessions are educational by design. You leave each track with tangible artifacts, frameworks, and a sharpened sense of direction — not just a chat.",
                            class_name="text-sm text-slate-600 mt-3 leading-relaxed",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Start your track",
                                rx.icon(
                                    "arrow-right",
                                    class_name="h-4 w-4 ml-2",
                                ),
                                on_click=lambda: AppState.go_to_register(""),
                                class_name="inline-flex items-center bg-indigo-900 text-white px-5 py-2.5 rounded-xl hover:bg-indigo-950 active:scale-[0.98] transition-all font-semibold text-sm shadow-sm",
                            ),
                            class_name="mt-6",
                        ),
                        class_name="",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "book-open-check",
                                    class_name="h-4 w-4 text-indigo-900",
                                ),
                                rx.el.span(
                                    "Outcomes checklist",
                                    class_name="text-sm font-bold text-slate-900 ml-2",
                                ),
                                class_name="flex items-center mb-3 pb-3 border-b border-slate-100",
                            ),
                            rx.el.ul(
                                rx.foreach(
                                    LEARNING_OUTCOMES,
                                    lambda o: outcome_item(o[0], o[1]),
                                ),
                                class_name="divide-y divide-slate-100",
                            ),
                            class_name="bg-white rounded-2xl border border-slate-200/70 p-6",
                        ),
                        class_name="",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-slate-50/70 border-b border-slate-200/60",
        ),
        # Mentor faculty
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "MEET THE FACULTY",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "Counsellors who've actually built the careers you're aiming for.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Every Pathwise mentor is vetted on real industry experience, teaching ability, and a track record of helping people level up.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    rx.foreach(MENTORS, mentor_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-white border-b border-slate-200/60",
        ),
        # Why Choose Pathwise
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "WHY PATHWISE",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "An academy-grade approach to career guidance.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Frameworks instead of feelings. Practice instead of platitudes. Outcomes you can point to.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    benefit_card(
                        "route",
                        "Actionable Roadmap",
                        "Walk away from every session with a clear, step-by-step PDF roadmap outlining exact skills to acquire and roles to target.",
                        "blue",
                    ),
                    benefit_card(
                        "search-code",
                        "ATS-Ready Portfolios",
                        "Our optimization process ensures your resume, GitHub, or portfolio passes applicant tracking systems with flying colors.",
                        "sage",
                    ),
                    benefit_card(
                        "award",
                        "Domain-Specific Coaches",
                        "Get matched with mentors who've actually worked at companies like Google, Microsoft, and high-growth scale-ups.",
                        "amber",
                    ),
                    benefit_card(
                        "messages-square",
                        "Unlimited Practice",
                        "Unlock realistic mock interviews tailored to your exact target tier, complete with detailed rubric-based grading.",
                        "rose",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-slate-50/70 border-b border-slate-200/60",
        ),
        # Testimonials
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "STUDENT STORIES",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "Careers, reshaped — in their own words.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "A glimpse of what people walk away with after just a few counselling sessions.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    rx.foreach(TESTIMONIALS, testimonial_card),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-white border-b border-slate-200/60",
        ),
        # FAQ Section
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "ANSWERS",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    rx.el.h2(
                        "Frequently asked questions.",
                        class_name="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Everything you need to know about our personal career counselling sessions.",
                        class_name="text-sm text-slate-600 mt-3 max-w-2xl mx-auto",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    faq_item(
                        "How does the match system work?",
                        "We automatically match you with a specialized career coach based on your selected career stage, field of study, and target roles during intake.",
                    ),
                    faq_item(
                        "Is my resume required for booking?",
                        "No! Resume upload is completely optional. If you don't have one ready, your counsellor will help you outline one from scratch during your session.",
                    ),
                    faq_item(
                        "Where is my private data stored?",
                        "If cloud sync is inactive, all registration, intake, and booking selections are saved completely on your private browser session. No data is sent to external servers.",
                    ),
                    faq_item(
                        "Can I reschedule after booking?",
                        "Absolutely. Your confirmation email will include a reschedule link. You can change your slot up to 12 hours in advance at no extra cost.",
                    ),
                    faq_item(
                        "Do you offer ongoing mentorship?",
                        "Yes — after your first session, your counsellor can opt you into a multi-session track with weekly check-ins, accountability, and homework reviews.",
                    ),
                    faq_item(
                        "Is Pathwise suitable for non-tech careers?",
                        "Absolutely. We have counsellors across product, design, finance, consulting, healthcare, education, and more. Our method is domain-agnostic.",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-5 max-w-5xl mx-auto",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-16 bg-slate-50/70 border-b border-slate-200/60",
        ),
        # Final CTA
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "graduation-cap",
                            class_name="h-6 w-6 text-white",
                        ),
                        class_name="h-12 w-12 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mx-auto mb-5",
                    ),
                    rx.el.h2(
                        "Your next chapter starts here.",
                        class_name="text-2xl sm:text-4xl font-bold text-white tracking-tight",
                    ),
                    rx.el.p(
                        "Join thousands who turned uncertainty into a clear, structured plan with Pathwise.",
                        class_name="text-sm sm:text-base text-indigo-100 mt-3 mb-7 max-w-xl mx-auto leading-relaxed",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("user-plus", class_name="h-4 w-4 mr-2"),
                            "Register — it's free to start",
                            rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                            on_click=lambda: AppState.go_to_register(""),
                            class_name="inline-flex items-center bg-white text-indigo-900 px-6 py-3 rounded-xl hover:bg-indigo-50 active:scale-[0.98] transition-all font-bold shadow-sm",
                        ),
                        rx.el.button(
                            rx.icon("log-in", class_name="h-4 w-4 mr-2"),
                            "Sign in",
                            on_click=AppState.go_to_login,
                            class_name="inline-flex items-center text-white px-6 py-3 rounded-xl hover:bg-white/10 transition-all font-semibold border border-white/30",
                        ),
                        class_name="flex flex-col sm:flex-row gap-3 justify-center",
                    ),
                    rx.el.div(
                        rx.icon(
                            "shield-check",
                            class_name="h-3.5 w-3.5 text-indigo-200",
                        ),
                        rx.el.span(
                            "Free intake • No credit card • Cancel anytime",
                            class_name="text-xs text-indigo-100 ml-1.5 font-medium",
                        ),
                        class_name="flex items-center justify-center mt-6",
                    ),
                    class_name="text-center bg-indigo-900 rounded-3xl p-10 sm:p-14 border border-indigo-800",
                ),
                class_name="max-w-4xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-14",
        ),
        class_name="w-full",
    )