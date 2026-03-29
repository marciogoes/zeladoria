@echo off
title DIAGNOSTICO CATALOGO DE SERVICOS
color 0A
cls

echo ========================================
echo   DIAGNOSTICO DO SISTEMA
echo ========================================
echo.

echo [1/5] Verificando diretorio...
cd
echo.

echo [2/5] Listando arquivos principais...
dir /B manage_catalogo.py 2>nul
if errorlevel 1 (
    echo ERRO: manage_catalogo.py nao encontrado!
    echo Voce esta na pasta correta?
    echo.
    goto erro
)
echo OK: manage_catalogo.py encontrado
echo.

echo [3/5] Testando Python...
python --version 2>nul
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ ou adicione ao PATH
    echo.
    goto erro
)
echo OK: Python instalado
echo.

echo [4/5] Verificando estrutura de pastas...
if exist app\ (echo OK: Pasta app/) else (echo ERRO: Pasta app/ nao encontrada & goto erro)
if exist migrations\ (echo OK: Pasta migrations/) else (echo ERRO: Pasta migrations/ nao encontrada & goto erro)
if exist docs\ (echo OK: Pasta docs/) else (echo ERRO: Pasta docs/ nao encontrada & goto erro)
echo.

echo [5/5] Testando import Python...
python -c "print('Import basico: OK')" 2>nul
if errorlevel 1 (
    echo ERRO: Python nao consegue executar comandos
    goto erro
)
echo.

echo ========================================
echo   TUDO OK! Sistema pronto para uso
echo ========================================
echo.
echo Proximos passos:
echo   1. Execute: python manage_catalogo.py
echo   2. Ou execute: START.bat
echo.
goto fim

:erro
echo ========================================
echo   ERRO DETECTADO!
echo ========================================
echo.
echo Verifique os erros acima e corrija.
echo.

:fim
echo Pressione qualquer tecla para fechar...
pause >nul
