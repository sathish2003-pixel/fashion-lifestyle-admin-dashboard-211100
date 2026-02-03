"""
Database configuration and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Read database connection from environment variables set by orchestrator
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5000")

# Construct database URL from individual components (more reliable than parsing POSTGRES_URL)
if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_DB:
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
else:
    # Fallback: try to use POSTGRES_URL if individual components not available
    POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://appuser:dbuser123@localhost:5000/myapp")
    DATABASE_URL = POSTGRES_URL

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
