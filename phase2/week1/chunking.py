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


#Strategy 4: Add metadata to each chunk
def chunk_with_metadata(text, size, overlap, source):
    text = text.replace("\n"," ")
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = start + size
        chunk_text = text[start:end]
        chunk = {
            "id": chunk_id,
            "text": chunk_text,
            "source": source,
            "start_char" : start, 
            "end_char": min(end, len(text)),
        }
        chunks.append(chunk)
        chunk_id +=1
        start = end - overlap
    return chunks

print("\n====CHUNKING WITH METADATA====\n")
meta_chunks = chunk_with_metadata(text, 150, 30, source="sample_doc.txt")
print(f"Split into {len(meta_chunks)} chunks with metadata:\n")
for chunk in meta_chunks:
    print(f"[id={chunk['id']}] source={chunk['source']} "
          f"chars {chunk['start_char']} - {chunk['end_char']} ")
    print(repr(chunk["text"]))
    print()


# Strategy 5: sections defined up front, then chunk within each section
  # We hand-label the document as (section_name, section_text) pairs.
sections = [
      ("Reliability Overview",
       "The Reliability pillar encompasses the ability of a workload to perform "
       "its intended function correctly and consistently when it is expected to. "
       "This includes the ability to operate and test the workload through its "
       "total lifecycle. A resilient workload recovers quickly from failures to "
       "meet business and customer demand. Key topics include distributed system "
       "design, recovery planning, and adapting to changing requirements."),
      ("Foundational Requirements",
       "Foundational requirements are those whose scope extends beyond a single "
       "workload or project. Before architecting any system, you must ensure that "
       "you have sufficient network bandwidth and other foundational requirements "
       "in place. Amazon Web Services provides service quotas, also referred to as "
       "limits, which are the maximum number of service resources or operations "
       "for your account."),
      ("Change and Failure Management",
       "Change management is how you monitor and respond to changes in demand. "
       "Failure management includes backing up data, designing for fault "
       "isolation, and planning for disaster recovery."),
  ]


def chunk_sections(sections, size, overlap, source):
    chunks = []
    chunk_id = 0
    for section_name, section_text in sections:
        section_text = section_text.replace("\n", " ")
        start = 0
        while start < len(section_text):
            end = start + size
            chunk_text = section_text[start:end]
            chunk = {
                "id": chunk_id,
                "text": chunk_text,
                "source": source,
                "section": section_name,
                "start_char": start,
                "end_char": min(end, len(section_text)),
            }
            chunks.append(chunk)
            chunk_id +=1
            start = end - overlap
    return chunks

print("\n===CHUNKING WITH SECTIONS====\n")
section_chunks = chunk_sections(sections, 150, 30, source="sample_doc.txt")
print(f"Split into {len(section_chunks)} chunks across {len(sections)} sections: \n")
for chunk in section_chunks:
    print(f"[id={chunk['id']}] section='{chunk['section']}' "
        f"chars {chunk['start_char']}-{chunk['end_char']}")
    print(repr(chunk["text"]))
    print()

def filter_by_section(chunks, section_name):
    return [c for c in chunks if c["section"] == section_name]

print("\n====SECTION FILTER: Only change and failure management ===\n")
subset = filter_by_section(section_chunks, "Change and Failure Management")
print(f"Filtered to {len(subset)} chunks (out of {len(section_chunks)} total):\n")
for chunk in subset:
    print(f"[id={chunk['id']}] section='{chunk['section']}'")
    print(repr(chunk["text"]))
    print()
