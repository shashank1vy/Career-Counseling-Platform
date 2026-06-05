import reflex as rx
from app.states.app_state import AppState
from app.components.storage_status import storage_inline_notice


INPUT_CLS = (
    "w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl "
    "hover:border-indigo-300 focus:ring-2 focus:ring-indigo-900/15 "
    "focus:border-indigo-700 outline-none transition-all duration-200 "
    "text-slate-900 placeholder-slate-400 text-sm shadow-sm"
)


def field_label(text: str, required: bool = True) -> rx.Component:
    return rx.el.label(
        text,
        rx.cond(
            required,
            rx.el.span(" *", class_name="text-rose-600"),
            rx.fragment(),
        ),
        class_name="block text-sm font-semibold text-slate-800 mb-1.5 tracking-tight",
    )


def error_text(msg) -> rx.Component:
    return rx.cond(
        msg != "",
        rx.el.p(
            rx.icon("circle-alert", class_name="h-3.5 w-3.5 mr-1 inline"),
            msg,
            class_name="text-xs text-rose-700 mt-1.5 flex items-center font-medium",
        ),
        rx.fragment(),
    )


def perk_pill(icon: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-3.5 w-3.5 text-indigo-900"),
        rx.el.span(
            text,
            class_name="text-[11px] font-semibold text-slate-700 ml-1.5 tracking-tight",
        ),
        class_name="inline-flex items-center bg-white border border-slate-200/80 px-2.5 py-1 rounded-full",
    )


def registration() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back to home",
                on_click=AppState.go_to_landing,
                class_name="flex items-center text-sm font-semibold text-slate-600 hover:text-indigo-900 mb-6 transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "MODULE 01 • REGISTRATION",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.icon("user-plus", class_name="h-5 w-5 text-indigo-900"),
                    class_name="h-11 w-11 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Create your Pathwise account",
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Just a few details so we can match you with the right counsellor and tailor your curriculum.",
                    class_name="text-sm text-slate-600 mt-2 max-w-xl",
                ),
                rx.el.div(
                    perk_pill("clock", "Under 60 seconds"),
                    perk_pill("shield-check", "Private to your device"),
                    perk_pill("graduation-cap", "Vetted counsellors"),
                    class_name="flex flex-wrap gap-2 mt-4",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                storage_inline_notice(),
                class_name="mb-5",
            ),
            rx.el.form(
                rx.el.div(
                    field_label("Full name"),
                    rx.el.input(
                        name="full_name",
                        type="text",
                        placeholder="e.g. Priya Sharma",
                        default_value=AppState.full_name,
                        class_name=INPUT_CLS,
                    ),
                    error_text(AppState.name_error),
                    class_name="mb-5",
                ),
                rx.el.div(
                    field_label("Email"),
                    rx.el.input(
                        name="email",
                        type="email",
                        placeholder="you@example.com",
                        default_value=AppState.email,
                        class_name=INPUT_CLS,
                    ),
                    rx.el.p(
                        "We'll send your session details and prep notes here.",
                        class_name="text-xs text-slate-500 mt-1.5",
                    ),
                    error_text(AppState.email_error),
                    class_name="mb-5",
                ),
                rx.el.div(
                    field_label("Phone number"),
                    rx.el.input(
                        name="phone",
                        type="tel",
                        placeholder="+1 555 123 4567",
                        default_value=AppState.phone,
                        class_name=INPUT_CLS,
                    ),
                    error_text(AppState.phone_error),
                    class_name="mb-5",
                ),
                rx.el.div(
                    field_label("Where are you in your career?"),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                "Select your stage…",
                                value="default",
                                disabled=True,
                            ),
                            rx.el.option("Fresher / Student", value="fresher"),
                            rx.el.option(
                                "Early-career professional (1–5 yrs)",
                                value="early_career",
                            ),
                            rx.el.option(
                                "Mid-career switcher", value="switcher"
                            ),
                            rx.el.option("Senior professional", value="senior"),
                            name="career_stage",
                            default_value=rx.cond(
                                AppState.career_stage != "",
                                AppState.career_stage,
                                "default",
                            ),
                            key=AppState.career_stage,
                            on_change=AppState.set_stage,
                            class_name="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl hover:border-indigo-300 focus:ring-2 focus:ring-indigo-900/15 focus:border-indigo-700 outline-none transition-all duration-200 text-slate-900 placeholder-slate-400 text-sm shadow-sm appearance-none cursor-pointer pr-10",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    rx.el.p(
                        "We'll route you to the matching counselling track.",
                        class_name="text-xs text-slate-500 mt-1.5",
                    ),
                    error_text(AppState.stage_error),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="agree",
                            required=True,
                            class_name="h-4 w-4 text-indigo-900 border-slate-300 rounded focus:ring-indigo-700 mt-0.5 mr-2.5",
                        ),
                        rx.el.span(
                            "I agree to Pathwise's terms of service and privacy policy.",
                            class_name="text-xs text-slate-600 leading-relaxed",
                        ),
                        class_name="flex items-start cursor-pointer",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    rx.icon("graduation-cap", class_name="h-4 w-4 mr-2"),
                    "Continue to intake",
                    rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                    type="submit",
                    class_name="w-full flex items-center justify-center bg-indigo-900 hover:bg-indigo-950 active:scale-[0.99] text-white px-6 py-3 rounded-xl transition-all duration-200 font-semibold shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
                ),
                rx.el.p(
                    rx.icon(
                        "shield-check",
                        class_name="h-3.5 w-3.5 mr-1 inline text-emerald-700",
                    ),
                    "Your information stays private and is saved on this device.",
                    class_name="text-xs text-slate-500 mt-4 text-center flex items-center justify-center",
                ),
                on_submit=AppState.submit_registration,
                reset_on_submit=False,
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account?",
                    class_name="text-xs text-slate-600",
                ),
                rx.el.button(
                    "Sign in",
                    type="button",
                    on_click=AppState.go_to_login,
                    class_name="text-xs font-bold text-indigo-900 hover:text-indigo-950 ml-1.5 underline underline-offset-2",
                ),
                class_name="text-center mt-5 pt-5 border-t border-slate-100",
            ),
            class_name="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 max-w-xl w-full shadow-sm",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-12 flex justify-center",
    )