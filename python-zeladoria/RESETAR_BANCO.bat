@echo off
cls
echo ========================================
echo   RESETAR BANCO DE DADOS
echo ========================================
echo.
echo ATENCAO: Isso vai DELETAR TODOS os dados!
echo.
echo Tem certeza? (s/N)
set /p confirma="> "

if /i not "%confirma%"=="s" (
    echo Cancelado.
    pause
    exit
)

echo.
echo Deletando banco antigo...
if exist zeladoria.db (
    del zeladoria.db
    echo OK: Banco deletado
) else (
    echo AVISO: Banco nao existe
)

echo.
echo Criando banco novo com estrutura atualizada...
python -c "from app.database.database import engine, Base; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; from app.models_servicos import ServicoSecretaria; from app.models.chamado import Chamado; from app.models.categoria import Categoria; from app.models.bairro import Bairro; Base.metadata.create_all(bind=engine); print('OK: Tabelas criadas')"

echo.
echo ========================================
echo   BANCO RESETADO!
echo ========================================
echo.
echo Agora execute: SETUP_COMPLETO.bat
echo.
pause
