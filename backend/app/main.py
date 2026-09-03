import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure root workspace is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.config import settings
from backend.app.database import init_db
from backend.app.seed_data import seed_demo_data
from backend.app.routers import products, ai_endpoints, artisan, buyer, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize SQLite DB and seed demo artisan products
    print("[TANTU Backend] Initializing database...")
    init_db()
    seed_demo_data()
    print(f"[TANTU Backend] Server initialized. MOCK_AI={settings.MOCK_AI}")
    yield
    # Shutdown logic if needed
    print("[TANTU Backend] Server shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "**TANTU API Backend** for Smart India Hackathon (Problem Statement 26090).\n\n"
        "AI-Driven Market Linkage and Smart Cataloging Mobile Application for Marginalized Artisans.\n\n"
        "Integrates AI modules from Team Members (M - Voice/NLP, R - Image Enhancer, S - Smart Pricing, P - Frontend UI)."
    ),
    lifespan=lifespan
)

# Enable CORS for frontend web / mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(products.router)
app.include_router(ai_endpoints.router)
app.include_router(artisan.router)
app.include_router(buyer.router)
app.include_router(orders.router)


@app.get("/", tags=["Health & Status"])
def root_status():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "sih_problem_statement": settings.SIH_PROBLEM_STATEMENT,
        "mock_ai": settings.MOCK_AI,
        "documentation": "/docs"
    }


@app.get("/api/health", tags=["Health & Status"])
def health_check():
    return {
        "status": "healthy",
        "database": "sqlite_connected",
        "mock_ai_mode": settings.MOCK_AI
    }


@app.get("/api/config", tags=["Health & Status"])
def get_config():
    return {
        "mock_ai": settings.MOCK_AI,
        "team_roles": {
            "P": "Frontend / Mobile UI",
            "M": "AI / Voice / NLP / Sentiment",
            "R": "AI Image Enhancement",
            "S": "Smart Pricing + B2B Marketplace",
            "A": "Backend Lead & Core Architecture"
        },
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
