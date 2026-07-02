from app.retrieval import search
from app.llm import get_grounded_response

def ask(question, top_k=3):
    """
    Full RAG flow: retrieve relevant chunks, then generate a grounded answer.
    """
    results = search(question, top_k=top_k)

    # Reformat ChromaDB results into simple chunk dicts
    retrieved_chunks = []
    for i in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "title": results["metadatas"][0][i]["title"],
            "text": results["documents"][0][i]
        })

    answer = get_grounded_response(question, retrieved_chunks)
    return answer, retrieved_chunks

if __name__ == "__main__":
    question = "How do I set up social login with Google?"
    answer, sources = ask(question)

    print(f"Question: {question}\n")
    print(f"Answer:\n{answer}\n")
    print("Sources used:")
    for chunk in sources:
        print(f"  - {chunk['title']}")