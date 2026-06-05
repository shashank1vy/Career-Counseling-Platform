import reflex as rx
from app.states.backend_state import BackendState


def storage_status_banner() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                BackendState.backend_ready,
                rx.el.div(
                    rx.icon(
                        "cloud-check",
                        class_name="h-4 w-4 text-emerald-600 shrink-0",
                    ),
                    class_name="h-9 w-9 rounded-2xl bg-emerald-50 flex items-center justify-center shrink-0 border border-emerald-100",
                ),
                rx.el.div(
                    rx.icon(
                        "hard-drive",
                        class_name="h-4 w-4 text-amber-600 shrink-0",
                    ),
                    class_name="h-9 w-9 rounded-2xl bg-amber-50 flex items-center justify-center shrink-0 border border-amber-100",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        BackendState.storage_mode_label,
                        class_name="text-sm font-semibold text-stone-900",
                    ),
                    rx.cond(
                        BackendState.backend_ready,
                        rx.el.span(
                            rx.icon(
                                "shield-check",
                                class_name="h-3 w-3 mr-1",
                            ),
                            "Synced",
                            class_name="inline-flex items-center text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200/60 px-2.5 py-0.5 rounded-full ml-2",
                        ),
                        rx.el.span(
                            rx.icon(
                                "circle-dashed",
                                class_name="h-3 w-3 mr-1",
                            ),
                            "Local fallback",
                            class_name="inline-flex items-center text-[10px] font-bold text-amber-700 bg-amber-50 border border-amber-200/60 px-2.5 py-0.5 rounded-full ml-2",
                        ),
                    ),
                    class_name="flex items-center flex-wrap",
                ),
                rx.el.p(
                    BackendState.storage_mode_description,
                    class_name="text-xs text-stone-600 mt-1 leading-relaxed",
                ),
                class_name="ml-3 flex-1 min-w-0",
            ),
            class_name="flex items-start",
        ),
        class_name=rx.cond(
            BackendState.backend_ready,
            "bg-white border-l-4 border-l-emerald-500 border-stone-200/80 rounded-3xl p-5 shadow-sm",
            "bg-white border-l-4 border-l-amber-500 border-stone-200/80 rounded-3xl p-5 shadow-sm",
        ),
        role="status",
        aria_live="polite",
    )


def storage_inline_notice() -> rx.Component:
    return rx.el.div(
        rx.cond(
            BackendState.backend_ready,
            rx.icon(
                "cloud-check",
                class_name="h-4 w-4 text-emerald-600 shrink-0",
            ),
            rx.icon(
                "hard-drive",
                class_name="h-4 w-4 text-amber-600 shrink-0",
            ),
        ),
        rx.el.p(
            BackendState.storage_inline_notice,
            class_name="text-xs ml-2 leading-relaxed font-semibold",
        ),
        class_name=rx.cond(
            BackendState.backend_ready,
            "flex items-start p-3.5 bg-emerald-50/50 border border-emerald-100 rounded-2xl text-emerald-800 shadow-sm",
            "flex items-start p-3.5 bg-amber-50/50 border border-amber-100 rounded-2xl text-amber-800 shadow-sm",
        ),
        role="status",
        aria_live="polite",
    )