# collect_and_segment_to_vectors.py
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
import wikipedia

# Naudojamas embedding modelis
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB Web (Cloud) klientas
client = chromadb.HttpClient(
    ssl=True,
    host='api.trychroma.com',
    tenant='16f8e81b-e223-4ede-b1f5-14d9f4fa22be',
    database='Homework0611',
    headers={
        'x-chroma-token': 'ck-B8gMe3BPJD2fijzck38eMuhE89gQcUcq63jD6owAUgB9'
    }
)

collection = client.get_or_create_collection("wiki")

def collect_and_store(topic: str):
    try:
        page = wikipedia.page(topic)
        text = page.content
    except Exception as e:
        print(f"⚠️ Nepavyko gauti straipsnio '{topic}': {e}")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": page.url}],
            ids=[f"{topic}_{i}"]
        )

    print(f"✅ Įkelta {len(chunks)} segmentų iš {page.url}")

if __name__ == "__main__":
    topics = [
        "Quantum computing",
        "Artificial intelligence",
        "Generative artificial intelligence",
        "Artificial neural network",
        "Computer vision",
        "Large language model"
    ]

    for topic in topics:
        print(f"\n📥 Tema: {topic}")
        collect_and_store(topic)
