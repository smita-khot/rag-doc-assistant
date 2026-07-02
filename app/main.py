from app.rag import ask, format_answer_with_citations

def main():
    print("RAG Document Assistant — type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        answer, sources = ask(user_input)
        response = format_answer_with_citations(answer, sources)
        print(f"\nAI: {response}\n")

if __name__ == "__main__":
    main()