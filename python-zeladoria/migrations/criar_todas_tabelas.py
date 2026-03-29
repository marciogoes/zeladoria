"""
Script SIMPLIFICADO para criar todas as tabelas
"""

import sys
import os

# Adicionar raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔧 Criando tabelas do banco de dados...")
print("=" * 60)

try:
    print("1. Importando database...")
    from app.database.database import engine, Base
    print("   ✓ Database OK")
    
    print("2. Importando Usuario...")
    from app.models.usuario import Usuario
    print("   ✓ Usuario OK")
    
    print("3. Importando Secretaria...")
    from app.models.secretaria import Secretaria
    print("   ✓ Secretaria OK")
    
    print("4. Importando ServicoSecretaria...")
    from app.models_servicos import ServicoSecretaria
    print("   ✓ ServicoSecretaria OK")
    
    print("5. Importando Chamado...")
    from app.models.chamado import Chamado
    print("   ✓ Chamado OK")
    
    print("6. Importando Categoria...")
    from app.models.categoria import Categoria
    print("   ✓ Categoria OK")
    
    print("7. Importando Bairro...")
    from app.models.bairro import Bairro
    print("   ✓ Bairro OK")
    
    print("\n8. Criando todas as tabelas...")
    Base.metadata.create_all(bind=engine)
    print("   ✓ Tabelas criadas!")
    
    print("\n" + "=" * 60)
    print("✅ SUCESSO! Todas as tabelas foram criadas!")
    print("=" * 60)
    print("\nTabelas disponíveis:")
    print("  • usuarios")
    print("  • secretarias")
    print("  • servicos_secretaria")
    print("  • chamados")
    print("  • categorias")
    print("  • bairros")
    print("=" * 60)
    
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ ERRO: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)
