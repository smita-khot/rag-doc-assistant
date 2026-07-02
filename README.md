# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) system that answers natural language questions over company/product documentation, with source citations and hallucination-resistant fallback behavior.

Built as a hands-on project to learn and demonstrate core LLM engineering skills: document processing, embeddings, vector search, grounded prompting, and evaluation.

## Demo

*(Screenshot or GIF goes here)*

## Features

- **Grounded Q&A** — answers are generated strictly from retrieved document content, not general LLM knowledge
- **Source citations** — every answer shows which documents it was based on
- **Hallucination prevention** — a distance-based confidence check rejects the query before calling the LLM if no genuinely relevant content is found, instead of guessing
- **Dynamic file upload** — users can upload new `.txt`/`.md` documents, which are immediately chunked, embedded, and made searchable — no restart required
- **Diverse, deduplicated retrieval** — filters out redundant chunks from the same document and weakly-relevant matches, prioritizing topical diversity in citations
- **Web UI** — clean chat interface built with Streamlit

## Architecture
Documents (.mdx/.txt/.md)
↓
Loader (parses frontmatter, extracts clean text)
↓
Chunker (splits into ~300-token chunks with overlap, adds metadata)
↓
Embedder (sentence-transformers, runs locally, 384-dim vectors)
↓
Vector Store (ChromaDB, persisted to disk)
↓
User Question → Embed → Similarity Search → Top Relevant Chunks
↓
Grounded Prompt (question + retrieved chunks + instructions)
↓
LLM (Groq, Llama 3.1) → Answer + Sources

## Tech Stack

| Component | Tool | Why |
|---|---|---|
| LLM | Groq (Llama 3.1 8B) | Free tier, fast inference, no billing required |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Runs locally, no API cost or rate limits |
| Vector store | ChromaDB | Simple, persistent, works well at this scale |
| UI | Streamlit | Fast to build, clean chat interface out of the box |
| Language | Python | Ecosystem fit for LLM/ML tooling |

## Setup

1. Clone the repo:
```bash
   git clone https://github.com/smita-khot/rag-doc-assistant.git
   cd rag-doc-assistant
```

2. Create a virtual environment and install dependencies:
```bash
   python -m venv venv
   venv\Scripts\Activate.ps1   # Windows
   pip install -r requirements.txt
```

3. Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys)

4. Create a `.env` file (see `.env.example`):
GROQ_API_KEY=your-key-here

5. Build the vector store from the included documents:
```bash
   python -m app.embeddings
   python -m app.retrieval
```

## Usage

**Command-line chat:**
```bash
python -m app.main
```

**Web UI:**
```bash
streamlit run app/ui.py --server.fileWatcherType none
```

Then open `http://localhost:8501` in your browser. Ask questions about Supabase Authentication (the included document set), or upload your own `.txt`/`.md` documents to query them instead.

## Evaluation

A 15-question evaluation set with expected answers is included in `eval/questions.json`. Running the assistant against this set achieved **14/15 (93%) accuracy** on a manual good/partial/bad review — see `eval/evaluation_results.json` for full results.

To re-run the evaluation:
```bash
python -m eval.run_evaluation
```

## Project Structure
rag-doc-assistant/
├── app/
│   ├── loaders.py       # Document loading, frontmatter parsing
│   ├── chunking.py      # Token-based chunking with metadata
│   ├── embeddings.py    # Local embedding generation
│   ├── retrieval.py     # Vector storage and semantic search
│   ├── llm.py           # LLM API calls, grounded prompting
│   ├── rag.py           # Full retrieval + generation pipeline
│   ├── ui.py            # Streamlit web interface
│   └── main.py          # CLI interface
├── data/
│   ├── raw/             # Source documents (Supabase Auth docs)
│   └── processed/       # Chunks with embeddings, vector DB
├── eval/                # Evaluation set and results
├── notes/               # Development notes and learnings
└── tests/               # Test scripts

## What I Learned

This project was built to develop practical RAG engineering skills, including:
- Tradeoffs in chunk size, overlap, and retrieval diversity
- Balancing grounding strictness against false "I don't know" responses
- Debugging retrieval failures back to root causes (including a real data collection gap)
- Building evaluation processes with objective, testable ground truth

Full development notes and decision log available in `notes/`.

## License

MIT