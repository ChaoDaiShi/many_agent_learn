from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from db import get_db
from service import RagService

router = APIRouter(prefix="/rag", tags=["rag"])

@router.post("/upload")
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = RagService(db)
    document = service.upload_pdf(file)
    return {"code": 200, "message": "上传成功", "data": document.__dict__}

@router.get("/documents")
def get_document_list(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    service = RagService(db)
    result = service.get_documents(page, size)
    return {"code": 200, "data": [doc.__dict__ for doc in result["data"]], "total": result["total"]}

@router.get("/document/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    service = RagService(db)
    document = service.get_document(doc_id)
    if not document:
        return {"code": 404, "message": "文档不存在"}
    return {"code": 200, "data": document.__dict__}

@router.delete("/document/{doc_id}")
def delete_document(doc_id: str, db: Session = Depends(get_db)):
    service = RagService(db)
    success = service.delete_document(doc_id)
    if not success:
        return {"code": 404, "message": "文档不存在"}
    return {"code": 200, "message": "删除成功"}

@router.post("/query")
def query_document(data: dict, db: Session = Depends(get_db)):
    service = RagService(db)
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    result = service.query_documents(query, top_k)
    return {"code": 200, "data": result["data"]}