"""
Sistema de Zeladoria Urbana - Belém/PA
Backend API com FastAPI
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uvicorn
from passlib.context import CryptContext

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./zeladoria.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuração de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================================
# MODELS (Banco de Dados)
# ==============================================

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    tipo_usuario = Column(String, nullable=False)  # cidadao, campo, gestor, admin
    telefone = Column(String)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(String)
    cor = Column(String)
    prioridade_padrao = Column(String, default="media")
    ativo = Column(Boolean, default=True)

class Bairro(Base):
    __tablename__ = "bairros"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    distrito = Column(String)
    populacao = Column(Integer)

class Chamado(Base):
    __tablename__ = "chamados"
    
    id = Column(Integer, primary_key=True, index=True)
    protocolo = Column(String, unique=True, nullable=False)
    categoria_id = Column(Integer, nullable=False)
    cidadao_id = Column(Integer, nullable=False)
    bairro_id = Column(Integer)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="aberto")  # aberto, em_andamento, concluido
    prioridade = Column(String, default="media")  # baixa, media, alta, critica
    data_abertura = Column(DateTime, default=datetime.now)
    data_conclusao = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# ==============================================
# SCHEMAS (Pydantic)
# ==============================================

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_usuario: str = "cidadao"
    telefone: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class ChamadoCreate(BaseModel):
    categoria_id: int
    titulo: str
    descricao: str
    endereco: str
    bairro_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# ==============================================
# FUNÇÕES AUXILIARES
# ==============================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerar_protocolo(db: Session):
    """Gera número de protocolo único"""
    ultimo = db.query(Chamado).count()
    ano = datetime.now().year
    numero = str(ultimo + 1).zfill(6)
    return f"BEL-{ano}-{numero}"

def hash_senha(senha: str):
    """Hash de senha com bcrypt"""
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    """Verifica senha"""
    return pwd_context.verify(senha, senha_hash)

# ==============================================
# POPULAR DADOS INICIAIS
# ==============================================

def popular_dados_iniciais():
    db = SessionLocal()
    
    # Verificar se já tem dados
    if db.query(Usuario).count() > 0:
        db.close()
        return
    
    print("🔄 Populando dados iniciais...")
    
    # Criar usuários
    usuarios = [
        Usuario(
            nome="Pedro Almeida",
            email="pedro.almeida@email.com",
            senha_hash=hash_senha("senha123"),
            tipo_usuario="cidadao"
        ),
        Usuario(
            nome="Gestor Municipal",
            email="gestor@belem.pa.gov.br",
            senha_hash=hash_senha("senha123"),
            tipo_usuario="gestor"
        ),
        Usuario(
            nome="João Silva",
            email="joao.silva@belem.pa.gov.br",
            senha_hash=hash_senha("senha123"),
            tipo_usuario="campo"
        ),
    ]
    
    for usuario in usuarios:
        db.add(usuario)
    
    # Criar categorias
    categorias = [
        Categoria(nome="Iluminação Pública", descricao="Postes e lâmpadas", cor="#F59E0B", prioridade_padrao="alta"),
        Categoria(nome="Buraco na Via", descricao="Buracos no asfalto", cor="#EF4444", prioridade_padrao="critica"),
        Categoria(nome="Lixo Acumulado", descricao="Acúmulo de lixo", cor="#10B981", prioridade_padrao="media"),
        Categoria(nome="Poda de Árvore", descricao="Árvores sobre fiação", cor="#22C55E", prioridade_padrao="alta"),
        Categoria(nome="Sinalização", descricao="Placas e semáforos", cor="#3B82F6", prioridade_padrao="critica"),
    ]
    
    for categoria in categorias:
        db.add(categoria)
    
    # Criar bairros
    bairros = [
        Bairro(nome="Campina", distrito="DABEL", populacao=15000),
        Bairro(nome="Cidade Velha", distrito="DABEL", populacao=18000),
        Bairro(nome="Umarizal", distrito="DABEL", populacao=14000),
        Bairro(nome="Nazaré", distrito="DABEL", populacao=10000),
        Bairro(nome="Marco", distrito="DABEL", populacao=25000),
        Bairro(nome="Guamá", distrito="DAGUA", populacao=98000),
        Bairro(nome="Terra Firme", distrito="DAGUA", populacao=65000),
    ]
    
    for bairro in bairros:
        db.add(bairro)
    
    db.commit()
    
    # Criar chamados de exemplo
    chamados = [
        Chamado(
            protocolo="BEL-2024-000001",
            categoria_id=1,
            cidadao_id=1,
            bairro_id=1,
            titulo="Poste apagado",
            descricao="Poste de iluminação apagado há 3 dias",
            endereco="Av. Presidente Vargas, 1234",
            latitude=-1.4558,
            longitude=-48.4902,
            status="aberto",
            prioridade="alta"
        ),
        Chamado(
            protocolo="BEL-2024-000002",
            categoria_id=2,
            cidadao_id=1,
            bairro_id=5,
            titulo="Buraco grande na via",
            descricao="Buraco causando risco de acidentes",
            endereco="Av. Almirante Barroso, 2500",
            latitude=-1.4350,
            longitude=-48.4650,
            status="em_andamento",
            prioridade="critica"
        ),
    ]
    
    for chamado in chamados:
        db.add(chamado)
    
    db.commit()
    db.close()
    
    print("✅ Dados iniciais criados com sucesso!")

# ==============================================
# CRIAR APP FASTAPI
# ==============================================

app = FastAPI(
    title="Sistema de Zeladoria Urbana - Belém/PA",
    description="API para gestão de zeladoria urbana",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================
# ROTAS
# ==============================================

@app.get("/")
def root():
    """Rota principal"""
    return {
        "message": "Sistema de Zeladoria Urbana - Belém/PA",
        "version": "1.0.0",
        "status": "Online",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check"""
    return {"status": "OK", "timestamp": datetime.now()}

