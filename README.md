# GlassBox

A self-serve preview tool for SmartRecover: enter a few funnel numbers and
instantly see a personalized recovery-potential estimate, a preview of the
attributed "live recovery feed" reporting, and a sample of the kind of 1:1
SMS conversation a real rep would have with one of your leads.

It exists to close one specific gap: SmartRecover's own FAQ says results
vary by funnel and are modeled live, on the sales call. GlassBox turns
that manual, once-per-call estimate into something a prospect can see
themselves, in seconds, before ever booking a call — without changing
anything about how SmartRecover actually delivers the service.

This is a demo/prototype, not a production system: no accounts, no
database, no real CRM integration, no real payment or commission
processing. See `docs/` (or the original strategy doc it was built from)
for the full reasoning behind the project.

## How it works

One FastAPI app serves both the API and the static frontend from a single
process:

- `POST /api/estimate` takes four inputs (monthly abandoned leads, average
  order value, funnel stage, current follow-up method) and returns a
  conservative-to-expected revenue range, a synthetic sample feed, and a
  sample SMS conversation matched to the funnel stage.
- The frontend (`frontend/`) is a single page with no build step — plain
  HTML, CSS, and JS — that calls that endpoint and renders the result.

The revenue math uses SmartRecover's own published aggregate benchmarks
(~50% SMS reply rate, ~23% average conversion lift) as illustrative
assumptions. Every output is labeled as an estimate, not a guarantee.

## Project structure

```
GlassBox/
  backend/
    requirements.txt
    app/
      main.py                 FastAPI app, routes, static file mount
      models.py                Request/response models
      constants.py             Published benchmark assumptions
      calculations.py          Recovery estimate math
      feed_generator.py        Synthetic "recovered lead" feed
      sample_conversations.py  Sample SMS conversations per funnel stage
  frontend/
    index.html
    styles.css
    app.js
  README.md
```

## Running it locally (Windows)

1. Open a terminal in the `backend` folder:

   ```
   cd GlassBox\backend
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the app:

   ```
   uvicorn app.main:app --reload --port 8000
   ```

5. Open **http://localhost:8000** in your browser. That single URL serves
   both the UI and the API — there's nothing else to run.

(macOS/Linux: same steps, but activate the virtual environment with
`source venv/bin/activate` instead.)

## Customizing

- **Booking link:** the "Book a call to model this for real" button in
  `frontend/index.html` currently points to a placeholder anchor
  (`#book-a-call`) — swap in the real Calendly/booking URL.
- **Benchmarks:** the reply-rate and conversion-lift assumptions live in
  `backend/app/constants.py`.
- **Sample conversations:** the three per-funnel-stage conversations live
  in `backend/app/sample_conversations.py` — replace `[Brand]` with a real
  brand name per use, or extend this to swap it in automatically.

## A note on git history

This repository's commits are authored as `GlassBox Builder
<builder@glassbox.local>` so the history could be generated without
needing your local git identity. If you'd like the commits attributed to
you instead, you can rewrite the author on all of them before pushing
anywhere:

```
git filter-branch -f --env-filter "GIT_AUTHOR_NAME='Your Name'; GIT_AUTHOR_EMAIL='you@example.com'; GIT_COMMITTER_NAME='Your Name'; GIT_COMMITTER_EMAIL='you@example.com'" -- --all
```

Or, if you don't need the existing history preserved, just run
`git config user.name` / `git config user.email` with your own details
before making your next commit — everything from here on will use that.
