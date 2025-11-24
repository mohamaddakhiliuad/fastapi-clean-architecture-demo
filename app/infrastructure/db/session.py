"""
Database session and Base configuration.

Responsibilities:
- Create SQLAlchemy engine using settings.database_url.
- Provide SessionLocal factory.
- Expose Base for SQLAlchemy models.
- Provide get_db dependency for FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLAlchemy base class for all models
Base = declarative_base()

# Create engine using the database URL from settings
engine = create_engine(
    settings.database_url,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI dependency that yields a database session.

    Ensures the session is closed after the request is handled.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
