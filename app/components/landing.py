import reflex as rx
from app.states.app_state import AppState


def feature_card(icon: str, title: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-rose-600"),
            class_name="h-10 w-10 rounded-2xl bg-rose-50 flex items-center justify-center mb-4 border border-rose-100",
        ),
        rx.el.h3(
            title, class_name="text-base font-semibold text-stone-900 mb-2"
        ),
        rx.el.p(desc, class_name="text-xs text-stone-600 leading-relaxed"),
        class_name="bg-gradient-to-b from-white to-stone-50/50 rounded-2xl border border-stone-200/60 p-6 hover:border-rose-200 hover:shadow-md transition-all duration-300",
    )


def audience_card(
    icon: str, title: str, desc: str, badge: str, stage: str
) -> rx.Component:
    color_classes = rx.match(
        stage,
        (
            "fresher",
            "border-emerald-100 bg-emerald-50/30 text-emerald-700 icon-bg-emerald-50 icon-emerald-600 hover-border-emerald-300",
        ),
        (
            "early_career",
            "border-blue-100 bg-blue-50/30 text-blue-700 icon-bg-blue-50 icon-blue-600 hover-border-blue-300",
        ),
        (
            "switcher",
            "border-amber-100 bg-amber-50/30 text-amber-700 icon-bg-amber-50 icon-amber-600 hover-border-amber-300",
        ),
        "border-stone-100 bg-stone-50/30 text-stone-700 icon-bg-stone-100 icon-stone-600 hover-border-stone-300",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    icon,
                    class_name=rx.cond(
                        stage == "fresher",
                        "h-5 w-5 text-emerald-600",
                        rx.cond(
                            stage == "early_career",
                            "h-5 w-5 text-blue-600",
                            "h-5 w-5 text-amber-600",
                        ),
                    ),
                ),
                class_name=rx.cond(
                    stage == "fresher",
                    "h-9 w-9 rounded-2xl bg-emerald-50 flex items-center justify-center border border-emerald-100",
                    rx.cond(
                        stage == "early_career",
                        "h-9 w-9 rounded-2xl bg-blue-50 flex items-center justify-center border border-blue-100",
                        "h-9 w-9 rounded-2xl bg-amber-50 flex items-center justify-center border border-amber-100",
                    ),
                ),
            ),
            rx.el.span(
                badge,
                class_name=rx.cond(
                    stage == "fresher",
                    "text-[11px] font-semibold text-emerald-800 bg-emerald-50 border border-emerald-100/80 px-2.5 py-1 rounded-full w-fit",
                    rx.cond(
                        stage == "early_career",
                        "text-[11px] font-semibold text-blue-800 bg-blue-50 border border-blue-100/80 px-2.5 py-1 rounded-full w-fit",
                        "text-[11px] font-semibold text-amber-800 bg-amber-50 border border-amber-100/80 px-2.5 py-1 rounded-full w-fit",
                    ),
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.h3(
            title, class_name="text-base font-semibold text-stone-900 mb-2"
        ),
        rx.el.p(desc, class_name="text-xs text-stone-600 leading-relaxed mb-5"),
        rx.el.button(
            "Get started",
            rx.icon(
                "arrow-right",
                class_name=rx.cond(
                    stage == "fresher",
                    "h-3.5 w-3.5 ml-1.5 text-emerald-700",
                    rx.cond(
                        stage == "early_career",
                        "h-3.5 w-3.5 ml-1.5 text-blue-700",
                        "h-3.5 w-3.5 ml-1.5 text-amber-700",
                    ),
                ),
            ),
            on_click=lambda: AppState.go_to_register(stage),
            class_name=rx.cond(
                stage == "fresher",
                "flex items-center text-xs font-semibold text-emerald-700 hover:text-emerald-800 transition-colors",
                rx.cond(
                    stage == "early_career",
                    "flex items-center text-xs font-semibold text-blue-700 hover:text-blue-800 transition-colors",
                    "flex items-center text-xs font-semibold text-amber-700 hover:text-amber-800 transition-colors",
                ),
            ),
        ),
        class_name=rx.cond(
            stage == "fresher",
            "bg-white rounded-3xl border border-stone-200/60 p-6 hover:border-emerald-300 hover:shadow-md transition-all duration-300",
            rx.cond(
                stage == "early_career",
                "bg-white rounded-3xl border border-stone-200/60 p-6 hover:border-blue-300 hover:shadow-md transition-all duration-300",
                "bg-white rounded-3xl border border-stone-200/60 p-6 hover:border-amber-300 hover:shadow-md transition-all duration-300",
            ),
        ),
    )


def stat(value: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            value,
            class_name="text-2xl sm:text-3xl font-extrabold text-stone-900 bg-gradient-to-r from-blue-700 via-indigo-600 to-rose-600 bg-clip-text text-transparent",
        ),
        rx.el.p(label, class_name="text-xs font-semibold text-stone-500 mt-1"),
    )


