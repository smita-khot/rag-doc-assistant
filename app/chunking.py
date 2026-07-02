import tiktoken

# Using a common encoding as an approximation (works well enough even for non-OpenAI models)
encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=300, overlap=50):
    """
    Splits text into chunks of roughly `chunk_size` tokens,
    with `overlap` tokens repeated between consecutive chunks
    to preserve context across chunk boundaries.
    """
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text_piece = encoding.decode(chunk_tokens)
        chunks.append(chunk_text_piece)
        start += chunk_size - overlap  # move forward, but overlap a bit

    return chunks

if __name__ == "__main__":
    from app.loaders import load_documents

    docs = load_documents()
    first_doc = docs[0]

    chunks = chunk_text(first_doc["content"])
    print(f"Document: {first_doc['title']}")
    print(f"Original length: {len(encoding.encode(first_doc['content']))} tokens")
    print(f"Split into {len(chunks)} chunks\n")

    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ({len(encoding.encode(chunk))} tokens) ---")
        print(chunk[:150] + "...\n")