"""
Simple RAG Utility - retrieves relevant chunks from service_standards.txt
"""

def load_standards(filepath: str = "data/service_standards.txt") -> list:
    """Load service standards and split into sections."""
    with open(filepath, "r") as f:
        content = f.read()
    # Split by blank lines into chunks
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks


def retrieve(query: str, chunks: list, top_k: int = 3) -> str:
    """
    Basic keyword-based retrieval (no vector DB needed for basic level).
    Returns the top_k most relevant chunks based on keyword overlap.
    """
    query_words = set(query.lower().split())

    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        # Score = number of matching words
        score = len(query_words & chunk_words)
        scored.append((score, chunk))

    # Sort by score descending, return top_k
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for score, chunk in scored[:top_k] if score > 0]

    if not top_chunks:
        return "No relevant standards found."
    return "\n\n".join(top_chunks)
