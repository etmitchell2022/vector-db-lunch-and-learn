import os
import chromadb
from chromadb.config import Settings


class ChromaDBClient:
    def __init__(self, persist_dir=None):
        if persist_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            persist_dir = os.path.join(base_dir, "vector_store", "chroma_storage")

        self.client = chromadb.PersistentClient(path=persist_dir)
        self.persist_dir = persist_dir

    def get_or_create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(name=collection_name)

    def get_all_items(self, collection_name: str):
        collection = self.get_or_create_collection(collection_name)
        results = collection.get()
        return results
