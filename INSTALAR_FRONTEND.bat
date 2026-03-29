@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🚀 INSTALAÇÃO DO FRONTEND REACT - CATÁLOGO           ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd frontend

echo [1/3] 📦 Instalando dependências base...
call npm install

echo.
echo [2/3] 🎨 Instalando Lucide React (ícones)...
call npm install lucide-react

echo.
echo [3/3] ✅ Verificando instalação...
call npm list lucide-react

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   ✅ INSTALAÇÃO CONCLUÍDA!                             ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📝 Próximos passos:
echo    1. Execute INICIAR_FRONTEND.bat para iniciar o frontend
echo    2. Execute INICIAR_BACKEND.bat para iniciar o backend
echo    3. Acesse http://localhost:5173 no navegador
echo.
pause
