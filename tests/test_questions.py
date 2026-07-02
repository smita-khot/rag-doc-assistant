from app.rag import ask, format_answer_with_citations

test_questions = [
    "How does multi-factor authentication work?",
    "How do I reset a user's password?",
    "What's the difference between a magic link and a one-time password?",
    "How does Supabase handle rate limiting for auth requests?",
    "How do I invalidate a user's session?",
    "What is a JWT and what claims does it contain?",
    "How do I set up social login with Google?",
    "What is a passkey and how does it work?",
    "How does phone-based login work?",
    "Can a user have multiple identities linked to one account?",
]

if __name__ == "__main__":
    results = []

    for i, question in enumerate(test_questions, 1):
        answer, sources = ask(question)
        response = format_answer_with_citations(answer, sources)

        print(f"\n{'='*60}")
        print(f"Q{i}: {question}")
        print('='*60)
        print(response)

        results.append({
            "question": question,
            "answer": answer,
            "sources": [s["title"] for s in sources]
        })

    # Save results to a file for review
    import json
    with open("eval/july19_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nSaved {len(results)} results to eval/july19_test_results.json")