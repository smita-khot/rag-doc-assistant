from app.retrieval import search
from app.llm import get_grounded_response

DISTANCE_THRESHOLD = 1.3
CHUNK_DISTANCE_THRESHOLD = 1.5  # slightly looser than the overall fallback threshold

def ask(question, top_k=5):
    # Retrieve more candidates than we need, so we can filter down to the best diverse set
    results = search(question, top_k=top_k)

    best_distance = results["distances"][0][0]
    if best_distance > DISTANCE_THRESHOLD:
        return "I don't know based on the provided documents. No sufficiently relevant information was found.", []

    seen_titles = set()
    retrieved_chunks = []

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        title = results["metadatas"][0][i]["title"]

        # Skip chunks that are too weakly related
        if distance > CHUNK_DISTANCE_THRESHOLD:
            continue

        # Skip if we already have a chunk from this same document (prioritize diversity)
        if title in seen_titles:
            continue

        retrieved_chunks.append({
            "title": title,
            "text": results["documents"][0][i]
        })
        seen_titles.add(title)

        if len(retrieved_chunks) >= 3:
            break

    if not retrieved_chunks:
        return "I don't know based on the provided documents. No sufficiently relevant information was found.", []

    answer = get_grounded_response(question, retrieved_chunks)
    return answer, retrieved_chunks

def format_answer_with_citations(answer, sources):
    if not sources:
        return answer

    unique_titles = []
    for chunk in sources:
        if chunk["title"] not in unique_titles:
            unique_titles.append(chunk["title"])

    citations = "\n".join(f"  - {title}" for title in unique_titles)
    return f"{answer}\n\nSources:\n{citations}"

if __name__ == "__main__":
    test_questions = [
        "How do I invalidate a user's session?",
    ]

    for question in test_questions:
        answer, sources = ask(question)
        response = format_answer_with_citations(answer, sources)
        print(f"Question: {question}\n{response}\n{'-'*60}\n")