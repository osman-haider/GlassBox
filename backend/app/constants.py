"""
Benchmark constants used for GlassBox recovery estimates.

These reflect SmartRecover's own publicly stated, aggregate,
cross-partner benchmarks (an ~50%+ SMS reply rate and an ~23%
average lift in checkout/quiz/intake conversion). They are used
here purely as illustrative assumptions to produce a directional
estimate — every number derived from them must be presented as an
estimate, not a guarantee, since actual results vary by funnel.
"""

# "Expected" case: SmartRecover's published aggregate averages.
EXPECTED_REPLY_RATE = 0.50
EXPECTED_CVR_LIFT = 0.23

# "Conservative" case: a deliberately lower assumption, so the estimate
# is shown as a believable range rather than a single optimistic number.
CONSERVATIVE_REPLY_RATE = 0.35
CONSERVATIVE_CVR_LIFT = 0.12

# A brand with no current follow-up has more upside from adding a human
# SMS layer; a brand already running automated SMS recovery has less
# incremental room left to capture.
FOLLOW_UP_METHOD_MULTIPLIER = {
    "none": 1.15,
    "email_only": 1.0,
    "automated_sms": 0.85,
}

FUNNEL_STAGE_LABELS = {
    "checkout": "Checkout abandonment",
    "quiz": "Quiz abandonment",
    "intake": "Intake form abandonment",
}
