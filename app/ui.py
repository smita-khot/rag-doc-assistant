import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.rag import ask, format_answer_with_citations

import streamlit as st
from app.rag import ask, format_answer_with_citations

st.set_page_config(page_title="RAG Document Assistant", page_icon="📚")

st.title("📚 RAG Document Assistant")
st.caption("Ask questions about Supabase Authentication documentation")

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask a question about Supabase Auth..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            answer, sources = ask(question)
            response = format_answer_with_citations(answer, sources)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})