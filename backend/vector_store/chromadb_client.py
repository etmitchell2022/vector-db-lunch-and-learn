import chromadb
from chromadb.config import Settings


class ChromaDBClient:
    def __init__(self, persist_dir="./chroma_storage"):
        self.client = chromadb.Client(Settings(persist_directory=persist_dir))
        self.persist_dir = persist_dir

    def get_or_create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(name=collection_name)

    def persist(self):
        self.client.persist()
