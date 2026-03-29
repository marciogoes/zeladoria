"""
Script para verificar integridade do banco de dados
"""
import sqlite3
import os

def verificar_banco():
    print("=" * 60)
    print("🔍 VERIFICANDO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    db_path = "zeladoria.db"
    
    # 1. Verificar se existe
    if not os.path.exists(db_path):
        print("❌ Banco de dados NÃO existe!")
        print("   Execute: POPULAR_CATALOGO_SQLITE.bat")
        return
    
    print(f"✅ Banco existe: {db_path}")
    print(f"   Tamanho: {os.path.getsize(db_path)} bytes")
    print()
    
    # 2. Conectar e verificar tabelas
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📋 Verificando tabelas...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        
        for tabela in tabelas:
            nome = tabela[0]
            cursor.execute(f"SELECT COUNT(*) FROM {nome}")
            count = cursor.fetchone()[0]
            
            if nome == "catalogo_servicos":
                print(f"   ✅ {nome}: {count} registros")
            elif nome == "secretarias":
                print(f"   ✅ {nome}: {count} registros")
            else:
                print(f"   📌 {nome}: {count} registros")
        
        print()
        
        # 3. Verificar estrutura da tabela catalogo_servicos
        print("🏗️ Estrutura da tabela catalogo_servicos:")
        cursor.execute("PRAGMA table_info(catalogo_servicos)")
        colunas = cursor.fetchall()
        
        if not colunas:
            print("   ❌ Tabela catalogo_servicos NÃO existe!")
            print("   Execute: POPULAR_CATALOGO_SQLITE.bat")
        else:
            for col in colunas:
                print(f"   ✅ {col[1]} ({col[2]})")
        
        print()
        
        # 4. Testar query
        print("🧪 Testando query do endpoint...")
        try:
            cursor.execute("""
                SELECT cs.*, s.nome as secretaria_nome, s.sigla as secretaria_sigla
                FROM catalogo_servicos cs
                LEFT JOIN secretarias s ON cs.secretaria_id = s.id
                LIMIT 1
            """)
            resultado = cursor.fetchone()
            if resultado:
                print("   ✅ Query funciona!")
            else:
                print("   ⚠️ Query retorna vazio (mas funciona)")
        except Exception as e:
            print(f"   ❌ ERRO na query: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERRO ao conectar: {e}")
        return
    
    print()
    print("=" * 60)
    print("✅ VERIFICAÇÃO COMPLETA!")
    print("=" * 60)

if __name__ == "__main__":
    verificar_banco()
    input("\nPressione Enter para sair...")
