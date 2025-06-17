🧠 RAG Chatbot with Information Sufficiency Validation
A structured chatbot that uses RAG (Retrieval-Augmented Generation) and a local LLM to answer questions based on Wikipedia documents — with an intermediate verification step to check whether the retrieved information is enough.

🔧 Tech Stack
Component	Tool
Embedding model	sentence-transformers
Vector database	Chroma Cloud (HTTP API)
LLM	Local via Ollama (gemma3:1b)
Language	Python
Interface	CLI

📂 Project Structure
graphql
Copy
Edit
rag_chatbot/
├── app.py                          # Main CLI interface
├── retriever.py                    # Retrieves relevant chunks from Chroma
├── verifier.py                     # Uses LLM to check if context is sufficient
├── generator.py                    # Generates final structured answer
├── collect_and_segment_to_vectors.py  # Collects Wikipedia articles and uploads to Chroma
├── .env                            # Optional: API keys or config (not required for local setup)
├── requirements.txt                # Python dependencies
└── README.md                       # You're here
🚀 How It Works
Ingest Wikipedia data
Run:

bash
Copy
Edit
python collect_and_segment_to_vectors.py
This collects and segments Wikipedia articles and sends them to Chroma Cloud.

Ask a question
Start the chatbot:

bash
Copy
Edit
python app.py
You'll be prompted to ask questions in natural language.

Behind the scenes

Documents are retrieved from Chroma.

verifier.py checks if there's enough info using your local LLM.

If yes, generator.py builds a structured JSON answer.

📦 Dependencies
Install everything with:

bash
Copy
Edit
pip install -r requirements.txt
Contents of requirements.txt:

text
Copy
Edit
chromadb
wikipedia
sentence-transformers
langchain
requests
🛠 Configuration
Ensure you have:

Chroma Cloud account: api.trychroma.com

Local LLM running via Ollama:

bash
Copy
Edit
ollama run gemma:1b
✅ Example Output
json
Copy
Edit
{
  "answer": "AI enables machines to perform human-like tasks such as learning, reasoning, and decision-making.",
  "source_chunks": ["Artificial intelligence refers to the simulation of human intelligence..."],
  "used_documents": ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
}
🧪 Future Improvements
Web UI (Streamlit / FastAPI)

Memory/history support

Auto-expansion if context is insufficient