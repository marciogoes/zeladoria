"""
Seed de Bairros de Belém/PA
Cria os principais bairros da cidade
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal
from app.models.bairro import Bairro


def seed_bairros():
    """Popula banco com bairros de Belém"""
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem bairros
        count = db.query(Bairro).count()
        
        if count > 0:
            print(f"⚠️  Já existem {count} bairro(s) cadastrado(s)")
            resposta = input("Deseja adicionar bairros mesmo assim? (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada")
                return
        
        # Principais bairros de Belém organizados por região
        bairros = [
            # Centro/Comercial
            {"nome": "Campina", "regiao": "Centro", "ativo": True},
            {"nome": "Comércio", "regiao": "Centro", "ativo": True},
            {"nome": "Cidade Velha", "regiao": "Centro", "ativo": True},
            {"nome": "Reduto", "regiao": "Centro", "ativo": True},
            
            # Zona Sul
            {"nome": "Nazaré", "regiao": "Sul", "ativo": True},
            {"nome": "Batista Campos", "regiao": "Sul", "ativo": True},
            {"nome": "Umarizal", "regiao": "Sul", "ativo": True},
            {"nome": "São Brás", "regiao": "Sul", "ativo": True},
            {"nome": "Marco", "regiao": "Sul", "ativo": True},
            {"nome": "Pedreira", "regiao": "Sul", "ativo": True},
            
            # Zona Leste
            {"nome": "Cremação", "regiao": "Leste", "ativo": True},
            {"nome": "Jurunas", "regiao": "Leste", "ativo": True},
            {"nome": "Condor", "regiao": "Leste", "ativo": True},
            {"nome": "Canudos", "regiao": "Leste", "ativo": True},
            {"nome": "Guamá", "regiao": "Leste", "ativo": True},
            {"nome": "Terra Firme", "regiao": "Leste", "ativo": True},
            
            # Zona Norte
            {"nome": "Telégrafo", "regiao": "Norte", "ativo": True},
            {"nome": "Marambaia", "regiao": "Norte", "ativo": True},
            {"nome": "Sacramenta", "regiao": "Norte", "ativo": True},
            {"nome": "Val-de-Cães", "regiao": "Norte", "ativo": True},
            
            # Entroncamento
            {"nome": "Entroncamento", "regiao": "Entroncamento", "ativo": True},
            {"nome": "Curió-Utinga", "regiao": "Entroncamento", "ativo": True},
            
            # Bengui
            {"nome": "Bengui", "regiao": "Bengui", "ativo": True},
            {"nome": "Pratinha", "regiao": "Bengui", "ativo": True},
            {"nome": "Parque Verde", "regiao": "Bengui", "ativo": True},
            
            # Icoaraci
            {"nome": "Icoaraci", "regiao": "Icoaraci", "ativo": True},
            {"nome": "Ponta Grossa", "regiao": "Icoaraci", "ativo": True},
            {"nome": "Águas Lindas", "regiao": "Icoaraci", "ativo": True},
            
            # Outeiro
            {"nome": "Outeiro", "regiao": "Outeiro", "ativo": True},
            
            # Mosqueiro
            {"nome": "Mosqueiro", "regiao": "Mosqueiro", "ativo": True},
            
            # Outros bairros importantes
            {"nome": "Souza", "regiao": "Sul", "ativo": True},
            {"nome": "Castanheira", "regiao": "Norte", "ativo": True},
            {"nome": "Tapanã", "regiao": "Norte", "ativo": True},
            {"nome": "Coqueiro", "regiao": "Norte", "ativo": True},
            {"nome": "Barreiro", "regiao": "Sul", "ativo": True},
        ]
        
        print("\n🏘️ Criando bairros de Belém...")
        print("=" * 80)
        
        # Ordenar por região e nome
        bairros_sorted = sorted(bairros, key=lambda x: (x['regiao'], x['nome']))
        
        regiao_atual = None
        for data in bairros_sorted:
            if data['regiao'] != regiao_atual:
                regiao_atual = data['regiao']
                print(f"\n📍 {regiao_atual}:")
            
            bairro = Bairro(**data)
            db.add(bairro)
            print(f"   ✅ {data['nome']}")
        
        db.commit()
        
        total = db.query(Bairro).count()
        
        print("\n" + "=" * 80)
        print(f"\n🎉 Bairros criados com sucesso!")
        print(f"\n📊 Total no banco: {total} bairro(s)")
        
        # Estatísticas por região
        print("\n📊 Bairros por região:")
        regioes = db.query(Bairro.regiao, db.func.count(Bairro.id)).group_by(Bairro.regiao).all()
        for regiao, count in sorted(regioes):
            print(f"   {regiao:15} → {count:2} bairro(s)")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar bairros: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_bairros()
