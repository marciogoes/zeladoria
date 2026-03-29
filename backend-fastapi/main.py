from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import engine, Base
from app.routes import tasks_router

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="API de Tarefas",
    description="API RESTful com FastAPI e SQLite",
    version="1.0.0"
)

# Configurar CORS (permitir requisições do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas da API
app.include_router(tasks_router)

# Servir arquivos estáticos do frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/app")
    def serve_frontend():
        """Servir a aplicação frontend"""
        return FileResponse(os.path.join(frontend_path, "index.html"))

# Rota raiz
@app.get("/")
def read_root():
    return {
        "message": "API de Tarefas está rodando!",
        "docs": "/docs",
        "app": "/app",
        "version": "1.0.0"
    }

# Rota de health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
