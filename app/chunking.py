import tiktoken
from app.loaders import load_documents

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=300, overlap=50):
    """
    Splits text into chunks of roughly `chunk_size` tokens,
    with `overlap` tokens repeated between consecutive chunks.
    """
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text_piece = encoding.decode(chunk_tokens)
        chunks.append(chunk_text_piece)
        start += chunk_size - overlap

    return chunks

def chunk_documents(documents, chunk_size=300, overlap=50):
    """
    Takes loaded documents (with filename/title/content) and returns
    a flat list of chunks, each with metadata attached.
    """
    all_chunks = []

    for doc in documents:
        text_chunks = chunk_text(doc["content"], chunk_size, overlap)

        for i, chunk in enumerate(text_chunks):
            all_chunks.append({
                "chunk_id": f"{doc['filename']}_{i}",
                "source": doc["filename"],
                "title": doc["title"],
                "chunk_index": i,
                "text": chunk
            })

    return all_chunks

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)

    print(f"Loaded {len(docs)} documents, produced {len(chunks)} total chunks.\n")
    print("Example chunk metadata:")
    print(f"  chunk_id: {chunks[0]['chunk_id']}")
    print(f"  source: {chunks[0]['source']}")
    print(f"  title: {chunks[0]['title']}")
    print(f"  chunk_index: {chunks[0]['chunk_index']}")
    print(f"  text preview: {chunks[0]['text'][:150]}...")