# ====== AUTENTICAÇÃO ======

@app.post("/api/auth/login")
def login(credenciais: UsuarioLogin, db: Session = Depends(get_db)):
    """Login de usuário"""
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()
    
    if not usuario or not verificar_senha(credenciais.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    return {
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        }
    }

@app.post("/api/auth/register")
def register(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar novo usuário"""
    # Verificar se email já existe
    existe = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar usuário
    novo_usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha_hash=hash_senha(usuario_data.senha),
        tipo_usuario=usuario_data.tipo_usuario,
        telefone=usuario_data.telefone
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {
        "success": True,
        "message": "Usuário criado com sucesso",
        "usuario": {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email
        }
    }

# ====== CHAMADOS ======

@app.get("/api/chamados")
def listar_chamados(
    status: Optional[str] = None,
    categoria_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar chamados"""
    query = db.query(Chamado)
    
    if status:
        query = query.filter(Chamado.status == status)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)
    
    chamados = query.order_by(Chamado.data_abertura.desc()).all()
    
    return {
        "success": True,
        "total": len(chamados),
        "chamados": chamados
    }

@app.get("/api/chamados/{chamado_id}")
def buscar_chamado(chamado_id: int, db: Session = Depends(get_db)):
    """Buscar chamado por ID"""
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    return {"success": True, "chamado": chamado}

@app.post("/api/chamados")
def criar_chamado(chamado_data: ChamadoCreate, db: Session = Depends(get_db)):
    """Criar novo chamado"""
    protocolo = gerar_protocolo(db)
    
    novo_chamado = Chamado(
        protocolo=protocolo,
        categoria_id=chamado_data.categoria_id,
        cidadao_id=1,  # TODO: Pegar do token JWT
        bairro_id=chamado_data.bairro_id,
        titulo=chamado_data.titulo,
        descricao=chamado_data.descricao,
        endereco=chamado_data.endereco,
        latitude=chamado_data.latitude,
        longitude=chamado_data.longitude
    )
    
    db.add(novo_chamado)
    db.commit()
    db.refresh(novo_chamado)
    
    return {
        "success": True,
        "message": "Chamado criado com sucesso",
        "protocolo": protocolo,
        "chamado": novo_chamado
    }

# ====== CATEGORIAS ======

@app.get("/api/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    """Listar categorias"""
    categorias = db.query(Categoria).filter(Categoria.ativo == True).all()
    return {"success": True, "categorias": categorias}

# ====== BAIRROS ======

@app.get("/api/bairros")
def listar_bairros(db: Session = Depends(get_db)):
    """Listar bairros"""
    bairros = db.query(Bairro).all()
    return {"success": True, "bairros": bairros}

# ====== ESTATÍSTICAS ======

@app.get("/api/estatisticas")
def estatisticas(db: Session = Depends(get_db)):
    """Estatísticas gerais"""
    total = db.query(Chamado).count()
    abertos = db.query(Chamado).filter(Chamado.status == "aberto").count()
    em_andamento = db.query(Chamado).filter(Chamado.status == "em_andamento").count()
    concluidos = db.query(Chamado).filter(Chamado.status == "concluido").count()
    
    return {
        "success": True,
        "stats": {
            "total": total,
            "abertos": abertos,
            "em_andamento": em_andamento,
            "concluidos": concluidos,
            "taxa_resolucao": round((concluidos / total * 100) if total > 0 else 0, 1)
        }
    }

# ==============================================
# INICIALIZAÇÃO
# ==============================================

@app.on_event("startup")
def startup_event():
    """Executar ao iniciar"""
    print("\n" + "="*60)
    print("🏛️  SISTEMA DE ZELADORIA URBANA - BELÉM/PA")
    print("="*60)
    popular_dados_iniciais()
    print("✅ API Online em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("="*60 + "\n")

# ==============================================
# EXECUTAR
# ==============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
