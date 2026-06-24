# ============================================
# chunker.py - Text Chunking Module
# AI Powered Smart Study Assistant
# ============================================

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """
    Split text into overlapping chunks
    Args:
        text: Full text to split
        chunk_size: Max characters per chunk (default 500)
        chunk_overlap: Overlap between chunks (default 50)
    Returns:
        List of text chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    print(f"Created {len(chunks)} chunks")
    return chunks