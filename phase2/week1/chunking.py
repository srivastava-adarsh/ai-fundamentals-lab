##ead the document
with open("sample_doc.txt", "r") as f:
    text = f.read().strip()

print(f"Total document length: {len(text)} characters\n")

#Naive fixed size chunking - cut every N characters
def chunk_fixed(text,size):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i + size])
    return chunks

chunks = chunk_fixed(text, 150)

print(f"Split into {len(chunks)} chunks of ~150 charcaters each\n")

for idx, chunk in enumerate(chunks):
    print(f"-----Chunk {idx} ------")
    print(repr(chunk))
    print()

#Strategy 2: Split on sentences
def chunk_by_sentence(text):
    #Split on ". "
    sentences = text.replace("\n", " ").split(". ")
    #Re-add the peiod that split removed
    chunks = []
    for s in sentences:
        s = s.strip()
        if s:
            if not s.endswith("."):
                s = s + "."
            chunks.append(s)
    return chunks
    
print("\n====SENTENCE AWARE CHUNKING =====\n")
sentence_chunks = chunk_by_sentence(text)
print(f"Split into {len(sentence_chunks)} sentence chunks: \n")
for idx, chunk in enumerate(sentence_chunks):
    print(f"----Chunk{idx}----")
    print(chunk)
    print()

#Strategy 3: fixed size chunk with overlap
def chunks_with_overlap(text, size, overlap):
    text = text.replace("\n"," ")
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end-overlap
    return chunks

print("====CHUNKING WITh OVERLAP----")
overlap_chunks = chunks_with_overlap(text, 150, 30)
print(f"Split into {len(overlap_chunks)} overlapping chunks (size 150, overlap 30): \n ")
for idx, chunk in enumerate(overlap_chunks):
    print(f"----chunk {idx} ----")
    print(repr(chunk))
    print()

