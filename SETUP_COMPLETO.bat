@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🚀 SETUP COMPLETO - CATÁLOGO DE SERVIÇOS             ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo [PASSO 1/5] 📦 Verificando estrutura de pastas...
if not exist "frontend" (
    echo ❌ Pasta frontend não encontrada!
    pause
    exit
)
if not exist "python-zeladoria" (
    echo ❌ Pasta python-zeladoria não encontrada!
    pause
    exit
)
echo ✅ Estrutura OK

echo.
echo [PASSO 2/5] 🎨 Instalando dependências do frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências base
    cd ..
    pause
    exit
)

call npm install lucide-react
if errorlevel 1 (
    echo ❌ Erro ao instalar lucide-react
    cd ..
    pause
    exit
)
cd ..
echo ✅ Frontend instalado

echo.
echo [PASSO 3/5] 🐍 Verificando backend Python...
cd python-zeladoria
if not exist "venv" (
    echo ⚠️ Ambiente virtual não encontrado. Criando...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt >nul 2>&1
cd ..
echo ✅ Backend verificado

echo.
echo [PASSO 4/5] 📊 Verificando banco de dados...
cd python-zeladoria
if not exist "zeladoria.db" (
    echo ⚠️ Banco de dados não encontrado. Execute popular_banco.py
)
cd ..
echo ✅ Verificação concluída

echo.
echo [PASSO 5/5] 📝 Criando atalhos...

rem Criar atalho para iniciar frontend
echo @echo off > QUICK_START_FRONTEND.bat
echo cd frontend >> QUICK_START_FRONTEND.bat
echo call npm run dev >> QUICK_START_FRONTEND.bat

rem Criar atalho para iniciar backend
echo @echo off > QUICK_START_BACKEND.bat
echo cd python-zeladoria >> QUICK_START_BACKEND.bat
echo call venv\Scripts\activate >> QUICK_START_BACKEND.bat
echo python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 >> QUICK_START_BACKEND.bat

echo ✅ Atalhos criados

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   ✅ SETUP COMPLETO!                                   ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo    1️⃣ Iniciar Backend:
echo       Execute: INICIAR_BACKEND.bat
echo       Ou: QUICK_START_BACKEND.bat
echo.
echo    2️⃣ Iniciar Frontend:
echo       Execute: INICIAR_FRONTEND.bat
echo       Ou: QUICK_START_FRONTEND.bat
echo.
echo    3️⃣ Acessar Sistema:
echo       Frontend: http://localhost:5173
echo       API Docs: http://localhost:8000/docs
echo.
echo    4️⃣ Popular Banco (se necessário):
echo       cd python-zeladoria
echo       python popular_banco.py
echo.
echo 📚 DOCUMENTAÇÃO:
echo    Leia: GUIA_CATALOGO_SERVICOS.md
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎉 Tudo pronto para começar!                         ║
echo ╚════════════════════════════════════════════════════════╝
echo.
pause
