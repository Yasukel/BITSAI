# verifier.py
import requests
import json
import re

LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "gemma3:1b"

def extract_json(text: str) -> str:
    """
    Extracts JSON content from a string. If wrapped in a Markdown-style code block,
    it will strip the surrounding ```json ... ``` tags.
    """
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def verify_information(question: str, documents: list, threshold: float = 0.75) -> dict:
    context = "\n\n".join([doc["document"] for doc in documents])

    prompt = f"""
You are a helpful assistant that evaluates whether a provided context is sufficient to reliably answer a user's question.

Context:
{context}

Question:
"{question}"

Reply ONLY in the following valid JSON format with no explanation or text around it:
{{
  "enough_information": true|false,
  "missing_concepts": ["concept1", "concept2"],
  "confidence": float
}}
"""

    response = requests.post(
        LLM_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    try:
        response_json = response.json()
        raw_output = response_json.get("response", "").strip()
        print("🔎 Raw model response:")
        print(raw_output)

        clean_output = extract_json(raw_output)
        return json.loads(clean_output)

    except Exception as e:
        print(f"❌ JSON decode error: {e}")
        return {
            "enough_information": False,
            "missing_concepts": ["unknown"],
            "confidence": 0.0
        }

# Example test
if __name__ == "__main__":
    test_docs = [
        {
            "document": (
                "Artificial intelligence (AI) refers to the simulation of human intelligence "
                "in machines that are programmed to think and learn like humans. These systems "
                "can perform tasks such as decision-making, language translation, and visual perception."
            ),
            "metadata": {"source": "https://en.wikipedia.org/wiki/Artificial_intelligence"}
        }
    ]
    question = "What is the role of AI in artificial intelligence?"
    result = verify_information(question, test_docs)
    print("\n✅ Verification result:")
    print(json.dumps(result, indent=2))
# Example output:
# {
#   "enough_information": true,
#   "missing_concepts": [],
#   "confidence": 0.85
# }