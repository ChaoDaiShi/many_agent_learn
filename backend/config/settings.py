from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DATABASE: str = "ai_edu_db"
    
    SPARK_APP_ID: str = ""
    SPARK_API_KEY: str = ""
    SPARK_API_SECRET: str = ""
    SPARK_API_URL: str = "wss://spark-api.xf-yun.com/v3.1/chat"
    
    CHROMA_PATH: str = "./chroma_db"
    UPLOAD_FOLDER: str = "./uploads"
    
    JWT_SECRET_KEY: str = "your_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"

settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / settings.UPLOAD_FOLDER
CHROMA_DIR = BASE_DIR / settings.CHROMA_PATH

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)