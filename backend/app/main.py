from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.database import init_db
from app.api.routes import feedback, analysis, integrations

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(
    feedback.router,
    prefix=f"{settings.API_V1_PREFIX}/feedback",
    tags=["feedback"]
)
app.include_router(
    analysis.router,
    prefix=f"{settings.API_V1_PREFIX}/analysis",
    tags=["analysis"]
)
app.include_router(
    integrations.router,
    prefix=f"{settings.API_V1_PREFIX}/integrations",
    tags=["integrations"]
)

@app.get("/")
async def root():
    return {
        "message": "Feedback Intelligence API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}