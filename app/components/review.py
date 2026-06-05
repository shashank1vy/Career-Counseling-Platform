import reflex as rx
from app.states.app_state import AppState
from app.components.storage_status import storage_inline_notice


def info_row(label: str, value) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
        ),
        rx.cond(
            value != "",
            rx.el.p(
                value, class_name="text-sm text-slate-900 mt-1 font-medium"
            ),
            rx.el.p(
                "Not provided",
                class_name="text-sm text-slate-400 italic mt-1",
            ),
        ),
        class_name="py-3",
    )


def chips(items) -> rx.Component:
    return rx.cond(
        items.length() > 0,
        rx.el.div(
            rx.foreach(
                items,
                lambda v: rx.el.span(
                    v,
                    class_name="text-xs font-semibold text-indigo-900 bg-indigo-50 border border-indigo-100/80 px-2.5 py-1 rounded-full",
                ),
            ),
            class_name="flex flex-wrap gap-1.5 mt-1",
        ),
        rx.el.p("None added", class_name="text-sm text-slate-400 italic mt-1"),
    )


def card(
    title: str, icon: str, body: rx.Component, action_icon: str = "pencil"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(icon, class_name="h-3.5 w-3.5 text-indigo-900"),
                    class_name="h-7 w-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center",
                ),
                rx.el.h3(
                    title,
                    class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.icon(action_icon, class_name="h-3.5 w-3.5 mr-1"),
                "Edit",
                type="button",
                on_click=AppState.edit_intake,
                class_name="flex items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
            ),
            class_name="flex items-center justify-between mb-3 pb-3 border-b border-slate-100",
        ),
        body,
        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm hover:border-indigo-200 transition-colors",
    )


def review() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back to intake",
                on_click=AppState.edit_intake,
                class_name="flex items-center text-sm font-semibold text-slate-600 hover:text-indigo-900 mb-6 transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "MODULE 03 • REVIEW",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.icon(
                        "circle-check-big",
                        class_name="h-5 w-5 text-emerald-700",
                    ),
                    class_name="h-11 w-11 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Review your counselling brief",
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "This is the picture your counsellor will see going into your session. Edit any section before booking.",
                    class_name="text-sm text-slate-600 mt-2 max-w-2xl",
                ),
                class_name="mb-6",
            ),
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            rx.el.div(
                # Account
                card(
                    "Account",
                    "user",
                    rx.el.div(
                        info_row("Full name", AppState.full_name),
                        info_row("Email", AppState.email),
                        info_row("Phone", AppState.phone),
                        info_row("Career stage", AppState.stage_label),
                        class_name="divide-y divide-gray-100",
                    ),
                ),
                # Background
                card(
                    "Background",
                    "briefcase",
                    rx.el.div(
                        info_row("Current role", AppState.current_role),
                        info_row("Experience", AppState.experience_level),
                        info_row("Education", AppState.education_level),
                        info_row("Institution", AppState.institution),
                        info_row("Field of study", AppState.field_of_study),
                        class_name="divide-y divide-gray-100",
                    ),
                ),
                # Skills & interests
                card(
                    "Skills & interests",
                    "sparkles",
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Skills",
                                class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                            ),
                            chips(AppState.skills_list),
                            class_name="py-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Interests",
                                class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                            ),
                            chips(AppState.interests_list),
                            class_name="py-3",
                        ),
                        class_name="divide-y divide-slate-100",
                    ),
                ),
                # Goals
                card(
                    "Goals & challenges",
                    "target",
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Target roles",
                                class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                            ),
                            chips(AppState.target_roles_list),
                            class_name="py-3",
                        ),
                        info_row("Biggest challenges", AppState.challenges),
                        info_row("Career objective", AppState.career_objective),
                        class_name="divide-y divide-slate-100",
                    ),
                ),
                # Guidance areas
                card(
                    "Preferred guidance",
                    "compass",
                    rx.cond(
                        AppState.guidance_areas.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                AppState.guidance_areas,
                                lambda a: rx.el.span(
                                    a,
                                    class_name="text-xs font-semibold text-indigo-900 bg-indigo-50 border border-indigo-100/80 px-2.5 py-1 rounded-full",
                                ),
                            ),
                            class_name="flex flex-wrap gap-1.5 pt-1",
                        ),
                        rx.el.p(
                            "No areas selected",
                            class_name="text-sm text-slate-400 italic",
                        ),
                    ),
                ),
                # Resume
                card(
                    "Resume",
                    "file-text",
                    rx.cond(
                        AppState.resume_filename != "",
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "file-check",
                                    class_name="h-4 w-4 text-emerald-700",
                                ),
                                class_name="h-9 w-9 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    AppState.resume_filename,
                                    class_name="text-sm font-semibold text-slate-900 truncate",
                                ),
                                rx.el.p(
                                    AppState.resume_size_label,
                                    class_name="text-xs text-slate-500",
                                ),
                                class_name="ml-3 flex-1 min-w-0",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.icon(
                                "file-x",
                                class_name="h-8 w-8 text-slate-300 mb-2",
                            ),
                            rx.el.p(
                                "No resume uploaded — that's okay, you can still book.",
                                class_name="text-xs text-slate-500 text-center",
                            ),
                            class_name="flex flex-col items-center justify-center py-4",
                        ),
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            # Completion banner
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle-check",
                        class_name="h-5 w-5 text-emerald-700 shrink-0",
                    ),
                    class_name="h-10 w-10 rounded-xl bg-white border border-emerald-200 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "Intake complete",
                        class_name="text-sm font-bold text-slate-900",
                    ),
                    rx.el.p(
                        "You're all set to book your 1:1 counselling session.",
                        class_name="text-xs text-slate-600 mt-0.5",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center gap-1 mt-6 p-4 bg-emerald-50/50 border border-emerald-200/70 rounded-2xl",
            ),
            # Actions
            rx.el.div(
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-4 w-4 mr-1.5"),
                    "Reset all",
                    type="button",
                    on_click=AppState.reset_intake,
                    class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all focus:ring-2 focus:ring-slate-300/30 focus:outline-none",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4 mr-1.5"),
                    "Edit intake",
                    type="button",
                    on_click=AppState.edit_intake,
                    class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-indigo-300 hover:text-indigo-900 transition-all focus:ring-2 focus:ring-indigo-300/30 focus:outline-none",
                ),
                rx.el.button(
                    rx.icon("calendar-check", class_name="h-4 w-4 mr-2"),
                    "Continue to booking",
                    rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                    type="button",
                    on_click=AppState.confirm_and_book,
                    class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-indigo-900 rounded-xl hover:bg-indigo-950 active:scale-[0.99] transition-all shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
                ),
                class_name="flex flex-col sm:flex-row gap-3 mt-5",
            ),
            class_name="max-w-4xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-10 flex justify-center",
    )