import os
from dotenv import load_dotenv

# Load .env file from project root or current working directory
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings:
    PROJECT_NAME: str = "TANTU - Artisans Market Linkage & Smart Cataloging API"
    VERSION: str = "1.0.0"
    SIH_PROBLEM_STATEMENT: str = "26090 - AI-Driven Market Linkage for Marginalized Artisans"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Mock AI toggle (Crucial for SIH demo resilience)
    MOCK_AI: bool = os.getenv("MOCK_AI", "true").lower() == "true"
    
    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "..", "tantu.db"))


settings = Settings()
