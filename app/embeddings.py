from sentence_transformers import SentenceTransformer

# This downloads a small pretrained model the first time you run it (~80MB), then reuses it locally
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks):
    """
    Takes a list of chunk dicts (with a 'text' field) and adds an 'embedding' field to each.
    """
    texts = [chunk["text"] for chunk in chunks]
    
    # encode() converts a list of texts into a list of embedding vectors
    vectors = model.encode(texts, show_progress_bar=True)

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector.tolist()  # convert numpy array to plain list for easy storage later

    return chunks

if __name__ == "__main__":
    import json
    from app.loaders import load_documents
    from app.chunking import chunk_documents

    docs = load_documents()
    chunks = chunk_documents(docs)
    chunks_with_embeddings = generate_embeddings(chunks)

    print(f"Generated embeddings for {len(chunks_with_embeddings)} chunks.\n")
    example = chunks_with_embeddings[0]
    print(f"Chunk: {example['chunk_id']}")
    print(f"Embedding vector length: {len(example['embedding'])}")
    print(f"First 5 numbers of the vector: {example['embedding'][:5]}")

    # Save to disk so we don't have to regenerate embeddings every time
    output_path = "data/processed/chunks_with_embeddings.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks_with_embeddings, f)

    print(f"\nSaved {len(chunks_with_embeddings)} chunks with embeddings to {output_path}")