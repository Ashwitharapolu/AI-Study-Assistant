# Day 4 - Text Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_loader import extract_text

def chunk_text(text):
    """Split text into small overlapping chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # each chunk = 500 characters
        chunk_overlap=50,      # 50 characters overlap between chunks
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks

# Test it
if __name__ == "__main__":
    # First extract text from PDF
    text = extract_text("data/sample.pdf")
    
    # Then chunk it
    chunks = chunk_text(text)
    
    # Print results
    print(f"Total chunks created: {len(chunks)}")
    print(f"\nFirst chunk:")
    print(chunks[0])
    print(f"\nSecond chunk:")
    print(chunks[1])