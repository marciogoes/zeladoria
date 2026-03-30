"""
Configuração central de testes
Sistema de Zeladoria Urbana - Belém/PA — Sprint 14
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Garante banco de testes antes de importar a app
os.environ.setdefault("SECRET_KEY", "test-secret-key-zero-seguranca")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.database.database import Base, get_db  # noqa: E402

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def criar_tabelas():
    """Cria todas as tabelas no banco de teste antes de qualquer teste."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="module")
def client(criar_tabelas):
    """Cliente FastAPI com banco SQLite em memória."""
    from main import app
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


def _get_or_create_usuario(email: str, nome: str, tipo: str) -> int:
    """Cria usuário no banco de teste se não existir. Retorna id."""
    from app.models.usuario import Usuario
    db = TestingSessionLocal()
    u = db.query(Usuario).filter_by(email=email).first()
    if not u:
        u = Usuario(
            nome=nome,
            email=email,
            senha=Usuario.hash_senha("senha123"),
            tipo=tipo,
            ativo=True,
        )
        db.add(u)
        db.commit()
        db.refresh(u)
    uid = u.id
    db.close()
    return uid


@pytest.fixture(scope="module")
def token_admin(client):
    """Token JWT de admin para testes."""
    from app.utils.auth import create_access_token
    uid = _get_or_create_usuario("admin@test.com", "Admin Teste", "admin")
    token = create_access_token(data={"sub": str(uid)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def token_cidadao(client):
    """Token JWT de cidadão para testes."""
    from app.utils.auth import create_access_token
    uid = _get_or_create_usuario("cidadao@test.com", "Cidadão Teste", "cidadao")
    token = create_access_token(data={"sub": str(uid)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def token_gestor(client):
    """Token JWT de gestor para testes."""
    from app.utils.auth import create_access_token
    uid = _get_or_create_usuario("gestor@test.com", "Gestor Teste", "gestor")
    token = create_access_token(data={"sub": str(uid)})
    return {"Authorization": f"Bearer {token}"}
