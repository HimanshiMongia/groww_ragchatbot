# Architecture Overview: Groww MF RAG Chatbot (Revised)

This project follows a 5-phase implementation strategy, modularizing the RAG pipeline components and application services.

## Phase-wise Roadmap

### [Phase 1: Ingest](../phase1_ingest/architecture.md)
Focuses on data acquisition from Groww.in, data normalization, and schema definition.

### [Phase 2: Retrieve](../phase2_retrieve/architecture.md)
Focuses on vector storage (ChromaDB), embedding models, and semantic retrieval strategies.

### [Phase 3: Generate](../phase3_generate/architecture.md)
Focuses on LLM integration, prompt engineering, and context-aware response generation.

### [Phase 4: Chat App](../phase4_chat_app/architecture.md)
Focuses on the user interface (Streamlit/React) and conversation state management.

### [Phase 5: Scheduler](../phase5_scheduler/architecture.md)
Focuses on automated data updates (NAV, fund stats) and system maintenance.
