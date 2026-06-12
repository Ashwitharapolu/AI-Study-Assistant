from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question, context_chunks):
    """
    Send question and relevant chunks to Groq
    and get a proper answer back
    """
    # Join all chunks into one context
    context = "\n\n".join(context_chunks)
    
    # Build prompt
    prompt = f"""You are a helpful study assistant. 
Answer the question using ONLY the context provided below.
If the answer is not in the context say 
"This topic is not covered in your uploaded material."

Context:
{context}

Question: {question}

Answer:"""

    # Send to Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Test it
if __name__ == "__main__":
    from retriever import retrieve_chunks
    
    # Test questions
    questions = [
        "What is Python programming?",
        "How do you define a function in Python?",
        "What are loops in Python?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        
        # Step 1 - Retrieve relevant chunks
        chunks = retrieve_chunks(question)
        
        # Step 2 - Get answer from Groq
        answer = get_answer(question, chunks)
        
        print(f"Answer: {answer}")
        print("=" * 50)