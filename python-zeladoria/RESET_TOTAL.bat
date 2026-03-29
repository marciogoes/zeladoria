@echo off
cls
echo ========================================
echo   RESET TOTAL DO BANCO
echo ========================================
echo.
echo ATENCAO: Deletando banco antigo...
echo.

if exist zeladoria.db (
    del /F /Q zeladoria.db
    echo OK: Banco deletado
) else (
    echo Banco nao existe
)

echo.
echo Criando banco NOVO com estrutura correta...
echo.

python migrations\criar_todas_tabelas.py

echo.
echo Populando secretarias...
python app\seeds\seed_secretarias.py

echo.
echo Criando usuarios...
python app\seeds\seed_usuarios.py

echo.
echo ========================================
echo   BANCO RECRIADO!
echo ========================================
echo.
echo Agora REINICIE a API:
echo   1. Pressione CTRL+C no terminal da API
echo   2. Execute: INICIAR_API_8001.bat
echo.
pause
