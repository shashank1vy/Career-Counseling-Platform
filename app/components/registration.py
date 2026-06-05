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


def registration() -> rx.Component:
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
                    rx.icon("user-plus", class_name="h-5 w-5 text-blue-600"),
                    class_name="h-11 w-11 rounded-xl bg-gradient-to-tr from-blue-50 to-indigo-50 border border-blue-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Create your account",
                    class_name="text-2xl sm:text-3xl font-bold text-stone-900",
                ),
                rx.el.p(
                    "Just a few details to get you matched with the right counsellor.",
                    class_name="text-sm text-stone-600 mt-2",
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
                        class_name="w-full px-4 py-2.5 bg-white border border-stone-250 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 placeholder-stone-400 text-sm",
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
                        class_name="w-full px-4 py-2.5 bg-white border border-stone-200 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 placeholder-stone-400 text-sm",
                    ),
                    rx.el.p(
                        "We'll send your session details here.",
                        class_name="text-xs text-stone-500 mt-1.5",
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
                        class_name="w-full px-4 py-2.5 bg-white border border-stone-200 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 placeholder-stone-400 text-sm",
                    ),
                    error_text(AppState.phone_error),
                    class_name="mb-5",
                ),
                rx.el.div(
                    field_label("Where are you in your career?"),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                "Select an option",
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
                            class_name="w-full px-4 py-2.5 bg-white border border-stone-200 rounded-xl hover:border-stone-400 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all duration-200 text-stone-900 text-sm appearance-none cursor-pointer pr-10",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-stone-500 pointer-events-none hover:text-stone-700 transition-colors",
                        ),
                        class_name="relative",
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
                            class_name="h-4 w-4 text-blue-600 border-stone-300 rounded focus:ring-blue-500 mt-0.5 mr-2.5",
                        ),
                        rx.el.span(
                            "I agree to the terms of service and privacy policy.",
                            class_name="text-xs text-stone-600 leading-relaxed",
                        ),
                        class_name="flex items-start cursor-pointer",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Continue to intake",
                    rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                    type="submit",
                    class_name="w-full flex items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-[0.99] text-white px-6 py-3 rounded-xl transition-all duration-200 font-semibold shadow-sm hover:shadow-md focus:ring-2 focus:ring-blue-500/20 focus:outline-none",
                ),
                rx.el.p(
                    rx.icon(
                        "shield-check",
                        class_name="h-3.5 w-3.5 mr-1 inline text-stone-400",
                    ),
                    "Your information is private and secure.",
                    class_name="text-xs text-stone-500 mt-4 text-center flex items-center justify-center",
                ),
                on_submit=AppState.submit_registration,
                reset_on_submit=False,
            ),
            class_name="bg-white rounded-2xl border border-stone-200/80 p-6 sm:p-8 max-w-xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-12 flex justify-center",
    )