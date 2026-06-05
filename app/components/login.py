import reflex as rx
from app.states.app_state import AppState
from app.components.storage_status import storage_inline_notice


def field_label(text: str, required: bool = True) -> rx.Component:
    return rx.el.label(
        text,
        rx.cond(
            required, rx.el.span(" *", class_name="text-red-500"), rx.fragment()
        ),
        class_name="block text-sm font-semibold text-gray-700 mb-1.5",
    )


def error_text(msg) -> rx.Component:
    return rx.cond(
        msg != "",
        rx.el.p(
            rx.icon("circle-alert", class_name="h-3.5 w-3.5 mr-1 inline"),
            msg,
            class_name="text-xs text-red-600 mt-1.5 flex items-center",
        ),
        rx.fragment(),
    )


def login() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back",
                on_click=AppState.go_to_landing,
                class_name="flex items-center text-sm font-medium text-stone-600 hover:text-stone-900 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("log-in", class_name="h-5 w-5 text-blue-600"),
                    class_name="h-11 w-11 rounded-xl bg-gradient-to-tr from-blue-50 to-indigo-50 border border-blue-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Welcome back",
                    class_name="text-2xl sm:text-3xl font-bold text-stone-900",
                ),
                rx.el.p(
                    "Sign in to continue your counselling journey. We'll pick up right where you left off.",
                    class_name="text-sm text-stone-600 mt-2",
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
                            class_name="w-full px-4 py-2.5 bg-white border border-stone-300 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 placeholder-stone-400/80 text-sm",
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
                            class_name="w-full px-4 py-2.5 bg-white border border-stone-300 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 placeholder-stone-400/80 text-sm",
                        ),
                        rx.el.p(
                            "Adds an extra check against the phone you registered with.",
                            class_name="text-xs text-gray-500 mt-1.5",
                        ),
                        error_text(AppState.login_phone_error),
                        class_name="mb-5",
                    ),
                    rx.cond(
                        AppState.login_general_error != "",
                        rx.el.div(
                            rx.icon(
                                "circle-alert",
                                class_name="h-4 w-4 text-red-600 shrink-0",
                            ),
                            rx.el.p(
                                AppState.login_general_error,
                                class_name="text-xs text-red-700 ml-2",
                            ),
                            class_name="flex items-start p-3 bg-red-50 border border-red-200 rounded-xl mb-5",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.button(
                        "Sign in",
                        rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                        type="submit",
                        class_name="w-full flex items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-[0.99] text-white px-6 py-3 rounded-xl transition-all duration-200 font-semibold shadow-sm hover:shadow-md focus:ring-2 focus:ring-blue-500/20 focus:outline-none",
                    ),
                    on_submit=AppState.submit_login,
                    reset_on_submit=False,
                ),
                rx.el.div(
                    rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                    rx.el.span(
                        "or",
                        class_name="text-xs text-gray-500 px-3",
                    ),
                    rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                    class_name="flex items-center my-5",
                ),
                rx.el.button(
                    rx.icon("user-plus", class_name="h-4 w-4 mr-2"),
                    "Create a new account",
                    type="button",
                    on_click=lambda: AppState.go_to_register(""),
                    class_name="w-full flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-stone-700 bg-white border border-stone-300 rounded-xl hover:bg-stone-50 hover:border-stone-400 active:scale-[0.99] transition-all duration-200 focus:ring-2 focus:ring-stone-500/10 focus:outline-none",
                ),
                rx.el.p(
                    rx.icon(
                        "shield-check",
                        class_name="h-3.5 w-3.5 mr-1 inline text-gray-400",
                    ),
                    "Saved locally on this device. We don't store anything on a server.",
                    class_name="text-xs text-gray-500 mt-4 text-center flex items-center justify-center",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8",
            ),
            class_name="max-w-xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-12 flex justify-center",
    )