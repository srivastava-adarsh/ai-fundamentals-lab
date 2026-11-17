from score import get_top_sections, evaluate, recall_at_k, mrr
from bm25_search import get_top_sections_bm25

vector_ranks = evaluate(get_top_sections)
bm25_ranks = evaluate(get_top_sections_bm25)

print(f"{'Q':>3} {'vector' :>7} {'bm25' :>6}")
for i, (v,b) in enumerate(zip(vector_ranks, bm25_ranks), start=1):
    print(f"{i:>3} {str(v):>7} {str(b):>6}")

print()
for name, ranks in (("vector", vector_ranks), ("bm25", bm25_ranks)):
    print(
        f"{name:7}  "
        f"r@1={recall_at_k(ranks,1):.2f}  "
        f"r@3={recall_at_k(ranks,3):.2f}  "
        f"r@5={recall_at_k(ranks,5):.2f}  "
        f"MRR={mrr(ranks):.3f}   "
    )