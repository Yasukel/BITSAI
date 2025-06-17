# generator.py
import requests
import json
import re

LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "gemma3:1b"

def extract_json(text: str) -> str:
    """
    Extracts JSON content from a string. Handles markdown-style ```json ... ``` if present.
    """
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_answer(question: str, documents: list) -> dict:
    context = "\n\n".join([doc["document"] for doc in documents])
    sources = list({doc["metadata"].get("source", "unknown") for doc in documents})
    source_list = '", "'.join(sources)

    prompt = f"""
You are an AI assistant. Using the context below, answer the user's question in structured JSON format.

Context:
{context}

Question:
"{question}"

Respond ONLY in this JSON format:
{{
  "answer": "your concise but informative answer",
  "source_chunks": ["list of 1-3 text chunks actually used in the answer"],
  "used_documents": ["{source_list}"]
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
        print(f"❌ Generation error: {e}")
        return {
            "answer": "Unable to generate a reliable response.",
            "source_chunks": [],
            "used_documents": []
        }

# Example test
if __name__ == "__main__":
    test_docs = [
        {
            "document": (
                "Artificial intelligence (AI) enables machines to mimic human intelligence, "
                "such as learning, problem-solving, and decision-making. It is used in areas "
                "like healthcare, finance, robotics, and transportation."
            ),
            "metadata": {
                "source": "https://en.wikipedia.org/wiki/Artificial_intelligence"
            }
        }
    ]
    question = "What are some real-world applications of artificial intelligence?"
    result = generate_answer(question, test_docs)
    print("\n✅ Generated answer:")
    print(json.dumps(result, indent=2))
