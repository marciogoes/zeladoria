"""
Script para testar se as rotas estão funcionando
"""
import os
import requests
import sys

def testar_rotas():
    base_url = "http://localhost:8001"
    
    print("=" * 60)
    print("🔍 TESTANDO ROTAS DO SISTEMA")
    print("=" * 60)
    print()
    
    # 1. Testar raiz
    print("1️⃣ Testando rota raiz...")
    try:
        r = requests.get(f"{base_url}/", timeout=5)
        if r.status_code == 200:
            print("   ✅ Backend respondendo na porta 8001")
        else:
            print(f"   ❌ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ ERRO: Backend não está rodando!")
        print(f"   Execute: INICIAR_API_8001.bat")
        return
    
    print()
    
    # 2. Testar API catálogo
    print("2️⃣ Testando API do catálogo...")
    try:
        r = requests.get(f"{base_url}/api/catalogo", timeout=5)
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ API funcionando! {len(data)} serviços cadastrados")
        else:
            print(f"   ❌ Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ ERRO: {e}")
    
    print()
    
    # 3. Verificar arquivos frontend
    print("3️⃣ Verificando arquivos do frontend...")
    frontend_path = "frontend"
    
    if os.path.exists(frontend_path):
        print(f"   ✅ Pasta frontend existe")
        
        arquivos = ["catalogo.html", "index.html", "catalogo.css", "catalogo.js"]
        for arquivo in arquivos:
            caminho = os.path.join(frontend_path, arquivo)
            if os.path.exists(caminho):
                tamanho = os.path.getsize(caminho)
                print(f"   ✅ {arquivo} ({tamanho} bytes)")
            else:
                print(f"   ❌ {arquivo} NÃO ENCONTRADO")
    else:
        print(f"   ❌ Pasta frontend NÃO existe")
    
    print()
    
    # 4. Testar rotas do frontend
    print("4️⃣ Testando acesso ao frontend...")
    
    rotas_testar = [
        "/static/catalogo.html",
        "/static/index.html",
        "/app",
        "/dashboard"
    ]
    
    for rota in rotas_testar:
        try:
            r = requests.get(f"{base_url}{rota}", timeout=5)
            if r.status_code == 200:
                print(f"   ✅ {rota}")
            else:
                print(f"   ❌ {rota} (Status: {r.status_code})")
        except Exception as e:
            print(f"   ❌ {rota} (Erro: {e})")
    
    print()
    print("=" * 60)
    print("🎯 URLS PARA ACESSAR:")
    print("=" * 60)
    print(f"📚 Documentação: {base_url}/docs")
    print(f"🎨 Catálogo:     {base_url}/static/catalogo.html")
    print(f"🏠 Sistema:      {base_url}/static/index.html")
    print(f"📊 Dashboard:    {base_url}/dashboard")
    print("=" * 60)
    
if __name__ == "__main__":
    testar_rotas()
    input("\nPressione Enter para sair...")
