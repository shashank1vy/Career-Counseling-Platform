import reflex as rx
from app.states.app_state import AppState
from app.components.storage_status import storage_inline_notice


COUNSELLING_PATH = [
    {
        "stage": "01",
        "value": "discovery",
        "title": "Discovery Session",
        "duration": "30 min",
        "availability": "Free",
        "availability_kind": "free",
        "icon": "compass",
        "desc": "A focused conversation to map your goals, surface blockers, and outline a clear next step.",
        "best_for": "Your starting point",
        "state": "current",
    },
    {
        "stage": "02",
        "value": "deep_dive",
        "title": "Deep Dive Session",
        "duration": "60 min",
        "availability": "Paid",
        "availability_kind": "paid",
        "icon": "telescope",
        "desc": "An in-depth strategy session covering career mapping, skill gaps, and a 90-day action plan.",
        "best_for": "After Discovery",
        "state": "upcoming",
    },
    {
        "stage": "03",
        "value": "mock_interview",
        "title": "Mock Interview",
        "duration": "45 min",
        "availability": "Paid",
        "availability_kind": "paid",
        "icon": "messages-square",
        "desc": "A realistic interview simulation with detailed feedback on content, structure, and delivery.",
        "best_for": "Once you're interviewing",
        "state": "upcoming",
    },
    {
        "stage": "04",
        "value": "resume_clinic",
        "title": "Resume Clinic",
        "duration": "45 min",
        "availability": "Paid",
        "availability_kind": "paid",
        "icon": "file-text",
        "desc": "Live, line-by-line review of your resume with concrete rewrites and ATS-ready formatting.",
        "best_for": "Polish before applying",
        "state": "upcoming",
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


def availability_pill(s: dict) -> rx.Component:
    is_free = s["availability_kind"] == "free"
    return rx.cond(
        is_free,
        rx.el.span(
            rx.icon("gift", class_name="h-3 w-3 mr-1"),
            s["availability"],
            class_name="inline-flex items-center text-[10px] font-bold text-emerald-800 bg-emerald-50 border border-emerald-200/70 px-2 py-0.5 rounded-full",
        ),
        rx.el.span(
            rx.icon("lock", class_name="h-3 w-3 mr-1"),
            s["availability"],
            class_name="inline-flex items-center text-[10px] font-bold text-amber-800 bg-amber-50 border border-amber-200/70 px-2 py-0.5 rounded-full",
        ),
    )


def current_session_card(s: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"STAGE {s['stage']}",
                    class_name="text-[9px] font-bold uppercase tracking-widest text-indigo-700",
                ),
                rx.el.span(
                    "•",
                    class_name="text-[10px] text-slate-400 mx-1.5",
                ),
                rx.el.span(
                    "Currently active",
                    class_name="text-[10px] font-bold uppercase tracking-wider text-emerald-700",
                ),
                class_name="flex items-center mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        s["icon"],
                        class_name="h-4 w-4 text-indigo-900",
                    ),
                    class_name="h-9 w-9 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.icon("check", class_name="h-3 w-3 text-white"),
                    class_name="h-5 w-5 rounded-full bg-indigo-900 flex items-center justify-center shadow-sm",
                ),
                class_name="flex items-center justify-between mb-3",
            ),
            rx.el.h3(
                s["title"],
                class_name="text-sm font-bold text-slate-900 tracking-tight",
            ),
            rx.el.div(
                rx.el.span(
                    s["duration"],
                    class_name="text-[11px] font-semibold text-slate-600",
                ),
                rx.el.span("•", class_name="text-[11px] text-slate-400 mx-1"),
                availability_pill(s),
                class_name="flex items-center mt-1 gap-1",
            ),
            rx.el.p(
                s["desc"],
                class_name="text-[11px] text-slate-600 mt-2 leading-relaxed",
            ),
            rx.el.div(
                rx.icon("sparkle", class_name="h-3 w-3 mr-1"),
                s["best_for"],
                class_name="inline-flex items-center text-[10px] font-bold text-indigo-800 bg-indigo-50 border border-indigo-100 px-2.5 py-0.5 rounded-full mt-3 w-fit",
            ),
        ),
        class_name="block w-full text-left p-4 rounded-2xl border-2 border-indigo-900 bg-indigo-50/30 shadow-md shadow-indigo-100 ring-2 ring-indigo-200/40 transition-academic animate-pulse-gentle relative",
        aria_current="step",
    )


