@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🧪 TESTAR APIS DO CATÁLOGO                           ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd python-zeladoria

echo ⚠️ IMPORTANTE: O backend deve estar rodando!
echo    Se não estiver, abra outro terminal e execute:
echo    INICIAR_BACKEND.bat
echo.
echo Pressione qualquer tecla para continuar com os testes...
pause >nul

echo.
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo 🧪 Executando testes...
python testar_catalogo_apis.py

echo.
pause
