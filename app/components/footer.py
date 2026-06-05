import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("compass", class_name="h-4 w-4 text-indigo-500"),
                    rx.el.span(
                        "Pathwise",
                        class_name="text-sm font-extrabold text-stone-900 tracking-tight bg-gradient-to-r from-indigo-600 to-rose-500 bg-clip-text text-transparent",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "© 2025 Pathwise Career Counselling. Muted multi-accent styling with soft cloud persistence.",
                    class_name="text-xs text-stone-500 font-medium",
                ),
                class_name="flex flex-col sm:flex-row items-center justify-between gap-3",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6",
        ),
        class_name="bg-white/90 border-t border-stone-200/60 mt-auto",
    )