def upcoming_session_card(s: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                f"STAGE {s['stage']}",
                class_name="text-[9px] font-bold uppercase tracking-widest text-slate-500",
            ),
            rx.el.span(
                "•",
                class_name="text-[10px] text-slate-300 mx-1.5",
            ),
            rx.el.span(
                "Upcoming",
                class_name="text-[10px] font-bold uppercase tracking-wider text-slate-500",
            ),
            class_name="flex items-center mb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    s["icon"],
                    class_name="h-4 w-4 text-slate-500",
                ),
                class_name="h-9 w-9 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.icon("lock", class_name="h-3 w-3 text-slate-400"),
                class_name="h-5 w-5 rounded-full bg-white border border-slate-200 flex items-center justify-center",
            ),
            class_name="flex items-center justify-between mb-3",
        ),
        rx.el.h3(
            s["title"],
            class_name="text-sm font-bold text-slate-700 tracking-tight",
        ),
        rx.el.div(
            rx.el.span(
                s["duration"],
                class_name="text-[11px] font-semibold text-slate-500",
            ),
            rx.el.span("•", class_name="text-[11px] text-slate-300 mx-1"),
            availability_pill(s),
            class_name="flex items-center mt-1 gap-1",
        ),
        rx.el.p(
            s["desc"],
            class_name="text-[11px] text-slate-500 mt-2 leading-relaxed",
        ),
        rx.el.div(
            rx.icon("sparkle", class_name="h-3 w-3 mr-1"),
            s["best_for"],
            class_name="inline-flex items-center text-[10px] font-semibold text-slate-600 bg-slate-100 border border-slate-200 px-2.5 py-0.5 rounded-full mt-3 w-fit",
        ),
        class_name="block w-full text-left p-4 rounded-2xl border border-dashed border-slate-300 bg-slate-50/60 opacity-90 cursor-not-allowed select-none transition-academic",
        aria_disabled="true",
    )


def session_card(s: dict) -> rx.Component:
    return rx.cond(
        s["state"] == "current",
        current_session_card(s),
        upcoming_session_card(s),
    )


def prep_item(item: tuple[str, str]) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(item[0], class_name="h-4 w-4 text-indigo-900"),
            class_name="h-8 w-8 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center shrink-0",
        ),
        rx.el.span(
            item[1],
            class_name="text-sm text-slate-700 ml-3 font-medium",
        ),
        class_name="flex items-center py-2",
    )


def context_summary() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "user-check",
                        class_name="h-3.5 w-3.5 text-indigo-900",
                    ),
                    class_name="h-7 w-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center",
                ),
                rx.el.h3(
                    "Your session context",
                    class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.icon("pencil", class_name="h-3.5 w-3.5 mr-1"),
                "Edit",
                type="button",
                on_click=AppState.edit_intake,
                class_name="flex items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
            ),
            class_name="flex items-center justify-between mb-4 pb-3 border-b border-slate-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Counselling for",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.el.p(
                    AppState.full_name,
                    class_name="text-sm font-semibold text-slate-900 mt-1",
                ),
                rx.el.p(
                    AppState.email,
                    class_name="text-xs text-slate-600 mt-0.5",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Stage",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.el.p(
                    AppState.stage_label,
                    class_name="text-sm text-slate-900 mt-1 font-medium",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Top focus areas",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.cond(
                    AppState.guidance_areas.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            AppState.guidance_areas,
                            lambda a: rx.el.span(
                                a,
                                class_name="text-[11px] font-semibold text-indigo-900 bg-indigo-50 border border-indigo-100/80 px-2 py-0.5 rounded-full",
                            ),
                        ),
                        class_name="flex flex-wrap gap-1 mt-1",
                    ),
                    rx.el.p(
                        "General career guidance",
                        class_name="text-sm text-slate-500 italic mt-1",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Resume",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.cond(
                    AppState.resume_filename != "",
                    rx.el.div(
                        rx.icon(
                            "file-check",
                            class_name="h-4 w-4 text-emerald-700 mr-1.5",
                        ),
                        rx.el.span(
                            "Attached",
                            class_name="text-sm font-semibold text-slate-900",
                        ),
                        class_name="flex items-center mt-1",
                    ),
                    rx.el.p(
                        "Not uploaded",
                        class_name="text-sm text-slate-500 italic mt-1",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
        ),
        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm",
    )


