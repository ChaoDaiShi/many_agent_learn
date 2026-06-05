from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import student_router, rag_router, gen_router, study_router
from db import engine, Base

app = FastAPI(title="AI智学助手", description="基于大模型的个性化资源生成与学习多智能体系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router, prefix="/api")
app.include_router(rag_router, prefix="/api")
app.include_router(gen_router, prefix="/api")
app.include_router(study_router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"code": 200, "message": "OK", "service": "AI智学助手"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)