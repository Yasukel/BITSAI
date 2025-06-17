# retriever.py
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict, Any

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Chroma Cloud
client = chromadb.HttpClient(
    host="api.trychroma.com",
    ssl=True,
    tenant="16f8e81b-e223-4ede-b1f5-14d9f4fa22be",
    database="Homework0611",
    headers={
        "x-chroma-token": "ck-B8gMe3BPJD2fijzck38eMuhE89gQcUcq63jD6owAUgB9"
    }
)

collection = client.get_or_create_collection("wiki")

def retrieve_documents(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    query_embedding = embedding_model.encode(query).tolist()

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return []

    documents = []
    docs_list = results.get("documents", [])
    metas_list = results.get("metadatas", [])

    if docs_list and metas_list:
        for doc, metadata in zip(docs_list[0], metas_list[0]):
            documents.append({
                "document": doc,
                "metadata": metadata
            })

    return documents

# Optional test
if __name__ == "__main__":
    results = retrieve_documents("How do quantum computers work?", top_k=3)
    for i, res in enumerate(results, 1):
        print(f"\n🔹 Chunk {i}:\n{res['document']}\n🔗 Source: {res['metadata'].get('source', 'unknown')}")
