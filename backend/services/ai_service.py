import requests
import os
import json
import re

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "").strip()

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_quiz_questions(topic, difficulty):
    prompt = (
        f"Generate 10 multiple choice questions.\n"
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n\n"
        "Return ONLY a JSON array.\n"
        "Each item must have:\n"
        "- question\n"
        "- options (A, B, C, D)\n"
        "- correct_answer\n"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.3,
            "max_new_tokens": 700
        }
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        return {"error": response.text}

    output = response.json()

    # HuggingFace returns a list
    text = output[0]["generated_text"]

    start = text.find("[")
    end = text.rfind("]") + 1

    if start == -1 or end == -1:
        return {"error": "Invalid AI output format"}

    return json.loads(text[start:end])