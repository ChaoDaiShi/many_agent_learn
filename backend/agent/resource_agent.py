from .base_agent import BaseAgent

class ResourceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="学习资源生成Agent",
            role="根据学生需求生成个性化学习资源"
        )
    
    def execute(self, resource_type: str, topic: str, **kwargs):
        type_prompts = {
            "document": "生成详细的专业课程讲解文档",
            "mindmap": "生成知识点思维导图（用Markdown列表格式）",
            "questions": "生成练习题库（包含题目、选项、答案、解析）",
            "video": "生成视频脚本或讲解大纲",
            "code": "生成代码实操案例（包含代码和详细解释）",
            "reading": "生成拓展阅读材料推荐和摘要"
        }
        
        major = kwargs.get("major", "")
        course = kwargs.get("course", "")
        difficulty = kwargs.get("difficulty", "basic")
        requirement = kwargs.get("requirement", "")
        
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