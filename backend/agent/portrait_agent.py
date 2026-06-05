from .base_agent import BaseAgent
import json

class PortraitAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="学生画像抽取Agent",
            role="从对话历史中提取学生特征信息，构建学生画像"
        )
    
    def execute(self, conversation_history: str):
        prompt = f"""
        请从以下对话历史中提取学生画像信息：
        
        {conversation_history}
        
        请以JSON格式输出，包含以下维度：
        - major: 专业
        - grade: 年级
        - learning_goal: 学习目标
        - interests: 兴趣方向
        - knowledge_base: 知识基础（JSON对象，科目:掌握程度0-100）
        - cognitive_traits: 认知风格（数组，包含name和value字段）
        - learning_preferences: 学习偏好（数组）
        - weak_points: 易错点（JSON对象，知识点:错误次数）
        """
        
        messages = [
            {"role": "system", "content": "你是一个学生画像分析助手，擅长从对话中提取学生特征信息。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self.chat(messages)
        
        try:
            return json.loads(result)
        except Exception:
            return {
                "major": "",
                "grade": "",
                "learning_goal": "",
                "interests": "",
                "knowledge_base": {},
                "cognitive_traits": [],
                "learning_preferences": [],
                "weak_points": {}
            }