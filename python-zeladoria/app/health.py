"""
Health Check API Endpoint
Sistema de Zeladoria Urbana - Belém/PA

Este arquivo adiciona endpoints de health check e monitoramento
para facilitar a observabilidade do sistema.
"""

from fastapi import APIRouter, Response, status
from sqlalchemy import text
from datetime import datetime
import psutil
import os
from typing import Dict, Any

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health Check básico
    
    Retorna:
        - status: ok
        - timestamp: data/hora atual
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "Sistema de Zeladoria Urbana - Belém/PA",
        "version": "2.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """
    Health Check detalhado com informações do sistema
    
    Retorna informações sobre:
        - Status geral
        - Banco de dados
        - Sistema operacional
        - Memória
        - Disco
        - CPU
    """
    from app.database import engine
    
    health_data = {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "Sistema de Zeladoria Urbana - Belém/PA",
        "version": "2.0.0",
        "checks": {}
    }
    
    # 1. Verificar Database
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        health_data["checks"]["database"] = {
            "status": "healthy",
            "message": "Conexão OK"
        }
    except Exception as e:
        health_data["status"] = "degraded"
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "message": str(e)
        }
    
    # 2. Verificar Sistema
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        health_data["checks"]["cpu"] = {
            "status": "healthy" if cpu_percent < 80 else "warning",
            "usage_percent": cpu_percent,
            "cores": psutil.cpu_count()
        }
        
        # Memória
        memory = psutil.virtual_memory()
        health_data["checks"]["memory"] = {
            "status": "healthy" if memory.percent < 80 else "warning",
            "usage_percent": memory.percent,
            "available_mb": memory.available // (1024 * 1024),
            "total_mb": memory.total // (1024 * 1024)
        }
        
        # Disco
        disk = psutil.disk_usage('/')
        health_data["checks"]["disk"] = {
            "status": "healthy" if disk.percent < 80 else "warning",
            "usage_percent": disk.percent,
            "available_gb": disk.free // (1024 * 1024 * 1024),
            "total_gb": disk.total // (1024 * 1024 * 1024)
        }
        
    except Exception as e:
        health_data["checks"]["system"] = {
            "status": "error",
            "message": str(e)
        }
    
    # 3. Verificar Diretórios importantes
    directories = ["uploads", "logs", "backups"]
    for directory in directories:
        try:
            exists = os.path.exists(directory)
            is_writable = os.access(directory, os.W_OK) if exists else False
            
            health_data["checks"][f"directory_{directory}"] = {
                "status": "healthy" if (exists and is_writable) else "unhealthy",
                "exists": exists,
                "writable": is_writable
            }
        except Exception as e:
            health_data["checks"][f"directory_{directory}"] = {
                "status": "error",
                "message": str(e)
            }
    
    # 4. Status geral baseado nos checks
    unhealthy_checks = [
        name for name, check in health_data["checks"].items()
        if check.get("status") == "unhealthy"
    ]
    
    if unhealthy_checks:
        health_data["status"] = "unhealthy"
        health_data["unhealthy_checks"] = unhealthy_checks
    elif any(check.get("status") == "warning" for check in health_data["checks"].values()):
        health_data["status"] = "warning"
    
    return health_data


@router.get("/health/readiness")
async def readiness_check():
    """
    Readiness Check - verifica se o serviço está pronto para receber tráfego
    
    Usado por:
        - Kubernetes
        - Docker Swarm
        - Load Balancers
    """
    from app.database import engine
    
    try:
        # Verificar conexão com banco
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        
        return Response(
            content='{"status": "ready"}',
            status_code=status.HTTP_200_OK,
            media_type="application/json"
        )
    except Exception as e:
        return Response(
            content=f'{{"status": "not ready", "error": "{str(e)}"}}',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )


@router.get("/health/liveness")
async def liveness_check():
    """
    Liveness Check - verifica se o serviço está vivo
    
    Usado por:
        - Kubernetes
        - Docker Swarm
        - Monitoramento
    """
    return Response(
        content='{"status": "alive"}',
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )


@router.get("/health/startup")
async def startup_check():
    """
    Startup Check - verifica se o serviço inicializou corretamente
    """
    from app.database import engine
    
    checks = {
        "database": False,
        "models": False,
        "directories": False
    }
    
    # 1. Verificar Database
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        checks["database"] = True
    except:
        pass
    
    # 2. Verificar Models
    try:
        from app.models import Usuario, Chamado, Categoria
        checks["models"] = True
    except:
        pass
    
    # 3. Verificar Diretórios
    try:
        directories_ok = all(
            os.path.exists(d) for d in ["uploads", "logs"]
        )
        checks["directories"] = directories_ok
    except:
        pass
    
    # Status geral
    all_ok = all(checks.values())
    
    if all_ok:
        return {
            "status": "started",
            "checks": checks
        }
    else:
        return Response(
            content=str({"status": "starting", "checks": checks}),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )


@router.get("/metrics")
async def metrics_endpoint():
    """
    Endpoint de métricas (formato Prometheus-like)
    
    Retorna métricas básicas do sistema para monitoramento
    """
    from app.database import engine
    from app.models import Chamado, Usuario
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "application": {
            "name": "zeladoria_urbana",
            "version": "2.0.0",
            "uptime_seconds": psutil.Process(os.getpid()).create_time()
        },
        "system": {
            "cpu_usage_percent": psutil.cpu_percent(interval=0.5),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        },
        "database": {
            "status": "unknown",
            "tables": {}
        }
    }
    
    # Métricas do banco de dados
    try:
        with engine.connect() as connection:
            # Total de registros por tabela
            result = connection.execute(text("SELECT COUNT(*) FROM chamados"))
            metrics["database"]["tables"]["chamados"] = result.scalar()
            
            result = connection.execute(text("SELECT COUNT(*) FROM usuarios"))
            metrics["database"]["tables"]["usuarios"] = result.scalar()
            
            result = connection.execute(text("SELECT COUNT(*) FROM categorias"))
            metrics["database"]["tables"]["categorias"] = result.scalar()
            
            metrics["database"]["status"] = "healthy"
    except Exception as e:
        metrics["database"]["status"] = "unhealthy"
        metrics["database"]["error"] = str(e)
    
    return metrics


# Adicionar ao main.py:
"""
# No arquivo main.py, adicione:

from app.health import router as health_router

app.include_router(health_router, tags=["Health Check"])
"""
