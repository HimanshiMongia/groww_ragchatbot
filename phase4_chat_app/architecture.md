# Phase 4: Chat App

## Objective
Provide a user-friendly interface for interacting with the RAG chatbot.

## Implementation Details
- **Frontend**: Streamlit (v1.0) for a responsive chat interface.
- **Features**:
  - Real-time streaming of responses.
  - Chat history persistence (local session or SQLite).
  - Quick-action buttons for common queries (e.g., "Check HDFC Mid Cap NAV").
- **Backend interface**: Minimal FastAPI layer if scaling beyond Streamlit is needed.
