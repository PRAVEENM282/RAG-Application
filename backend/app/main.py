from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health, ingest, auth
from app.api import websocket
from app.infrastructure.database.models import init_db

app = FastAPI(title=settings.APP_NAME)

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()

# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["Auth"])
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["Ingestion"])
app.include_router(websocket.router, prefix="/ws", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Welcome to RAG System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
