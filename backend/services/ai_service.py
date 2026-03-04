import os
import requests
import json
import random
import re

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api.aimlapi.com/v1/chat/completions"

# Load local question bank
with open("backend/data/question_bank.json", "r") as f:
    QUESTION_BANK = json.load(f)


def get_local_questions(topic):
    topic = topic.lower()

    if topic in QUESTION_BANK:
        questions = QUESTION_BANK[topic]
        return random.sample(questions, min(5, len(questions)))

    # fallback if topic not found
    return random.sample(QUESTION_BANK["python"], 5)


def generate_quiz_questions(topic, difficulty):

    prompt = f"""
Generate EXACTLY 5 multiple choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON array.

Format:
[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "A"
  }}
]
"""

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-3n-e4b-it",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)

        if response.status_code != 200:
            print("⚠️ AI API failed. Using local questions.")
            return get_local_questions(topic)

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        match = re.search(r"\[\s*{.*}\s*\]", content, re.DOTALL)

        if not match:
            print("⚠️ AI response invalid. Using local questions.")
            return get_local_questions(topic)

        clean_json = match.group(0)

        return json.loads(clean_json)

    except Exception as e:
        print("⚠️ AI error:", e)
        print("⚠️ Falling back to local question bank.")

        return get_local_questions(topic)