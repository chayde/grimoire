"""Database connection and session management."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

# Create database engine
# For SQLite, we need connect_args to allow multithreading
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
    connect_args=connect_args,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    Yields:
        Database session

    Example:
        @app.get("/blueprints/")
        def get_blueprints(db: Session = Depends(get_db)):
            return db.query(Blueprint).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    from app.models.blueprint import Base

    Base.metadata.create_all(bind=engine)
