from app.retrieval import search

test_queries = [
    "How do I reset a user's password?",
    "What is a JWT?",
    "How does social login work?",
    "What happens when a session expires?",
    "Can users sign in without a password?",
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)

    results = search(query, top_k=2)

    for i in range(len(results["ids"][0])):
        title = results["metadatas"][0][i]["title"]
        text_preview = results["documents"][0][i][:150]
        print(f"\n  Result {i+1}: {title}")
        print(f"  {text_preview}...")