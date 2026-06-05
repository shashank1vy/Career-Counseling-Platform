import reflex as rx
from app.states.app_state import AppState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.landing import landing
from app.components.registration import registration
from app.components.login import login
from app.components.intake import intake_placeholder
from app.components.review import review
from app.components.booking import booking_placeholder
from app.components.storage_status import storage_status_banner


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                storage_status_banner(),
                class_name="max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6",
            ),
            rx.match(
                AppState.current_step,
                ("landing", landing()),
                ("register", registration()),
                ("login", login()),
                ("intake", intake_placeholder()),
                ("review", review()),
                ("booking", booking_placeholder()),
                ("done", booking_placeholder()),
                landing(),
            ),
            class_name="flex-1",
        ),
        footer(),
        class_name="font-['Inter'] bg-slate-50/70 min-h-screen flex flex-col text-slate-800 antialiased selection:bg-indigo-100/80",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")