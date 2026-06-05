import reflex as rx
from app.states.app_state import AppState
from app.components.storage_status import storage_inline_notice


SESSION_TYPES = [
    {
        "value": "discovery",
        "title": "Discovery Session",
        "duration": "30 min",
        "price": "Free",
        "icon": "compass",
        "desc": "A focused conversation to map your goals, surface blockers, and outline a clear next step.",
        "best_for": "First-time bookings",
    },
    {
        "value": "deep_dive",
        "title": "Deep Dive Session",
        "duration": "60 min",
        "price": "$79",
        "icon": "telescope",
        "desc": "An in-depth strategy session covering career mapping, skill gaps, and a 90-day action plan.",
        "best_for": "Serious planning",
    },
    {
        "value": "mock_interview",
        "title": "Mock Interview",
        "duration": "45 min",
        "price": "$59",
        "icon": "messages-square",
        "desc": "A realistic interview simulation with detailed feedback on content, structure, and delivery.",
        "best_for": "Active job seekers",
    },
    {
        "value": "resume_clinic",
        "title": "Resume Clinic",
        "duration": "45 min",
        "price": "$49",
        "icon": "file-text",
        "desc": "Live, line-by-line review of your resume with concrete rewrites and ATS-ready formatting.",
        "best_for": "Resume polish",
    },
]


PREP_CHECKLIST = [
    ("circle-user", "Be in a quiet, distraction-free space"),
    ("video", "Test your camera and microphone in advance"),
    (
        "notebook-pen",
        "Have a notebook ready — you'll get a lot of action items",
    ),
    ("link", "Keep your LinkedIn profile open for reference"),
    ("file-text", "Review your uploaded resume one more time"),
    ("target", "Bring 1–2 specific questions you want answered"),
]


def session_card(s: dict) -> rx.Component:
    selected = AppState.session_type == s["value"]
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    s["icon"],
                    class_name=rx.cond(
                        selected,
                        "h-4 w-4 text-blue-600",
                        "h-4 w-4 text-stone-600",
                    ),
                ),
                class_name=rx.cond(
                    selected,
                    "h-9 w-9 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                    "h-9 w-9 rounded-xl bg-stone-50 border border-stone-200 flex items-center justify-center shrink-0",
                ),
            ),
            rx.cond(
                selected,
                rx.el.div(
                    rx.icon("check", class_name="h-3 w-3 text-white"),
                    class_name="h-5 w-5 rounded-full bg-blue-600 flex items-center justify-center shadow-sm",
                ),
                rx.el.div(
                    class_name="h-5 w-5 rounded-full border border-stone-300",
                ),
            ),
            class_name="flex items-center justify-between mb-3",
        ),
        rx.el.div(
            rx.el.h3(
                s["title"],
                class_name="text-xs font-semibold text-stone-900",
            ),
            rx.el.div(
                rx.el.span(
                    s["duration"],
                    class_name="text-[11px] font-medium text-stone-600",
                ),
                rx.el.span("•", class_name="text-[11px] text-stone-400 mx-1"),
                rx.el.span(
                    s["price"],
                    class_name="text-[11px] font-semibold text-blue-700",
                ),
                class_name="flex items-center mt-0.5",
            ),
            rx.el.p(
                s["desc"],
                class_name="text-[11px] text-stone-600 mt-2 leading-relaxed",
            ),
            rx.el.div(
                rx.icon("sparkle", class_name="h-3 w-3 mr-1"),
                s["best_for"],
                class_name=rx.cond(
                    selected,
                    "inline-flex items-center text-[10px] font-semibold text-blue-800 bg-blue-50 border border-blue-100 px-2.5 py-0.5 rounded-full mt-3 w-fit",
                    "inline-flex items-center text-[10px] font-semibold text-stone-700 bg-stone-100 border border-stone-200 px-2.5 py-0.5 rounded-full mt-3 w-fit",
                ),
            ),
            class_name="text-left",
        ),
        type="button",
        on_click=lambda: AppState.select_session_type(s["value"]),
        class_name=rx.cond(
            selected,
            "block w-full text-left p-4 rounded-2xl border-2 border-blue-600 bg-gradient-to-b from-blue-50/50 to-blue-50/10 shadow-md transition-all duration-200 ring-2 ring-blue-500/10 scale-[1.01]",
            "block w-full text-left p-4 rounded-2xl border border-stone-200 bg-white hover:border-blue-300 hover:bg-stone-50/30 active:scale-[0.99] transition-all duration-200",
        ),
    )


