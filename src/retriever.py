from embeddings import get_embeddings, model
from vector_store import load_index, search

def retrieve_chunks(question, k=5):
    """
    Load saved FAISS index and retrieve
    top k most relevant chunks for a question
    """
    # Load saved index from disk
    print("Loading FAISS index from disk...")
    index, chunks = load_index()
    
    # Search for relevant chunks
    results = search(question, index, chunks, model, k=k)
    
    return results

def display_results(question, results):
    """Display retrieved chunks nicely"""
    print(f"\nQuestion: {question}")
    print(f"\nTop {len(results)} relevant chunks found:")
    print("=" * 50)
    
    for i, chunk in enumerate(results):
        print(f"\nChunk {i+1}:")
        print(chunk)
        print("-" * 50)

# Test it
if __name__ == "__main__":
    # Test questions
    questions = [
        "What is Python programming?",
        "How do you use loops in Python?",
        "What are functions in Python?"
    ]
    
    for question in questions:
        results = retrieve_chunks(question)
        display_results(question, results)
        print("\n" + "=" * 50 + "\n")