import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usa DATABASE_URL do ambiente se disponível e não vazia, senão SQLite local
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# Railway fornece URLs postgres:// mas SQLAlchemy precisa de postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Se vazio ou inválido, usa SQLite
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./zeladoria.db"

# Configurar engine conforme o banco
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
