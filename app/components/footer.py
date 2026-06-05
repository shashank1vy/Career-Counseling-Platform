import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "graduation-cap",
                        class_name="h-4 w-4 text-indigo-900",
                    ),
                    rx.el.span(
                        "Pathwise Advisory",
                        class_name="text-sm font-bold text-slate-900 tracking-tight",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "© 2025 Pathwise Academy. Scholarly & professional development advisory. Muted local persistence.",
                    class_name="text-xs text-slate-500 font-medium",
                ),
                class_name="flex flex-col sm:flex-row items-center justify-between gap-3",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6",
        ),
        class_name="bg-white/95 border-t border-slate-200/80 mt-auto",
    )