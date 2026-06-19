# Day 9 - Updated LLM with better prompts
from groq import Groq
from dotenv import load_dotenv
from prompts import build_qa_prompt, build_summary_prompt, build_quiz_prompt
import os
import json

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question, context_chunks, history_text=""):
    """Get answer from Groq using improved prompt with memory"""
    prompt = build_qa_prompt(question, context_chunks, history_text)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_summary(context_chunks):
    """Get summary of document"""
    prompt = build_summary_prompt(context_chunks)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def get_quiz(context_chunks):
    """Generate MCQ quiz from document"""
    prompt = build_quiz_prompt(context_chunks)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse JSON response
    try:
        text = response.choices[0].message.content
        # Clean response in case model adds extra text
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        quiz = json.loads(text)
        return quiz
    except:
        return None

# Test it
if __name__ == "__main__":
    from retriever import retrieve_chunks
    
    # Test 1 - QA with source
    print("TEST 1 - QA WITH SOURCE")
    print("=" * 50)
    question = "How do you define a function in Python?"
    chunks = retrieve_chunks(question)
    answer = get_answer(question, chunks)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    
    # Test 2 - Summary
    print("\nTEST 2 - SUMMARY")
    print("=" * 50)
    chunks = retrieve_chunks("Python programming overview")
    summary = get_summary(chunks)
    print(summary)
    
    # Test 3 - Quiz
    print("\nTEST 3 - QUIZ")
    print("=" * 50)
    chunks = retrieve_chunks("Python functions and loops")
    quiz = get_quiz(chunks)
    if quiz:
        for i, q in enumerate(quiz):
            print(f"\nQ{i+1}: {q['question']}")
            for option in q['options']:
                print(f"  {option}")
            print(f"Answer: {q['answer']}")