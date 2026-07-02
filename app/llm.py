import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

def get_response(messages, temperature=0.2, model="llama-3.1-8b-instant"):
    """
    Send a prompt to the LLM and return its text response.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def get_grounded_response(question, retrieved_chunks, temperature=0.2, model="llama-3.1-8b-instant"):
    context = "\n\n".join(
        f"[Source: {chunk['title']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""Answer the question using the information in the context below. You may paraphrase 
and combine information across the context, but do not introduce facts that aren't supported by it.
If the context genuinely doesn't contain relevant information to answer the question, say 
"I don't know based on the provided documents."

Context:
{context}

Question: {question}

Answer:"""

    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content