# Phase 2 · Week 3 — Hybrid Search + Eval Harness

**Status:** in progress. The vector-only baseline is measured, and BM25 and RRF are next.

## Goal
Measure retrieval quality instead of eyeballing it. Build a fixed eval set, score a
vector-only retriever against it, then add BM25 keyword search and a rank-fusion (RRF)
hybrid, and compare all three with the same metrics.

## Corpus
A small public sample of AWS Well-Architected Framework sections (10 sections, 28 chunks at
size=150 / overlap=30). Public data only.

## Files
| File | What it does |
|---|---|
| `corpus.json` | The 10 sections, kept separate from code so re-chunking is stable |
| `load_corpus.py` | Chunks the corpus, embeds with an offline MiniLM, loads a persistent Chroma collection |
| `eval_set.py` | 18 questions, each anchored to the *section* that answers it (not a chunk id) |
| `score.py` | Retrieval + metrics: recall@1/3/5 and MRR |

## Design decisions
- Score against the section name, not chunk ids, so changing chunk size or overlap doesn't
  invalidate the eval.
- Every retriever returns a plain list of section names, so vector, BM25 and hybrid are
  scored identically.
- Questions are tagged by lexical difficulty: Z0 (shared keywords), Z1 (paraphrase, no shared
  words), Z2 (rare literal terms).

## Results so far (vector-only baseline)
| Metric | Score |
|---|---|
| recall@1 | 0.83 |
| recall@3 | 0.83 |
| recall@5 | 0.94 |
| MRR | 0.861 |

Finding: with only 28 chunks, top-5 covers about 18% of the corpus, so recall@5 has little
headroom (a ceiling effect). recall@1/@3 and MRR are reported alongside it for that reason.

## Run it
```
uv run python load_corpus.py   # build the Chroma collection
uv run python score.py         # score the baseline
```

BM25 and RRF results will be added here when they are done.
