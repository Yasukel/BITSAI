import requests
import json
import re
import pprint
from typing import List
from pydantic import BaseModel, ValidationError


# === 1. Pydantic model (Pydantic v2+) ===
class LetterInformation(BaseModel):
    is_complaint: bool
    is_refund: bool
    positive_score: float
    complaint_tags: List[str]


# === 2. Local keyword matcher ===
def detect_complaint_tags(text: str) -> List[str]:
    keywords = [
        "not satisfied", "very disappointed", "complain", "unacceptable",
        "issue", "problem", "angry", "bad experience", "frustrated", "refund",
        "faulty", "poor service", "doesn't work", "worst", "late delivery",
        "rude", "damaged", "delayed", "broken", "cancel", "missing"
    ]
    text_lower = text.lower()
    return [kw for kw in keywords if kw in text_lower]


# === 3. Clean messy model output (```json ... ```) ===
def extract_json_from_response(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"


# === 4. Main logic: LLM + local keyword override ===
def analyze_letter(text: str) -> LetterInformation | dict:
    detected_tags = detect_complaint_tags(text)
    raw_output = None  # Always define it

    prompt = f"""
You are an assistant analyzing customer messages.

Return valid JSON in this format:
{{
  "is_complaint": true,
  "is_refund": false,
  "positive_score": 0.25,
  "complaint_tags": []
}}

Analyze this message:
\"{text}\"

Only return the JSON. Do not include explanation or markdown.
"""

    try:
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "gemma3:1b",
            "messages": [
                {"role": "user", "content": prompt.strip()}
            ],
            "stream": False
        })

        response.raise_for_status()
        raw_output = response.json()["message"]["content"]

        json_data = extract_json_from_response(raw_output)
        parsed = json.loads(json_data)

        parsed["complaint_tags"] = detected_tags

        return LetterInformation(**parsed)

    except (json.JSONDecodeError, ValidationError, requests.RequestException) as e:
        return {
            "error": str(e),
            "raw_output": raw_output,
            "fallback_complaint_tags": detected_tags
        }


# === 5. Example usage ===
if __name__ == "__main__":
    message = (
        "I expected the product to arrive sooner. It’s a bit disappointing that there was no update about the delay. Please let me know how to proceed."
    )

    result = analyze_letter(message)

    if isinstance(result, LetterInformation):
        pprint.pprint(result.model_dump())
    else:
        print("LLM error/fallback:\n", json.dumps(result, indent=2))