def landing() -> rx.Component:
    return rx.el.div(
        # Hero
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-3.5 w-3.5 text-blue-600"),
                    rx.el.span(
                        "Personalized 1:1 career guidance",
                        class_name="text-xs font-semibold text-stone-800",
                    ),
                    class_name="inline-flex items-center gap-1.5 bg-blue-50/80 border border-blue-100/60 px-3 py-1.5 rounded-full mb-6",
                ),
                rx.el.h1(
                    "Build a career you ",
                    rx.el.span(
                        "truly love.",
                        class_name="bg-gradient-to-r from-blue-600 via-indigo-600 to-rose-500 bg-clip-text text-transparent",
                    ),
                    class_name="text-4xl sm:text-5xl md:text-6xl font-extrabold text-stone-900 tracking-tight leading-tight",
                ),
                rx.el.p(
                    "Get clarity on your next move with trusted, expert counsellors. Whether you are stepping into the workforce, growing fast, or pivoting to a new domain — we help you map out the path ahead.",
                    class_name="text-sm sm:text-base text-stone-600 mt-6 max-w-2xl mx-auto leading-relaxed",
                ),
                rx.el.div(
                    rx.el.button(
                        "Get started",
                        rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                        on_click=lambda: AppState.go_to_register(""),
                        class_name="flex items-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl hover:shadow-lg hover:shadow-blue-100 active:scale-95 transition-all font-semibold",
                    ),
                    rx.el.button(
                        rx.icon("log-in", class_name="h-4 w-4 mr-2"),
                        "Sign in",
                        on_click=AppState.go_to_login,
                        class_name="flex items-center text-stone-700 px-6 py-3 rounded-xl hover:bg-stone-50 transition-all font-semibold border border-stone-200/80 bg-white",
                    ),
                    class_name="flex flex-col sm:flex-row gap-3 justify-center mt-8",
                ),
                rx.cond(
                    AppState.has_saved_account,
                    rx.el.div(
                        rx.icon(
                            "hard-drive",
                            class_name="h-3.5 w-3.5 text-blue-600",
                        ),
                        rx.el.span(
                            "We found saved details from a previous session on this device.",
                            class_name="text-xs font-medium text-stone-700 ml-1.5",
                        ),
                        rx.el.button(
                            "Sign in",
                            on_click=AppState.go_to_login,
                            class_name="text-xs font-bold text-blue-700 hover:text-blue-900 ml-2 underline underline-offset-2",
                        ),
                        class_name="inline-flex items-center bg-blue-50/50 border border-blue-100/60 px-3.5 py-2 rounded-2xl mt-5 shadow-sm",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    stat("12,000+", "Sessions completed"),
                    rx.el.div(
                        class_name="h-8 w-px bg-stone-200 hidden sm:block"
                    ),
                    stat("4.9 / 5", "Average rating"),
                    rx.el.div(
                        class_name="h-8 w-px bg-stone-200 hidden sm:block"
                    ),
                    stat("85%", "Career clarity gained"),
                    class_name="flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 mt-12 pt-8 border-t border-stone-200/60",
                ),
                class_name="text-center max-w-4xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-12 sm:py-20",
        ),
        # Audience
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Who we help",
                        class_name="text-2xl sm:text-3xl font-semibold text-stone-900",
                    ),
                    rx.el.p(
                        "Tailored counselling for every stage of your career journey.",
                        class_name="text-sm text-stone-600 mt-2",
                    ),
                    class_name="text-center mb-10",
                ),
                rx.el.div(
                    audience_card(
                        "graduation-cap",
                        "Freshers & Students",
                        "Just stepping into the workforce? Discover roles that match your strengths and build a launch plan that works.",
                        "Starting out",
                        "fresher",
                    ),
                    audience_card(
                        "trending-up",
                        "Early-Career Pros",
                        "1–5 years in? Get strategic guidance on growth, skill gaps, and how to land the next big opportunity.",
                        "Growing",
                        "early_career",
                    ),
                    audience_card(
                        "shuffle",
                        "Role Switchers",
                        "Ready for a pivot? Map a clear, confident transition into a new domain or industry — without starting over.",
                        "Pivoting",
                        "switcher",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-12",
        ),
        # How it works
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "How it works",
                        class_name="text-2xl sm:text-3xl font-semibold text-stone-900",
                    ),
                    rx.el.p(
                        "Three simple steps to clarity.",
                        class_name="text-sm text-stone-600 mt-2",
                    ),
                    class_name="text-center mb-10",
                ),
                rx.el.div(
                    feature_card(
                        "user-plus",
                        "1. Register",
                        "Tell us a bit about yourself and where you are in your career — takes under a minute.",
                    ),
                    feature_card(
                        "clipboard-list",
                        "2. Share your goals",
                        "Complete a guided intake so your counsellor understands your background, aspirations, and challenges.",
                    ),
                    feature_card(
                        "calendar-check",
                        "3. Book your session",
                        "Pick a time that works for you and meet your counsellor 1:1 for actionable, personalized advice.",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="max-w-6xl mx-auto",
                id="how",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-12 bg-stone-50/40 border-y border-stone-200/60",
        ),
        # CTA
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Your next chapter starts here.",
                        class_name="text-2xl sm:text-3xl font-semibold text-stone-900",
                    ),
                    rx.el.p(
                        "Join thousands who found direction with our counsellors.",
                        class_name="text-sm text-stone-600 mt-2 mb-6",
                    ),
                    rx.el.button(
                        "Register now — it's free",
                        rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                        on_click=lambda: AppState.go_to_register(""),
                        class_name="inline-flex items-center bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-all font-semibold shadow-sm",
                    ),
                    class_name="text-center bg-white border border-stone-200/60 rounded-3xl p-8 sm:p-12",
                ),
                class_name="max-w-4xl mx-auto",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-12",
        ),
        class_name="w-full",
    )