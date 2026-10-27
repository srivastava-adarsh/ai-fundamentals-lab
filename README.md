# ai-fundamentals-lab

My hands-on journey learning AI engineering from the ground up — building the
internals by hand so I can reason about, explain, and defend every design decision.

## Who / why

I'm an infrastructure and cloud architect (18 years). I've envisioned, architected,
and shipped several internal AI tools using spec-driven, AI-assisted development —
but the *code* was largely AI-generated while I directed, validated, and integrated it.

This repo is where I rebuild those internals **by hand** — RAG, agents, evaluation,
and more — to reach architect/principal-level depth: for any design choice, be able to
defend it, name an alternative, and state its failure mode.

**Ground rules I set for myself:**
- **Build from primitives** before reaching for frameworks.
- **AI-assist OFF while learning** — I type the code myself and debug my own mistakes.
- **Document everything** — if I can't explain it, I don't really know it.
- **Consistency over intensity** — about an hour a day.
- **Public/sample data only — no employer code or proprietary architecture.**

## The plan (4 phases, ~32 weeks)

| Phase | Focus | Status |
|-------|-------|--------|
| **1** | Python fluency + how LLMs actually work | Complete (validated) |
| **2** | RAG & agents from the inside | In progress |
| **3** | Evaluation, observability, cost & safety | Planned |
| **4** | AWS Bedrock, system design & portfolio | Planned |

## Repo structure

```
phase1/   Python fundamentals, APIs, LLM calls, embeddings, semantic search
  week1/  Python for AI (variables, data structures, functions, files/JSON)
  week2/  APIs, corporate TLS, secrets/.env, error handling, venvs
  week3/  Kiro CLI LLM wrapper, structured output, conversation memory, MCP
  week4/  Embeddings (MiniLM), cosine similarity, semantic search from scratch
phase2/   RAG & agents
  week1/  Chunking strategies (fixed, sentence, overlap, metadata, sections)
  week2/  Vector DBs — Chroma + pgvector, distance metrics, HNSW/IVFFlat, end-to-end retrieval
blog/     Long-form write-ups (also published on Hashnode)
LEARNING_LOG.md   Running day-by-day log, newest on top
```

## Writing

I write up the journey as I go — including what breaks:

- [18 Years in Infrastructure — Why I'm Learning AI Engineering From the Ground Up](https://srivastava-adarsh.hashnode.dev/18-years-in-infrastructure-why-i-m-learning-ai-engineering-from-the-ground-up)
- [pgvector vs a local vector store (Chroma) — what an infra person notices](https://srivastava-adarsh.hashnode.dev/pgvector-vs-chroma-what-an-infra-engineer-notices)

Blog home: https://srivastava-adarsh.hashnode.dev
