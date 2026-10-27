# pgvector vs a local vector store (Chroma) — what an infra person notices

*Part of my ongoing "going under the hood of AI" learning series. A few weeks ago I wrote about [why, after 18 years in infrastructure, I'm learning AI engineering from the ground up](https://srivastava-adarsh.hashnode.dev/18-years-in-infrastructure-why-i-m-learning-ai-engineering-from-the-ground-up). This is the first real deep dive. All examples use public AWS Well-Architected sample content — no proprietary data. Hand-built and measured myself, with AI-assist off while I learn.*

After 18 years in infrastructure, I spent this week standing up **two** vector stores from scratch — pgvector (a Postgres extension) and Chroma (a purpose-built vector DB) — and loading the same content into both. A few things jumped out from an ops lens that I don't see talked about much:

## 1. "Vector database" is two different philosophies

Chroma exists *only* to do vector search. pgvector is a plugin that teaches your *existing* Postgres to do it. If an enterprise already runs Postgres (most do), pgvector means one fewer system to back up, secure, and monitor — and vectors live in the same row as your normal data. That "reuse what you already operate" instinct is deeply familiar to anyone from infrastructure.

## 2. The distance metric is a real decision, not a default

I proved to myself that cosine and L2 can *rank the same vectors differently* — two vectors pointing the same direction but with different lengths were "identical" to cosine and "far apart" to L2. For text embeddings, meaning lives in a vector's **direction**, not its magnitude, so cosine is usually the honest choice. With normalized embeddings like MiniLM's, the two converge — so the metric choice becomes a cost decision, not a correctness one.

## 3. The index is where my infra brain lit up

Brute-force search is O(n) per query — fine for 5 rows, a problem at millions. The two approximate-nearest-neighbor indexes trade a little recall for a lot of speed:

- **IVFFlat** — clusters the space, searches only the nearest clusters. Low memory, but it goes stale as data grows → needs periodic rebuilds.
- **HNSW** — a navigable graph you "walk" toward the query. Faster queries and graceful inserts — but the link graph lives in RAM, so at tens of millions of vectors it becomes a real *cost* line item.

The architect's call: default to HNSW for query performance and streaming inserts; reach for IVFFlat when memory/cost at scale dominates or the corpus is static. Same recall-vs-speed-vs-cost tradeoff I've made a hundred times in other systems — just a new runtime.

## The through-line

A vector store is a distributed system with the same old tradeoffs — memory, cost, freshness, latency. The vocabulary is new; the engineering judgment isn't.

*Hand-built and measured myself (AI-assist off while I learn). Code in my public repo: [github.com/srivastava-adarsh/ai-fundamentals-lab](https://github.com/srivastava-adarsh/ai-fundamentals-lab)*
