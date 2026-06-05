import requests
import json
import time
import hashlib
import base64
import hmac
from urllib.parse import urlparse
from config.settings import settings

class SparkLLM:
    def __init__(self):
        self.app_id = settings.SPARK_APP_ID
        self.api_key = settings.SPARK_API_KEY
        self.api_secret = settings.SPARK_API_SECRET
        self.api_url = settings.SPARK_API_URL
    
    def _generate_signature(self, date, host, path):
        signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')
        return signature
    
    def _get_auth_headers(self):
        parsed_url = urlparse(self.api_url)
        host = parsed_url.hostname
        path = parsed_url.path
        
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        
        signature = self._generate_signature(date, host, path)
        
        authorization = (
            f'api_key="{self.api_key}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature}"'
        )
        
        return {
            "Host": host,
            "Date": date,
            "Authorization": authorization
        }
    
    def chat(self, messages, temperature=0.7, max_tokens=2048):
        url = f"https://{urlparse(self.api_url).hostname}/v3.1/chat"
        
        payload = {
            "header": {
                "app_id": self.app_id
            },
            "parameter": {
                "chat": {
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        
        headers = self._get_auth_headers()
        headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("header", {}).get("code") == 0:
                choices = result.get("payload", {}).get("choices", {}).get("text", [])
                if choices:
                    return choices[0].get("content", "")
            return ""
        except Exception as e:
            return f"调用失败: {str(e)}"
    
    def extract_portrait(self, conversation_history):
        prompt = f"""
        请从以下对话历史中提取学生画像信息：
        
        {conversation_history}
        
        请以JSON格式输出，包含以下维度：
        - major: 专业
        - grade: 年级
        - learning_goal: 学习目标
        - interests: 兴趣方向
        - knowledge_base: 知识基础（JSON对象，科目:掌握程度0-100）
        - cognitive_traits: 认知风格（数组，包含name和value）
        - learning_preferences: 学习偏好（数组）
        - weak_points: 易错点（JSON对象，知识点:错误次数）
        """
        
        messages = [
            {"role": "system", "content": "你是一个学生画像分析助手，擅长从对话中提取学生特征信息。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages)
    
    def generate_resource(self, resource_type, topic, major="", course="", difficulty="basic", requirement=""):
        type_prompts = {
            "document": "生成详细的专业课程讲解文档",
            "mindmap": "生成知识点思维导图（用Markdown列表格式）",
            "questions": "生成练习题库（包含题目、选项、答案、解析）",
            "video": "生成视频脚本或讲解大纲",
            "code": "生成代码实操案例（包含代码和详细解释）",
            "reading": "生成拓展阅读材料推荐和摘要"
        }
        
        prompt = f"""
        请生成{type_prompts.get(resource_type, "学习资源")}：
        
        专业：{major}
        课程：{course}
        知识点：{topic}
        难度：{difficulty}
        额外要求：{requirement}
        
        请用中文输出，格式清晰，内容专业。
        """
        
        messages = [
            {"role": "system", "content": "你是一个教育资源生成专家，擅长生成高质量的学习材料。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat(messages)

spark_llm = SparkLLM()