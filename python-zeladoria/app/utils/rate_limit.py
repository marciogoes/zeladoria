"""
Sprint 17 — Rate Limiting em memória
Proteção anti-brute-force para rotas de autenticação.
Em produção com múltiplos workers, use Redis (slowapi + redis backend).
"""
import time
from collections import defaultdict
from threading import Lock
from fastapi import HTTPException, Request

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
