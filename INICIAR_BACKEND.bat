@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🚀 INICIANDO BACKEND FASTAPI                         ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🔧 Backend API será iniciado em: http://localhost:8000
echo 📚 Documentação: http://localhost:8000/docs
echo.

cd python-zeladoria

echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate

echo [INFO] Iniciando servidor FastAPI...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
