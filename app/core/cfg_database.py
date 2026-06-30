from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from app.core.cfg_config import get_settings

settings = get_settings()

_db_url = URL.create(
    "postgresql+pg8000",
    username="postgres",
    password="postgres",
    host="localhost",
    port=5432,
    database="compartamos_banco_db",
)
engine = create_engine(_db_url, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
