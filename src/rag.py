from pdf_loader import extract_text
from chunker import chunk_text
from embeddings import get_embeddings, model
from vector_store import build_index, save_index, load_index, search
from llm import get_answer, get_summary, get_quiz
import os

class RAGPipeline:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.is_ready = False

    def process_pdf(self, pdf_path):
        """
        Complete pipeline to process a PDF file
        Extract → Chunk → Embed → Store
        """
        print(f"Processing {pdf_path}...")

        # Step 1 - Extract text
        print("Step 1 - Extracting text...")
        text = extract_text(pdf_path)
        if not text.strip():
            print("Error: Could not extract text from PDF")
            return False

        # Step 2 - Chunk text
        print("Step 2 - Chunking text...")
        self.chunks = chunk_text(text)
        print(f"Total chunks: {len(self.chunks)}")

        # Step 3 - Create embeddings
        print("Step 3 - Creating embeddings...")
        embeddings = get_embeddings(self.chunks)

        # Step 4 - Build FAISS index
        print("Step 4 - Building FAISS index...")
        self.index = build_index(embeddings)

        # Step 5 - Save index
        print("Step 5 - Saving index...")
        save_index(self.index, self.chunks)

        self.is_ready = True
        print("PDF processed successfully!")
        return True

    def load_existing(self):
        """Load already processed PDF from disk"""
        try:
            self.index, self.chunks = load_index()
            self.is_ready = True
            print("Loaded existing index successfully!")
            return True
        except:
            print("No existing index found")
            return False

    def ask(self, question):
        """Ask a question and get answer"""
        if not self.is_ready:
            return "Please upload a PDF first!"

        # Get relevant chunks
        results = search(question, self.index, self.chunks, model, k=5)

        # Get answer from Groq
        answer = get_answer(question, results)
        return answer

    def summarize(self):
        """Summarize the uploaded document"""
        if not self.is_ready:
            return "Please upload a PDF first!"

        summary = get_summary(self.chunks)
        return summary

    def generate_quiz(self):
        """Generate quiz from uploaded document"""
        if not self.is_ready:
            return None

        quiz = get_quiz(self.chunks)
        return quiz


# Test it
if __name__ == "__main__":
    # Create RAG pipeline
    rag = RAGPipeline()

    # Option 1 - Process new PDF
    # rag.process_pdf("data/sample.pdf")

    # Option 2 - Load existing index
    rag.load_existing()

    if rag.is_ready:
        # Test 1 - Ask questions
        print("\n" + "="*50)
        print("TEST 1 - ASK QUESTIONS")
        print("="*50)

        questions = [
            "What is Python?",
            "How do you define a function?",
            "What are loops?"
        ]

        for q in questions:
            print(f"\nQ: {q}")
            answer = rag.ask(q)
            print(f"A: {answer}")

        # Test 2 - Summary
        print("\n" + "="*50)
        print("TEST 2 - SUMMARY")
        print("="*50)
        summary = rag.summarize()
        print(summary)

        # Test 3 - Quiz
        print("\n" + "="*50)
        print("TEST 3 - QUIZ")
        print("="*50)
        quiz = rag.generate_quiz()
        if quiz:
            for i, q in enumerate(quiz):
                print(f"\nQ{i+1}: {q['question']}")
                for option in q['options']:
                    print(f"  {option}")
                print(f"Answer: {q['answer']}")