from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database.database import engine, Base
from app.routes import auth, chamados, categorias, bairros, usuarios, relatorios, secretarias, comentarios
from app.routers.servicos_router import router as servicos_router
from app.routers.catalogo_router import router as catalogo_router
from app.routers.engajamento_router import router as engajamento_router

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="🏛️ Sistema de Zeladoria Urbana - Belém/PA",
    description="API completa para gestão de zeladoria urbana municipal",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Servir frontend
frontend_path = "frontend"
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/app")
    def serve_app():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    @app.get("/dashboard")
    def serve_dashboard():
        return FileResponse(os.path.join(frontend_path, "dashboard.html"))

    @app.get("/manifest.json")
    def serve_manifest():
        return FileResponse(os.path.join(frontend_path, "manifest.json"), media_type="application/manifest+json")

    @app.get("/sw.js")
    def serve_sw():
        return FileResponse(os.path.join(frontend_path, "sw.js"), media_type="application/javascript")

# Registrar rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(chamados.router, prefix="/api/chamados", tags=["Chamados"])
app.include_router(comentarios.router, tags=["Comentários"])
app.include_router(categorias.router, prefix="/api/categorias", tags=["Categorias"])
app.include_router(bairros.router, prefix="/api/bairros", tags=["Bairros"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuários"])
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])
app.include_router(secretarias.router, tags=["Secretarias"])
app.include_router(servicos_router, tags=["Catálogo de Serviços"])
app.include_router(catalogo_router, tags=["Catálogo Completo"])
app.include_router(engajamento_router)

# Rota raiz
@app.get("/")
def read_root():
    return {
        "message": "🏛️ Sistema de Zeladoria Urbana - Belém/PA",
        "version": "2.0.0",
        "docs": "/docs",
        "app": "/app",
        "dashboard": "/dashboard",
        "endpoints": {
            "auth": "/api/auth",
            "chamados": "/api/chamados",
            "categorias": "/api/categorias",
            "bairros": "/api/bairros",
            "secretarias": "/api/secretarias",
            "servicos": "/api/servicos",
            "catalogo": "/api/catalogo"
        }
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Sistema funcionando perfeitamente"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
