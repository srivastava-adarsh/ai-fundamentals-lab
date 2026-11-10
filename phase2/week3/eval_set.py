# eval_set.py
# The measuring stick for week 3. A fixed list of test questions , each with a 
# known good answer anchored to the SECTION it should come from (stable across
# re chunking ). Everything this week measures retrieval against THIS list

eval_questions = [
    {
        "question": "How do I recover my workload after a failure?",
        "answer_section": "Change and Failure Management",
        "why": "This section covers disaster recovery and fault isolation",
    },
    {
        "question": "What does it mean for a workload to be reliable",
        "answer_section": "Reliability Overview",
        "why": "Defines reliability as performing correctly and consistently",
    },
    {
        "question": "What should I check before I start architecting a system",
        "answer_section": "Foundational Requirements",
        "why": "Covers service quotas and network bandwidth prerequisites.",
    },

    # --- Z0 - easy / normal (natural keyword overlap; BM25 and vector both succeed) ---
    {
        "question": "What is elasticity and how does automatic scaling respond to demand?",
        "answer_section": "Scaling and Elasticity",
        "why": "Z0: shares 'elasticity', 'automatic scaling', 'demand' directly with the section text.",
    },
    {
        "question": "How does cost optimization let me deliver business value at the lowest price point?",
        "answer_section": "Cost Optimization",
        "why": "Z0: 'cost optimization', 'business value', 'lowest price point' all appear verbatim.",
    },
    {
        "question": "What does detection help me identify about security misconfiguration or threats?",
        "answer_section": "Detection and Monitoring",
        "why": "Z0: 'detection', 'misconfiguration', 'threat' overlap directly with the section.",
    },
    {
        "question": "What are the disaster recovery strategies and their trade-offs?",
        "answer_section": "Disaster Recovery Strategies",
        "why": "Z0: 'disaster recovery strategies' matches the section wording; 'trade-offs' ~ 'trades off'.",
    },
    {
        "question": "How do I use computing resources efficiently to meet performance requirements?",
        "answer_section": "Performance Efficiency",
        "why": "Z0: 'computing resources efficiently', 'requirements' overlap with the section text.",
    },

    # --- Z1 - BM25-fails / vector-rescues (paraphrased, keyword-poor; no shared content words) ---
    {
        "question": "How do I keep my monthly bill small and avoid paying for things I don't use?",
        "answer_section": "Cost Optimization",
        "why": "Z1: paraphrase of cost control using 'bill', 'paying' - none appear in the section.",
    },
    {
        "question": "How do I grow and shrink capacity on its own as traffic rises and falls?",
        "answer_section": "Scaling and Elasticity",
        "why": "Z1: 'grow', 'shrink', 'capacity', 'traffic' convey elasticity with no shared tokens.",
    },
    {
        "question": "How can I spot a break-in or something behaving oddly in my environment?",
        "answer_section": "Detection and Monitoring",
        "why": "Z1: 'break-in', 'behaving oddly' map to threat/unexpected behavior with no literal overlap.",
    },
    {
        "question": "How do I ship updates in tiny safe steps and treat running the system as software?",
        "answer_section": "Operational Excellence",
        "why": "Z1: paraphrases 'frequent, small, reversible changes' and 'operations as code' lexically.",
    },
    {
        "question": "What falls back the fastest versus cheapest when a whole region goes dark?",
        "answer_section": "Disaster Recovery Strategies",
        "why": "Z1: recovery-time/point vs cost idea expressed as 'fastest', 'cheapest', 'region goes dark'.",
    },

    # --- Z2 - vector-weak / BM25-rescues (exact literal term: precise phrase or rare token) ---
    {
        "question": "How does recovery point objective factor into choosing a strategy?",
        "answer_section": "Disaster Recovery Strategies",
        "why": "Z2: 'recovery point objective' / 'objective' is a rare literal phrase found only in this section.",
    },
    {
        "question": "What is a 'pilot light' strategy?",
        "answer_section": "Disaster Recovery Strategies",
        "why": "Z2: 'pilot light' is a rare exact token that BM25 matches but vectors may miss.",
    },
    {
        "question": "What are service quotas, also called limits?",
        "answer_section": "Foundational Requirements",
        "why": "Z2: 'service quotas' and 'limits' are the precise literal terms only in this section.",
    },
    {
        "question": "What does 'least-privilege access' mean for a strong identity foundation?",
        "answer_section": "Security Foundations",
        "why": "Z2: 'least-privilege' is an exact rare term; BM25 keys on it directly.",
    },
    {
        "question": "How does fault isolation across Availability Zones work?",
        "answer_section": "Change and Failure Management",
        "why": "Z2: 'Availability Zones' and 'fault isolation' are precise literal phrases unique to this section.",
    },
]

#quick sanity print so running the file shows what is built
if __name__ == "__main__":
    print(f"Eval set holds {len(eval_questions)} qustions:\n")
    for i,q in enumerate(eval_questions, start=1):
        print(f"{i}, {q['question']}")
        print(f"  -> correct question {q['answer_section']}")
        print()