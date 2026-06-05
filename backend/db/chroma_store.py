import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import CHROMA_DIR

class ChromaStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = chromadb.PersistentClient(
                path=str(CHROMA_DIR),
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
        return cls._instance
    
    def get_collection(self, name):
        return self._client.get_or_create_collection(name=name)
    
    def add_documents(self, collection_name, documents, metadatas=None, ids=None):
        collection = self.get_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, collection_name, query_texts, n_results=5):
        collection = self.get_collection(collection_name)
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results
    
    def delete_collection(self, collection_name):
        try:
            self._client.delete_collection(name=collection_name)
            return True
        except Exception:
            return False
    
    def list_collections(self):
        return self._client.list_collections()

chroma_store = ChromaStore()