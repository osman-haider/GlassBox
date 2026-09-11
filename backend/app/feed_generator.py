"""
Synthetic "recovered lead" feed generator.

Produces a handful of preview entries styled after SmartRecover's
homepage live feed (name, plan, channel, time, amount). These are
randomly generated for illustration only — never real recovered sales.
"""

import random

_FIRST_INITIALS = ["S", "P", "M", "J", "A", "R", "T", "K", "D", "L"]
_LAST_INITIALS = ["M.", "R.", "L.", "K.", "B.", "H.", "N.", "W."]
_PLAN_LABELS = [
    "Purchased 1-mo plan",
    "Purchased 3-mo plan",
    "Purchased 6-mo plan",
    "Purchased 12-mo plan",
    "Recovered checkout",
    "Completed intake",
]
_TIME_LABELS = ["2m ago", "6m ago", "14m ago", "23m ago", "38m ago", "51m ago"]


def generate_sample_feed(average_order_value: float, entry_count: int = 4) -> list:
    """
    Build a small, clearly-illustrative list of "recovered lead" entries,
    scaled loosely to the prospect's own average order value so the
    numbers feel proportionate rather than arbitrary.
    """
    entry_count = min(entry_count, len(_TIME_LABELS))
    time_labels = random.sample(_TIME_LABELS, k=entry_count)

    entries = []
    for time_label in time_labels:
        name = f"{random.choice(_FIRST_INITIALS)}. {random.choice(_LAST_INITIALS)}"
        plan_label = random.choice(_PLAN_LABELS)
        variance = random.uniform(0.6, 1.6)
        amount = round(max(average_order_value * variance, 15), 2)

        entries.append(
            {
                "name": name,
                "plan_label": plan_label,
                "channel": "Replied via SMS",
                "time_ago": time_label,
                "amount": amount,
            }
        )

    entries.sort(key=lambda entry: _TIME_LABELS.index(entry["time_ago"]))
    return entries
