# Phase 5: Scheduler

## Objective
Ensure the chatbot always has access to the most recent fund data (NAV, Returns).

## Implementation Details
- **Tooling**: GitHub Actions (Primary) using `.github/workflows/daily_update.yml`.
- **Frequency**: Daily updates at 10:00 AM IST (04:30 AM UTC).
- **Process**:
  - Checkout repository.
  - Install dependencies and Playwright.
  - Run `phase1_ingest/scraper.py` (updates `sample_fund_data.json` with new NAVs and `last_updated` timestamps).
  - Run `phase2_retrieve/vector_store.py` (rebuilds ChromaDB with new metadata).
  - Commit and push changes back to the repository.
  - Vercel automatically redeploys on every push to `main`, ensuring the app remains fresh.