def calendly_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "calendar",
                        class_name="h-3.5 w-3.5 text-indigo-900",
                    ),
                    class_name="h-7 w-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center",
                ),
                rx.el.h3(
                    "Pick a time that works for you",
                    class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon(
                    "shield-check",
                    class_name="h-3.5 w-3.5 text-emerald-700",
                ),
                rx.el.span(
                    "Configured Event Active",
                    class_name="text-[11px] font-semibold text-slate-600 ml-1",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-4 pb-3 border-b border-slate-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Booking System Status:",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.el.p(
                    "Environment-verified official calendar integration",
                    class_name="text-sm font-semibold text-slate-900 mt-0.5",
                ),
            ),
            rx.el.a(
                rx.icon("external-link", class_name="h-3.5 w-3.5 ml-1"),
                "Open official calendar",
                href=AppState.calendly_url,
                target="_blank",
                rel="noopener noreferrer",
                class_name="flex flex-row-reverse items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
            ),
            class_name="flex items-center justify-between mb-4 p-3.5 bg-indigo-50/40 border border-indigo-100 rounded-xl",
        ),
        rx.el.iframe(
            src=AppState.calendly_url,
            title="Calendly booking calendar",
            class_name="w-full rounded-xl border border-slate-200/80 bg-white",
            style={"minWidth": "320px"},
            custom_attrs={"frameborder": "0", "loading": "lazy"},
            key=AppState.calendly_url,
        ),
        rx.el.p(
            rx.icon(
                "info",
                class_name="h-3.5 w-3.5 mr-1 inline text-slate-400",
            ),
            "Don't see your timezone? The calendar adapts automatically.",
            class_name="text-xs text-slate-500 mt-3 flex items-center",
        ),
        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm",
    )


def booking_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-1.5"),
                "Back to review",
                on_click=AppState.go_to_review,
                class_name="flex items-center text-sm font-semibold text-slate-600 hover:text-indigo-900 mb-6 transition-colors",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "STEP 04 • BOOKING",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.icon(
                        "calendar-check",
                        class_name="h-5 w-5 text-indigo-900",
                    ),
                    class_name="h-11 w-11 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mb-4",
                ),
                rx.el.h1(
                    "Book your session, ",
                    AppState.first_name,
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Choose a session type, pick a time, and we'll meet you 1:1 with personalized guidance based on everything you've shared.",
                    class_name="text-sm text-slate-600 mt-2 max-w-2xl",
                ),
                class_name="mb-8",
            ),
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            # Layout grid
            rx.el.div(
                # Left: main flow
                rx.el.div(
                    # Session type
                    # Counselling path
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "route",
                                        class_name="h-3.5 w-3.5 text-indigo-900",
                                    ),
                                    class_name="h-7 w-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center",
                                ),
                                rx.el.div(
                                    rx.el.h3(
                                        "Your counselling path",
                                        class_name="text-sm font-semibold text-slate-900 tracking-tight",
                                    ),
                                    rx.el.p(
                                        "Everyone begins with a free Discovery Session — advanced sessions unlock as your journey progresses.",
                                        class_name="text-[11px] text-slate-500 mt-0.5",
                                    ),
                                    class_name="ml-2",
                                ),
                                class_name="flex items-start",
                            ),
                            rx.el.span(
                                rx.el.span(
                                    "Stage 1 of 4",
                                    class_name="text-[11px] font-bold text-indigo-700",
                                ),
                                class_name="bg-indigo-50 border border-indigo-100/80 px-2.5 py-0.5 rounded-full shrink-0 ml-3",
                            ),
                            class_name="flex items-center justify-between mb-4 pb-3 border-b border-slate-100",
                        ),
                        rx.el.div(
                            rx.icon(
                                "info",
                                class_name="h-3.5 w-3.5 text-indigo-900 shrink-0 mt-0.5",
                            ),
                            rx.el.p(
                                "You're booking your ",
                                rx.el.span(
                                    "Discovery Session",
                                    class_name="font-bold text-slate-900",
                                ),
                                " — the free first stage of every Pathwise journey. Your counsellor will recommend the right next stage at the end of this session.",
                                class_name="text-xs text-slate-700 ml-2 leading-relaxed font-medium",
                            ),
                            class_name="flex items-start p-3 bg-indigo-50/50 border border-indigo-100 rounded-xl mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(COUNSELLING_PATH, session_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "lock",
                                    class_name="h-3 w-3 text-slate-400 mr-1.5",
                                ),
                                rx.el.span(
                                    "Locked stages",
                                    class_name="text-[10px] font-bold uppercase tracking-wider text-slate-500",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.span(
                                "Unlock after Discovery",
                                class_name="text-[10px] font-semibold text-slate-500",
                            ),
                            class_name="flex items-center justify-between mt-4 pt-3 border-t border-slate-100",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm",
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
                                    class_name="h-5 w-5 text-emerald-700",
                                ),
                                class_name="h-10 w-10 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Already picked a slot?",
                                    class_name="text-sm font-semibold text-slate-900",
                                ),
                                rx.el.p(
                                    "Tap below once your booking is confirmed in Calendly. We'll send you everything you need to prepare.",
                                    class_name="text-xs text-slate-600 mt-0.5",
                                ),
                                class_name="ml-3 flex-1",
                            ),
                            class_name="flex items-start mb-4",
                        ),
                        rx.el.button(
                            rx.icon(
                                "check",
                                class_name="h-4 w-4 mr-2",
                            ),
                            "I've booked my session",
                            type="button",
                            on_click=AppState.confirm_booking,
                            class_name="w-full flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-indigo-900 hover:bg-indigo-950 active:scale-[0.99] rounded-xl transition-all duration-200 shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm",
                    ),
                    class_name="lg:col-span-2",
                ),
                # Right: sidebar
                rx.el.div(
                    context_summary(),
                    rx.el.div(class_name="h-5"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "list-checks",
                                    class_name="h-3.5 w-3.5 text-amber-700",
                                ),
                                class_name="h-7 w-7 rounded-lg bg-amber-50 border border-amber-100 flex items-center justify-center",
                            ),
                            rx.el.h3(
                                "How to prepare",
                                class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                            ),
                            class_name="flex items-center mb-3 pb-3 border-b border-slate-100",
                        ),
                        rx.el.ul(
                            rx.foreach(PREP_CHECKLIST, prep_item),
                            class_name="divide-y divide-slate-100",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm",
                    ),
                    rx.el.div(class_name="h-5"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "life-buoy",
                                    class_name="h-3.5 w-3.5 text-indigo-900",
                                ),
                                class_name="h-7 w-7 rounded-lg bg-white border border-indigo-100 flex items-center justify-center",
                            ),
                            rx.el.h3(
                                "Need help?",
                                class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                            ),
                            class_name="flex items-center mb-3",
                        ),
                        rx.el.p(
                            "Trouble finding a time, or need to reschedule? We're here.",
                            class_name="text-xs text-slate-600 mb-3 leading-relaxed",
                        ),
                        rx.el.a(
                            rx.icon(
                                "mail",
                                class_name="h-3.5 w-3.5 mr-1.5",
                            ),
                            "support@pathwise.app",
                            href="mailto:support@pathwise.app",
                            class_name="flex items-center text-xs font-bold text-indigo-900 hover:text-indigo-950 transition-colors",
                        ),
                        class_name="bg-indigo-50/40 rounded-2xl border border-indigo-100 p-5",
                    ),
                    class_name="",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-5 items-start",
            ),
            class_name="max-w-6xl w-full",
        ),
        class_name="px-4 sm:px-6 lg:px-8 py-10 flex justify-center",
    )


