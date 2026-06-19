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
        # Conversation memory - stores last 5 exchanges
        self.chat_history = []

    def process_pdf(self, pdf_path):
        """Complete pipeline to process a PDF file"""
        print(f"Processing {pdf_path}...")

        print("Step 1 - Extracting text...")
        text = extract_text(pdf_path)
        if not text.strip():
            print("Error: Could not extract text from PDF")
            return False

        print("Step 2 - Chunking text...")
        self.chunks = chunk_text(text)
        print(f"Total chunks: {len(self.chunks)}")

        print("Step 3 - Creating embeddings...")
        embeddings = get_embeddings(self.chunks)

        print("Step 4 - Building FAISS index...")
        self.index = build_index(embeddings)

        print("Step 5 - Saving index...")
        save_index(self.index, self.chunks)

        self.is_ready = True
        self.chat_history = []
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
        """Ask a question with conversation memory"""
        if not self.is_ready:
            return "Please upload a PDF first!"

        # Get relevant chunks
        results = search(question, self.index, self.chunks, model, k=5)

        # Build context with chat history
        history_text = ""
        if self.chat_history:
            history_text = "\n\nPrevious conversation:\n"
            for exchange in self.chat_history[-5:]:
                history_text += f"Human: {exchange['question']}\n"
                history_text += f"Assistant: {exchange['answer']}\n"

        # Get answer from Groq with history
        answer = get_answer(question, results, history_text)

        # Save to chat history
        self.chat_history.append({
            "question": question,
            "answer": answer
        })

        # Keep only last 5 exchanges
        if len(self.chat_history) > 5:
            self.chat_history = self.chat_history[-5:]

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

    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []