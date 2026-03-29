@echo off
cls
echo ========================================
echo   TESTE DETALHADO DE LOGIN
echo ========================================
echo.

echo [1] Verificando usuarios no banco...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; db = SessionLocal(); usuarios = db.query(Usuario).all(); print(f'Total: {len(usuarios)} usuarios'); [print(f'  - {u.email} ({u.tipo})') for u in usuarios]; db.close()"
echo.

echo [2] Testando login via API...
echo.
echo Requisicao:
echo POST http://localhost:8001/api/auth/login
echo Body: {"email":"admin@zeladoria.com","senha":"admin123"}
echo.
echo Resposta:
curl -v -X POST http://localhost:8001/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"admin@zeladoria.com\",\"senha\":\"admin123\"}" 2>&1
echo.
echo.
echo ========================================
pause
