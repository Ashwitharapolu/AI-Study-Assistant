# ============================================
# embeddings.py - Embedding Generation Module
# AI Powered Smart Study Assistant
# ============================================

from sentence_transformers import SentenceTransformer

# Load model once at module level
# all-MiniLM-L6-v2 is free, fast and runs locally
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embeddings(chunks, show_progress=True):
    """
    Convert text chunks into vectors
    Args:
        chunks: List of text chunks
        show_progress: Show progress bar (default True)
    Returns:
        Numpy array of embeddings shape (n_chunks, 384)
    """
    print(f"Creating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=show_progress)
    print(f"Embeddings shape: {embeddings.shape}")
    return embeddings