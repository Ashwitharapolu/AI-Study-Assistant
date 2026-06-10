import faiss
import numpy as np
import pickle
from embeddings import get_embeddings
from chunker import chunk_text
from pdf_loader import extract_text

def build_index(embeddings):
    """Store embeddings in FAISS index"""
    # Convert to float32 - FAISS requires this format
    embeddings = np.array(embeddings).astype('float32')
    
    # Get dimension - how many numbers per vector (384)
    dimension = embeddings.shape[1]
    
    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    
    # Add all vectors to index
    index.add(embeddings)
    
    return index

def save_index(index, chunks, path="faiss_index"):
    """Save FAISS index and chunks to disk"""
    import os
    os.makedirs(path, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(index, f"{path}/index.faiss")
    
    # Save chunks separately
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
    # Convert question to vector
    query_vector = model.encode([query]).astype('float32')
    
    # Search FAISS
    distances, indices = index.search(query_vector, k)
    
    # Return relevant chunks
    results = [chunks[i] for i in indices[0]]
    return results

# Test it
if __name__ == "__main__":
    from embeddings import model
    
    # Step 1 - Extract text
    print("Step 1 - Extracting text...")
    text = extract_text("data/sample.pdf")
    
    # Step 2 - Chunk it
    print("Step 2 - Chunking...")
    chunks = chunk_text(text)
    
    # Step 3 - Create embeddings
    print("Step 3 - Creating embeddings...")
    embeddings = get_embeddings(chunks)
    
    # Step 4 - Build FAISS index
    print("Step 4 - Building FAISS index...")
    index = build_index(embeddings)
    print(f"Total vectors stored: {index.ntotal}")
    
    # Step 5 - Save index
    print("Step 5 - Saving index...")
    save_index(index, chunks)
    
    # Step 6 - Test search
    print("\nStep 6 - Testing search...")
    question = "What is Python programming?"
    results = search(question, index, chunks, model)
    
    print(f"\nQuestion: {question}")
    print(f"\nTop relevant chunk found:")
    print(results[0])