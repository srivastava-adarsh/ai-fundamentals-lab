import os
os.environ["HF_HUB_OFFLINE"] = "1"

import re

import chromadb
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())

client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_collection(name="well_architected")

data = collection.get(include=["documents", "metadatas"])
chunk_texts = data["documents"]
chunk_sections = [meta["section"] for meta in data["metadatas"]]

tokenized_chunks = [tokenize(text) for text in chunk_texts]
bm25 = BM25Okapi(tokenized_chunks)

def get_top_sections_bm25 (question, k=5):
    scores = bm25.get_scores(tokenize(question))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [chunk_sections[i] for i in ranked[:k]]


if __name__ == "__main__":
    from eval_set import eval_questions

    for i in [0,12]:
        q = eval_questions[i]
        print(f"Q{i + 1}: {q['question']}")
        print(" expected: ", q["answer_section"])
        print("   BM25   :", get_top_sections_bm25(q["question"]))
