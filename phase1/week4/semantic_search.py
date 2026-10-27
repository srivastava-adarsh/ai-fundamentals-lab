from sentence_transformers import SentenceTransformer, util

print("Loading model")
model = SentenceTransformer('all-miniLM-L6-v2')
print("Model Loaded")

#A small knowledge base
documents = [
    "Python is a popular programming language for data science.",
    "The great wall of china is visible from space",
    "Dogs are loyal animals and make great pets",
    "Machine learning moels require large amount of training data",
    "Cats are independent and often aloof pets.",
]

#Embed all documents at once
print("Embedding documents")
doc_vectors = model.encode(documents)
print(f"Indexed {len(documents)} documents.")

def search(query, top_k=3):
    #Embed the query
    query_vector = model.encode(query)

    #Compare query to every document
    scores = util.cos_sim(query_vector, doc_vectors)[0]

    #Pair each document with its score
    results = []
    for i in range(len(documents)):
        results.append((scores[i].item(), documents[i]))

    #Sort by score, highest first
    results.sort(reverse=True)

    #Return the top_k best matches
    return results[:top_k]

#Try a query
query = "Tell me about pet animals"
print(f"\nQuery: {query}\n")
matches = search(query)
for score, doc in matches:
    print(f" {score:.3f}. {doc}")


