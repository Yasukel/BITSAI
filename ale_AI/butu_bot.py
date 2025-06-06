from dotenv import load_dotenv
import os
from openai import OpenAI

# ✅ Load environment variables
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

# ✅ Define constants
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
KW = ["apartment", "flat", "room", "renovation", "furniture", "storage", "decor"]
SYSTEM = (
    "You are an expert on improving apartments. "
    "If the user asks anything outside that domain, answer: "
    "\"I'd tell you, but unfortunately, my toolbox doesn’t come with a manual for that.\" Wait for a new question."
)

# ✅ Set up client
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# ✅ Helper function: check if question is on-topic
def is_on_topic(question):
    question = question.lower()
    return any(keyword in question for keyword in KW)

# ✅ Main logic
def main():
    question = input("Ask a question: ").strip()
    
    if not is_on_topic(question):
        print("I'd tell you, but unfortunately, my toolbox doesn’t come with a manual for that.")
        return

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        model=model
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
