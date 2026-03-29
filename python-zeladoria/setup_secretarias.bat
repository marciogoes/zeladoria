@echo off
REM ============================================
REM Implementacao de Secretarias - Corrigido
REM Sistema de Zeladoria Urbana - Belem/PA
REM Versao: 2.1.1
REM ============================================

echo.
echo ========================================================
echo    Implementacao de Secretarias
echo    Prefeitura de Belem - v2.1.1
echo ========================================================
echo.

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo [INFO] Execute install.bat primeiro
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado

REM Popular secretarias
echo.
echo [INFO] Populando 20 secretarias da Prefeitura de Belem...
python seed_secretarias.py
if errorlevel 1 (
    echo [ERRO] Erro ao popular secretarias
    pause
    exit /b 1
)

echo.
echo ========================================================
echo    IMPLEMENTACAO CONCLUIDA!
echo ========================================================
echo.

echo [INFO] O que foi feito:
echo   - 20 secretarias da Prefeitura de Belem cadastradas
echo.

echo [INFO] Verificar secretarias criadas:
echo.
python -c "from app.models_secretarias import Secretaria; from app.database.database import SessionLocal; db = SessionLocal(); secs = db.query(Secretaria).all(); [print(f'  {s.sigla:8} - {s.nome}') for s in secs]; db.close()"
echo.

echo [INFO] Arquivos disponiveis:
echo   - app/models_secretarias.py      (Modelo Secretaria)
echo   - app/mapeamento_secretarias.py  (Mapeamento Categoria-Secretaria)
echo   - frontend/tema-belem.css        (Tema visual)
echo   - SISTEMA_SECRETARIAS.md         (Documentacao completa)
echo.

echo [INFO] Proximos passos:
echo   1. Ver documentacao: SISTEMA_SECRETARIAS.md
echo   2. Integrar tema: adicione tema-belem.css no HTML
echo   3. Criar endpoints API para secretarias
echo.

pause
