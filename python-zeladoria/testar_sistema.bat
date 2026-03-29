@echo off
chcp 65001 >nul
cls
echo ========================================
echo   TESTE DE DIAGNÓSTICO
echo ========================================
echo.

echo Testando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo Instale Python ou adicione ao PATH
    pause
    exit /b 1
)

echo.
echo ✅ Python encontrado!
echo.

echo Testando diretório atual...
cd
echo.

echo Verificando arquivos necessários...
if exist "app\models_servicos.py" (
    echo ✅ models_servicos.py encontrado
) else (
    echo ❌ models_servicos.py NÃO encontrado
)

if exist "app\seeds\seed_servicos.py" (
    echo ✅ seed_servicos.py encontrado
) else (
    echo ❌ seed_servicos.py NÃO encontrado
)

if exist "migrations\create_servicos_table.py" (
    echo ✅ create_servicos_table.py encontrado
) else (
    echo ❌ create_servicos_table.py NÃO encontrado
)

if exist "manage_catalogo.py" (
    echo ✅ manage_catalogo.py encontrado
) else (
    echo ❌ manage_catalogo.py NÃO encontrado
)

echo.
echo Testando imports Python...
echo.

python -c "import sys; print('Python Path OK')"
if %errorlevel% neq 0 (
    echo ❌ Erro ao importar sys
    pause
    exit /b 1
)

echo.
echo Testando import do projeto...
python -c "from app.models_servicos import ServicoSecretaria; print('Import models OK')"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao importar models_servicos
    echo.
    echo Possíveis causas:
    echo - Você não está na pasta raiz do projeto
    echo - Faltam dependências (SQLAlchemy)
    echo - Erro de sintaxe no arquivo
    echo.
    pause
    exit /b 1
)

echo ✅ Import models OK
echo.

echo Testando conexão com banco...
python -c "from app.database.database import SessionLocal; db = SessionLocal(); print('Conexão OK'); db.close()"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao conectar com banco
    echo.
    echo Verifique app\database\database.py
    echo.
    pause
    exit /b 1
)

echo ✅ Conexão com banco OK
echo.

echo.
echo ========================================
echo   ✅ TODOS OS TESTES PASSARAM!
echo ========================================
echo.
echo O sistema está pronto para uso.
echo Execute: catalogo.bat
echo.

pause
