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
    prompt = (
        "Generate 10 multiple choice questions.\n"
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n\n"
        "Return ONLY a JSON array.\n"
        "Each item must have:\n"
        "- question (string)\n"
        "- options (object with keys A, B, C, D)\n"
        "- correct_answer (one of A, B, C, D)\n\n"
        "Do not include any explanation or text outside JSON."
    )

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 700
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

    print("🔴 GROQ STATUS:", response.status_code)
    print("🔴 GROQ BODY:", response.text)

    if response.status_code != 200:
        print("🔴 GROQ ERROR BODY:", response.text)
        return {"error": response.text}   

    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Safe JSON extraction
    start = content.find("[")
    end = content.rfind("]") + 1

    if start == -1 or end == -1:
        raise ValueError("No JSON array found in Groq response")

    return json.loads(content[start:end])

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