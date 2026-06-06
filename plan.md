# User Activity Analytics Persistence Plan

## Phase 1: Analytics Data Capture Foundation ✅
- [x] Define user-based analytics events for app opens, page views, button interactions, login, and logout activity.
- [x] Add safe timestamping and session identification for activity events.
- [x] Persist analytics events to Firebase without storing credentials, secrets, or raw uploaded file contents.
- [x] Preserve the existing cookie draft flow, Firebase form sync, and fallback behavior.

## Phase 2: Login, Logout, and Journey Event Tracking ✅
- [x] Capture login timestamps, logout timestamps, and account identity context per user.
- [x] Track major journey transitions across registration, intake, review, booking, confirmation, and home views.
- [x] Track important CTA and form-action button interactions with clear event names.
- [x] Add graceful error handling so analytics failures never block the user experience.

## Phase 3: Page Duration and App Lifecycle Metrics ✅
- [x] Track time spent on each visible page or journey step per user/session.
- [x] Capture app open and close/exit timing where browser lifecycle events allow it.
- [x] Store aggregated and event-level metrics in Firebase for per-user analysis.
- [x] Keep the UI design unchanged while adding invisible analytics behavior.