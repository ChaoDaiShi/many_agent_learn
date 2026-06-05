import uuid
from sqlalchemy.orm import Session
from db.models import Resource, StudentPortrait
from utils.spark_llm import spark_llm
import json

class GenService:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_resource(self, data: dict):
        resource_type = data.get("type", "document")
        topic = data.get("topic", "")
        major = data.get("major", "")
        course = data.get("course", "")
        difficulty = data.get("difficulty", "basic")
        requirement = data.get("requirement", "")
        
        content = spark_llm.generate_resource(
            resource_type=resource_type,
            topic=topic,
            major=major,
            course=course,
            difficulty=difficulty,
            requirement=requirement
        )
        
        resource = Resource(
            id=str(uuid.uuid4()),
            title=f"{topic} - {resource_type}",
            type=resource_type,
            content=content,
            major=major,
            course=course,
            topic=topic,
            difficulty=difficulty,
            metadata={}
        )
        
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        
        return resource
    
    def get_resources(self, page: int, size: int):
        skip = (page - 1) * size
        resources = self.db.query(Resource).order_by(Resource.created_at.desc()).offset(skip).limit(size).all()
        total = self.db.query(Resource).count()
        return {"data": resources, "total": total}
    
    def get_resource(self, resource_id: str):
        return self.db.query(Resource).filter(Resource.id == resource_id).first()
    
    def delete_resource(self, resource_id: str):
        resource = self.get_resource(resource_id)
        if not resource:
            return False
        
        self.db.delete(resource)
        self.db.commit()
        return True
    
    def regenerate_resource(self, resource_id: str, data: dict):
        resource = self.get_resource(resource_id)
        if not resource:
            return None
        
        content = spark_llm.generate_resource(
            resource_type=data.get("type", resource.type),
            topic=data.get("topic", resource.topic),
            major=data.get("major", resource.major),
            course=data.get("course", resource.course),
            difficulty=data.get("difficulty", resource.difficulty),
            requirement=data.get("requirement", "")
        )
        
        resource.content = content
        resource.type = data.get("type", resource.type)
        resource.topic = data.get("topic", resource.topic)
        resource.major = data.get("major", resource.major)
        resource.course = data.get("course", resource.course)
        resource.difficulty = data.get("difficulty", resource.difficulty)
        
        self.db.commit()
        self.db.refresh(resource)
        return resource