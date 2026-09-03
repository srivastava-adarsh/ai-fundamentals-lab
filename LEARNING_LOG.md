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
  
  ## 2026-09-03 — Week 2, Day 1: Calling APIs with requests
  - Set up week2 as a uv project (uv init / uv add requests) — used the tool we chose, not raw venv.
  - Wrote week2/api_call.py: requests.get(), response.json() -> dict, nested access (address.city).
  - Error handling: try/except, timeout, raise_for_status; tested happy path, 404, and bad-DNS — all fail gracefully.
  - BIG real-world detour: solved corporate TLS. Charter proxy intercepts HTTPS with its own CA.
    requests uses certifi (didn't trust Charter). Fix: extracted the on-the-wire Charter root via
    openssl s_client, combined with certifi into ~/charter-combined-ca.pem, set REQUESTS_CA_BUNDLE
    (+ SSL_CERT_FILE) in ~/.zshrc. Keychain-exported root differed from the wire cert — the wire one worked.
  - Kept cert files out of git (.gitignore *.pem, .venv/, .DS_Store) — employer infra never goes public.

  ## 2026-09-01 — Week 1, Day 4: Files + JSON  (WEEK 1 COMPLETE)
  - Built week1/files_json.py. Plain text files with `with open(...)` (write "w" / read "r").
  - JSON: json.dump (dict -> JSON text / serialize) and json.load (JSON text -> dict / deserialize).
  - The load -> modify -> save cycle (the everyday config/API-data pattern).
  - Learned .gitignore: kept generated artifacts (notes.txt, config.json) out of version control.
  - WEEK 1 DONE: variables, subprocess, parsing, lists, dicts, LLM messages format, functions, files, JSON.
    Foundation set for Week 2 (calling APIs) and Week 3 (Kiro CLI wrapper).

  ## 2026-09-01 — Week 1, Day 3: Functions
  - Built week1/functions.py. Learned def, arguments, return (vs print).
  - Refactored the disk-checker into a reusable check_disk_usage(threshold) that RETURNS
    a list of warnings instead of printing — separating "compute" from "display."
  - Proved reuse: same function called with threshold 80 and 60 gives different results, no code duplication.
  - Debugging lesson (big one): an over-indented block put the threshold logic inside the inner
    loop, so a break skipped it -> "runs but does nothing." Also caught a $ used instead of % (shell habit).

  ## 2026-08-28 — Week 1, Day 2: Lists & Dicts (the shape of AI data)
  - Built week1/data_structures.py. Lists: indexing, len(), append(), enumerate().
  - Dicts: key→value pairs, access by name not position.
  - Combined lists + dicts into an LLM "messages" array — the exact data structure
    every LLM API uses (system/user/assistant roles). Now I know what I'll be building in Week 3.
  - f-string with dict keys inside (single vs double quote nesting).

  ## 2026-08-27 — Week 1, Day 1: First Python (shell script → Python)
  - Rewrote an ops disk-usage checker from bash into Python (week1/disk_check.py).
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