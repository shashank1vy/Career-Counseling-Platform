import reflex as rx
from app.states.app_state import AppState
from app.states.analytics_state import AnalyticsState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.landing import landing
from app.components.registration import registration
from app.components.login import login
from app.components.intake import intake_placeholder
from app.components.review import review
from app.components.booking import booking_placeholder
from app.components.storage_status import storage_status_banner


# Best-effort browser lifecycle beacon. Uses `navigator.sendBeacon` against a
# tiny, no-credential public endpoint so the analytics layer can still observe
# unload approximations server-side via Firebase heartbeats. The script is
# completely invisible (no UI), wrapped in try/catch, and falls back to a
# no-op if the browser doesn't support the API.
_LIFECYCLE_SCRIPT = """
(function() {
  try {
    if (window.__pathwiseLifecycleHooked) return;
    window.__pathwiseLifecycleHooked = true;
    var openedAt = Date.now();
    window.__pathwiseOpenedAt = openedAt;
    function markClose(reason) {
      try {
        var key = 'pathwise_last_close_ms';
        var payload = JSON.stringify({
          reason: reason,
          at: Date.now(),
          duration_ms: Date.now() - openedAt
        });
        try { localStorage.setItem(key, payload); } catch (e) {}
      } catch (e) {}
    }
    window.addEventListener('beforeunload', function() { markClose('beforeunload'); });
    window.addEventListener('pagehide', function() { markClose('pagehide'); });
    document.addEventListener('visibilitychange', function() {
      if (document.visibilityState === 'hidden') { markClose('hidden'); }
    });
  } catch (e) {}
})();
"""


def index() -> rx.Component:
    return rx.el.main(
        rx.script(_LIFECYCLE_SCRIPT),
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
    stylesheets=["/styles.css"],
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
app.add_page(index, route="/", on_load=AnalyticsState.on_app_open)