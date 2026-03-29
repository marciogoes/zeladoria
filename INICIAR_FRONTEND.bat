@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎨 INICIANDO FRONTEND REACT                          ║
echo ║   Sistema de Zeladoria Urbana - Belém/PA               ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🌐 Frontend será iniciado em: http://localhost:5173
echo.

cd frontend
call npm run dev

pause
