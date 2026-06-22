from pdf_loader import extract_text
from chunker import chunk_text
from embeddings import get_embeddings, model
from vector_store import build_index, save_index, load_index, search_mmr
from llm import get_answer, get_summary, get_quiz
import os
import faiss
import numpy as np
import pickle

class RAGPipeline:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.is_ready = False
        self.chat_history = []
        self.uploaded_pdfs = []  # Track uploaded PDFs

    def process_pdf(self, pdf_path):
        """Process a single PDF and add to existing index"""
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
            new_chunks = chunk_text(text)
            if not new_chunks:
                print("Error: Could not create chunks")
                return False
            print(f"New chunks: {len(new_chunks)}")

            print("Step 3 - Creating embeddings...")
            new_embeddings = get_embeddings(new_chunks)

            print("Step 4 - Building/updating FAISS index...")
            if self.index is None:
                # First PDF - create new index
                self.chunks = new_chunks
                self.index = build_index(new_embeddings)
            else:
                # Additional PDF - add to existing index
                self.chunks.extend(new_chunks)
                new_embeddings_float = np.array(new_embeddings).astype('float32')
                self.index.add(new_embeddings_float)

            print("Step 5 - Saving index...")
            save_index(self.index, self.chunks)

            # Track uploaded PDFs
            pdf_name = os.path.basename(pdf_path)
            if pdf_name not in self.uploaded_pdfs:
                self.uploaded_pdfs.append(pdf_name)

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
        """Ask question with conversation memory"""
        try:
            if not self.is_ready:
                return "Please upload a PDF first!"

            if not question.strip():
                return "Please ask a valid question!"

            results = search_mmr(
                question, self.index, self.chunks, model, k=5, fetch_k=20
            )

            history_text = ""
            if self.chat_history:
                history_text = "\n\nPrevious conversation:\n"
                for exchange in self.chat_history[-5:]:
                    history_text += f"Human: {exchange['question']}\n"
                    history_text += f"Assistant: {exchange['answer']}\n"

            answer = get_answer(question, results, history_text)

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

    def reset(self):
        """Reset entire pipeline"""
        self.index = None
        self.chunks = None
        self.is_ready = False
        self.chat_history = []
        self.uploaded_pdfs = []