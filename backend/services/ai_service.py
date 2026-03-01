import json
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_KEY = GROQ_API_KEY.strip().replace('"', '')

API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "llama3-8b-8192"  # Free + stable


def generate_quiz_questions(topic, difficulty):
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a quiz generator. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": f"Generate 10 multiple choice questions on {topic} with difficulty {difficulty}. "
                           f"Return a JSON array with question, options A-D, and correct_answer."
            }
        ],
        "temperature": 0.3,
        "max_tokens": 800,
        "response_format": { "type": "json_object" }
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY').strip()}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    return json.loads(data["choices"][0]["message"]["content"])

#     prompt = f"""
# Generate EXACTLY 10 multiple choice questions.

# Topic: {topic}
# Difficulty: {difficulty}

# Return ONLY a valid JSON array.
# No text. No explanation. No markdown.

# Format:
# [
#   {{
#     "question": "...",
#     "options": {{
#       "A": "...",
#       "B": "...",
#       "C": "...",
#       "D": "..."
#     }},
#     "correct_answer": "A"
#   }}
# ]
# """

#     payload = {
#         "model": MODEL,
#         "messages": [
#         {
#             "role": "user",
#             "content": prompt.strip()
#         }
#         ],
#         "temperature": 0.7,
#         "max_tokens": 600, 
#         "stream": False 
#     }

#     response = requests.post(
#         API_URL,
#         headers=HEADERS,
#         json=payload,
#         timeout=30
#     )
#     print("GROQ STATUS:", response.status_code)
#     print("GROQ BODY:", response.text)
#     response.raise_for_status()

#     data = response.json()
#     content = data["choices"][0]["message"]["content"]

#     match = re.search(r"\[\s*{.*}\s*\]", content, re.DOTALL)

#     if not match:
#         raise ValueError("AI did not return a valid JSON array")

#     clean_json = match.group(0)

#     questions = json.loads(clean_json)

#     if not isinstance(questions, list):
#         raise ValueError("Parsed JSON is not a list")

#     return questions