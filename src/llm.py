# Day 19 - LLM with Error Handling
from groq import Groq
from dotenv import load_dotenv
from prompts import build_qa_prompt, build_summary_prompt, build_quiz_prompt
import os
import json
import time

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question, context_chunks, history_text=""):
    """Get answer from Groq with error handling"""
    try:
        prompt = build_qa_prompt(question, context_chunks, history_text)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting answer: {e}")
        return "Sorry I am having trouble connecting to the AI. Please try again in a moment."

def get_summary(context_chunks):
    """Get summary with error handling"""
    try:
        prompt = build_summary_prompt(context_chunks)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting summary: {e}")
        return "Sorry I could not generate a summary. Please try again."

def get_quiz(context_chunks):
    """Generate MCQ quiz with error handling"""
    try:
        prompt = build_quiz_prompt(context_chunks)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        quiz = json.loads(text)
        return quiz
    except json.JSONDecodeError as e:
        print(f"Error parsing quiz JSON: {e}")
        return None
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None