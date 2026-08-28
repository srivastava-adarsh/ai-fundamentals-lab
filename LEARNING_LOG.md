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