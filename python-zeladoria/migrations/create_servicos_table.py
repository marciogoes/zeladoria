"""
Script de Migração - Criar Tabela de Serviços
Sistema de Zeladoria Urbana - Belém/PA
"""

import sys
import os

# Adicionar o diretório raiz ao path
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, raiz)

from sqlalchemy import create_engine
from app.database.database import Base, SQLALCHEMY_DATABASE_URL, engine
from app.models_servicos import ServicoSecretaria


def criar_tabela_servicos():
    """Cria a tabela de serviços no banco"""
    print("🔧 Criando tabela de serviços...")
    
    try:
        # Criar apenas a tabela de serviços
        ServicoSecretaria.__table__.create(engine, checkfirst=True)
        
        print("✅ Tabela 'servicos_secretaria' criada com sucesso!")
        print(f"📊 Colunas criadas: {len(ServicoSecretaria.__table__.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_tabela():
    """Verifica se a tabela existe"""
    try:
        if ServicoSecretaria.__table__.exists(engine):
            print("✅ Tabela 'servicos_secretaria' existe no banco")
            return True
        else:
            print("❌ Tabela 'servicos_secretaria' NÃO existe")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False


def dropar_tabela():
    """CUIDADO: Deleta a tabela e todos os dados"""
    print("⚠️  ATENÇÃO: Esta operação vai deletar a tabela e TODOS os dados!")
    confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ")
    
    if confirmacao != "CONFIRMAR":
        print("❌ Operação cancelada")
        return False
    
    try:
        ServicoSecretaria.__table__.drop(engine, checkfirst=True)
        print("✅ Tabela deletada")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao deletar tabela: {e}")
        return False


def recriar_tabela():
    """Recria a tabela (deleta e cria novamente)"""
    print("🔄 Recriando tabela...")
    
    if dropar_tabela():
        return criar_tabela_servicos()
    
    return False


def main():
    """Menu principal"""
    print("=" * 60)
    print("  MIGRAÇÃO - TABELA DE SERVIÇOS")
    print("  Sistema de Zeladoria Urbana - Belém/PA")
    print("=" * 60)
    print()
    print(f"Banco de dados: {SQLALCHEMY_DATABASE_URL}")
    print()
    print("Escolha uma opção:")
    print("1. Criar tabela")
    print("2. Verificar se tabela existe")
    print("3. Recriar tabela (DELETA DADOS!)")
    print("4. Dropar tabela (DELETA DADOS!)")
    print("0. Sair")
    print()
    
    opcao = input("Opção: ")
    
    if opcao == "1":
        criar_tabela_servicos()
    elif opcao == "2":
        verificar_tabela()
    elif opcao == "3":
        recriar_tabela()
    elif opcao == "4":
        dropar_tabela()
    elif opcao == "0":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida")


if __name__ == "__main__":
    main()
