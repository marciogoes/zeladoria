"""
Script para popular categorias e bairros no banco de dados
"""
from app.database.database import SessionLocal
from app.models.categoria import Categoria
from app.models.bairro import Bairro

def popular_dados():
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        categorias_count = db.query(Categoria).count()
        bairros_count = db.query(Bairro).count()
        
        # CATEGORIAS
        if categorias_count > 0:
            print(f'✅ Já existem {categorias_count} categorias cadastradas')
        else:
            print('📝 Criando categorias...')
            categorias = [
                Categoria(nome='Iluminacao Publica', icone='💡', descricao='Problemas com iluminacao de ruas e pracas'),
                Categoria(nome='Limpeza Urbana', icone='🧹', descricao='Lixo acumulado, sujeira em vias'),
                Categoria(nome='Buracos e Pavimentacao', icone='🚧', descricao='Buracos em ruas e calcadas'),
                Categoria(nome='Arborizacao', icone='🌳', descricao='Poda, remocao ou plantio de arvores'),
                Categoria(nome='Sinalizacao', icone='🚦', descricao='Problemas com placas e semaforos'),
                Categoria(nome='Drenagem', icone='💧', descricao='Bueiros entupidos, alagamentos'),
                Categoria(nome='Pracas e Parques', icone='🏞️', descricao='Manutencao de espacos publicos'),
                Categoria(nome='Transporte Publico', icone='🚌', descricao='Problemas em pontos de onibus'),
                Categoria(nome='Outros', icone='📋', descricao='Outros problemas urbanos')
            ]
            
            for cat in categorias:
                db.add(cat)
            
            db.commit()
            print(f'✅ {len(categorias)} categorias criadas!')
        
        # BAIRROS
        if bairros_count > 0:
            print(f'✅ Já existem {bairros_count} bairros cadastrados')
        else:
            print('📝 Criando bairros de Belem...')
            bairros = [
                # Centro
                Bairro(nome='Batista Campos', regiao='Centro'),
                Bairro(nome='Campina', regiao='Centro'),
                Bairro(nome='Cidade Velha', regiao='Centro'),
                Bairro(nome='Comercio', regiao='Centro'),
                Bairro(nome='Nazare', regiao='Centro'),
                Bairro(nome='Reduto', regiao='Centro'),
                Bairro(nome='Umarizal', regiao='Centro'),
                Bairro(nome='Marco', regiao='Centro'),
                Bairro(nome='Sao Bras', regiao='Centro'),
                Bairro(nome='Pedreira', regiao='Centro'),
                Bairro(nome='Cremacao', regiao='Centro'),
                # Entroncamento
                Bairro(nome='Condor', regiao='Entroncamento'),
                Bairro(nome='Guama', regiao='Entroncamento'),
                Bairro(nome='Jurunas', regiao='Entroncamento'),
                Bairro(nome='Telegrafo', regiao='Entroncamento'),
                Bairro(nome='Terra Firme', regiao='Entroncamento'),
                Bairro(nome='Canudos', regiao='Entroncamento'),
                Bairro(nome='Sacramenta', regiao='Entroncamento'),
                # Bengui
                Bairro(nome='Bengui', regiao='Bengui'),
                Bairro(nome='Cabanagem', regiao='Bengui'),
                Bairro(nome='Marambaia', regiao='Bengui'),
                Bairro(nome='Tapana', regiao='Bengui'),
                Bairro(nome='Val-de-Caes', regiao='Bengui'),
                # Outeiro
                Bairro(nome='Coqueiro', regiao='Outeiro'),
                Bairro(nome='Outeiro', regiao='Outeiro'),
                # Icoaraci
                Bairro(nome='Icoaraci', regiao='Icoaraci'),
                Bairro(nome='Agulha', regiao='Icoaraci'),
                # Mosqueiro
                Bairro(nome='Mosqueiro', regiao='Mosqueiro')
            ]
            
            for bairro in bairros:
                db.add(bairro)
            
            db.commit()
            print(f'✅ {len(bairros)} bairros criados!')
        
        print()
        print('🎉 CONCLUIDO! Categorias e bairros populados.')
        return True
        
    except Exception as e:
        print(f'❌ ERRO: {e}')
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == '__main__':
    popular_dados()
