@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   📋 POPULAR CATÁLOGO COM DADOS DE EXEMPLO             ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd python-zeladoria

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo 📊 Populando catálogo de serviços...
python popular_catalogo_exemplo.py

echo.
pause
