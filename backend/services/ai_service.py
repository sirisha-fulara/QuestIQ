import json
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "stepfun/step-3.5-flash:free"


def generate_quiz_questions(topic, difficulty):
    prompt = f"""
Generate EXACTLY 10 multiple choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY a valid JSON array.
No text. No explanation. No markdown.

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

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    match = re.search(r"\[\s*{.*}\s*\]", content, re.DOTALL)

    if not match:
        raise ValueError("AI did not return a valid JSON array")

    clean_json = match.group(0)

    questions = json.loads(clean_json)

    if not isinstance(questions, list):
        raise ValueError("Parsed JSON is not a list")

    return questions
