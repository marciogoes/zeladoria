@echo off
echo ========================================
echo CRIAR TABELA DE COMENTARIOS
echo ========================================
echo.

python -c "from app.database.database import engine, Base; from app.models import Comentario; Base.metadata.create_all(bind=engine); print('✅ Tabela de comentários criada com sucesso!')"

echo.
echo Pressione qualquer tecla para sair...
pause > nul
