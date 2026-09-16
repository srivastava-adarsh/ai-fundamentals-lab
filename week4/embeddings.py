from sentence_transformers import SentenceTransformer
from sentence_transformers import util


#Load the miniLLM embedding model
print("Loading model....")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model Loaded")

#Part -1: Embded a single sentence and inspect it
sentence = "The dog barked loudly."
vector = model.encode(sentence)

print(f"\nSentence: {sentence}")
print(f"Vector Type: {type(vector)}")
print(f"Vector Length (dimensions): {len(vector)}")
print(f"First 10 numbers: {vector[:10]}")

#PART 2: COMPARE MEANINGS OF SEVERAL SENTENCES
sentences = [""
    "The dog barked loudly.",
    "TRhe puppy made noise.",
    "I filed my tax return",
]

vectors = model.encode(sentences)
print(f"\nEmbded {len(sentences)} sentences, each {len(vectors[0])} dimensions.")

#Compare each pair with cosine similarity
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        similarity = util.cos_sim(vectors[i], vectors[j]).item()
        print(f"\n '{sentences[i]} ")
        print(f". '{sentences[j]} ")
        print(f"similarity: {similarity:.3f}")

