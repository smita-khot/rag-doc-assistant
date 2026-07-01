from app.chat_history import add_message, load_history, save_history
from app.llm import get_response

def main():
    print("Simple LLM chat — type 'exit' to quit\n")
    history = load_history()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            save_history(history)
            print("Conversation Saved. GoodBye!!")
            break
        history = add_message(history,"user",user_input)
        answer = get_response(history)
        history = add_message(history,"assistant",answer)
        print(f"AI: {answer}\n")

if __name__ == "__main__":
    main()