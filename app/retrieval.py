import json
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent client saves the database to disk, so it survives between runs
client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = client.get_or_create_collection(name="supabase_auth_docs")

def load_chunks_with_embeddings(path="data/processed/chunks_with_embeddings.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def store_chunks(chunks):
    """
    Adds all chunks (with their precomputed embeddings) into the ChromaDB collection.
    """
    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {"source": chunk["source"], "title": chunk["title"], "chunk_index": chunk["chunk_index"]}
            for chunk in chunks
        ]
    )

def search(query, top_k=3):
    """
    Embeds the query and returns the top_k most similar chunks.
    """
    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

if __name__ == "__main__":
    # Only store chunks if the collection is empty (avoid duplicate inserts on repeated runs)
    if collection.count() == 0:
        chunks = load_chunks_with_embeddings()
        store_chunks(chunks)
        print(f"Stored {len(chunks)} chunks in the vector database.\n")
    else:
        print(f"Collection already has {collection.count()} chunks. Skipping insert.\n")

    # Test search
    test_query = "How can I add an extra security step when users log in?"
    results = search(test_query)

    print(f"Query: {test_query}\n")
    for i in range(len(results["ids"][0])):
        print(f"--- Result {i+1} ---")
        print(f"Source: {results['metadatas'][0][i]['title']}")
        print(f"Text: {results['documents'][0][i][:200]}...\n")