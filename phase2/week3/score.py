import os
os.environ["HF_HUB_OFFLINE"] = "1"

import chromadb
from chromadb.utils import embedding_functions

my_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="chroma_store")

collection = client.get_collection(
    name="well_architected",
    embedding_function=my_embedder,
)

def get_top_sections(question, k=5):
    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    return [meta["section"] for meta in results ["metadatas"][0]]

def is_hit(answer_section, retrieved_section):
    return answer_section in retrieved_section 


def first_hit_rank(answer_section, retrieved_sections):
    if answer_section in retrieved_sections:
        return retrieved_sections.index(answer_section) + 1
    return None

def recall_at_k(ranks, k):
    if not ranks:
        return 0.0
    hits = sum(1 for r in ranks if r is not None and r<=k)
    return hits / len(ranks)


def mrr(ranks):
    total = sum(1 / r for r in ranks if r is not None)
    return total / len(ranks)

if __name__ == "__main__":
    from eval_set import eval_questions

    ranks = []
    for i, q in enumerate(eval_questions, start=1):
        retrieved = get_top_sections(q["question"])
        rank = first_hit_rank(q["answer_section"], retrieved)
        ranks.append(rank)
        print(f"Q{i:>2}  rank={rank}  expected={q['answer_section']}") 

    print()
    print(f"recall@1 = {recall_at_k(ranks,1):.2f}")
    print(f"recall@3 = {recall_at_k(ranks,3):.2f}")
    print(f"recall@5 = {recall_at_k(ranks,5):.2f}")

    print(f"MRR     = {mrr(ranks):.3f}")