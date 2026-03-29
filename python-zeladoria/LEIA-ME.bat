@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo   CATÁLOGO DE SERVIÇOS - SCRIPTS BATCH DISPONÍVEIS
echo   Sistema de Zeladoria Urbana - Belém/PA
echo ========================================================================
echo.
echo 📁 SCRIPTS PRINCIPAIS
echo ========================================================================
echo.
echo   catalogo.bat
echo   └─ Menu interativo com todas as opções
echo      Execute este para começar!
echo.
echo   setup_catalogo.bat
echo   └─ Setup completo automático
echo      Cria tabela + popula banco + mostra estatísticas
echo.
echo ========================================================================
echo.
echo 📋 SCRIPTS INDIVIDUAIS
echo ========================================================================
echo.
echo   criar_tabela.bat        - Cria a tabela no banco de dados
echo   popular_catalogo.bat    - Popula com 100+ serviços
echo   listar_servicos.bat     - Lista todos os serviços
echo   ver_estatisticas.bat    - Mostra estatísticas do catálogo
echo   buscar_servico.bat      - Busca serviços por termo
echo.
echo ========================================================================
echo.
echo 🚀 API E TESTES
echo ========================================================================
echo.
echo   iniciar_api.bat         - Inicia o servidor FastAPI
echo   testar_api.bat          - Testa os endpoints da API
echo.
echo ========================================================================
echo.
echo 🎯 QUICK START (Primeira vez)
echo ========================================================================
echo.
echo   1. Execute: catalogo.bat
echo   2. Escolha opção: 1 (Setup Completo)
echo   3. Aguarde a conclusão
echo   4. Execute opção: 8 (Iniciar API)
echo   5. Acesse: http://localhost:8000/docs
echo.
echo ========================================================================
echo.
echo ⚠️  IMPORTANTE - ANTES DE POPULAR O BANCO
echo ========================================================================
echo.
echo   Edite: app\seeds\seed_servicos.py
echo.
echo   Ajuste o mapeamento de IDs das secretarias:
echo.
echo   secretarias_map = {
echo       "SEURB": 1,   # ^<-- Seu ID real da SEURB
echo       "SESAN": 2,   # ^<-- Seu ID real da SESAN
echo       "SEMOB": 3,   # ^<-- Seu ID real da SEMOB
echo       "SEMMA": 4,   # ^<-- Seu ID real da SEMMA
echo       "SESMA": 5,   # ^<-- Seu ID real da SESMA
echo   }
echo.
echo ========================================================================
echo.
echo 📚 DOCUMENTAÇÃO COMPLETA
echo ========================================================================
echo.
echo   docs\CATALOGO_SERVICOS.md    - Documentação técnica
echo   docs\GUIA_USO_CATALOGO.md    - Guia de uso
echo   README_CATALOGO.md           - Resumo executivo
echo.
echo ========================================================================
echo.
echo 🎉 COMANDOS PYTHON DIRETOS (Alternativa)
echo ========================================================================
echo.
echo   python manage_catalogo.py            - Menu interativo
echo   python manage_catalogo.py seed       - Popular banco
echo   python manage_catalogo.py listar     - Listar serviços
echo   python manage_catalogo.py stats      - Estatísticas
echo   python manage_catalogo.py categorias - Ver categorias
echo   python manage_catalogo.py buscar X   - Buscar termo
echo.
echo ========================================================================
echo.

pause
