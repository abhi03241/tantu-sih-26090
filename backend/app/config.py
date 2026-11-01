import os
from dotenv import load_dotenv

# Load .env file from project root or current working directory
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings:
    PROJECT_NAME: str = "ShilpVani - Artisans Market Linkage & Smart Cataloging API"
    VERSION: str = "1.0.0"
    SIH_PROBLEM_STATEMENT: str = "26090 - AI-Driven Market Linkage for Marginalized Artisans"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Mock AI toggle (Crucial for SIH demo resilience)
    MOCK_AI: bool = os.getenv("MOCK_AI", "true").lower() == "true"
    
    # Prototype persistence. Cloud hosts can point all three paths at one
    # persistent disk without changing the SQLite/file-storage architecture.
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "..", "tantu.db"))
    UPLOADS_DIR: str = os.getenv(
        "UPLOADS_DIR", os.path.join(os.path.dirname(__file__), "uploads")
    )
    ENHANCED_IMAGES_DIR: str = os.getenv(
        "ENHANCED_IMAGES_DIR",
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "enhanced"),
    )
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "*").split(",")
        if origin.strip()
    ]


settings = Settings()
