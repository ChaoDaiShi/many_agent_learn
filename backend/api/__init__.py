from .student_api import router as student_router
from .rag_api import router as rag_router
from .gen_api import router as gen_router
from .study_api import router as study_router

__all__ = ["student_router", "rag_router", "gen_router", "study_router"]