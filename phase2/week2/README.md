# Phase 2 · Week 2 — Vector Databases (pgvector + Chroma)

Part of my "going under the hood of AI" learning series. Everything here uses
**public AWS Well-Architected sample content** and toy vectors — no proprietary data.
Hand-built and measured myself (AI-assist off while I learn).

## What this week covers

Moving from "embeddings in a Python list" to **real vector stores**, and
understanding the decisions an architect actually has to defend.

### 1. Two vector stores, same content
- **Chroma** — a purpose-built vector database (my primary store for the rest of Phase 2).
- **pgvector** — a Postgres extension that adds vector search to a general-purpose DB.

Takeaway: Chroma exists *only* to do vector search; pgvector lets an enterprise
that already runs Postgres add vectors next to its normal data — one fewer system
to operate.

### 2. Distance metrics
- `<->` L2 / Euclidean, `<=>` cosine, `<#>` inner product.
- Proved that cosine and L2 can **rank the same vectors differently**: two vectors
  pointing the same direction but different lengths were *identical* to cosine and
  *far apart* to L2.
- Meaning lives in a vector's **direction**, so text embeddings default to cosine.
  With normalized embeddings (MiniLM), the metrics converge → the choice becomes
  a compute-cost decision.

### 3. Index internals (how search stays fast at scale)
- Brute-force k-NN is exact but **O(n) per query** — a problem at millions of vectors.
- **IVFFlat** — clusters the space, probes only the nearest clusters. Low memory,
  but goes stale as data grows → periodic rebuilds. Knob: `probes` (recall ↔ speed).
- **HNSW** — a navigable layered graph walked greedily toward the query. Faster
  queries, graceful inserts, but the link graph lives in RAM → a real cost at scale.
  Knobs: `m` (links/memory, build-time), `ef_search` (recall ↔ speed, query-time).
- Heuristic: **default HNSW** for query performance + streaming inserts; **IVFFlat**
  when memory/cost at large scale dominates or the corpus is static/batch-rebuilt.

## Files

- **`vector_db.py`** — Chroma fundamentals: persistent collection, own offline
  MiniLM embedder, semantic query, metadata pre-filtering.
- **`load_real_chunks.py`** — end-to-end retrieval on real content:
  section-based chunking → embed with cached `all-MiniLM-L6-v2` (fully offline) →
  persistent Chroma collection → semantic query → metadata `where` filter.

## Proof it works (from live output)

Query: *"How do I recover when my system fails?"*
Top hit was a chunk containing **none** of the query's keywords
("failure management… backing up data…") — ranked #1 by **meaning**.
A keyword method like BM25 would have missed it. Adding
`where={"section": ...}` then constrained the candidate set **before** ranking,
proving filter-first / rank-second.

## Notes
- Embeddings: local `sentence-transformers` (`all-MiniLM-L6-v2`), `HF_HUB_OFFLINE=1`
  — no network calls.
- `chroma_store/` (the generated DB) is git-ignored.
