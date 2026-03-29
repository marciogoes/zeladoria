"""
Seed de Secretarias
Popula banco com as secretarias da Prefeitura de Belém
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal
from app.models.secretaria import Secretaria


def seed_secretarias():
    """Popula banco com secretarias de Belém"""
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem secretarias
        count = db.query(Secretaria).count()
        
        if count > 0:
            print(f"⚠️  Já existem {count} secretaria(s) cadastrada(s)")
            resposta = input("Deseja recriar todas? (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada")
                return
            
            # Deletar todas
            db.query(Secretaria).delete()
            db.commit()
            print("🗑️  Secretarias antigas removidas")
        
        secretarias = [
            {
                "nome": "Secretaria Municipal de Urbanismo",
                "sigla": "SEURB",
                "descricao": "Responsável por planejamento urbano, obras, pavimentação, iluminação pública e infraestrutura da cidade",
                "telefone": "(91) 3184-1000",
                "email": "seurb@belem.pa.gov.br",
                "endereco": "Av. Governador José Malcher, 1000",
                "bairro": "Nazaré",
                "cep": "66055-260",
                "horario_funcionamento": "Segunda a Sexta, 8h às 14h",
                "cor_primaria": "#1976D2",
                "icone": "building",
                "ativo": True
            },
            {
                "nome": "Secretaria Municipal de Saneamento",
                "sigla": "SESAN",
                "descricao": "Gestão de limpeza urbana, coleta de resíduos, drenagem e serviços de saneamento básico",
                "telefone": "(91) 3242-9500",
                "email": "sesan@belem.pa.gov.br",
                "endereco": "Av. Visconde de Souza Franco, 1500",
                "bairro": "Reduto",
                "cep": "66053-000",
                "horario_funcionamento": "Segunda a Sexta, 8h às 14h",
                "cor_primaria": "#4CAF50",
                "icone": "recycle",
                "ativo": True
            },
            {
                "nome": "Secretaria Municipal de Mobilidade",
                "sigla": "SEMOB",
                "descricao": "Gestão de trânsito, transporte público, sinalização e mobilidade urbana",
                "telefone": "(91) 3242-1100",
                "email": "semob@belem.pa.gov.br",
                "endereco": "Rua Aristides Lobo, 300",
                "bairro": "Campina",
                "cep": "66015-060",
                "horario_funcionamento": "Segunda a Sexta, 8h às 18h",
                "cor_primaria": "#FF9800",
                "icone": "car",
                "ativo": True
            },
            {
                "nome": "Secretaria Municipal de Meio Ambiente",
                "sigla": "SEMMA",
                "descricao": "Proteção ambiental, áreas verdes, fiscalização ambiental e educação ecológica",
                "telefone": "(91) 3242-6500",
                "email": "semma@belem.pa.gov.br",
                "endereco": "Travessa Lomas Valentinas, 2100",
                "bairro": "Marco",
                "cep": "66093-677",
                "horario_funcionamento": "Segunda a Sexta, 8h às 14h",
                "cor_primaria": "#2E7D32",
                "icone": "leaf",
                "ativo": True
            },
            {
                "nome": "Secretaria Municipal de Saúde",
                "sigla": "SESMA",
                "descricao": "Gestão da saúde pública, unidades de saúde, vigilância sanitária e epidemiológica",
                "telefone": "(91) 3242-3600",
                "email": "sesma@belem.pa.gov.br",
                "endereco": "Rua 28 de Setembro, 2526",
                "bairro": "Cremação",
                "cep": "66040-010",
                "horario_funcionamento": "24 horas (emergência)",
                "cor_primaria": "#D32F2F",
                "icone": "heartbeat",
                "ativo": True
            }
        ]
        
        print("\n🌱 Populando secretarias...")
        print("=" * 60)
        
        for data in secretarias:
            secretaria = Secretaria(**data)
            db.add(secretaria)
            print(f"✅ {data['sigla']} - {data['nome']}")
        
        db.commit()
        
        total = db.query(Secretaria).count()
        
        print("=" * 60)
        print(f"\n🎉 {total} secretarias cadastradas com sucesso!")
        print("\nSecretarias criadas:")
        
        for sec in db.query(Secretaria).all():
            print(f"  ID {sec.id}: {sec.sigla} - {sec.nome}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao popular secretarias: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_secretarias()
