import ollama
import os
from vector_store.embeddings import Embeddings
from vector_store.chromadb_client import ChromaDBClient


def run_llm_rag():
    embeddings_client = Embeddings()
    db_client = ChromaDBClient()

    collection = db_client.get_or_create_collection("movies")
    query = input("Enter your query: ")

    embedded_query = embeddings_client.create_embedding(query)
    results = collection.query(
        query_embeddings=[embedded_query],
        n_results=3)
    
    context_docs = "\n\n".join(results["documents"][0])

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": f"Use the following context to answer the user's question:\n\n{context_docs}"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    print(f"LLM Response: {response['message']['content']}")


if __name__ == "__main__":
    run_llm_rag()