def next_step_item(
    num: str, title: str, desc: str, is_first: bool
) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            num,
            class_name="h-7 w-7 rounded-full bg-indigo-900 text-white text-xs font-bold flex items-center justify-center shrink-0 shadow-sm",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-semibold text-slate-900 tracking-tight",
            ),
            rx.el.p(
                desc,
                class_name="text-xs text-slate-600 mt-0.5 leading-relaxed",
            ),
            class_name="ml-3",
        ),
        class_name=rx.cond(
            is_first,
            "flex items-start py-3",
            "flex items-start py-3 border-t border-slate-100",
        ),
    )


def confirmation_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("check", class_name="h-7 w-7 text-white"),
                    class_name="h-14 w-14 rounded-full bg-emerald-600 flex items-center justify-center mx-auto mb-5 ring-8 ring-emerald-50 shadow-lg shadow-emerald-100",
                ),
                rx.el.div(
                    rx.el.span(
                        "STEP 05 • CONFIRMED",
                        class_name="text-[11px] font-bold uppercase tracking-widest text-emerald-700",
                    ),
                    class_name="text-center mb-3",
                ),
                rx.el.h1(
                    "You're booked!",
                    class_name="text-3xl sm:text-4xl font-bold text-slate-900 text-center tracking-tight",
                ),
                rx.el.p(
                    "Nice work, ",
                    AppState.first_name,
                    " — a calendar invite is on its way to ",
                    rx.el.span(
                        AppState.email,
                        class_name="font-semibold text-slate-900",
                    ),
                    ".",
                    class_name="text-sm sm:text-base text-slate-600 text-center mt-3 max-w-xl mx-auto",
                ),
                class_name="mb-8",
            ),
            # Session summary card
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "calendar-check",
                            class_name="h-4 w-4 text-indigo-900",
                        ),
                        rx.el.span(
                            "Confirmed session",
                            class_name="text-[11px] font-bold uppercase tracking-widest text-indigo-700 ml-1.5",
                        ),
                        class_name="flex items-center mb-3",
                    ),
                    rx.el.h2(
                        AppState.session_label,
                        class_name="text-xl font-bold text-slate-900 tracking-tight",
                    ),
                    rx.el.p(
                        "1:1 video session with a Pathwise career counsellor.",
                        class_name="text-sm text-slate-600 mt-1",
                    ),
                    class_name="mb-5 pb-5 border-b border-slate-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Booked for",
                            class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                        ),
                        rx.el.p(
                            AppState.full_name,
                            class_name="text-sm font-semibold text-slate-900 mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Confirmation sent to",
                            class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                        ),
                        rx.el.p(
                            AppState.email,
                            class_name="text-sm text-slate-900 mt-1 font-medium",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Stage",
                            class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                        ),
                        rx.el.p(
                            AppState.stage_label,
                            class_name="text-sm text-slate-900 mt-1 font-medium",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Phone",
                            class_name="text-[10px] font-bold uppercase tracking-widest text-slate-500",
                        ),
                        rx.el.p(
                            AppState.phone,
                            class_name="text-sm text-slate-900 mt-1 font-medium",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
            ),
            # Next steps
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "rocket",
                            class_name="h-3.5 w-3.5 text-indigo-900",
                        ),
                        class_name="h-7 w-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center",
                    ),
                    rx.el.h3(
                        "What's next",
                        class_name="text-sm font-semibold text-slate-900 ml-2 tracking-tight",
                    ),
                    class_name="flex items-center mb-4 pb-3 border-b border-slate-100",
                ),
                rx.el.ol(
                    next_step_item(
                        "1",
                        "Check your inbox",
                        "We've sent a calendar invite with the video link. Add it to your calendar so you don't miss it.",
                        True,
                    ),
                    next_step_item(
                        "2",
                        "Get matched with a counsellor",
                        "Within 24 hours, we'll match you with a counsellor who specializes in your goals and stage.",
                        False,
                    ),
                    next_step_item(
                        "3",
                        "Show up prepared",
                        "Review your goals, have your questions ready, and join from a quiet space 5 minutes early.",
                        False,
                    ),
                    next_step_item(
                        "4",
                        "Walk away with a plan",
                        "After the session, you'll receive a written summary with action items and recommended resources.",
                        False,
                    ),
                ),
                class_name="bg-white rounded-2xl border border-slate-200/80 p-6 mb-5 shadow-sm",
            ),
            # Support / actions
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "life-buoy",
                            class_name="h-5 w-5 text-amber-700",
                        ),
                        class_name="h-10 w-10 rounded-xl bg-white border border-amber-200 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Need to reschedule or have questions?",
                            class_name="text-sm font-semibold text-slate-900 tracking-tight",
                        ),
                        rx.el.p(
                            "Use the link in your confirmation email to reschedule, or reach our team anytime.",
                            class_name="text-xs text-slate-600 mt-0.5 leading-relaxed",
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
                        class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-amber-300 transition-all",
                    ),
                    rx.el.a(
                        rx.icon("message-circle", class_name="h-4 w-4 mr-2"),
                        "Help center",
                        href="#",
                        class_name="flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-amber-300 transition-all",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                ),
                class_name="bg-amber-50/40 rounded-2xl border border-amber-200/70 p-5 mb-5",
            ),
            # Storage notice
            rx.el.div(storage_inline_notice(), class_name="mb-5"),
            # Bottom actions
            rx.el.div(
                rx.el.button(
                    rx.icon("home", class_name="h-4 w-4 mr-2"),
                    "Back to home",
                    on_click=AppState.restart_journey,
                    class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:border-slate-400 active:scale-[0.99] transition-all duration-200 focus:ring-2 focus:ring-slate-300/30 focus:outline-none",
                ),
                rx.el.a(
                    rx.icon("share-2", class_name="h-4 w-4 mr-2"),
                    "Tell a friend",
                    href="mailto:?subject=Check%20out%20Pathwise&body=I%20just%20booked%20a%20career%20counselling%20session%20with%20Pathwise%20—%20you%20might%20like%20it%20too%3A%20https%3A%2F%2Fpathwise.app",
                    class_name="flex-1 flex items-center justify-center px-4 py-3 text-sm font-semibold text-white bg-indigo-900 hover:bg-indigo-950 active:scale-[0.99] rounded-xl transition-all duration-200 shadow-sm hover:shadow-lg hover:shadow-indigo-100 focus:ring-2 focus:ring-indigo-300/50 focus:outline-none",
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