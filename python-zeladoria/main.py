from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os, logging

from app.database.database import engine, Base, SessionLocal
from app.models.historico import ChamadoHistorico  # Sprint 17 — garante criação da tabela
from app.routes import auth, chamados, categorias, bairros, usuarios, relatorios, secretarias, comentarios
# inovacoes.py descontinuado — migrado para geo_router.py e ia_router.py (sprints 9-12)
from app.routers.servicos_router import router as servicos_router
from app.routers.catalogo_router import router as catalogo_router
from app.routers.engajamento_router import router as engajamento_router
from app.routers.integracoes_router import router as integracoes_router
from app.routers.transparencia_router import router as transparencia_router, router_publico
from app.routers.contratos_router import router as contratos_router
from app.routers.geo_router import router as geo_router
from app.routers.ia_router import router as ia_router
from app.routers.sso_router import router as sso_router
from app.routers.notificacoes_router import router as notificacoes_router
from app.routers.onboarding_router import router as onboarding_router
from app.utils.scheduler_sla import iniciar_scheduler, parar_scheduler
from app.utils.db_indexes import criar_indexes
from app.health import router as health_router

# Sentry (Sprint 8) — ativa apenas se SENTRY_DSN estiver configurado
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    import sentry_sdk
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.1)
    logging.getLogger("zelo").info("Sentry ativado")

logger = logging.getLogger("zelo")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / Shutdown — Sprint 15."""
    # Criar índices de performance (silencioso em SQLite)
    try:
        db = SessionLocal()
        resultado = criar_indexes(db)
        db.close()
        logger.info(f"DB Indexes: {resultado['criados']} criados, {resultado['ignorados']} já existiam")
    except Exception as e:
        logger.warning(f"Indexes não criados: {e}")

    iniciar_scheduler(SessionLocal)
    logger.info("Scheduler completo iniciado (SLA + relatório mensal + backup + limpeza GPS)")
    yield
    parar_scheduler()
    logger.info("Scheduler encerrado")

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="🏛️ Zelô — Zeladoria Urbana de Belém/PA",
    description="Plataforma integrada de zeladoria urbana municipal — Belém, Pará | COP 30",
    version="4.0.0",
    lifespan=lifespan,
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

    @app.get("/landing")
    def serve_landing():
        return FileResponse(os.path.join(frontend_path, "landing.html"))

    @app.get("/tv")
    def serve_tv():
        """Painel TV para exibição pública em telões."""
        return FileResponse(os.path.join(frontend_path, "painel-tv.html"))

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
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuários"])  # Sprint 18: gestão completa
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])
app.include_router(secretarias.router, tags=["Secretarias"])
app.include_router(servicos_router, tags=["Catálogo de Serviços"])
app.include_router(catalogo_router, tags=["Catálogo Completo"])
app.include_router(engajamento_router)
app.include_router(integracoes_router)
app.include_router(transparencia_router)
app.include_router(router_publico)
app.include_router(contratos_router)
app.include_router(geo_router)
app.include_router(ia_router)
app.include_router(sso_router)
app.include_router(notificacoes_router)
app.include_router(onboarding_router)
app.include_router(health_router, tags=["Health Check"])

# Rota raiz
@app.get("/")
def read_root():
    return {
        "message": "🏛️ Zelô — Zeladoria Urbana de Belém/PA",
        "version": "4.0.0",
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
            "catalogo": "/api/catalogo",
            "engajamento": "/api/engajamento",
            "integracoes": "/api/integracoes",
            "transparencia": "/api/transparencia",
            "publico": "/api/publico",
            "contratos": "/api/contratos",
            "geo": "/api/geo",
            "ia": "/api/ia",
            "landing": "/landing",
            "painel": "/api/ia/painel-publico"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
