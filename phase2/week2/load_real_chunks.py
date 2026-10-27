import os
os.environ["HF_HUB_OFFLINE"] = "1"

import chromadb
from chromadb.utils import embedding_functions

sections = [
    ("Reliability Overview",
    "The Reliability pillar encompasses the ability of a workload to perform "
    "its intended function correctly and consistently when it is expected to. "
    "A resilient workload recovers quickly from failures to meet business and "
    "customer demand."),
    ("Foundational Requirements",
    "Foundational requirements extend beyond a single workload. Before "
    "architecting any system, ensure you have sufficient network bandwidth. "
    "Amazon Web Services provides service quotas, also called limits."),
    ("Change and Failure Management",
    "Change management is how you monitor and respond to changes in demand. "
    "Failure management includes backing up data, designing for fault "
    "isolation, and planning for disaster recovery."),
]

def chunk_sections(sections, size, overlap, source):
    chunks = []
    chunk_id = 0
    for section_name, section_text in sections:
        section_text = section_text.replace("\n"," ")
        start = 0
        while start < len(section_text):
            end = start + size
            chunk_text = section_text[start:end]
            chunk = {
                "id" : chunk_id,
                "text" : chunk_text,
                "source" : source,
                "section" : section_name,
                "start_char" : start,
                "end_char" : min(end, len(section_text)),
            }
            chunks.append(chunk)
            chunk_id +=1
            start = end - overlap
    return chunks


chunks = chunk_sections(sections, size=150, overlap=30, source="sample_doc.txt")
print(f"Produced {len(chunks)} chunks")

for c in chunks:
    print(f"[id={c['id']}] section='{c['section']}' chars {c['start_char']}-{c['end_char']}")


my_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="chroma_store")

collection = client.get_or_create_collection(
    name="well_architected",
    embedding_function=my_embedder,
)

print(f"Collection '{collection.name}' ready, currently holds {collection.count()} items")


documents = [c["text"] for c in chunks]
ids = [str(c["id"]) for c in chunks]
metadatas = [
    {"section": c["section"], "source": c["source"]} for c in chunks
]

collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas,
)

print(f"Added chunks. Collection now holds {collection.count()} items")


query = "How do I recover when my system fails?"

results = collection.query(
    query_texts=[query],
    n_results=3,
)

print(f"\n----Query {query} ----\n")
for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    print(f"[section='{meta['section']}' distance={dist:.4f}  ]")
    print(doc)
    print()

filtered_query = "How do I recover when my system fails?"

filtered_results = collection.query(
    query_texts=[filtered_query],
    n_results=3,
    where={"section": "Foundational Requirements"},
)

print(f"\n--- Same query, filtered to section = 'Foundational Requirements'----\n ")

for doc, meta, dist in zip(
    filtered_results["documents"][0],
    filtered_results["metadatas"][0],
    filtered_results["distances"][0],
):
    print(f"[section='{meta['section']}' distance={dist:.4f}]")
    print(doc)
    print()



