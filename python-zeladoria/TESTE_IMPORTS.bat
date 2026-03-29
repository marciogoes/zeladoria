@echo off
cls
echo ========================================
echo   TESTE DE IMPORTS
echo ========================================
echo.
echo Testando se todos os modelos carregam...
echo.

python -c "import sys; import os; sys.path.insert(0, '.'); print('1. Testando imports...'); from app.database.database import engine, Base; print('   OK: database'); from app.models.usuario import Usuario; print('   OK: usuario'); from app.models.secretaria import Secretaria; print('   OK: secretaria'); from app.models_servicos import ServicoSecretaria; print('   OK: servicos'); print('\n2. Criando tabelas...'); Base.metadata.create_all(bind=engine); print('   OK: Tabelas criadas!'); print('\nSUCESSO!')"

echo.
echo ========================================
pause
