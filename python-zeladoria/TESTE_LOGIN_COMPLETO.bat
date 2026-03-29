@echo off
cls
echo ========================================
echo   TESTE COMPLETO - LOGIN E USUARIOS
echo ========================================
echo.

echo [1] Verificando usuarios no banco...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; db = SessionLocal(); count = db.query(Usuario).count(); db.close(); print(f'    Total: {count} usuario(s)')" 2>nul

echo.
echo [2] Listando usuarios...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; db = SessionLocal(); usuarios = db.query(Usuario).all(); [print(f'    - {u.email} ({u.tipo})') for u in usuarios]; db.close()" 2>nul

echo.
echo [3] Testando login via API...
echo.
curl -X POST http://localhost:8001/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"admin@zeladoria.com\",\"senha\":\"admin123\"}" 2>nul

echo.
echo.
echo ========================================
echo.

echo Se mostrou "access_token" acima, o login funciona!
echo Se mostrou erro 401, os usuarios nao existem ou senha errada.
echo.

pause