def prep_item(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(item[0], class_name="h-4 w-4 text-blue-600"),
            class_name="h-8 w-8 rounded-lg bg-blue-50 flex items-center justify-center shrink-0",
        ),
        rx.el.span(item[1], class_name="text-sm text-gray-700 ml-3"),
        class_name="flex items-center py-2",
    )


def context_summary() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user-check", class_name="h-4 w-4 text-stone-600"),
                rx.el.h3(
                    "Your session context",
                    class_name="text-sm font-semibold text-stone-900 ml-2",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.icon("pencil", class_name="h-3.5 w-3.5 mr-1"),
                "Edit",
                type="button",
                on_click=AppState.edit_intake,
                class_name="flex items-center text-xs font-semibold text-stone-600 hover:text-stone-800",
            ),
            class_name="flex items-center justify-between mb-4 pb-3 border-b border-stone-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Counselling for",
                    class_name="text-[10px] font-semibold uppercase tracking-wide text-stone-500",
                ),
                rx.el.p(
                    AppState.full_name,
                    class_name="text-sm font-semibold text-stone-900 mt-1",
                ),
                rx.el.p(
                    AppState.email,
                    class_name="text-xs text-stone-600 mt-0.5",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Stage",
                    class_name="text-[10px] font-semibold uppercase tracking-wide text-stone-500",
                ),
                rx.el.p(
                    AppState.stage_label,
                    class_name="text-sm text-stone-900 mt-1",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Top focus areas",
                    class_name="text-[10px] font-semibold uppercase tracking-wide text-stone-500",
                ),
                rx.cond(
                    AppState.guidance_areas.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            AppState.guidance_areas,
                            lambda a: rx.el.span(
                                a,
                                class_name="text-[11px] font-semibold text-stone-700 bg-stone-100 border border-stone-200 px-2 py-0.5 rounded-full",
                            ),
                        ),
                        class_name="flex flex-wrap gap-1 mt-1",
                    ),
                    rx.el.p(
                        "General career guidance",
                        class_name="text-sm text-stone-500 italic mt-1",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Resume",
                    class_name="text-[10px] font-semibold uppercase tracking-wide text-stone-500",
                ),
                rx.cond(
                    AppState.resume_filename != "",
                    rx.el.div(
                        rx.icon(
                            "file-check",
                            class_name="h-4 w-4 text-stone-600 mr-1.5",
                        ),
                        rx.el.span(
                            "Attached",
                            class_name="text-sm font-medium text-stone-900",
                        ),
                        class_name="flex items-center mt-1",
                    ),
                    rx.el.p(
                        "Not uploaded",
                        class_name="text-sm text-stone-500 italic mt-1",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
        ),
        class_name="bg-white rounded-2xl border border-stone-200/80 p-5",
    )


