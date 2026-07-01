from app.llm import get_response

def main():
    print("Simple LLM chat — type 'exit' to quit\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        answer = get_response(user_input)
        print(f"AI: {answer}\n")

if __name__ == "__main__":
    main()