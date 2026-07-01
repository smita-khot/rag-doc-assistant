# LLM Basics — Notes

## Tokens
When you send text to an AI, it doesn't read it as whole words or sentences — it breaks it into smaller pieces called tokens. The AI's usage and cost are measured by how many tokens are used, not by word or character count.

## Context Window
This is the maximum number of tokens an AI can handle at once — including the text you send it AND its reply. If the total goes over this limit, it won't all fit, so some of it gets cut off or the request fails.

## Temperature
A setting that controls how random or predictable the AI's answers are. A lower value makes answers more consistent and focused. A higher value makes answers more varied and creative.

## Embeddings
A way of converting text into numbers that represent its meaning. Text with similar meaning gets converted into similar numbers, which lets the AI compare pieces of text and find related ones.