# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite の DB ファイルを app/app.db に作成
DATABASE_URL = "sqlite:///app.db"

# Engine（DB 接続の本体）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 用
)

# Base（モデルの親クラス）
Base = declarative_base()

# SessionLocal（セッションファクトリ）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
