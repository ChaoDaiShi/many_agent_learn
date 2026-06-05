from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .mysql_base import Base

class StudentPortrait(Base):
    __tablename__ = "student_portraits"
    
    id = Column(String(36), primary_key=True, index=True)
    student_id = Column(String(36), unique=True, index=True)
    major = Column(String(100))
    grade = Column(String(50))
    learning_goal = Column(Text)
    interests = Column(Text)
    knowledge_base = Column(JSON)
    cognitive_traits = Column(JSON)
    learning_preferences = Column(JSON)
    weak_points = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), index=True)
    file_path = Column(String(500))
    size = Column(Integer)
    chunk_count = Column(Integer, default=0)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255))
    type = Column(String(50), index=True)
    content = Column(Text)
    major = Column(String(100))
    course = Column(String(200))
    topic = Column(String(200))
    difficulty = Column(String(20))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)

class StudyPath(Base):
    __tablename__ = "study_paths"
    
    id = Column(String(36), primary_key=True, index=True)
    student_id = Column(String(36), ForeignKey("student_portraits.student_id"))
    steps = Column(JSON)
    current_step = Column(Integer, default=0)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    student = relationship("StudentPortrait", back_populates="study_paths")

class WrongQuestion(Base):
    __tablename__ = "wrong_questions"
    
    id = Column(String(36), primary_key=True, index=True)
    student_id = Column(String(36), ForeignKey("student_portraits.student_id"))
    title = Column(String(255))
    content = Column(Text)
    subject = Column(String(100))
    error_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    
    student = relationship("StudentPortrait", back_populates="wrong_questions")

StudentPortrait.study_paths = relationship("StudyPath", order_by=StudyPath.created_at, back_populates="student")
StudentPortrait.wrong_questions = relationship("WrongQuestion", order_by=WrongQuestion.created_at, back_populates="student")