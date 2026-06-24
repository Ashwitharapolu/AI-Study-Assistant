# ============================================
# rag.py - Complete RAG Pipeline
# AI Powered Smart Study Assistant
# ============================================

from pdf_loader import extract_text
from chunker import chunk_text
from embeddings import get_embeddings, model
from vector_store import build_index, save_index, load_index, search_mmr
from llm import get_answer, get_summary, get_quiz
from logger import logger
import os
import numpy as np

class RAGPipeline:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.is_ready = False
        self.chat_history = []
        self.uploaded_pdfs = []

    def process_pdf(self, pdf_path):
        """Process a PDF file through complete RAG pipeline"""
        try:
            logger.info(f"Starting PDF processing: {pdf_path}")

            if not os.path.exists(pdf_path):
                logger.error(f"File not found: {pdf_path}")
                return False

            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                logger.error("PDF file is empty")
                return False

            logger.info("Step 1 - Extracting text...")
            text = extract_text(pdf_path)
            if not text.strip():
                logger.error("Could not extract text from PDF")
                return False

            logger.info("Step 2 - Chunking text...")
            new_chunks = chunk_text(text)
            if not new_chunks:
                logger.error("Could not create chunks")
                return False
            logger.info(f"Created {len(new_chunks)} chunks")

            logger.info("Step 3 - Creating embeddings...")
            new_embeddings = get_embeddings(new_chunks)

            logger.info("Step 4 - Building FAISS index...")
            if self.index is None:
                self.chunks = new_chunks
                self.index = build_index(new_embeddings)
            else:
                self.chunks.extend(new_chunks)
                new_embeddings_float = np.array(new_embeddings).astype('float32')
                self.index.add(new_embeddings_float)

            logger.info("Step 5 - Saving index...")
            save_index(self.index, self.chunks)

            pdf_name = os.path.basename(pdf_path)
            if pdf_name not in self.uploaded_pdfs:
                self.uploaded_pdfs.append(pdf_name)

            self.is_ready = True
            self.chat_history = []
            logger.info(f"PDF processed successfully: {pdf_name}")
            return True

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return False

    def load_existing(self):
        """Load existing FAISS index from disk"""
        try:
            self.index, self.chunks = load_index()
            self.is_ready = True
            logger.info("Loaded existing index successfully")
            return True
        except FileNotFoundError:
            logger.warning("No existing index found")
            return False
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False

    def ask(self, question):
        """Ask a question and get answer from RAG pipeline"""
        try:
            if not self.is_ready:
                return "Please upload a PDF first!"

            if not question.strip():
                return "Please ask a valid question!"

            logger.info(f"Question asked: {question}")

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

            logger.info(f"Answer generated: {len(answer)} characters")

            self.chat_history.append({
                "question": question,
                "answer": answer
            })

            if len(self.chat_history) > 5:
                self.chat_history = self.chat_history[-5:]

            return answer

        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return "Sorry something went wrong. Please try again."

    def summarize(self):
        """Summarize uploaded document"""
        try:
            if not self.is_ready:
                return "Please upload a PDF first!"
            logger.info("Generating document summary")
            summary = get_summary(self.chunks)
            logger.info("Summary generated successfully")
            return summary
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return "Sorry could not generate summary."

    def generate_quiz(self):
        """Generate MCQ quiz from document"""
        try:
            if not self.is_ready:
                return None
            logger.info("Generating quiz")
            quiz = get_quiz(self.chunks)
            logger.info(f"Quiz generated: {len(quiz) if quiz else 0} questions")
            return quiz
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return None

    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        logger.info("Chat history cleared")

    def reset(self):
        """Reset entire pipeline"""
        self.index = None
        self.chunks = None
        self.is_ready = False
        self.chat_history = []
        self.uploaded_pdfs = []
        logger.info("Pipeline reset")