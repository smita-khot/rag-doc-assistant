import os
import re

RAW_DATA_DIR = "data/raw"

def parse_frontmatter(text):
    """
    Splits frontmatter (YAML between --- markers) from the main content.
    Returns (title, content_without_frontmatter).
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return None, text  # no frontmatter found

    frontmatter, content = match.groups()

    # Extract just the title field from frontmatter
    title_match = re.search(r"title:\s*['\"]?(.*?)['\"]?\s*$", frontmatter, re.MULTILINE)
    title = title_match.group(1) if title_match else None

    return title, content.strip()

def load_documents(folder_path=RAW_DATA_DIR):
    """
    Load all .mdx files from the given folder.
    Returns a list of dicts: [{"filename": ..., "title": ..., "content": ...}, ...]
    """
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".mdx"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            title, content = parse_frontmatter(raw_text)

            documents.append({
                "filename": filename,
                "title": title or filename,  # fallback to filename if no title found
                "content": content
            })

    return documents

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.\n")
    print(f"Example — filename: {docs[0]['filename']}")
    print(f"Title: {docs[0]['title']}")
    print(f"First 300 characters of content:\n{docs[0]['content'][:300]}")