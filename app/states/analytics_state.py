"""Phase 1-3: Analytics state foundation.

Owns the per-browser anonymous session id, page/step duration tracking,
and app lifecycle (open/heartbeat) capture. Exposes a thin event wrapper
so other states/components can safely emit analytics events without
coupling to Firebase directly.

All analytics flows are best-effort and fully insulated from the user
experience: failures are logged and swallowed, and no analytics path can
block UI rendering, persistence, validation, navigation, or booking.
"""

import asyncio
import logging
import time

import reflex as rx

from app.states.analytics import log_event, new_session_id


class AnalyticsState(rx.State):
    # Anonymous, per-browser session identifier. Persisted to LocalStorage
    # so it survives reloads but is fully scoped to this browser. It is
    # NOT a credential, NOT tied to identity, and is safe to expose.
    session_id: str = rx.LocalStorage("", name="pathwise_analytics_sid")

    # Step/page duration tracking (server-side timestamps in epoch ms).
    current_step_name: str = ""
    step_started_at_ms: int = 0

    # App open lifecycle. app_open_logged_session_id is the session id we
    # already logged an open for, so reloads under the same browser session
    # don't re-fire app_opened needlessly within the same Reflex client.
    app_opened_at_ms: int = 0
    app_open_logged_session_id: str = ""

    # Heartbeat coordination so we never spawn duplicate background loops.
    heartbeat_running: bool = False

    @rx.event
    def ensure_session(self):
        """Lazily initialize the analytics session id on first interaction."""
        if not self.session_id:
            self.session_id = new_session_id()

    async def _build_user_context(
        self, allow_cross_state: bool = True
    ) -> tuple[str, dict]:
        """Returns (user_email, sanitized metadata) for the current user.

        Pulls journey context from AppState when available so events are
        meaningfully tagged regardless of identity. Never raises.

        When `allow_cross_state` is False (e.g. inside background lifecycle
        loops where we are not currently holding the state lock), this
        skips the cross-state fetch entirely and returns safe anonymous
        defaults to avoid Reflex `ImmutableStateError`.
        """
        if not allow_cross_state:
            return "", {"is_logged_in": False}
        try:
            from app.states.app_state import AppState

            app_state = await self.get_state(AppState)
            email = getattr(app_state, "current_user_email", "") or ""
            md: dict = {
                "is_logged_in": bool(email),
                "registered": bool(getattr(app_state, "registered", False)),
                "intake_submitted": bool(
                    getattr(app_state, "intake_submitted", False)
                ),
                "booking_confirmed": bool(
                    getattr(app_state, "booking_confirmed", False)
                ),
                "career_stage": getattr(app_state, "career_stage", "") or "",
                "has_resume": bool(
                    getattr(app_state, "resume_filename", "") or ""
                ),
            }
            return email, md
        except Exception as e:
            # Cross-state access is not always available (e.g. when called
            # from a background task outside an `async with self:` block).
            # That is an expected condition — fall back silently to safe
            # anonymous metadata. Only log truly unexpected failures.
            name = type(e).__name__
            if name not in {
                "ImmutableStateError",
                "StateNotFoundError",
                "RuntimeError",
            }:
                logging.exception(
                    "Pathwise analytics: failed to build user context"
                )
            return "", {"is_logged_in": False}

    @rx.event
    async def track(
        self,
        event_name: str,
        journey_step: str = "",
        metadata: dict | None = None,
    ):
        """Fire-and-forget analytics event. Never raises into the UI."""
        try:
            if not self.session_id:
                self.session_id = new_session_id()
            user_email, ctx_md = await self._build_user_context()
            md = dict(ctx_md)
            if metadata:
                # Caller-provided metadata wins for keys it explicitly sets.
                md.update(metadata)
            log_event(
                event_name,
                session_id=self.session_id,
                user_email=user_email,
                journey_step=journey_step,
                metadata=md,
            )
        except Exception:
            # Analytics must never break the user experience.
            logging.exception("Pathwise analytics: AnalyticsState.track failed")

    @rx.event
    async def on_app_open(self):
        """Fired from the page on_load. Logs an app_opened event once per
        Reflex client session and primes step duration tracking."""
        try:
            if not self.session_id:
                self.session_id = new_session_id()
            now_ms = int(time.time() * 1000)
            self.app_opened_at_ms = now_ms

            user_email, ctx_md = await self._build_user_context()

            if self.app_open_logged_session_id != self.session_id:
                self.app_open_logged_session_id = self.session_id
                md = dict(ctx_md)
                md.update({"page": "landing", "step": "landing"})
                log_event(
                    "app_opened",
                    session_id=self.session_id,
                    user_email=user_email,
                    journey_step="landing",
                    metadata=md,
                )
            else:
                # Reload within the same client session — log a softer event
                # so we can still see active sessions over time without
                # double-counting opens.
                md = dict(ctx_md)
                md.update({"page": "landing", "step": "landing"})
                log_event(
                    "app_reopened",
                    session_id=self.session_id,
                    user_email=user_email,
                    journey_step="landing",
                    metadata=md,
                )

            # Prime step tracking with the landing page so the first
            # transition produces a clean step_exit duration.
            if not self.current_step_name:
                self.current_step_name = "landing"
                self.step_started_at_ms = now_ms

            # Kick off the heartbeat loop (idempotent).
            if not self.heartbeat_running:
                return AnalyticsState.heartbeat_loop
        except Exception:
            logging.exception("Pathwise analytics: on_app_open failed")

    @rx.event
    async def enter_step(self, step_name: str):
        """Record exit duration of the previous step and entry of a new one.

        Called by AppState navigation handlers. Safe to call repeatedly with
        the same step name (no-op when nothing has changed).
        """
        try:
            if not step_name:
                return
            if not self.session_id:
                self.session_id = new_session_id()
            now_ms = int(time.time() * 1000)
            prev_step = self.current_step_name
            prev_start = self.step_started_at_ms

            user_email, ctx_md = await self._build_user_context()

            if prev_step and prev_step != step_name and prev_start > 0:
                duration_ms = max(0, now_ms - prev_start)
                duration_seconds = round(duration_ms / 1000.0, 2)
                exit_md = dict(ctx_md)
                exit_md.update(
                    {
                        "from_step": prev_step,
                        "to_step": step_name,
                        "duration_ms": int(duration_ms),
                        "duration_seconds": duration_seconds,
                        "page": prev_step,
                        "step": prev_step,
                    }
                )
                log_event(
                    "step_exit",
                    session_id=self.session_id,
                    user_email=user_email,
                    journey_step=prev_step,
                    metadata=exit_md,
                )

            if prev_step != step_name:
                entry_md = dict(ctx_md)
                entry_md.update(
                    {
                        "from_step": prev_step,
                        "to_step": step_name,
                        "page": step_name,
                        "step": step_name,
                    }
                )
                log_event(
                    "step_entry",
                    session_id=self.session_id,
                    user_email=user_email,
                    journey_step=step_name,
                    metadata=entry_md,
                )

            self.current_step_name = step_name
            self.step_started_at_ms = now_ms
        except Exception:
            logging.exception("Pathwise analytics: enter_step failed")

    @rx.event(background=True)
    async def heartbeat_loop(self):
        """Best-effort 'app still open' heartbeat. Persists a lightweight
        event approximately every 60 seconds with cumulative session
        duration. When the browser tab is closed the loop terminates with
        the connection — the last heartbeat acts as the implicit
        'app_close' approximation that browser lifecycle events allow.
        """
        try:
            async with self:
                if self.heartbeat_running:
                    return
                self.heartbeat_running = True
                start_session_id = self.session_id
                opened_at_ms = self.app_opened_at_ms or int(time.time() * 1000)
                if not self.app_opened_at_ms:
                    self.app_opened_at_ms = opened_at_ms

            heartbeats_emitted = 0
            try:
                while True:
                    await asyncio.sleep(60.0)
                    try:
                        # Read all state (including cross-state user
                        # context) while holding the state lock — this is
                        # the only safe way to call `get_state` from a
                        # background task without triggering
                        # ImmutableStateError.
                        async with self:
                            if (
                                not self.session_id
                                or self.session_id != start_session_id
                            ):
                                # Session id changed — stop this loop.
                                break
                            current_step = self.current_step_name or "landing"
                            session_id_local = self.session_id
                            opened_at_local = self.app_opened_at_ms
                            user_email, ctx_md = await self._build_user_context(
                                allow_cross_state=True
                            )
                        # Outside the lock: only do log/network work.
                        now_ms = int(time.time() * 1000)
                        elapsed_ms = max(0, now_ms - opened_at_local)
                        md = dict(ctx_md)
                        md.update(
                            {
                                "page": current_step,
                                "step": current_step,
                                "duration_ms": int(elapsed_ms),
                                "duration_seconds": round(
                                    elapsed_ms / 1000.0, 2
                                ),
                            }
                        )
                        log_event(
                            "app_heartbeat",
                            session_id=session_id_local,
                            user_email=user_email,
                            journey_step=current_step,
                            metadata=md,
                        )
                        heartbeats_emitted += 1
                    except Exception:
                        logging.exception(
                            "Pathwise analytics: heartbeat tick failed"
                        )
            finally:
                async with self:
                    self.heartbeat_running = False
        except Exception:
            logging.exception("Pathwise analytics: heartbeat_loop failed")
            try:
                async with self:
                    self.heartbeat_running = False
            except Exception:
                logging.exception(
                    "Pathwise analytics: heartbeat shutdown failed"
                )