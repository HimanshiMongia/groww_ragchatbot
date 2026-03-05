# Phase 1: Ingest

## Objective
Automated extraction of mutual fund data from Groww.in URLs.

## Data Points to Extract
- Fund Name
- NAV (Net Asset Value)
- Expense Ratio
- Exit Load
- Minimum SIP
- Risk Level
- 1-Year Return
- ELSS Lock-in (if applicable)

## Implementation Details
- **Tooling**: Playwright/Selenium for web scraping.
- **Output**: Standardized JSON format for downstream processing.
- **Target Funds**: 8 specific funds provided by the user.
