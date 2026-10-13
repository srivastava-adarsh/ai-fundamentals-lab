import os
os.environ["HF_HUB_OFFLINE"] = "1"

import chromadb

#1. Create a chroma client that saves to disk
client = chromadb.PersistentClient(path="./chroma_store")

#2. Create or get a collection
collection = client.get_or_create_collection(name="reliability_docs")

#3. Add a few chunks
collection.add(
    ids=["0", "1", "2"],
    documents=[
        "A resilient workload recovers quickly from failures.",
        "Amazon web services provides service quotas, also called limits", 
        "Change management is how you monitor and respond to changes in demand",
    ],
    metadatas=[
        {"source":"sample_doc.txt", "section": "Reliability Overview"},
        {"source":"sample_doc.txt", "section": "Foundational Requirements"},
        {"source": "sample_doc.txt", "section": "Change and Failure Management"},
    ],
)

#4. Confirm what is stored
print(f"Collection '{collection.name}' now holds {collection.count()} chunks")

#5. Query the collection by meaning
results = collection.query(
    query_texts=["How do I handle recovering from outages?"],
    n_results=2,
)

print("\n---Query: How do I handle recovering from outages?----\n")
for i in range(len(results["ids"][0])):
    print(f"Rank {i+1}:")
    print(f" id  = {results['ids'][0][i]} ")
    print(f" document  = {results['documents'][0][i]}")
    print(f" section  = {results['metadatas'][0][i]['section']}")
    print(f" disctance = {results['distances'][0][i]}")
    print()

#6. Query by meaning , but ONLY within a chosen section
filtered = collection.query(
    query_texts = ["How do I handle recovering from outages"],
    n_results=2,
    where={"section": "Foundational Requirements"}
)

print("\n---Same query, filtered to section = 'Foundational Requirements'----\n")
for i in range(len(filtered["ids"][0])):
    print(f"Rank {i+1}:")
    print(f" id  = {filtered['ids'][0][i]}")
    print(f" document  = {filtered['documents'][0][i]} ")
    print(f" section. =  {filtered['metadatas'][0][i]['section']}")
    print(f" distance =  {filtered['distances'][0][i]}")
    print()


from chromadb.utils import embedding_functions

my_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)