"""
Script de População do Banco de Dados (Seed)
Sistema de Zeladoria Urbana - Belém/PA
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database.database import engine, SessionLocal, Base
from app.models.usuario import Usuario
from app.models.secretaria import Secretaria
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.chamado import Chamado


def criar_tabelas():
    print("\n📦 Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas")


def popular_secretarias(db: Session):
    print("\n🏛️  Criando secretarias...")
    secretarias_data = [
        {"sigla": "SEURB", "nome": "Secretaria Municipal de Urbanismo", "descricao": "Planejamento urbano, obras e infraestrutura", "email": "seurb@belem.pa.gov.br", "telefone": "(91) 3242-1500"},
        {"sigla": "SESAN", "nome": "Secretaria Municipal de Saneamento", "descricao": "Saneamento básico, limpeza pública e resíduos", "email": "sesan@belem.pa.gov.br", "telefone": "(91) 3242-1600"},
        {"sigla": "SEMMA", "nome": "Secretaria Municipal de Meio Ambiente", "descricao": "Preservação ambiental e áreas verdes", "email": "semma@belem.pa.gov.br", "telefone": "(91) 3242-2100"},
        {"sigla": "SESMA", "nome": "Secretaria Municipal de Saúde", "descricao": "Saúde pública e atenção básica", "email": "sesma@belem.pa.gov.br", "telefone": "(91) 3242-1800"},
        {"sigla": "SEMEC", "nome": "Secretaria Municipal de Educação", "descricao": "Educação infantil e fundamental", "email": "semec@belem.pa.gov.br", "telefone": "(91) 3242-2000"},
        {"sigla": "GMB",   "nome": "Guarda Municipal de Belém", "descricao": "Segurança patrimonial e comunitária", "email": "gmb@belem.pa.gov.br", "telefone": "(91) 3242-2400"},
        {"sigla": "OGM",   "nome": "Ouvidoria Geral do Município", "descricao": "Ouvidoria e atendimento ao cidadão", "email": "ouvidoria@belem.pa.gov.br", "telefone": "(91) 3242-2500"},
    ]
    secretarias = []
    for data in secretarias_data:
        s = Secretaria(**data)
        db.add(s)
        secretarias.append(s)
    db.commit()
    print(f"✓ {len(secretarias)} secretarias criadas")
    return secretarias


def popular_categorias(db: Session):
    print("\n📦 Criando categorias...")
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()
    sesma = db.query(Secretaria).filter_by(sigla="SESMA").first()

    categorias_data = [
        {"nome": "Buraco na via", "descricao": "Buracos e problemas no asfalto", "icone": "road", "cor": "#FF6B6B", "secretaria_id": seurb.id if seurb else None, "sla_horas": 48},
        {"nome": "Iluminação pública", "descricao": "Lâmpadas queimadas ou postes danificados", "icone": "lightbulb", "cor": "#FFD93D", "secretaria_id": seurb.id if seurb else None, "sla_horas": 24},
        {"nome": "Calçada danificada", "descricao": "Calçadas quebradas ou irregulares", "icone": "shoe-prints", "cor": "#A8DADC", "secretaria_id": seurb.id if seurb else None, "sla_horas": 72},
        {"nome": "Lixo acumulado", "descricao": "Acúmulo de lixo e entulho", "icone": "trash", "cor": "#6C757D", "secretaria_id": sesan.id if sesan else None, "sla_horas": 24},
        {"nome": "Esgoto", "descricao": "Problemas com rede de esgoto", "icone": "water", "cor": "#8B4513", "secretaria_id": sesan.id if sesan else None, "sla_horas": 12},
        {"nome": "Poda de árvore", "descricao": "Árvores que precisam de poda", "icone": "tree", "cor": "#27AE60", "secretaria_id": semma.id if semma else None, "sla_horas": 72},
        {"nome": "Foco de dengue", "descricao": "Água parada e focos do mosquito", "icone": "bug", "cor": "#E63946", "secretaria_id": sesma.id if sesma else None, "sla_horas": 12},
    ]
    categorias = []
    for data in categorias_data:
        c = Categoria(**data)
        db.add(c)
        categorias.append(c)
    db.commit()
    print(f"✓ {len(categorias)} categorias criadas")
    return categorias


def popular_bairros(db: Session):
    print("\n🏘️  Criando bairros...")
    bairros_data = [
        {"nome": "Cidade Velha", "regiao": "Centro"},
        {"nome": "Campina", "regiao": "Centro"},
        {"nome": "Nazaré", "regiao": "Centro"},
        {"nome": "Batista Campos", "regiao": "Centro"},
        {"nome": "Umarizal", "regiao": "Oeste"},
        {"nome": "São Brás", "regiao": "Oeste"},
        {"nome": "Marco", "regiao": "Sul"},
        {"nome": "Pedreira", "regiao": "Sul"},
        {"nome": "Guamá", "regiao": "Norte"},
        {"nome": "Terra Firme", "regiao": "Norte"},
    ]
    bairros = []
    for data in bairros_data:
        b = Bairro(**data)
        db.add(b)
        bairros.append(b)
    db.commit()
    print(f"✓ {len(bairros)} bairros criados")
    return bairros


def popular_usuarios(db: Session):
    print("\n👤 Criando usuários...")
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()

    usuarios_data = [
        {"nome": "Pedro Almeida", "email": "pedro.almeida@email.com", "senha": Usuario.hash_senha("senha123"), "cpf": "123.456.789-00", "telefone": "(91) 98888-1111", "tipo": "cidadao"},
        {"nome": "João Silva", "email": "joao.silva@belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "234.567.890-11", "telefone": "(91) 98888-2222", "tipo": "equipe"},
        {"nome": "Carlos Mendes - SEURB", "email": "carlos.mendes@seurb.belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "345.678.901-22", "telefone": "(91) 3242-1500", "tipo": "secretaria", "secretaria_id": seurb.id if seurb else None},
        {"nome": "Ana Costa - SESAN", "email": "ana.costa@sesan.belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "456.789.012-33", "telefone": "(91) 3242-1600", "tipo": "secretaria", "secretaria_id": sesan.id if sesan else None},
        {"nome": "Roberto Lima - SEMMA", "email": "roberto.lima@semma.belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "567.890.123-44", "telefone": "(91) 3242-2100", "tipo": "secretaria", "secretaria_id": semma.id if semma else None},
        {"nome": "Maria Santos - Gestão", "email": "maria.santos@belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "678.901.234-55", "telefone": "(91) 3242-1000", "tipo": "gestor"},
        {"nome": "Administrador", "email": "admin@belem.pa.gov.br", "senha": Usuario.hash_senha("senha123"), "cpf": "789.012.345-66", "telefone": "(91) 3242-1001", "tipo": "admin"},
    ]
    usuarios = []
    for data in usuarios_data:
        u = Usuario(**data)
        db.add(u)
        usuarios.append(u)
    db.commit()
    print(f"✓ {len(usuarios)} usuários criados")
    return usuarios


def popular_chamados(db: Session):
    print("\n📞 Criando chamados de exemplo...")
    categorias = db.query(Categoria).all()
    bairros = db.query(Bairro).all()
    cidadao = db.query(Usuario).filter_by(tipo="cidadao").first()

    if not cidadao or not categorias or not bairros:
        print("⚠️  Dados insuficientes para criar chamados")
        return []

    chamados_data = [
        {"titulo": "Buraco na Av. Presidente Vargas", "descricao": "Buraco de 50cm causando risco", "categoria_id": categorias[0].id, "bairro_id": bairros[1].id, "usuario_id": cidadao.id, "endereco": "Av. Presidente Vargas, 1000", "status": "resolvido", "prioridade": "alta"},
        {"titulo": "Lixo acumulado na rua", "descricao": "Acúmulo de lixo há mais de uma semana", "categoria_id": categorias[3].id if len(categorias) > 3 else categorias[0].id, "bairro_id": bairros[2].id, "usuario_id": cidadao.id, "endereco": "Tv. Barão do Triunfo, 234", "status": "em_andamento", "prioridade": "media"},
        {"titulo": "Poste de iluminação queimado", "descricao": "Poste apagado há 3 dias", "categoria_id": categorias[1].id if len(categorias) > 1 else categorias[0].id, "bairro_id": bairros[0].id, "usuario_id": cidadao.id, "endereco": "Rua João Diogo, 567", "status": "aberto", "prioridade": "alta"},
    ]
    chamados = []
    for data in chamados_data:
        c = Chamado(**data)
        db.add(c)
        chamados.append(c)
    db.commit()
    print(f"✓ {len(chamados)} chamados criados")
    return chamados


def main():
    print("🌱 Iniciando seed do banco de dados...")
    print("=" * 50)

    criar_tabelas()

    db = SessionLocal()
    try:
        popular_secretarias(db)
        popular_categorias(db)
        popular_bairros(db)
        popular_usuarios(db)
        popular_chamados(db)

        print("\n" + "=" * 50)
        print("✅ Seed concluído com sucesso!")
        print("\n👤 LOGINS DISPONÍVEIS (senha: senha123):")
        print("   Cidadão:   pedro.almeida@email.com")
        print("   Equipe:    joao.silva@belem.pa.gov.br")
        print("   SEURB:     carlos.mendes@seurb.belem.pa.gov.br")
        print("   Gestor:    maria.santos@belem.pa.gov.br")
        print("   Admin:     admin@belem.pa.gov.br")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Erro ao popular banco: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
