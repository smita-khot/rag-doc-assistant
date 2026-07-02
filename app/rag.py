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

def format_answer_with_citations(answer, sources):
    """
    Appends a clean, deduplicated list of sources to the answer.
    """
    unique_titles = []
    for chunk in sources:
        if chunk["title"] not in unique_titles:
            unique_titles.append(chunk["title"])

    citations = "\n".join(f"  - {title}" for title in unique_titles)
    return f"{answer}\n\nSources:\n{citations}"

if __name__ == "__main__":
    question = "How does multi-factor authentication work?"
    answer, sources = ask(question)

    full_response = format_answer_with_citations(answer, sources)
    print(f"Question: {question}\n")
    print(full_response)