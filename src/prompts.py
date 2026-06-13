def build_qa_prompt(question, context_chunks):
    """Build a detailed QA prompt with context"""
    
    # Add chunk numbers to context
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

Context:
{context}

Question: {question}

Answer (with source):"""
    
    return prompt


def build_summary_prompt(context_chunks):
    """Build a prompt to summarize document"""
    context = "\n\n".join(context_chunks[:10])
    
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
    """Build a prompt to generate MCQ quiz"""
    context = "\n\n".join(context_chunks[:5])
    
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