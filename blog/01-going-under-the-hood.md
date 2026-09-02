# 18 Years in Infrastructure — Why I'm Learning AI Engineering From the Ground Up

I've spent about eighteen years working in infrastructure and cloud — networks, systems, automation, the kind of work that keeps things running and scales when they need to. I'm comfortable reasoning about distributed systems, failure modes, and trade-offs at an architectural level.

But here's an honest admission: when it comes to AI systems, I've mostly been a *user*. I can wire things together and get results. What I couldn't always do was explain, from first principles, *why* they work — or defend the design decisions under hard questioning.

I decided that wasn't good enough. So I'm changing it, in public.

## Why now

AI isn't a side technology anymore; it's becoming part of how everything gets built. As someone who has always understood the systems I work with at a deep level, being a surface-level AI user started to feel like a gap I didn't want to carry.

I don't want to just *use* retrieval-augmented generation, agents, and embeddings. I want to understand them well enough to design them, reason about their trade-offs, and explain them to a room of skeptical engineers. That's a different bar — and it's the one I'm aiming for.

## The approach: learn by building, in public

A few rules I've set for myself:

- **Build from primitives.** Before reaching for a framework, I write the basic version by hand so I actually understand what the framework is doing for me.
- **AI-assist off while learning.** It's tempting to let AI generate the code. But the whole point is to understand it, so during learning I type it myself — and debug my own mistakes.
- **Document everything.** Every step goes into a public repo and a learning log. If I can't explain it, I don't really know it.
- **Low drama, steady pace.** About an hour a day. Consistency over intensity.

Everything lives here: [github.com/srivastava-adarsh/ai-fundamentals-lab](https://github.com/srivastava-adarsh/ai-fundamentals-lab)

## Week 1: back to fundamentals

I started where it makes sense for someone rebuilding hands-on muscle — Python fundamentals, framed around things I'd actually use for AI work.

In the first week I:

- Rewrote an operations shell script (a disk-usage checker) in Python — learning variables, running shell commands from code, parsing output, and handling real-world edge cases where the data isn't as clean as you'd like.
- Worked through lists and dictionaries, and built the exact data structure that every LLM API uses to represent a conversation (a list of `{"role": ..., "content": ...}` messages).
- Refactored my code into reusable functions — separating *computing* a result from *displaying* it.
- Handled files and JSON: the load → modify → save cycle that underpins config and API data.

Along the way I hit every classic beginner bug — indentation that changes your logic, booleans that must be capitalized, a stray shell-style `$` where a `%` belonged. Debugging those myself was the point.

## What's next

From here the plan moves outward:

- Calling APIs from Python
- Building a small wrapper to talk to a language model programmatically
- Retrieval and embeddings — understanding semantic search by building it
- Agents and tool use
- Evaluation, observability, cost, and safety — the things that separate a demo from a production system

I'll write these up as I go — including what breaks, because that's usually where the learning is.

## Why write it down

Two reasons. First, explaining something forces me to actually understand it. Second, I think there's value in showing the *unglamorous middle* of learning — not a polished expert, but an experienced engineer deliberately rebuilding a skill in the open.

If you're on a similar path — experienced in one area, deliberately going deep in another — I'd genuinely like to hear how you're approaching it.

More soon.
