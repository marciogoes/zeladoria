@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   ✅ VERIFICAÇÃO DO SISTEMA                            ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

set ERROR=0

echo [1/10] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não instalado! Baixe em: https://nodejs.org/
    set ERROR=1
) else (
    echo ✅ Node.js instalado
)

echo.
echo [2/10] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não instalado! Baixe em: https://python.org/
    set ERROR=1
) else (
    echo ✅ Python instalado
)

echo.
echo [3/10] Verificando pasta frontend...
if exist "frontend" (
    echo ✅ Pasta frontend encontrada
) else (
    echo ❌ Pasta frontend não encontrada!
    set ERROR=1
)

echo.
echo [4/10] Verificando pasta backend...
if exist "python-zeladoria" (
    echo ✅ Pasta backend encontrada
) else (
    echo ❌ Pasta backend não encontrada!
    set ERROR=1
)

echo.
echo [5/10] Verificando App.jsx...
if exist "frontend\src\App.jsx" (
    echo ✅ App.jsx encontrado
) else (
    echo ❌ App.jsx não encontrado!
    set ERROR=1
)

echo.
echo [6/10] Verificando node_modules...
if exist "frontend\node_modules" (
    echo ✅ Dependências do frontend instaladas
) else (
    echo ⚠️ Dependências do frontend não instaladas
    echo    Execute: INSTALAR_FRONTEND.bat
)

echo.
echo [7/10] Verificando lucide-react...
if exist "frontend\node_modules\lucide-react" (
    echo ✅ lucide-react instalado
) else (
    echo ⚠️ lucide-react não instalado
    echo    Execute: cd frontend ^& npm install lucide-react
)

echo.
echo [8/10] Verificando venv Python...
if exist "python-zeladoria\venv" (
    echo ✅ Ambiente virtual Python criado
) else (
    echo ⚠️ Ambiente virtual não criado
    echo    Execute: cd python-zeladoria ^& python -m venv venv
)

echo.
echo [9/10] Verificando banco de dados...
if exist "python-zeladoria\zeladoria.db" (
    echo ✅ Banco de dados encontrado
) else (
    echo ⚠️ Banco de dados não encontrado
    echo    Execute: cd python-zeladoria ^& python popular_banco.py
)

echo.
echo [10/10] Verificando scripts...
if exist "INICIAR_FRONTEND.bat" (
    echo ✅ Scripts de inicialização presentes
) else (
    echo ❌ Scripts não encontrados!
    set ERROR=1
)

echo.
echo ══════════════════════════════════════════════════════
echo.

if %ERROR%==0 (
    echo ✅ SISTEMA PRONTO PARA USO!
    echo.
    echo 📋 PRÓXIMOS PASSOS:
    echo.
    echo    1. Iniciar Backend:
    echo       Execute: INICIAR_BACKEND.bat
    echo.
    echo    2. Iniciar Frontend:
    echo       Execute: INICIAR_FRONTEND.bat
    echo.
    echo    3. Acessar:
    echo       http://localhost:5173
    echo.
) else (
    echo ❌ SISTEMA COM PROBLEMAS!
    echo.
    echo Corrija os erros acima antes de continuar.
    echo.
    echo 💡 SUGESTÃO:
    echo    Execute: SETUP_COMPLETO.bat
    echo.
)

echo ══════════════════════════════════════════════════════
echo.

echo 📚 DOCUMENTAÇÃO:
echo    • README_CATALOGO.md (guia rápido)
echo    • GUIA_CATALOGO_SERVICOS.md (completo)
echo    • RESUMO_IMPLEMENTACAO.txt (overview)
echo.

pause
