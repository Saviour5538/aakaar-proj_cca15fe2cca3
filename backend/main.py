import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from database.config import get_db, Base, engine
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from backend.routes.conversations import router as conversations_router

# Import pgvector adapter registration
try:
    import psycopg2
    from pgvector.psycopg2 import register_vector
    # Register vector adapter for psycopg2
    psycopg2.extensions.register_adapter(list, register_vector)
except ImportError:
    pass

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        # Ensure all tables are created
        Base.metadata.create_all(bind=engine)
        
        # Test database connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute("SELECT 1"))
            
    except Exception as e:
        raise RuntimeError(f"Failed to initialize database: {str(e)}")
    
    yield  # Application is running

    # Shutdown logic
    await engine.dispose()

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="DocMind",
    description="AI-powered document management and conversational assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")

# Auto-mounted AI router — ai/routes.py exposes /api/ai/* (it carries its own prefix)
try:
    from ai.routes import router as ai_router
    app.include_router(ai_router)
except ImportError as e:
    print(f"Warning: AI router not found: {e}")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# This ensures the module can be imported correctly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)