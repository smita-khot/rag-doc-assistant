# LLM Basics — Notes

## Tokens
When you send text to an AI, it doesn't read it as whole words or sentences — it breaks it into smaller pieces called tokens. The AI's usage and cost are measured by how many tokens are used, not by word or character count.

## Context Window
This is the maximum number of tokens an AI can handle at once — including the text you send it AND its reply. If the total goes over this limit, it won't all fit, so some of it gets cut off or the request fails.

## Temperature
A setting that controls how random or predictable the AI's answers are. A lower value makes answers more consistent and focused. A higher value makes answers more varied and creative.

## Embeddings
A way of converting text into numbers that represent its meaning. Text with similar meaning gets converted into similar numbers, which lets the AI compare pieces of text and find related ones.

## Grounded Prompting
Telling the AI to answer ONLY using specific text I provide, instead of its own general knowledge.
This matters for my RAG project because I want answers based on my documents, not made-up facts.

Tested 5 prompt variations:
1. No context given -> AI admitted it didn't know (didn't hallucinate)
2. Context given, no strict instruction -> answered correctly
3. Strict "answer only using this text" instruction -> answered correctly and concisely
4. Strict instruction + "say I don't know if not in text" + question NOT in text -> correctly said "I don't know" instead of guessing
5. Strict instruction + "say I don't know if not in text" + question IS in text -> answered correctly

Key takeaway: giving explicit permission to say "I don't know" prevents the AI from guessing when it lacks the answer. This is the fallback behavior I'll need for my RAG assistant .

# Data Source

Documents: Supabase Authentication documentation
Source: https://github.com/supabase/supabase (apps/docs/content/guides/auth)
License: Supabase docs are open source
Collected: July 2, 2026
Count: 32 files (.mdx format)

## Chunking Experiment 
Tested chunk_size=300/overlap=50 vs chunk_size=150/overlap=30 on a 766-token document.

- 300 tokens -> 4 chunks (last chunk very small: 16 tokens)
- 150 tokens -> 7 chunks (last chunk still small: 46 tokens, but less extreme)

Observations:
- Smaller chunks = more precise retrieval (each chunk is more topic-focused) but more chunks to store and search
- Trailing small chunks happen regardless of chunk size - it's a structural side effect of fixed-size splitting, not something size alone fixes
- Smaller chunks risk losing surrounding context (sentences can end awkwardly without the next chunk)

Decision: using chunk_size=300, overlap=50 as the default - balances context retention with retrieval precision.

## Vector Search Test (July 13)
Stored 311 chunks with embeddings in ChromaDB. Tested retrieval with two queries:

1. "How does multi-factor authentication work?" -> all 3 results correctly came from the MFA document, 
   even though the query never said "MFA" -> proves semantic search works, not just keyword matching.

2. "How can I add an extra security step when users log in?" (vaguer phrasing) -> only 1 of 3 results 
   was clearly relevant (MFA); the other 2 (OAuth server, Users) were topically related but not on-target.

Observation: retrieval quality depends heavily on how specific/clear the query is. Vague questions 
retrieve vaguely-related results. This is expected and something to watch for when testing with 
real questions later (July 19).