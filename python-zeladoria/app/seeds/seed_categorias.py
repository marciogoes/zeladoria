"""
Seed de Categorias
Cria as categorias padrão de chamados
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import SessionLocal
from app.models.categoria import Categoria


def seed_categorias():
    """Popula banco com categorias padrão"""
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem categorias
        count = db.query(Categoria).count()
        
        if count > 0:
            print(f"⚠️  Já existem {count} categoria(s) cadastrada(s)")
            resposta = input("Deseja adicionar categorias mesmo assim? (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada")
                return
        
        categorias = [
            {
                "nome": "Iluminação Pública",
                "descricao": "Lâmpadas queimadas, postes danificados, falta de iluminação",
                "icone": "💡",
                "cor": "#f59e0b",
                "secretaria_id": 1,  # SEURB
                "ativo": True
            },
            {
                "nome": "Buracos na Via",
                "descricao": "Buracos, crateras e irregularidades no asfalto",
                "icone": "🕳️",
                "cor": "#ef4444",
                "secretaria_id": 1,  # SEURB
                "ativo": True
            },
            {
                "nome": "Lixo Acumulado",
                "descricao": "Acúmulo de lixo, entulho e resíduos",
                "icone": "🗑️",
                "cor": "#84cc16",
                "secretaria_id": 2,  # SESAN
                "ativo": True
            },
            {
                "nome": "Calçada Danificada",
                "descricao": "Calçadas quebradas, irregulares ou obstruídas",
                "icone": "🚶",
                "cor": "#8b5cf6",
                "secretaria_id": 1,  # SEURB
                "ativo": True
            },
            {
                "nome": "Esgoto/Vazamento",
                "descricao": "Vazamentos de esgoto, bueiros entupidos",
                "icone": "💧",
                "cor": "#06b6d4",
                "secretaria_id": 2,  # SESAN
                "ativo": True
            },
            {
                "nome": "Arborização",
                "descricao": "Árvores caídas, galhos perigosos, poda necessária",
                "icone": "🌳",
                "cor": "#10b981",
                "secretaria_id": 4,  # SEMMA
                "ativo": True
            },
            {
                "nome": "Sinalização de Trânsito",
                "descricao": "Placas danificadas, falta de sinalização",
                "icone": "🚦",
                "cor": "#f97316",
                "secretaria_id": 3,  # SEMOB
                "ativo": True
            },
            {
                "nome": "Ponto de Ônibus",
                "descricao": "Abrigos danificados, falta de manutenção",
                "icone": "🚌",
                "cor": "#3b82f6",
                "secretaria_id": 3,  # SEMOB
                "ativo": True
            },
            {
                "nome": "Limpeza Urbana",
                "descricao": "Varrição, capina, limpeza de vias públicas",
                "icone": "🧹",
                "cor": "#a855f7",
                "secretaria_id": 2,  # SESAN
                "ativo": True
            },
            {
                "nome": "Animais na Via",
                "descricao": "Animais soltos, situação de risco",
                "icone": "🐕",
                "cor": "#ec4899",
                "secretaria_id": 5,  # SESMA
                "ativo": True
            },
            {
                "nome": "Poluição Sonora",
                "descricao": "Barulho excessivo, perturbação do sossego",
                "icone": "🔊",
                "cor": "#64748b",
                "secretaria_id": 4,  # SEMMA
                "ativo": True
            },
            {
                "nome": "Fiscalização",
                "descricao": "Denúncias diversas, irregularidades",
                "icone": "👮",
                "cor": "#78716c",
                "secretaria_id": 1,  # SEURB
                "ativo": True
            }
        ]
        
        print("\n🏷️ Criando categorias...")
        print("=" * 80)
        
        for data in categorias:
            categoria = Categoria(**data)
            db.add(categoria)
            print(f"✅ {data['icone']} {data['nome']:<30} | Cor: {data['cor']}")
        
        db.commit()
        
        total = db.query(Categoria).count()
        
        print("=" * 80)
        print(f"\n🎉 Categorias criadas com sucesso!")
        print(f"\n📊 Total no banco: {total} categoria(s)")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar categorias: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_categorias()
