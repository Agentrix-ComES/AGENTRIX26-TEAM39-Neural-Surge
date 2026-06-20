# app.py
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent path to PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.db import init_db
from vector_db.qdrant import init_qdrant
from routes import plan

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize SQLite tables and index Qdrant collection on startup.
    """
    # 1. Initialize SQLite db
    init_db()
    # 2. Initialize Qdrant local vector db
    init_qdrant()
    yield

app = FastAPI(
    title="HomeOS Economic Intelligence API", 
    version="0.1.0", 
    lifespan=lifespan
)

# CORS setup for local React integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(plan.router, prefix="/api/plan", tags=["Plan"])

@app.get("/health")
@app.get("/")
def health_check():
    """
    Simple health check endpoint.
    """
    return {
        "status": "healthy",
        "message": "HomeOS Economic Intelligence Service is active."
    }
