"""
Sprint 17 — Rate Limiting em memória (sliding window)
Proteção anti-brute-force para rotas de autenticação.

AVISO: implementação em memória — funciona corretamente apenas com 1 worker.
Em produção com múltiplos workers (gunicorn -w N), cada processo tem seu
próprio _store, então o limite efetivo é N × max_attempts.
Migração para Redis: use slowapi + Redis backend e defina REDIS_URL no ambiente.
"""
import os
import logging
import time
from collections import defaultdict
from threading import Lock
from fastapi import HTTPException, Request

logger = logging.getLogger("zelo.rate_limit")

# Avisa em startup se rodando com múltiplos workers (Railway/Gunicorn)
_WORKERS = int(os.environ.get("WEB_CONCURRENCY", "1"))
if _WORKERS > 1:
    logger.warning(
        f"Rate limiting em memória ativo com {_WORKERS} workers. "
        "O limite efetivo será multiplicado pelo número de workers. "
        "Considere migrar para Redis (REDIS_URL + slowapi)."
    )

# Estrutura: key -> lista de timestamps de tentativas
_store: dict[str, list[float]] = defaultdict(list)
_lock = Lock()

# Limites padrão
_DEFAULT_MAX   = 10    # tentativas
_DEFAULT_WINDOW = 900  # 15 minutos em segundos


def check_rate_limit(
    key: str,
    max_attempts: int = _DEFAULT_MAX,
    window_seconds: int = _DEFAULT_WINDOW,
) -> None:
    """
    Verifica se `key` excedeu `max_attempts` dentro de `window_seconds`.
    Lança HTTPException 429 se excedido.
    `key` deve ser algo como: f"login:{ip}" ou f"register:{email}"
    """
    now = time.monotonic()
    cutoff = now - window_seconds

    with _lock:
        # Remove tentativas antigas
        _store[key] = [t for t in _store[key] if t > cutoff]

        if len(_store[key]) >= max_attempts:
            minutes = window_seconds // 60
            raise HTTPException(
                status_code=429,
                detail=(
                    f"Muitas tentativas ({max_attempts} em {minutes} min). "
                    f"Aguarde antes de tentar novamente."
                ),
                headers={"Retry-After": str(window_seconds)},
            )

        _store[key].append(now)


def get_client_ip(request: Request) -> str:
    """Extrai IP real, considerando proxy/Railway."""
    # X-Forwarded-For → pode ter lista de IPs
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    # Fallback
    if request.client:
        return request.client.host
    return "unknown"


def reset_attempts(key: str) -> None:
    """Limpa tentativas após login bem-sucedido (opcional)."""
    with _lock:
        _store.pop(key, None)
