# app.py
from retriever import retrieve_documents
from verifier import verify_information
from generator import generate_answer
import json

def main():
    print("🤖 Welcome to the RAG Chatbot (Powered by gemma3:1b + Chroma Cloud)")
    
    while True:
        question = input("\n🧠 Ask a question (or type 'exit'): ").strip()
        if question.lower() in ("exit", "quit"):
            break

        print("\n🔍 Retrieving relevant documents...")
        docs = retrieve_documents(question, top_k=5)

        if not docs:
            print("⚠️ No relevant documents found.")
            continue

        print("✅ Verifying information sufficiency...")
        verification = verify_information(question, docs)

        if not verification["enough_information"]:
            print("\n🚧 Not enough information to answer confidently.")
            print(f"Missing concepts: {', '.join(verification['missing_concepts'])}")
            print(f"Confidence: {verification['confidence']}")
            continue

        print("✍️ Generating final answer...")
        result = generate_answer(question, docs)

        print("\n📝 Final Answer:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
