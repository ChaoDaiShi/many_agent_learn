from abc import ABC, abstractmethod
from utils.spark_llm import spark_llm

class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    def chat(self, messages):
        return spark_llm.chat(messages)