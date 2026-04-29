from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, chapters, quizzes, progress, access, admin, search, hybrid

app = FastAPI(title="Course Companion API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(access.router, prefix="/access", tags=["access"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(search.router, tags=["search"])
app.include_router(hybrid.router, prefix="/hybrid", tags=["hybrid"])


@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
