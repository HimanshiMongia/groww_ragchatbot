# Phase 3: Generate

## Objective
Generate human-like, accurate responses based on retrieved mutual fund data.

## Behavioral Constraints & Guardrails
- **Citations**: Every answer MUST include one clear, direct citation link to a public Groww source.
- **Opinionated Queries**: Refuse "Should I buy/sell?" or "Is this a good fund?" type questions.
  - *Response Style*: Polite, facts-only refusal with a link to an educational resource (e.g., [Groww MF Knowledge Centre](https://groww.in/blog/category/mutual-funds)).
- **Data Integrity**: 
  - Use **Public Sources Only**. No screenshots, no third-party blogs.
  - **No PII**: Strictly refuse and do not store PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers.
- **No Performance Claims**: Do not compute or compare returns. If asked for a comparison, provide links to the official fund factsheets.
- **Response Formatting**:
  - Length: Maximum **3 sentences**.
  - Footer: Mandatory "Last updated from sources: [Date/Source]" line.
