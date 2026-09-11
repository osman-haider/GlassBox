"""
Core recovery estimate logic.

Deliberately simple, transparent math — this is meant to be an
illustrative, directional estimate a prospect can sanity-check
themselves, not a black-box model.
"""

from .constants import (
    CONSERVATIVE_CVR_LIFT,
    CONSERVATIVE_REPLY_RATE,
    EXPECTED_CVR_LIFT,
    EXPECTED_REPLY_RATE,
    FOLLOW_UP_METHOD_MULTIPLIER,
)


def _recovered_leads(
    monthly_abandoned_leads: float,
    reply_rate: float,
    cvr_lift: float,
    follow_up_multiplier: float,
) -> float:
    """
    Estimate how many abandoned leads convert to a sale in a given month,
    given a reply rate and an incremental conversion lift.
    """
    engaged_leads = monthly_abandoned_leads * reply_rate
    recovered = engaged_leads * cvr_lift * follow_up_multiplier
    return max(recovered, 0.0)


def estimate_recovery(
    monthly_abandoned_leads: float,
    average_order_value: float,
    follow_up_method: str,
) -> dict:
    """
    Return a conservative-to-expected monthly recovery estimate.

    This is directional only, built from SmartRecover's own published
    aggregate benchmarks — not a guarantee for any specific brand.
    """
    follow_up_multiplier = FOLLOW_UP_METHOD_MULTIPLIER.get(follow_up_method, 1.0)

    conservative_leads = _recovered_leads(
        monthly_abandoned_leads,
        CONSERVATIVE_REPLY_RATE,
        CONSERVATIVE_CVR_LIFT,
        follow_up_multiplier,
    )
    expected_leads = _recovered_leads(
        monthly_abandoned_leads,
        EXPECTED_REPLY_RATE,
        EXPECTED_CVR_LIFT,
        follow_up_multiplier,
    )

    return {
        "conservative_recovered_leads": round(conservative_leads, 1),
        "expected_recovered_leads": round(expected_leads, 1),
        "conservative_monthly_revenue": round(conservative_leads * average_order_value, 2),
        "expected_monthly_revenue": round(expected_leads * average_order_value, 2),
    }
