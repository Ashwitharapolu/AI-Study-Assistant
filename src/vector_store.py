# ============================================
# vector_store.py - FAISS Vector Store Module
# AI Powered Smart Study Assistant
# ============================================
import faiss
import numpy as np
import pickle
import os
from embeddings import get_embeddings

def build_index(embeddings):
    """Store embeddings in FAISS index"""
    embeddings = np.array(embeddings).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_index(index, chunks, path="faiss_index"):
    """Save FAISS index and chunks to disk"""
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, f"{path}/index.faiss")
    with open(f"{path}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    print(f"Index saved to {path}/")

def load_index(path="faiss_index"):
    """Load FAISS index and chunks from disk"""
    index = faiss.read_index(f"{path}/index.faiss")
    with open(f"{path}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def search(query, index, chunks, model, k=5):
    """Search for top k most relevant chunks"""
    query_vector = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vector, k)
    results = [chunks[i] for i in indices[0]]
    return results

def search_mmr(query, index, chunks, model, k=5, fetch_k=20):
    """MMR Search - finds relevant AND diverse chunks"""
    # Convert query to vector
    query_vector = model.encode([query]).astype('float32')

    # Fetch more candidates first
    distances, indices = index.search(query_vector, min(fetch_k, index.ntotal))

    # Get candidate chunks and their vectors
    candidate_indices = indices[0].tolist()
    candidate_chunks = [chunks[i] for i in candidate_indices]

    # Get embeddings for candidates
    candidate_embeddings = model.encode(candidate_chunks).astype('float32')
    query_vec = query_vector[0]

    # MMR selection
    selected = []
    remaining = list(range(len(candidate_indices)))

    while len(selected) < k and remaining:
        if not selected:
            # First selection - most relevant to query
            scores = [
                np.dot(query_vec, candidate_embeddings[i]) /
                (np.linalg.norm(query_vec) * np.linalg.norm(candidate_embeddings[i]) + 1e-8)
                for i in remaining
            ]
            best = remaining[np.argmax(scores)]
        else:
            # Subsequent selections - balance relevance and diversity
            mmr_scores = []
            for i in remaining:
                relevance = np.dot(query_vec, candidate_embeddings[i]) / \
                    (np.linalg.norm(query_vec) * np.linalg.norm(candidate_embeddings[i]) + 1e-8)

                redundancy = max([
                    np.dot(candidate_embeddings[i], candidate_embeddings[s]) /
                    (np.linalg.norm(candidate_embeddings[i]) * np.linalg.norm(candidate_embeddings[s]) + 1e-8)
                    for s in selected
                ])

                mmr_score = 0.7 * relevance - 0.3 * redundancy
                mmr_scores.append(mmr_score)

            best = remaining[np.argmax(mmr_scores)]

        selected.append(best)
        remaining.remove(best)

    return [chunks[candidate_indices[i]] for i in selected]