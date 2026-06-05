from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from service import GenService

router = APIRouter(prefix="/gen", tags=["gen"])

@router.post("/resource")
def generate_resource(data: dict, db: Session = Depends(get_db)):
    service = GenService(db)
    resource = service.generate_resource(data)
    return {"code": 200, "data": resource.__dict__}

@router.get("/resources")
def get_resource_list(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    service = GenService(db)
    result = service.get_resources(page, size)
    return {"code": 200, "data": [res.__dict__ for res in result["data"]], "total": result["total"]}

@router.get("/resource/{resource_id}")
def get_resource(resource_id: str, db: Session = Depends(get_db)):
    service = GenService(db)
    resource = service.get_resource(resource_id)
    if not resource:
        return {"code": 404, "message": "资源不存在"}
    return {"code": 200, "data": resource.__dict__}

@router.delete("/resource/{resource_id}")
def delete_resource(resource_id: str, db: Session = Depends(get_db)):
    service = GenService(db)
    success = service.delete_resource(resource_id)
    if not success:
        return {"code": 404, "message": "资源不存在"}
    return {"code": 200, "message": "删除成功"}

@router.put("/resource/{resource_id}")
def regenerate_resource(resource_id: str, data: dict, db: Session = Depends(get_db)):
    service = GenService(db)
    resource = service.regenerate_resource(resource_id, data)
    if not resource:
        return {"code": 404, "message": "资源不存在"}
    return {"code": 200, "data": resource.__dict__}

@router.get("/types")
def get_resource_types():
    types = [
        {"type": "document", "label": "专业课程讲解"},
        {"type": "mindmap", "label": "知识点思维导图"},
        {"type": "questions", "label": "练习题库"},
        {"type": "video", "label": "多模态视频"},
        {"type": "code", "label": "代码实操案例"},
        {"type": "reading", "label": "拓展阅读材料"}
    ]
    return {"code": 200, "data": types}