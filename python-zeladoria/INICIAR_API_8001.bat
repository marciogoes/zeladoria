@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🚀 INICIANDO BACKEND NA PORTA 8001                   ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🔧 Backend API: http://localhost:8001
echo 📚 Documentação: http://localhost:8001/docs
echo 🎨 Catálogo: http://localhost:8001/static/catalogo.html
echo 🏠 Sistema: http://localhost:8001/static/index.html
echo.

echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate

echo [INFO] Iniciando servidor na porta 8001...
python main.py

pause
