import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag import ask, format_answer_with_citations

def load_eval_set(path="eval/questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_evaluation():
    eval_set = load_eval_set()
    results = []

    for item in eval_set:
        answer, sources = ask(item["question"])

        results.append({
            "id": item["id"],
            "question": item["question"],
            "expected_answer": item["expected_answer"],
            "actual_answer": answer,
            "sources": [s["title"] for s in sources],
            "grade": None  # to be filled in manually
        })

        print(f"\n{'='*60}")
        print(f"Q{item['id']}: {item['question']}")
        print('='*60)
        print(f"Expected: {item['expected_answer']}")
        print(f"\nActual: {answer}")
        print(f"\nSources: {', '.join(s['title'] for s in [] ) if not sources else ', '.join(s['title'] for s in sources)}")

    with open("eval/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nSaved {len(results)} results to eval/evaluation_results.json")
    print("Next: manually review each and fill in 'grade': 'good' / 'partial' / 'bad'")

if __name__ == "__main__":
    run_evaluation()