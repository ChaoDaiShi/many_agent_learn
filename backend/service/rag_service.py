import uuid
from sqlalchemy.orm import Session
from db.models import Document
from db.chroma_store import chroma_store
from utils.pdf_parse import process_pdf
from config.settings import UPLOAD_DIR
import os

class RagService:
    def __init__(self, db: Session):
        self.db = db
    
    def upload_pdf(self, file):
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        result = process_pdf(str(file_path))
        
        document = Document(
            id=file_id,
            name=file.filename,
            file_path=str(file_path),
            size=os.path.getsize(file_path),
            chunk_count=result["chunk_count"],
            content=result["text"]
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        metadatas = [{"doc_id": file_id, "chunk_index": i} for i in range(len(result["chunks"]))]
        ids = [f"{file_id}_{i}" for i in range(len(result["chunks"]))]
        
        chroma_store.add_documents(
            collection_name="documents",
            documents=result["chunks"],
            metadatas=metadatas,
            ids=ids
        )
        
        return document
    
    def get_documents(self, page: int, size: int):
        skip = (page - 1) * size
        documents = self.db.query(Document).order_by(Document.created_at.desc()).offset(skip).limit(size).all()
        total = self.db.query(Document).count()
        return {"data": documents, "total": total}
    
    def get_document(self, doc_id: str):
        return self.db.query(Document).filter(Document.id == doc_id).first()
    
    def delete_document(self, doc_id: str):
        document = self.get_document(doc_id)
        if not document:
            return False
        
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        chroma_store.get_collection("documents").delete(ids=[f"{doc_id}_{i}" for i in range(document.chunk_count)])
        
        self.db.delete(document)
        self.db.commit()
        return True
    
    def query_documents(self, query: str, top_k: int = 5):
        results = chroma_store.query("documents", [query], n_results=top_k)
        
        docs = []
        for i in range(len(results.get("documents", []))):
            docs.extend([{
                "title": results["metadatas"][i][j].get("doc_id", "Unknown"),
                "content": results["documents"][i][j],
                "score": results["distances"][i][j]
            } for j in range(len(results["documents"][i]))])
        
        docs.sort(key=lambda x: x["score"])
        return {"data": docs[:top_k]}