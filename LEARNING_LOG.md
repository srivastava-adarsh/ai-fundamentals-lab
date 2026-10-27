# Learning Log
  
  A running log of my journey going *under the hood* of AI engineering — newest entries on top.
  
  ## Context (why this repo exists)
  I'm an infrastructure and cloud architect (18 yrs). I've already envisioned, architected,
  and shipped several internal AI tools using spec-driven, AI-assisted development — but the
  *code* was largely AI-generated while I directed, validated, and integrated it.
  
  This repo is where I rebuild the internals by hand — RAG, agents, evaluation, and more —
  so I can reason about, explain, and defend every design decision myself. Not starting from
  zero; going deeper.
  
  All work here uses public/sample data only. No employer code or proprietary architecture.
  
  ## 2026-10-27 — PHASE 2, Week 2: end-to-end retrieval on real content + repo tidy  (WEEK 2 LEARNING COMPLETE)
  - phase2/week2/load_real_chunks.py: wired the whole pipeline on real content (public AWS Well-Architected sample):
    section-based chunking -> embed with own cached all-MiniLM-L6-v2 (HF_HUB_OFFLINE=1, no network) ->
    persistent Chroma collection -> semantic query -> metadata where-filter.
  - Proof it works: query "How do I recover when my system fails?" ranked #1 a chunk with ZERO keyword overlap
    ("failure management... backing up data...") -> meaning > keyword (BM25 would've missed it). where={"section":...}
    then constrained candidates BEFORE ranking (a worse match surfaced because better ones were filtered out).
  - Debug: the classic return-inside-the-for-loop bug again (only the first section chunked) -> dedented return -> all 3 sections.
  - Learned the if __name__ == "__main__" guard (import-vs-run); chose a self-contained Week-2 file over cross-dir import.
  - Repo housekeeping: restructured week1-4 -> phase1/week1-4 for consistency with phase2/ (git mv, history preserved);
    rewrote the root README; added blog/02. Everything pushed to GitHub (public, IP-safe).

  ## 2026-10-26 — PHASE 2, Week 2: index internals (brute-force, IVFFlat, HNSW) at architect depth
  - Brute-force k-NN is exact but O(n) per query -> breaks at millions. ANN indexes trade a little recall for big speed.
  - IVFFlat: clusters + centroids; query compares all centroids (round 1) then brute-forces inside the nearest clusters
    (round 2). Misses concentrate at cluster boundaries; `probes` trades speed<->recall (max probes = brute force).
    Needs representative data at build + periodic rebuilds as data drifts.
  - HNSW: navigable LAYERED graph (highways->arterials->local streets); greedy hop per layer until a local minimum,
    then descend; bottom layer explores an ef_search-sized candidate pool. Memory cost = the link graph (knob `m`),
    a real bill at tens of millions of vectors (must live in RAM). Graceful incremental inserts (vs IVFFlat staleness).
    Knobs: ef_construction (build-time, baked in) vs ef_search (query-time, tunable recall<->speed).
  - Decision heuristic: default HNSW for query perf + streaming inserts; IVFFlat when memory/cost at scale dominates
    or the corpus is static/batch-rebuilt. (Scenario: 80M + 500k/day + latency SLO -> HNSW; manage memory via m / quantization / sharding.)
  - Remediation caught: don't reach for ef_search to cut MEMORY -> that's `m` (ef_search tunes query speed/recall only).

  ## 2026-10-15 — PHASE 2, Week 2: distance metrics (L2 vs cosine vs inner product)
  - pgvector operators: <-> L2/Euclidean, <=> cosine, <#> inner product.
  - Direction = meaning, magnitude = (noisy, often length-related) artifact. Proved it: two SAME-direction vectors of
    different length -> cosine distance 0 (identical), L2 distance 8 (far). Same vectors, metrics disagree.
  - Text embeddings default to cosine (meaning lives in direction). MiniLM normalizes vectors -> cosine/L2 converge,
    so the choice becomes a compute-cost call (inner product cheapest). Failure mode: magnitude-sensitive metric on
    UN-normalized vectors skews ranking by length/repetition.

  ## 2026-10-13 — PHASE 2, Week 2: real vector stores (Chroma + pgvector) stood up
  - phase2/week2/vector_db.py: Chroma PersistentClient, own offline MiniLM embedder
    (SentenceTransformerEmbeddingFunction, all-MiniLM-L6-v2), forced offline via os.environ["HF_HUB_OFFLINE"]="1"
    placed ABOVE the imports (HF reads the setting at import time). Proved the HF Hub warning disappears; weights load from cache.
  - pgvector: installed Postgres 17 + pgvector 0.8.7 (switched off 16 — the prebuilt bottle only targets pg17/18);
    createdb vectorlab; CREATE EXTENSION vector (extensions are enabled PER-database). CREATE TABLE with a vector(3) column,
    inserted toy vectors, ran real similarity SQL (embedding <-> '[...]' ORDER BY distance). Nearest-first proven.
  - Git hygiene: chroma_store/ (generated DB) added to .gitignore; verified excluded via git check-ignore before committing.

  ## 2026-09-27 — PHASE 2, Week 1: chunking metadata, section tagging, section pre-filter  (WEEK 1 COMPLETE)
  - Extended phase2/week1/chunking.py: #4 attach metadata to each chunk (id, source, char offsets);
    #5 define sections up front then chunk WITHIN each section (section label travels with the chunk);
    then filter chunks by section. This is the metadata that makes pre-filtered retrieval possible later.
  - Learned the discipline of ONE small concept at a time (metadata, then sectioning, then filtering — not all at once).

  ## 2026-09-23 — PHASE 1 VALIDATION PASSED — cleared for Phase 2
  - End-of-phase gate: explained/applied Phase 1 concepts from memory, no notes. Scored 10/10 after two sharpenings
    (conversation-memory mechanism; sentence-level embeddings). Phase 1 (Python fluency + how LLMs work) complete.
  - Confirms the rule: don't advance until I can defend the concepts in my own words.

  ## 2026-09-24 — PHASE 2, Week 1, Day 1: Chunking strategies
  - phase2/week1/chunking.py on a public AWS Well-Architected paragraph (sample_doc.txt).
  - #1 fixed-size (cut every N chars): butchers words at every boundary -> muddy embeddings -> worse retrieval.
  - #2 sentence-aware (split on '. '): clean whole-thought chunks. (Debug: return was inside the for-loop -> only 1 chunk;
    same indentation-scope bug family as before. Fixed by dedenting return.)
  - #3 fixed-size WITH overlap (while loop, start = end - overlap): tail of each chunk repeats at head of next,
    preserving context across boundaries so answers don't fall between chunks. Learned while-loop.
  - Takeaway: chunking quality drives retrieval quality. Next: summarize the 3 tradeoffs, then metadata on chunks.

  ## 2026-09-22 — Week 4, Day 2: Semantic search from scratch  (PHASE 1 CONTENT COMPLETE)
  - phase1/week4/semantic_search.py: embed a set of docs (the "index"), embed a query into the SAME space,
    cosine-sim query vs all docs, pair (score, doc) as tuples, sort desc, return top_k.
  - Query "Tell me about pet animals" -> ranked the dog (0.591) and cat (0.408) docs top, Python (0.148) low —
    despite no shared keywords. This IS the Retrieval in RAG; COMPASS does retrieve->augment->generate.
  - Concepts locked: meaning->location in 384-dim space; same model/space for query+docs; search = nearest vectors;
    tuples (two-parens = append one tuple); list.sort(reverse=True) ranks by first element (score).
  - PHASE 1 LEARNING DONE. Next: Phase 1 refresher + validation gate before Phase 2.

  ## 2026-09-16 — Week 4, Day 1: Embeddings ("meaning as numbers")
  - phase1/week4/embeddings.py: loaded MiniLM (all-MiniLM-L6-v2) via sentence-transformers; embedded text -> 384-dim vector.
  - Compared sentences with cosine similarity: "dog barked" vs "puppy made noise" = 0.526 (HIGH, despite ~no shared words);
    either vs "filed my tax return" = ~0.06-0.10 (LOW). Proved semantic > keyword matching. This is the MiniLM half of COMPASS.
  - Deep-dive Q&A (understood, not just used): how models learn meaning (trained neural net, statistical geometry, not true
    comprehension); dimension COUNT is a design choice (384), dimension MEANING is emergent/not human-interpretable;
    values are floats (~7 digits), NOT bounded to [-1,1] — the [-1,1] bound is on the cosine-similarity SCORE.
  - Cosine similarity mechanics: dot product / (magnitudes) = cosine of angle; ignores length, keeps direction; symmetric
    (hence (0,1)==(1,0)); similarity matrix is symmetric with 1.0 diagonal -> compute upper triangle only (the nested loop, j=i+1).
  - Debug: fixed "MiniLLM" (2 L's) typo -> HF 401/NotFound; correct name is MiniLM (1 L).

  ## 2026-09-12 — Week 3, Day 4: MCP (Model Context Protocol) — concept (Option A)
  - Understood MCP as the standard protocol connecting an AI app to external tools/data ("USB for AI tools").
  - Roles: Host/Client (the AI app) <-> Server (exposes tools, adapts to a real system's API) via the protocol;
    Host discovers tools and calls them. Servers are configured/scoped.
  - Inspected the live setup via `kiro-cli mcp` (list/add/remove/status/import) to make it concrete.
  - Mapped it to how a RAG assistant works: it's a Host connected to tool Servers; the server translates a
    tool call into the real system's API and returns data in MCP format.
  - Comprehension check passed (add a new source = create/obtain an MCP server + `kiro-cli mcp add`).
  - NOTE: kept all specific configured server names/internal details OUT of this log and out of anything public (IP boundary).
  - MCP vs REST (key distinction): REST is for developers to code against (endpoints known from docs, deterministic calls);
    MCP is for an LLM to DISCOVER tools at runtime (server self-describes tools/params) and invoke them autonomously,
    with one standard protocol across all servers. MCP often WRAPS REST: LLM --(MCP)--> server --(REST)--> real system.
    The MCP server is the adapter/translator between the two.
  - Option B DONE: built a minimal MCP server (FastMCP, one 'add' tool) + a client that launches it, does the
    handshake, list_tools (discovery), and call_tool. Saw the full round-trip return 5.
  - Learned by bug: without @mcp.tool() the tool was INVISIBLE (empty list, 'Unknown tool') -> with it, discovered & callable.
  - Confirmed self-describing property live: tool description came from the docstring, params from type hints.
  - Also hit a real versioning break: mcp 2.x renamed FastMCP->MCPServer; pinned mcp<2 for the throwaway (why uv.lock matters).
  - Touched async/await (client I/O) at a 'use it' level; deeper async is later. WEEK 3 COMPLETE.

  ## 2026-09-12 — Week 3, Day 3: Multi-turn conversation (memory)
  - Key insight: LLMs have NO memory between calls. "Memory" = you resend the whole history each time.
  - Proved it: two separate ask_llm() calls -> model didn't recall my name. Then ask_with_history(messages)
    flattens the messages list (Week 1 structure) into a transcript and resends it -> model recalls "Bond".
  - Learned += (string concatenation/accumulate) and why the for-loop rebuilds the transcript; "assistant:" cue.
  - Cleanup lesson — "works" != "correct": fixed subprocess.TimeoutExpired (was Timeout.Expired),
    content: reply1 (was the literal string "reply1"), key casing "error", stray backtick. Right output, wrong reasons before.
  - Caveat noted: kiro-cli injects its own agent context/tools (username, Jira, steering files) — not a clean model endpoint.

  ## 2026-09-11 — Week 3, Day 2: Structured JSON output from the LLM
  - Added ask_llm_json(prompt) to kiro_wrapper.py: appends an instruction to return ONLY valid JSON
    (no markdown/code fences), then json.loads() into a dict.
  - Guarded the parse with except json.JSONDecodeError -> safe fallback {"error":..., "raw":...} (LLM output isn't guaranteed).
  - Used the structured result like any dict to build a sentence from typed fields (year_created came back as int 1991).
  - Key idea: structured/parseable output is what turns "a chatbot" into "an AI system." (Reinforced dict syntax: colon = key/value separator; f-string literal text incl. trailing period.)
  - IMPORTANT follow-up: don't let the model GUESS the JSON key names (I got year_created by luck the first time,
    then observed it after the fact — fragile). Fix: SPECIFY exact keys/types in the prompt ("Return JSON with exactly
    these keys: name (string), year_created (integer), creator (string)"). Define the contract; still keep the parse
    fallback. Industry-grade version = JSON Schema / Pydantic (coming in Phase 3 guardrails).

  ## 2026-09-09 — Week 3, Day 1: The Kiro CLI wrapper (first real AI tool)
  - Built phase1/week3/kiro_wrapper.py: ask_llm(prompt) calls `kiro-cli chat --no-interactive --model auto` via subprocess.
  - Cleaned output: used repr() to reveal hidden ANSI color codes; stripped them with a regex, removed the "> " prefix.
  - Debug lesson: defining clean_output() isn't enough — ask_llm() has to actually CALL it (was returning raw stdout).
  - Robust error handling: timeout (TimeoutExpired), non-zero returncode (reports stderr), empty response.
  - Verified failure path on purpose (bad model name -> clean ERROR, no crash). Combines Weeks 1-2: functions,
    subprocess, string parsing, regex, error handling. This is the COMPASS chat layer, understood by hand.

  ## 2026-09-08 — Week 2, Day 4: Virtual environments  (WEEK 2 COMPLETE)
  - Understood the three pieces: pyproject.toml (declared deps / "the order"), uv.lock (exact pinned
    versions + hashes / "the recipe", reproducible), .venv/ (the isolated installed env / "the kitchen", gitignored).
  - Key uv commands: init, add, remove, sync, run, lock. `uv run` auto-activates the venv.
  - Ran `uv sync` — it cleaned up a stale self-install (leftover from the removed package scaffold). Env is reproducible.
  - WEEK 2 DONE: requests + APIs, corporate TLS solved, secrets via .env, error handling, virtual environments.
    Full foundation for Week 3 (Kiro CLI wrapper).

  ## 2026-09-08 — Week 2, Day 3: Error handling (deeper)
  - phase1/week2/error_handling.py: saw a raw crash first (ZeroDivisionError), then handled it.
  - Specific exception types: ZeroDivisionError, TypeError, FileNotFoundError — each handled deliberately.
  - `finally` always runs (success or failure) — for guaranteed cleanup.
  - Sharpened error-reading: decoded an AttributeError that was really a `.` vs `,` typo. Not every error is a logic bug.

  ## 2026-09-08 — Week 2, Day 2: Secrets with env vars & .env
  - phase1/week2/secrets_demo.py: os.environ.get() to read env vars; printed only the LENGTH, never the secret.
  - Inline var for one run (VAR=... uv run ...), then python-dotenv: load_dotenv() reads a .env file automatically.
  - Security discipline: added .env (+ *.env) to .gitignore; used `git check-ignore` to POSITIVELY confirm
    .env and charter-ca.pem are ignored before committing. Verify, don't assume — no secret/cert leaves local.

  ## 2026-09-03 — Week 2, Day 1: Calling APIs with requests
  - Set up week2 as a uv project (uv init / uv add requests) — used the tool we chose, not raw venv.
  - Wrote phase1/week2/api_call.py: requests.get(), response.json() -> dict, nested access (address.city).
  - Error handling: try/except, timeout, raise_for_status; tested happy path, 404, and bad-DNS — all fail gracefully.
  - BIG real-world detour: solved corporate TLS. Charter proxy intercepts HTTPS with its own CA.
    requests uses certifi (didn't trust Charter). Fix: extracted the on-the-wire Charter root via
    openssl s_client, combined with certifi into ~/charter-combined-ca.pem, set REQUESTS_CA_BUNDLE
    (+ SSL_CERT_FILE) in ~/.zshrc. Keychain-exported root differed from the wire cert — the wire one worked.
  - Kept cert files out of git (.gitignore *.pem, .venv/, .DS_Store) — employer infra never goes public.

  ## 2026-09-01 — Week 1, Day 4: Files + JSON  (WEEK 1 COMPLETE)
  - Built phase1/week1/files_json.py. Plain text files with `with open(...)` (write "w" / read "r").
  - JSON: json.dump (dict -> JSON text / serialize) and json.load (JSON text -> dict / deserialize).
  - The load -> modify -> save cycle (the everyday config/API-data pattern).
  - Learned .gitignore: kept generated artifacts (notes.txt, config.json) out of version control.
  - WEEK 1 DONE: variables, subprocess, parsing, lists, dicts, LLM messages format, functions, files, JSON.
    Foundation set for Week 2 (calling APIs) and Week 3 (Kiro CLI wrapper).

  ## 2026-09-01 — Week 1, Day 3: Functions
  - Built phase1/week1/functions.py. Learned def, arguments, return (vs print).
  - Refactored the disk-checker into a reusable check_disk_usage(threshold) that RETURNS
    a list of warnings instead of printing — separating "compute" from "display."
  - Proved reuse: same function called with threshold 80 and 60 gives different results, no code duplication.
  - Debugging lesson (big one): an over-indented block put the threshold logic inside the inner
    loop, so a break skipped it -> "runs but does nothing." Also caught a $ used instead of % (shell habit).

  ## 2026-08-28 — Week 1, Day 2: Lists & Dicts (the shape of AI data)
  - Built phase1/week1/data_structures.py. Lists: indexing, len(), append(), enumerate().
  - Dicts: key→value pairs, access by name not position.
  - Combined lists + dicts into an LLM "messages" array — the exact data structure
    every LLM API uses (system/user/assistant roles). Now I know what I'll be building in Week 3.
  - f-string with dict keys inside (single vs double quote nesting).

  ## 2026-08-27 — Week 1, Day 1: First Python (shell script → Python)
  - Rewrote an ops disk-usage checker from bash into Python (phase1/week1/disk_check.py).
  - Learned by building: variables, print(), import, subprocess.run() to call shell commands,
    .split()/.split("\n"), for loops, list indexing (parts[4], parts[-1], lines[1:]),
    .endswith(), break/continue, int() + .replace(), f-strings, and None.
  - Debugged real errors myself: True/False must be capitalized; a break mis-indented outside
    an if (indentation defines blocks in Python); missing f-string prefix; smart vs straight quotes.
  - Handled a real-world parsing edge case (df rows with spaces / extra words) by finding the
    first token ending in "%" instead of trusting a fixed column position.
  - Committed + pushed; saw my own BRACE git-hook run on the commit.

  ## 2026-08-24 — Day 1
  - Renamed GitHub, created this lab repo, set up local toolchain (git, VS Code, Python 3.12).
  - Goal: deepen hands-on AI-engineering mastery to architect/principal parity.
  - Plan: 4 phases over ~32 weeks. Phase 1 = Python fluency + how LLMs actually work.
  - Set up local workspace: cloned repo, first local commit.