def calendly_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="h-4 w-4 text-stone-600"),
                rx.el.h3(
                    "Pick a time that works for you",
                    class_name="text-sm font-semibold text-stone-900 ml-2",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon(
                    "shield-check", class_name="h-3.5 w-3.5 text-stone-500"
                ),
                rx.el.span(
                    "Powered by Calendly",
                    class_name="text-[11px] font-medium text-stone-500 ml-1",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-4 pb-3 border-b border-stone-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Selected:",
                    class_name="text-xs text-stone-500",
                ),
                rx.el.p(
                    AppState.session_label,
                    class_name="text-sm font-semibold text-stone-900 mt-0.5",
                ),
            ),
            rx.el.a(
                rx.icon("external-link", class_name="h-3.5 w-3.5 ml-1"),
                "Open in new tab",
                href=AppState.calendly_url,
                target="_blank",
                rel="noopener noreferrer",
                class_name="flex flex-row-reverse items-center text-xs font-semibold text-stone-600 hover:text-stone-800",
            ),
            class_name="flex items-center justify-between mb-4 p-3 bg-stone-50/50 border border-stone-150 rounded-xl",
        ),
        rx.el.iframe(
            src=AppState.calendly_url,
            title="Calendly booking calendar",
            class_name="w-full rounded-xl border border-stone-200/80 bg-white",
            style={"minWidth": "320px", "height": "720px"},
            custom_attrs={"frameborder": "0", "loading": "lazy"},
            key=AppState.calendly_url,
        ),
        rx.el.p(
            rx.icon(
                "info", class_name="h-3.5 w-3.5 mr-1 inline text-stone-400"
            ),
            "Don't see your timezone? The calendar adapts automatically.",
            class_name="text-xs text-stone-500 mt-3 flex items-center",
        ),
        class_name="bg-white rounded-2xl border border-stone-200/80 p-5",
    )


def booking_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back to review",
                on_click=AppState.go_to_review,
                class_name="flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "calendar-check", class_name="h-5 w-5 text-blue-600"
                    ),
                    class_name="h-11 w-11 rounded-xl bg-blue-50 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Book your session, ",
                    AppState.first_name,
                    class_name="text-2xl sm:text-3xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Choose a session type, pick a time, and we'll meet you 1:1 with personalized guidance based on everything you've shared.",
                    class_name="text-sm text-gray-600 mt-2 max-w-2xl",
                ),
                class_name="mb-8",
            ),
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            # Layout grid
            rx.el.div(
                # Left: main flow
                rx.el.div(
                    # Session type
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "layers",
                                    class_name="h-4 w-4 text-stone-700",
                                ),
                                rx.el.h3(
                                    "Choose a session type",
                                    class_name="text-sm font-semibold text-stone-900 ml-2",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.span(
                                rx.el.span(
                                    "Step 1 of 2",
                                    class_name="text-[11px] font-semibold text-stone-700",
                                ),
                                class_name="bg-stone-100 px-2 py-0.5 rounded-full",
                            ),
                            class_name="flex items-center justify-between mb-4 pb-3 border-b border-stone-100",
                        ),
                        rx.el.div(
                            rx.foreach(SESSION_TYPES, session_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                        ),
                        class_name="bg-white rounded-2xl border border-stone-200/80 p-5",
                    ),
                    rx.el.div(class_name="h-5"),
                    calendly_section(),
                    rx.el.div(class_name="h-5"),
                    # Confirmation CTA
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "circle-check",
                                    class_name="h-5 w-5 text-stone-700",
                                ),
                                class_name="h-10 w-10 rounded-xl bg-stone-100 flex items-center justify-center shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Already picked a slot?",
                                    class_name="text-sm font-semibold text-stone-900",
                                ),
                                rx.el.p(
                                    "Tap below once your booking is confirmed in Calendly. We'll send you everything you need to prepare.",
                                    class_name="text-xs text-stone-600 mt-0.5",
                                ),
                                class_name="ml-3 flex-1",
                            ),
                            class_name="flex items-start mb-4",
                        ),
                        rx.el.button(
                            rx.icon("check", class_name="h-4 w-4 mr-2"),
                            "I've booked my session",
                            type="button",
                            on_click=AppState.confirm_booking,
                            class_name="w-full flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-[0.99] rounded-xl transition-all duration-200 shadow-sm hover:shadow-md focus:ring-2 focus:ring-blue-500/20 focus:outline-none",
                        ),
                        class_name="bg-white rounded-2xl border border-stone-200/80 p-5",
                    ),
                    class_name="lg:col-span-2",
                ),
                # Right: sidebar
                rx.el.div(
                    context_summary(),
                    rx.el.div(class_name="h-5"),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "list-checks",
                                class_name="h-4 w-4 text-stone-700",
                            ),
                            rx.el.h3(
                                "How to prepare",
                                class_name="text-sm font-semibold text-stone-900 ml-2",
                            ),
                            class_name="flex items-center mb-3 pb-3 border-b border-stone-100",
                        ),
                        rx.el.ul(
                            rx.foreach(PREP_CHECKLIST, prep_item),
                            class_name="divide-y divide-stone-100",
                        ),
                        class_name="bg-white rounded-2xl border border-stone-200/80 p-5",
                    ),
                    rx.el.div(class_name="h-5"),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "life-buoy",
                                class_name="h-4 w-4 text-blue-600",
                            ),
                            rx.el.h3(
                                "Need help?",
                                class_name="text-sm font-semibold text-gray-900 ml-2",
                            ),
                            class_name="flex items-center mb-3",
                        ),
                        rx.el.p(
                            "Trouble finding a time, or need to reschedule? We're here.",
                            class_name="text-xs text-gray-600 mb-3",
                        ),
                        rx.el.a(
                            rx.icon("mail", class_name="h-3.5 w-3.5 mr-1.5"),
                            "support@pathwise.app",
                            href="mailto:support@pathwise.app",
                            class_name="flex items-center text-xs font-semibold text-blue-600 hover:text-blue-700",
                        ),
                        class_name="bg-blue-50/40 rounded-2xl border border-blue-100 p-5",
                    ),
                    class_name="",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-5 items-start",
            ),
            class_name="max-w-6xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-10 flex justify-center",
    )


