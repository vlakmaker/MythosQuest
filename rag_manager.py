import chromadb
import json

class RAGManager:
    def __init__(self, host="chroma_db", port=8000):
        """Connect to ChromaDB running in Docker."""
        self.client = chromadb.PersistentClient(f"http://{host}:{port}")

    def add_document(self, doc_id, text):
        """Store a document in the RAG system."""
        collection = self.client.get_or_create_collection("historical_data")
        collection.add(documents=[text], ids=[doc_id])

    def query(self, query_text):
        """Retrieve relevant documents based on a query."""
        collection = self.client.get_collection("historical_data")
        results = collection.query(query_text)
        return results

if __name__ == "__main__":
    rag = RAGManager()
    rag.add_document("1", "The French Revolution began in 1789.")
    print(rag.query("When did the French Revolution start?"))
