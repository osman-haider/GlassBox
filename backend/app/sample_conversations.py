"""
Sample rep-to-lead SMS conversations.

One hand-written template per funnel stage, illustrating the kind of
real, brand-voiced conversation a SmartRecover rep would have with a
lead at that specific drop-off point. Kept static/templated rather
than generated live, so the demo is fast, predictable, and easy to
rehearse.
"""

SAMPLE_CONVERSATIONS = {
    "checkout": [
        {
            "sender": "rep",
            "text": (
                "Hi Sarah, this is Jess from [Brand]. Saw you were finishing "
                "up your order earlier — did something come up, or is there "
                "a question I can help with?"
            ),
        },
        {"sender": "lead", "text": "Hey! Just wasn't sure if it's covered by my insurance"},
        {
            "sender": "rep",
            "text": (
                "Totally fair question — we're not insurance-billed, but most "
                "members pay less than a coffee a day on the monthly plan. "
                "Want me to send the exact breakdown for your cart?"
            ),
        },
        {"sender": "lead", "text": "Yeah that would help"},
        {
            "sender": "rep",
            "text": "Sending now — here's your cart with today's pricing locked in: [link]",
        },
    ],
    "quiz": [
        {
            "sender": "rep",
            "text": (
                "Hi Marcus, it's Priya from [Brand]. Looks like you got "
                "partway through the quiz — want help finishing it, or any "
                "questions first?"
            ),
        },
        {"sender": "lead", "text": "How long before I'd actually hear back from a provider?"},
        {
            "sender": "rep",
            "text": (
                "Great question — most members get matched within 24 hours "
                "of finishing the quiz. Want me to send you the last couple "
                "questions so you're not starting over?"
            ),
        },
        {"sender": "lead", "text": "Sure, go ahead"},
        {"sender": "rep", "text": "Here's your saved progress: [link] — just 2 questions left!"},
    ],
    "intake": [
        {
            "sender": "rep",
            "text": (
                "Hi Dana, this is Alex from [Brand]. Noticed your intake "
                "form got saved but not submitted — anything I can clarify "
                "before you finish it up?"
            ),
        },
        {"sender": "lead", "text": "I wasn't sure what to put for current medications"},
        {
            "sender": "rep",
            "text": (
                "That trips a lot of people up — just list anything you're "
                "currently taking, even over-the-counter. Your provider "
                "reviews it before anything is prescribed."
            ),
        },
        {"sender": "lead", "text": "Okay, that makes sense, thank you"},
        {"sender": "rep", "text": "Anytime! Here's your saved intake so you can pick right back up: [link]"},
    ],
}
