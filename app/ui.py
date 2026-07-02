import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.rag import ask, format_answer_with_citations

st.set_page_config(page_title="RAG Document Assistant", page_icon="📚")

st.title("📚 RAG Document Assistant")
st.caption("Ask questions about Supabase Authentication documentation")

# File upload section
uploaded_file = st.file_uploader("Upload a document to add it to the knowledge base", type=["txt", "md"])

if uploaded_file is not None:
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    if uploaded_file.name not in st.session_state.processed_files:
        content = uploaded_file.read().decode("utf-8")
        from app.retrieval import add_uploaded_document
        with st.spinner(f"Processing {uploaded_file.name}..."):
            num_chunks = add_uploaded_document(uploaded_file.name, content)
        st.success(f"Added '{uploaded_file.name}' ({num_chunks} chunks) to the knowledge base!")
        st.session_state.processed_files.add(uploaded_file.name)

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