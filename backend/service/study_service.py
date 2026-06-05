import uuid
from sqlalchemy.orm import Session
from db.models import StudyPath, WrongQuestion, StudentPortrait
from utils.spark_llm import spark_llm
import json

class StudyService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_study_path(self, student_id: str, data: dict):
        target = data.get("target", "complete")
        duration = data.get("duration", 30)
        
        portrait = self.db.query(StudentPortrait).filter(StudentPortrait.student_id == student_id).first()
        
        prompt = f"""
        请为学生生成个性化学习路径：
        
        学生信息：
        专业：{portrait.major if portrait else '未知'}
        年级：{portrait.grade if portrait else '未知'}
        学习目标：{portrait.learning_goal if portrait else '未知'}
        知识基础：{json.dumps(portrait.knowledge_base) if portrait else '{}'}
        
        目标：{target}
        预计时长：{duration}分钟
        
        请以JSON格式输出学习路径，包含steps数组，每个step包含：
        - title: 步骤标题
        - description: 步骤描述
        - duration: 预计时长（分钟）
        - resource_type: 资源类型
        """
        
        messages = [
            {"role": "system", "content": "你是一个学习路径规划专家，擅长为学生制定个性化学习计划。"},
            {"role": "user", "content": prompt}
        ]
        
        result = spark_llm.chat(messages)
        
        try:
            steps = json.loads(result)
        except Exception:
            steps = self._generate_default_path(duration)
        
        study_path = StudyPath(
            id=str(uuid.uuid4()),
            student_id=student_id,
            steps=steps,
            current_step=0
        )
        
        self.db.add(study_path)
        self.db.commit()
        self.db.refresh(study_path)
        
        return study_path
    
    def _generate_default_path(self, duration):
        steps = []
        num_steps = min(5, max(2, duration // 15))
        step_duration = duration // num_steps
        
        resources = ["视频讲解", "文档阅读", "练习题目", "代码实操", "知识测验"]
        
        for i in range(num_steps):
            steps.append({
                "title": f"学习模块 {i + 1}",
                "description": f"完成第 {i + 1} 个学习模块",
                "duration": step_duration,
                "resource_type": resources[i % len(resources)]
            })
        
        return steps
    
    def get_study_path(self, student_id: str):
        return self.db.query(StudyPath).filter(StudyPath.student_id == student_id).order_by(StudyPath.created_at.desc()).first()
    
    def update_study_path(self, path_id: str, data: dict):
        path = self.db.query(StudyPath).filter(StudyPath.id == path_id).first()
        if not path:
            return None
        
        if "current_step" in data:
            path.current_step = data["current_step"]
        if "status" in data:
            path.status = data["status"]
        
        self.db.commit()
        self.db.refresh(path)
        return path
    
    def get_wrong_questions(self, student_id: str, page: int, size: int):
        skip = (page - 1) * size
        questions = self.db.query(WrongQuestion).filter(WrongQuestion.student_id == student_id).order_by(WrongQuestion.created_at.desc()).offset(skip).limit(size).all()
        total = self.db.query(WrongQuestion).filter(WrongQuestion.student_id == student_id).count()
        return {"data": questions, "total": total}
    
    def add_wrong_question(self, data: dict):
        question = WrongQuestion(
            id=str(uuid.uuid4()),
            student_id=data.get("student_id"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            subject=data.get("subject", ""),
            error_count=data.get("error_count", 1)
        )
        
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question
    
    def delete_wrong_question(self, question_id: str):
        question = self.db.query(WrongQuestion).filter(WrongQuestion.id == question_id).first()
        if not question:
            return False
        
        self.db.delete(question)
        self.db.commit()
        return True