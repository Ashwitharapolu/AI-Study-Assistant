# ============================================
# prompts.py - Prompt Engineering Module
# AI Powered Smart Study Assistant
# ============================================

def build_qa_prompt(question, context_chunks, history_text=""):
    """
    Build a detailed QA prompt with context and memory
    Args:
        question: User's question
        context_chunks: Top 5 relevant chunks from FAISS
        history_text: Last 5 conversation exchanges
    Returns:
        Formatted prompt string
    """
    # Add source numbers to each chunk
    context = ""
    for i, chunk in enumerate(context_chunks):
        context += f"\n[Source {i+1}]:\n{chunk}\n"

    prompt = f"""You are an intelligent study assistant helping a student understand their study material.

Your rules:
1. Answer ONLY from the context provided below
2. If answer is not in context say "This topic is not covered in your uploaded material"
3. Give clear structured answers
4. Mention which source number you used at the end
5. Use simple language a student can understand
6. Use previous conversation for context if relevant
{history_text}

Context:
{context}

Question: {question}

Answer (with source):"""

    return prompt


def build_summary_prompt(context_chunks):
    """
    Build a prompt to summarize document
    Uses chunks 10-30 to skip copyright/intro pages
    Args:
        context_chunks: All chunks from document
    Returns:
        Formatted summary prompt
    """
    # Skip first 10 chunks (copyright/org info)
    # Use chunks 10-30 for actual content
    context = "\n\n".join(context_chunks[10:30])

    prompt = f"""You are a study assistant. Summarize the following study material clearly.

Format your response exactly like this:
## Overview
(2-3 sentence overview)

## Key Concepts
(5 most important concepts as bullet points)

## Important Points
(3 most important things to remember)

Material:
{context}

Summary:"""

    return prompt


def build_quiz_prompt(context_chunks):
    """
    Build a prompt to generate MCQ quiz
    Uses chunks 10-20 to get actual content
    Args:
        context_chunks: All chunks from document
    Returns:
        Formatted quiz prompt
    """
    # Skip first 10 chunks (copyright/org info)
    # Use chunks 10-20 for actual content
    context = "\n\n".join(context_chunks[10:20])

    prompt = f"""You are a study assistant. Generate 5 multiple choice questions from the material below.

Return ONLY a JSON array in this exact format, nothing else:
[
    {{
        "question": "Question here?",
        "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
        "answer": "A. option1",
        "explanation": "Brief explanation"
    }}
]

Material:
{context}

JSON:"""

    return prompt