def confirmation_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("check", class_name="h-7 w-7 text-white"),
                    class_name="h-14 w-14 rounded-full bg-green-500 flex items-center justify-center mx-auto mb-5 ring-8 ring-green-50",
                ),
                rx.el.h1(
                    "You're booked!",
                    class_name="text-3xl sm:text-4xl font-bold text-gray-900 text-center",
                ),
                rx.el.p(
                    "Nice work, ",
                    AppState.first_name,
                    " — a calendar invite is on its way to ",
                    rx.el.span(
                        AppState.email,
                        class_name="font-semibold text-gray-900",
                    ),
                    ".",
                    class_name="text-sm sm:text-base text-gray-600 text-center mt-3 max-w-xl mx-auto",
                ),
                class_name="mb-8",
            ),
            # Session summary card
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "calendar-check",
                            class_name="h-4 w-4 text-blue-600",
                        ),
                        rx.el.span(
                            "Confirmed session",
                            class_name="text-[11px] font-semibold uppercase tracking-wide text-blue-700 ml-1.5",
                        ),
                        class_name="flex items-center mb-3",
                    ),
                    rx.el.h2(
                        AppState.session_label,
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "1:1 video session with a Pathwise career counsellor.",
                        class_name="text-sm text-gray-600 mt-1",
                    ),
                    class_name="mb-5 pb-5 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Booked for",
                            class_name="text-[10px] font-semibold uppercase tracking-wide text-gray-500",
                        ),
                        rx.el.p(
                            AppState.full_name,
                            class_name="text-sm font-semibold text-gray-900 mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Confirmation sent to",
                            class_name="text-[10px] font-semibold uppercase tracking-wide text-gray-500",
                        ),
                        rx.el.p(
                            AppState.email,
                            class_name="text-sm text-gray-900 mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Stage",
                            class_name="text-[10px] font-semibold uppercase tracking-wide text-gray-500",
                        ),
                        rx.el.p(
                            AppState.stage_label,
                            class_name="text-sm text-gray-900 mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Phone",
                            class_name="text-[10px] font-semibold uppercase tracking-wide text-gray-500",
                        ),
                        rx.el.p(
                            AppState.phone,
                            class_name="text-sm text-gray-900 mt-1",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 p-6 mb-5",
            ),
            # Next steps
            rx.el.div(
                rx.el.div(
                    rx.icon("rocket", class_name="h-4 w-4 text-blue-600"),
                    rx.el.h3(
                        "What's next",
                        class_name="text-sm font-semibold text-gray-900 ml-2",
                    ),
                    class_name="flex items-center mb-4 pb-3 border-b border-gray-100",
                ),
                rx.el.ol(
                    rx.el.li(
                        rx.el.div(
                            "1",
                            class_name="h-6 w-6 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Check your inbox",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "We've sent a calendar invite with the video link. Add it to your calendar so you don't miss it.",
                                class_name="text-xs text-gray-600 mt-0.5",
                            ),
                            class_name="ml-3",
                        ),
                        class_name="flex items-start py-3",
                    ),
                    rx.el.li(
                        rx.el.div(
                            "2",
                            class_name="h-6 w-6 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Get matched with a counsellor",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "Within 24 hours, we'll match you with a counsellor who specializes in your goals and stage.",
                                class_name="text-xs text-gray-600 mt-0.5",
                            ),
                            class_name="ml-3",
                        ),
                        class_name="flex items-start py-3 border-t border-gray-100",
                    ),
                    rx.el.li(
                        rx.el.div(
                            "3",
                            class_name="h-6 w-6 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Show up prepared",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "Review your goals, have your questions ready, and join from a quiet space 5 minutes early.",
                                class_name="text-xs text-gray-600 mt-0.5",
                            ),
                            class_name="ml-3",
                        ),
                        class_name="flex items-start py-3 border-t border-gray-100",
                    ),
                    rx.el.li(
                        rx.el.div(
                            "4",
                            class_name="h-6 w-6 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Walk away with a plan",
                                class_name="text-sm font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                "After the session, you'll receive a written summary with action items and recommended resources.",
                                class_name="text-xs text-gray-600 mt-0.5",
                            ),
                            class_name="ml-3",
                        ),
                        class_name="flex items-start py-3 border-t border-gray-100",
                    ),
                    class_name="",
                ),
                class_name="bg-white rounded-2xl border border-gray-200 p-6 mb-5",
            ),
            # Support / actions
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "life-buoy",
                            class_name="h-5 w-5 text-blue-600",
                        ),
                        class_name="h-10 w-10 rounded-xl bg-blue-50 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Need to reschedule or have questions?",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Use the link in your confirmation email to reschedule, or reach our team anytime.",
                            class_name="text-xs text-gray-600 mt-0.5",
                        ),
                        class_name="ml-3 flex-1",
                    ),
                    class_name="flex items-start mb-4",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.icon("mail", class_name="h-4 w-4 mr-2"),
                        "Email support",
                        href="mailto:support@pathwise.app",
                        class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition-all",
                    ),
                    rx.el.a(
                        rx.icon("message-circle", class_name="h-4 w-4 mr-2"),
                        "Help center",
                        href="#",
                        class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition-all",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                ),
                class_name="bg-blue-50/40 rounded-2xl border border-blue-100 p-5 mb-5",
            ),
            # Storage notice
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            # Bottom actions
            rx.el.div(
                rx.el.button(
                    rx.icon("home", class_name="h-4 w-4 mr-2"),
                    "Back to home",
                    on_click=AppState.restart_journey,
                    class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-stone-700 bg-white border border-stone-300 rounded-xl hover:bg-stone-50 hover:border-stone-400 active:scale-[0.99] transition-all duration-200 focus:ring-2 focus:ring-stone-500/10 focus:outline-none",
                ),
                rx.el.a(
                    rx.icon("share-2", class_name="h-4 w-4 mr-2"),
                    "Tell a friend",
                    href="mailto:?subject=Check%20out%20Pathwise&body=I%20just%20booked%20a%20career%20counselling%20session%20with%20Pathwise%20—%20you%20might%20like%20it%20too%3A%20https%3A%2F%2Fpathwise.app",
                    class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 active:scale-[0.99] rounded-xl transition-all duration-200 shadow-sm hover:shadow-md focus:ring-2 focus:ring-blue-500/20 focus:outline-none",
                ),
                class_name="flex flex-col sm:flex-row gap-3",
            ),
            class_name="max-w-2xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-12 flex justify-center",
    )


def booking_placeholder() -> rx.Component:
    return rx.cond(
        AppState.booking_confirmed,
        confirmation_view(),
        booking_view(),
    )