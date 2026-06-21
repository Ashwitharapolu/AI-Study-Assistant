# Day 19 - RAG Pipeline with Error Handling
from pdf_loader import extract_text
from chunker import chunk_text
from embeddings import get_embeddings, model
from vector_store import build_index, save_index, load_index, search_mmr
from llm import get_answer, get_summary, get_quiz
import os

class RAGPipeline:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.is_ready = False
        self.chat_history = []

    def process_pdf(self, pdf_path):
        """Complete pipeline with error handling"""
        try:
            print(f"Processing {pdf_path}...")

            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"Error: File not found: {pdf_path}")
                return False

            # Check file size
            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                print("Error: PDF file is empty")
                return False

            print("Step 1 - Extracting text...")
            text = extract_text(pdf_path)
            if not text.strip():
                print("Error: Could not extract text from PDF")
                return False

            print("Step 2 - Chunking text...")
            self.chunks = chunk_text(text)
            if not self.chunks:
                print("Error: Could not create chunks")
                return False
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

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False

    def load_existing(self):
        """Load existing index with error handling"""
        try:
            self.index, self.chunks = load_index()
            self.is_ready = True
            print("Loaded existing index successfully!")
            return True
        except FileNotFoundError:
            print("No existing index found")
            return False
        except Exception as e:
            print(f"Error loading index: {e}")
            return False

    def ask(self, question):
        """Ask question with error handling"""
        try:
            if not self.is_ready:
                return "Please upload a PDF first!"

            if not question.strip():
                return "Please ask a valid question!"

            # Get relevant chunks using MMR
            results = search_mmr(
                question, self.index, self.chunks, model, k=5, fetch_k=20
            )

            # Build history text
            history_text = ""
            if self.chat_history:
                history_text = "\n\nPrevious conversation:\n"
                for exchange in self.chat_history[-5:]:
                    history_text += f"Human: {exchange['question']}\n"
                    history_text += f"Assistant: {exchange['answer']}\n"

            answer = get_answer(question, results, history_text)

            # Save to history
            self.chat_history.append({
                "question": question,
                "answer": answer
            })

            if len(self.chat_history) > 5:
                self.chat_history = self.chat_history[-5:]

            return answer

        except Exception as e:
            print(f"Error answering question: {e}")
            return "Sorry something went wrong. Please try again."

    def summarize(self):
        """Summarize with error handling"""
        try:
            if not self.is_ready:
                return "Please upload a PDF first!"
            return get_summary(self.chunks)
        except Exception as e:
            print(f"Error summarizing: {e}")
            return "Sorry could not generate summary. Please try again."

    def generate_quiz(self):
        """Generate quiz with error handling"""
        try:
            if not self.is_ready:
                return None
            return get_quiz(self.chunks)
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return None

    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []