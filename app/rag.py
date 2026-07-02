from app.retrieval import search
from app.llm import get_grounded_response

DISTANCE_THRESHOLD = 1.3  # lower = more similar; tune this based on testing

def ask(question, top_k=3):
    results = search(question, top_k=top_k)

    # Check if even the best match is too weak
    best_distance = results["distances"][0][0]
    if best_distance > DISTANCE_THRESHOLD:
        return "I don't know based on the provided documents. No sufficiently relevant information was found.", []

    retrieved_chunks = []
    for i in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "title": results["metadatas"][0][i]["title"],
            "text": results["documents"][0][i]
        })

    answer = get_grounded_response(question, retrieved_chunks)
    return answer, retrieved_chunks

def format_answer_with_citations(answer, sources):
    if not sources:
        return answer  # no sources to cite if fallback triggered

    unique_titles = []
    for chunk in sources:
        if chunk["title"] not in unique_titles:
            unique_titles.append(chunk["title"])

    citations = "\n".join(f"  - {title}" for title in unique_titles)
    return f"{answer}\n\nSources:\n{citations}"

if __name__ == "__main__":
    test_questions = [
        "How do I invalidate a user's session?",
        "What's the best pizza topping?",
    ]

    for question in test_questions:
        answer, sources = ask(question)
        response = format_answer_with_citations(answer, sources)
        print(f"Question: {question}\n{response}\n{'-'*60}\n")