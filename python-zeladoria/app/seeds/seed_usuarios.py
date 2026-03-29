"""
Seed de Usuários Padrão
Cria usuários de teste para cada perfil do sistema
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal
from app.models.usuario import Usuario


def seed_usuarios():
    """Popula banco com usuários de teste"""
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem usuários
        count = db.query(Usuario).count()
        
        if count > 0:
            print(f"⚠️  Já existem {count} usuário(s) cadastrado(s)")
            resposta = input("Deseja adicionar usuários de teste mesmo assim? (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada")
                return
        
        usuarios = [
            {
                "nome": "Admin Sistema",
                "email": "admin@zeladoria.com",
                "senha": "admin123",
                "tipo": "admin",
                "telefone": "(91) 98888-0001",
                "cpf": "111.111.111-11",
                "ativo": True
            },
            {
                "nome": "João Silva - SEURB",
                "email": "seurb@zeladoria.com",
                "senha": "seurb123",
                "tipo": "secretaria",
                "telefone": "(91) 3184-1001",
                "cpf": "222.222.222-22",
                "secretaria_id": 1,  # SEURB
                "ativo": True
            },
            {
                "nome": "Maria Santos - SESAN",
                "email": "sesan@zeladoria.com",
                "senha": "sesan123",
                "tipo": "secretaria",
                "telefone": "(91) 3242-9501",
                "cpf": "333.333.333-33",
                "secretaria_id": 2,  # SESAN
                "ativo": True
            },
            {
                "nome": "Carlos Oliveira - SEMOB",
                "email": "semob@zeladoria.com",
                "senha": "semob123",
                "tipo": "secretaria",
                "telefone": "(91) 3242-1101",
                "cpf": "444.444.444-44",
                "secretaria_id": 3,  # SEMOB
                "ativo": True
            },
            {
                "nome": "Ana Costa - SEMMA",
                "email": "semma@zeladoria.com",
                "senha": "semma123",
                "tipo": "secretaria",
                "telefone": "(91) 3242-6501",
                "cpf": "555.555.555-55",
                "secretaria_id": 4,  # SEMMA
                "ativo": True
            },
            {
                "nome": "Pedro Ferreira - SESMA",
                "email": "sesma@zeladoria.com",
                "senha": "sesma123",
                "tipo": "secretaria",
                "telefone": "(91) 3242-3601",
                "cpf": "666.666.666-66",
                "secretaria_id": 5,  # SESMA
                "ativo": True
            },
            {
                "nome": "Gestor Municipal",
                "email": "gestor@zeladoria.com",
                "senha": "gestor123",
                "tipo": "gestor",
                "telefone": "(91) 98888-0002",
                "cpf": "777.777.777-77",
                "ativo": True
            },
            {
                "nome": "Equipe Zeladoria",
                "email": "equipe@zeladoria.com",
                "senha": "equipe123",
                "tipo": "equipe",
                "telefone": "(91) 98888-0003",
                "cpf": "888.888.888-88",
                "ativo": True
            },
            {
                "nome": "Cidadão Teste",
                "email": "cidadao@zeladoria.com",
                "senha": "cidadao123",
                "tipo": "cidadao",
                "telefone": "(91) 98888-0004",
                "cpf": "999.999.999-99",
                "ativo": True
            }
        ]
        
        print("\n🌱 Criando usuários de teste...")
        print("=" * 80)
        
        for data in usuarios:
            # Hash da senha
            senha = data.pop("senha")
            usuario = Usuario(**data)
            usuario.senha = Usuario.hash_senha(senha)
            
            db.add(usuario)
            print(f"✅ {data['tipo']:12} | {data['email']:30} | {data['nome']}")
        
        db.commit()
        
        total = db.query(Usuario).count()
        
        print("=" * 80)
        print(f"\n🎉 Usuários criados com sucesso!")
        print(f"\n📊 Total no banco: {total} usuário(s)")
        
        print("\n🔑 CREDENCIAIS DE TESTE:")
        print("=" * 80)
        print("Tipo          | Email                      | Senha")
        print("-" * 80)
        print("Admin         | admin@zeladoria.com        | admin123")
        print("SEURB         | seurb@zeladoria.com        | seurb123")
        print("SESAN         | sesan@zeladoria.com        | sesan123")
        print("SEMOB         | semob@zeladoria.com        | semob123")
        print("SEMMA         | semma@zeladoria.com        | semma123")
        print("SESMA         | sesma@zeladoria.com        | sesma123")
        print("Gestor        | gestor@zeladoria.com       | gestor123")
        print("Equipe        | equipe@zeladoria.com       | equipe123")
        print("Cidadão       | cidadao@zeladoria.com      | cidadao123")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar usuários: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_usuarios()
