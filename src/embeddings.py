from sentence_transformers import SentenceTransformer
from chunker import chunk_text
from pdf_loader import extract_text

# Load embedding model - runs locally, completely free!
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(chunks):
    """Convert list of text chunks into vectors"""
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings

# Test it
if __name__ == "__main__":
    # Step 1 - Extract text
    print("Step 1 - Extracting text from PDF...")
    text = extract_text("data/sample.pdf")

    # Step 2 - Chunk it
    print("Step 2 - Chunking text...")
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")

    # Step 3 - Create embeddings
    print("Step 3 - Creating embeddings...")
    embeddings = get_embeddings(chunks)

    # Print results
    print(f"\nEmbeddings shape: {embeddings.shape}")
    print(f"Each chunk becomes {embeddings.shape[1]} numbers")
    print(f"\nFirst embedding first 10 numbers:")
    print(embeddings[0][:10])