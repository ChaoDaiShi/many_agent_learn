from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from service import StudentService

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/portrait/{student_id}")
def get_portrait(student_id: str, db: Session = Depends(get_db)):
    service = StudentService(db)
    portrait = service.get_portrait(student_id)
    if not portrait:
        return {"code": 404, "message": "画像不存在"}
    return {"code": 200, "data": portrait.__dict__}

@router.post("/portrait")
def create_portrait(data: dict, db: Session = Depends(get_db)):
    service = StudentService(db)
    student_id = data.get("student_id", "default_student")
    portrait = service.create_portrait(student_id, data)
    return {"code": 200, "data": portrait.__dict__}

@router.put("/portrait/{student_id}")
def update_portrait(student_id: str, data: dict, db: Session = Depends(get_db)):
    service = StudentService(db)
    portrait = service.update_portrait(student_id, data)
    if not portrait:
        return {"code": 404, "message": "画像不存在"}
    return {"code": 200, "data": portrait.__dict__}

@router.delete("/portrait/{student_id}")
def delete_portrait(student_id: str, db: Session = Depends(get_db)):
    service = StudentService(db)
    success = service.delete_portrait(student_id)
    if not success:
        return {"code": 404, "message": "画像不存在"}
    return {"code": 200, "message": "删除成功"}

@router.post("/chat/{student_id}")
def chat_with_portrait(student_id: str, data: dict, db: Session = Depends(get_db)):
    service = StudentService(db)
    message = data.get("message", "")
    result = service.chat_with_portrait(student_id, message)
    return {"code": 200, "data": result}

@router.get("/portrait")
def get_portrait_list(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    service = StudentService(db)
    portraits = service.get_portrait_list(page, size)
    return {"code": 200, "data": portraits}