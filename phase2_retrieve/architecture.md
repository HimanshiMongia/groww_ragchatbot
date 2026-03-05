# Phase 2: Retrieve

## Objective
Convert raw fund data into searchable vector embeddings for semantic retrieval.

## Implementation Details
- **Embedding Model**: OpenAI `text-embedding-3-small` or HuggingFace local models.
- **Vector Store**: ChromaDB (local persistence).
- **Strategy**: 
  - Metadata filtering (by fund name, risk level).
  - Semantic search across fund descriptions and stats.
- **Goal**: Efficiently fetch relevant context for user queries like "Which fund has the lowest exit load?".
