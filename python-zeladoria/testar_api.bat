@echo off
chcp 65001 >nul
echo ========================================
echo   TESTAR API - Catálogo de Serviços
echo ========================================
echo.

echo ⚠️  Certifique-se de que a API está rodando!
echo Execute: iniciar_api.bat em outra janela
echo.

pause

echo.
echo 🧪 Testando endpoints da API...
echo.

echo 1️⃣  Testando GET /api/servicos/ (listar serviços)
echo.
curl -s http://localhost:8000/api/servicos/ | python -m json.tool
echo.
echo ========================================
echo.

pause

echo.
echo 2️⃣  Testando GET /api/servicos/dashboard
echo.
curl -s http://localhost:8000/api/servicos/dashboard | python -m json.tool
echo.
echo ========================================
echo.

pause

echo.
echo 3️⃣  Testando GET /api/servicos/categorias/listar
echo.
curl -s http://localhost:8000/api/servicos/categorias/listar | python -m json.tool
echo.
echo ========================================
echo.

pause

echo.
echo 4️⃣  Testando busca: /api/servicos/?busca=iluminacao
echo.
curl -s "http://localhost:8000/api/servicos/?busca=iluminacao" | python -m json.tool
echo.
echo ========================================
echo.

pause

echo.
echo 5️⃣  Testando autocomplete: /api/servicos/autocomplete?q=ilum
echo.
curl -s "http://localhost:8000/api/servicos/autocomplete?q=ilum" | python -m json.tool
echo.
echo ========================================
echo.

echo.
echo ✅ Testes concluídos!
echo.
echo Acesse a documentação interativa em:
echo   http://localhost:8000/docs
echo.

pause
