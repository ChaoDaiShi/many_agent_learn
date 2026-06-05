from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from service import StudyService

router = APIRouter(prefix="/study", tags=["study"])

@router.get("/path/{student_id}")
def get_study_path(student_id: str, db: Session = Depends(get_db)):
    service = StudyService(db)
    study_path = service.get_study_path(student_id)
    if not study_path:
        return {"code": 404, "message": "学习路径不存在"}
    return {"code": 200, "data": study_path.__dict__}

@router.post("/path/{student_id}")
def generate_study_path(student_id: str, data: dict, db: Session = Depends(get_db)):
    service = StudyService(db)
    study_path = service.generate_study_path(student_id, data)
    return {"code": 200, "data": study_path.__dict__}

@router.put("/path/{path_id}")
def update_study_path(path_id: str, data: dict, db: Session = Depends(get_db)):
    service = StudyService(db)
    study_path = service.update_study_path(path_id, data)
    if not study_path:
        return {"code": 404, "message": "学习路径不存在"}
    return {"code": 200, "data": study_path.__dict__}

@router.get("/wrong-questions/{student_id}")
def get_wrong_questions(student_id: str, page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    service = StudyService(db)
    result = service.get_wrong_questions(student_id, page, size)
    return {"code": 200, "data": [q.__dict__ for q in result["data"]], "total": result["total"]}

@router.post("/wrong-question")
def add_wrong_question(data: dict, db: Session = Depends(get_db)):
    service = StudyService(db)
    question = service.add_wrong_question(data)
    return {"code": 200, "data": question.__dict__}

@router.delete("/wrong-question/{question_id}")
def delete_wrong_question(question_id: str, db: Session = Depends(get_db)):
    service = StudyService(db)
    success = service.delete_wrong_question(question_id)
    if not success:
        return {"code": 404, "message": "错题不存在"}
    return {"code": 200, "message": "删除成功"}

@router.get("/progress/{student_id}")
def get_progress(student_id: str, db: Session = Depends(get_db)):
    service = StudyService(db)
    study_path = service.get_study_path(student_id)
    if not study_path:
        return {"code": 404, "message": "学习路径不存在"}
    
    total_steps = len(study_path.steps) if study_path.steps else 0
    progress = (study_path.current_step / total_steps) * 100 if total_steps > 0 else 0
    
    return {"code": 200, "data": {
        "student_id": student_id,
        "current_step": study_path.current_step,
        "total_steps": total_steps,
        "progress": progress,
        "status": study_path.status
    }}

@router.put("/progress/{student_id}")
def update_progress(student_id: str, data: dict, db: Session = Depends(get_db)):
    service = StudyService(db)
    study_path = service.get_study_path(student_id)
    if not study_path:
        return {"code": 404, "message": "学习路径不存在"}
    
    updated = service.update_study_path(study_path.id, data)
    return {"code": 200, "data": updated.__dict__}