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


def login() -> rx.Component:
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
                        "RETURNING LEARNER",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.icon("log-in", class_name="h-5 w-5 text-indigo-900"),
                    class_name="h-11 w-11 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Welcome back",
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Sign in to continue your counselling journey. We'll pick up exactly where you left off.",
                    class_name="text-sm text-slate-600 mt-2",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    storage_inline_notice(),
                    class_name="mb-5",
                ),
                rx.el.form(
                    rx.el.div(
                        field_label("Email"),
                        rx.el.input(
                            name="login_email",
                            type="email",
                            placeholder="you@example.com",
                            default_value=AppState.login_email,
                            class_name=INPUT_CLS,
                        ),
                        error_text(AppState.login_email_error),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        field_label("Phone number", required=False),
                        rx.el.input(
                            name="login_phone",
                            type="tel",
                            placeholder="Optional — last 7 digits to verify",
                            default_value=AppState.login_phone,
                            class_name=INPUT_CLS,
                        ),
                        rx.el.p(
                            "Adds an extra check against the phone you registered with.",
                            class_name="text-xs text-slate-500 mt-1.5",
                        ),
                        error_text(AppState.login_phone_error),
                        class_name="mb-5",
                    ),
                    rx.cond(
                        AppState.login_general_error != "",
                        rx.el.div(
                            rx.icon(
                                "circle-alert",
                                class_name="h-4 w-4 text-rose-700 shrink-0 mt-0.5",
                            ),
                            rx.el.p(
                                AppState.login_general_error,
                                class_name="text-xs text-rose-800 ml-2 font-medium",
                            ),
                            class_name="flex items-start p-3.5 bg-rose-50/70 border border-rose-200 rounded-xl mb-5",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.button(
                        rx.icon("log-in", class_name="h-4 w-4 mr-2"),
                        "Sign in",
                        rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                        type="submit",
                        class_name="w-full flex items-center justify-center bg-indigo-900 hover:bg-indigo-950 active:scale-[0.99] text-white px-6 py-3 rounded-xl transition-all duration-200 font-semibold shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
                    ),
                    on_submit=AppState.submit_login,
                    reset_on_submit=False,
                ),
                rx.el.div(
                    rx.el.div(class_name="flex-1 h-px bg-slate-200"),
                    rx.el.span(
                        "or",
                        class_name="text-xs text-slate-500 px-3 font-medium",
                    ),
                    rx.el.div(class_name="flex-1 h-px bg-slate-200"),
                    class_name="flex items-center my-5",
                ),
                rx.el.button(
                    rx.icon("user-plus", class_name="h-4 w-4 mr-2"),
                    "Create a new account",
                    type="button",
                    on_click=lambda: AppState.go_to_register(""),
                    class_name="w-full flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-indigo-300 hover:text-indigo-900 active:scale-[0.99] transition-all duration-200 focus:ring-2 focus:ring-indigo-300/30 focus:outline-none",
                ),
                rx.el.p(
                    rx.icon(
                        "shield-check",
                        class_name="h-3.5 w-3.5 mr-1 inline text-emerald-700",
                    ),
                    "Saved privately on this device. Cloud sync activates only with secure backend.",
                    class_name="text-xs text-slate-500 mt-4 text-center flex items-center justify-center",
                ),
                class_name="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-sm",
            ),
            class_name="max-w-xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-12 flex justify-center",
    )