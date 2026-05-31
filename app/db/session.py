from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

# SQLite（MVP 用）
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 用
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# 初回起動時にテーブル作成
def init_db():
    Base.metadata.create_all(bind=engine)
