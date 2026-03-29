@echo off
cls
echo ========================================
echo   RESET FORCADO - FECHAR API E RESETAR
echo ========================================
echo.
echo PASSO 1: FECHE TODOS OS TERMINAIS COM A API
echo.
echo Pressione qualquer tecla DEPOIS de fechar a API...
pause >nul
echo.

echo PASSO 2: Tentando deletar banco...
if exist zeladoria.db (
    del /F /Q zeladoria.db 2>nul
    if exist zeladoria.db (
        echo ERRO: Nao conseguiu deletar. API ainda rodando?
        echo Feche TODOS os terminais e tente novamente.
        pause
        exit
    )
    echo OK: Banco deletado
) else (
    echo OK: Banco nao existe
)

echo.
echo PASSO 3: Criando tabelas...
python migrations\criar_todas_tabelas.py

echo.
echo PASSO 4: Populando secretarias...
python app\seeds\seed_secretarias.py

echo.
echo PASSO 5: Criando usuarios...
python app\seeds\seed_usuarios.py

echo.
echo ========================================
echo   SUCESSO!
echo ========================================
echo.
echo Agora execute: INICIAR_API_8001.bat
echo E acesse: http://localhost:8001/app
echo.
echo Login: admin@zeladoria.com / admin123
echo.
pause
