import reflex as rx
from app.states.app_state import AppState


def step_indicator(label: str, step_key: str, num: int) -> rx.Component:
    is_active = AppState.current_step == step_key
    is_done = AppState.progress_percent >= (num * 25 + 25)
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_done,
                rx.icon(
                    "check",
                    class_name="h-3.5 w-3.5 text-white",
                ),
                rx.el.span(num, class_name="text-xs font-bold"),
            ),
            class_name=rx.cond(
                is_active,
                "h-7 w-7 rounded-full bg-indigo-900 text-white flex items-center justify-center ring-4 ring-indigo-100 transition-all duration-300 shadow-sm",
                rx.cond(
                    is_done,
                    "h-7 w-7 rounded-full bg-emerald-600 text-white flex items-center justify-center transition-all duration-300 shadow-sm",
                    "h-7 w-7 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center border border-slate-200 transition-all duration-300",
                ),
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active,
                "text-xs font-bold text-slate-900 ml-2 hidden sm:inline transition-colors",
                "text-xs font-semibold text-slate-500 ml-2 hidden sm:inline transition-colors",
            ),
        ),
        class_name="flex items-center",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "graduation-cap",
                        class_name="h-5 w-5 text-white",
                    ),
                    class_name="h-9 w-9 rounded-xl bg-indigo-900 flex items-center justify-center shadow-sm",
                ),
                rx.el.div(
                    rx.el.p(
                        "Pathwise",
                        class_name="text-sm font-extrabold text-slate-900 leading-none tracking-tight",
                    ),
                    rx.el.p(
                        "Academic & Career Consulting",
                        class_name="text-[9px] font-bold text-indigo-700 tracking-wider uppercase mt-0.5",
                    ),
                ),
                on_click=AppState.go_to_landing,
                class_name="flex items-center gap-2.5 cursor-pointer hover:opacity-90 transition-opacity",
            ),
            rx.cond(
                AppState.current_step != "landing",
                rx.el.div(
                    step_indicator("Register", "register", 1),
                    rx.el.div(
                        class_name="h-px w-6 sm:w-10 bg-slate-200 mx-1.5"
                    ),
                    step_indicator("Intake", "intake", 2),
                    rx.el.div(
                        class_name="h-px w-6 sm:w-10 bg-slate-200 mx-1.5"
                    ),
                    step_indicator("Booking", "booking", 3),
                    class_name="flex items-center",
                ),
                rx.cond(
                    AppState.is_logged_in,
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "circle-user",
                                class_name="h-4 w-4 text-emerald-700 mr-1.5",
                            ),
                            rx.el.span(
                                AppState.first_name,
                                class_name="text-sm font-semibold text-slate-800",
                            ),
                            class_name="hidden sm:flex items-center px-3 py-2 rounded-xl bg-emerald-50/80 border border-emerald-200/40",
                        ),
                        rx.el.button(
                            "Sign out",
                            on_click=AppState.logout,
                            class_name="text-sm font-semibold text-slate-700 hover:text-slate-900 px-4 py-2 rounded-xl hover:bg-slate-100 transition-all focus:outline-none focus:ring-2 focus:ring-slate-300/50",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Sign in",
                            on_click=AppState.go_to_login,
                            class_name="text-sm font-semibold text-slate-700 hover:text-slate-900 px-4 py-2 rounded-xl hover:bg-slate-100 transition-all focus:outline-none focus:ring-2 focus:ring-slate-300/50",
                        ),
                        rx.el.button(
                            "Get started",
                            on_click=lambda: AppState.go_to_register(""),
                            class_name="bg-indigo-900 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-indigo-950 active:scale-95 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-300/60 focus:ring-offset-1",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between",
        ),
        rx.cond(
            AppState.current_step != "landing",
            rx.el.div(
                rx.el.div(
                    class_name="h-full bg-gradient-to-r from-indigo-900 via-indigo-700 to-emerald-600 transition-all duration-500 ease-out",
                    style={"width": f"{AppState.progress_percent}%"},
                ),
                class_name="h-1 bg-slate-100 w-full",
            ),
            rx.fragment(),
        ),
        class_name="bg-white/95 backdrop-blur-sm border-b border-slate-200/80 sticky top-0 z-40",
    )