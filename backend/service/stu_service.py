import uuid
from sqlalchemy.orm import Session
from db.models import StudentPortrait
from utils.spark_llm import spark_llm
import json

class StudentService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_portrait(self, student_id: str):
        return self.db.query(StudentPortrait).filter(StudentPortrait.student_id == student_id).first()
    
    def create_portrait(self, student_id: str, data: dict):
        portrait = StudentPortrait(
            id=str(uuid.uuid4()),
            student_id=student_id,
            major=data.get("major", ""),
            grade=data.get("grade", ""),
            learning_goal=data.get("learning_goal", ""),
            interests=data.get("interests", ""),
            knowledge_base=data.get("knowledge_base", {}),
            cognitive_traits=data.get("cognitive_traits", []),
            learning_preferences=data.get("learning_preferences", []),
            weak_points=data.get("weak_points", {})
        )
        self.db.add(portrait)
        self.db.commit()
        self.db.refresh(portrait)
        return portrait
    
    def update_portrait(self, student_id: str, data: dict):
        portrait = self.get_portrait(student_id)
        if not portrait:
            return None
        
        if "major" in data:
            portrait.major = data["major"]
        if "grade" in data:
            portrait.grade = data["grade"]
        if "learning_goal" in data:
            portrait.learning_goal = data["learning_goal"]
        if "interests" in data:
            portrait.interests = data["interests"]
        if "knowledge_base" in data:
            portrait.knowledge_base = data["knowledge_base"]
        if "cognitive_traits" in data:
            portrait.cognitive_traits = data["cognitive_traits"]
        if "learning_preferences" in data:
            portrait.learning_preferences = data["learning_preferences"]
        if "weak_points" in data:
            portrait.weak_points = data["weak_points"]
        
        self.db.commit()
        self.db.refresh(portrait)
        return portrait
    
    def delete_portrait(self, student_id: str):
        portrait = self.get_portrait(student_id)
        if not portrait:
            return False
        
        self.db.delete(portrait)
        self.db.commit()
        return True
    
    def chat_with_portrait(self, student_id: str, message: str):
        portrait = self.get_portrait(student_id)
        
        conversation_history = ""
        if portrait:
            conversation_history = f"""
            学生画像：
            专业：{portrait.major}
            年级：{portrait.grade}
            学习目标：{portrait.learning_goal}
            兴趣方向：{portrait.interests}
            知识基础：{json.dumps(portrait.knowledge_base)}
            认知风格：{json.dumps(portrait.cognitive_traits)}
            学习偏好：{json.dumps(portrait.learning_preferences)}
            易错点：{json.dumps(portrait.weak_points)}
            """
        
        conversation_history += f"\n用户问题：{message}"
        
        messages = [
            {
                "role": "system",
                "content": "你是一个AI学习助手，根据学生画像信息回答问题，帮助学生学习。"
            },
            {
                "role": "user",
                "content": conversation_history
            }
        ]
        
        response = spark_llm.chat(messages)
        
        new_portrait_data = {}
        try:
            extracted = spark_llm.extract_portrait(conversation_history)
            new_portrait_data = json.loads(extracted)
        except Exception:
            pass
        
        if portrait:
            self.update_portrait(student_id, new_portrait_data)
        elif new_portrait_data:
            self.create_portrait(student_id, new_portrait_data)
        
        return {
            "content": response,
            "portrait": new_portrait_data if new_portrait_data else None
        }