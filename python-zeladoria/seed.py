"""
Seed idempotente — verifica antes de inserir.
Sistema de Zeladoria Urbana - Belém/PA
"""
from sqlalchemy.orm import Session
from app.database.database import engine, SessionLocal, Base
from app.models.usuario import Usuario
from app.models.secretaria import Secretaria
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.chamado import Chamado


def criar_tabelas():
    print("\n📦 Criando/verificando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas OK")


def popular_secretarias(db: Session):
    if db.query(Secretaria).count() > 0:
        print("⏭️  Secretarias já existem — pulando")
        return db.query(Secretaria).all()
    print("\n🏛️  Criando secretarias...")
    dados = [
        {"sigla": "SEURB", "nome": "Secretaria Municipal de Urbanismo",      "descricao": "Planejamento urbano, obras e infraestrutura", "email": "seurb@belem.pa.gov.br",     "telefone": "(91) 3242-1500"},
        {"sigla": "SESAN", "nome": "Secretaria Municipal de Saneamento",     "descricao": "Saneamento básico e limpeza pública",        "email": "sesan@belem.pa.gov.br",     "telefone": "(91) 3242-1600"},
        {"sigla": "SEMMA", "nome": "Secretaria Municipal de Meio Ambiente",  "descricao": "Preservação ambiental e áreas verdes",      "email": "semma@belem.pa.gov.br",     "telefone": "(91) 3242-2100"},
        {"sigla": "SESMA", "nome": "Secretaria Municipal de Saúde",          "descricao": "Saúde pública e atenção básica",             "email": "sesma@belem.pa.gov.br",     "telefone": "(91) 3242-1800"},
        {"sigla": "SEMEC", "nome": "Secretaria Municipal de Educação",       "descricao": "Educação infantil e fundamental",            "email": "semec@belem.pa.gov.br",     "telefone": "(91) 3242-2000"},
        {"sigla": "GMB",   "nome": "Guarda Municipal de Belém",              "descricao": "Segurança patrimonial e comunitária",       "email": "gmb@belem.pa.gov.br",       "telefone": "(91) 3242-2400"},
        {"sigla": "OGM",   "nome": "Ouvidoria Geral do Município",           "descricao": "Ouvidoria e atendimento ao cidadão",        "email": "ouvidoria@belem.pa.gov.br", "telefone": "(91) 3242-2500"},
    ]
    result = []
    for d in dados:
        s = Secretaria(**d)
        db.add(s)
        result.append(s)
    db.commit()
    print(f"✓ {len(result)} secretarias criadas")
    return result


def popular_categorias(db: Session):
    if db.query(Categoria).count() > 0:
        print("⏭️  Categorias já existem — pulando")
        return db.query(Categoria).all()
    print("\n📦 Criando categorias...")
    dados = [
        {"nome": "Buraco na via",       "descricao": "Buracos e problemas no asfalto",             "icone": "road",        "cor": "#FF6B6B", "sla_horas": 48},
        {"nome": "Iluminação pública",  "descricao": "Lâmpadas queimadas ou postes danificados",   "icone": "lightbulb",   "cor": "#FFD93D", "sla_horas": 24},
        {"nome": "Calçada danificada",  "descricao": "Calçadas quebradas ou irregulares",          "icone": "shoe-prints", "cor": "#A8DADC", "sla_horas": 72},
        {"nome": "Lixo acumulado",      "descricao": "Acúmulo de lixo e entulho",                  "icone": "trash",       "cor": "#6C757D", "sla_horas": 24},
        {"nome": "Esgoto",              "descricao": "Problemas com rede de esgoto",               "icone": "water",       "cor": "#8B4513", "sla_horas": 12},
        {"nome": "Poda de árvore",      "descricao": "Árvores que precisam de poda",               "icone": "tree",        "cor": "#27AE60", "sla_horas": 72},
        {"nome": "Foco de dengue",      "descricao": "Água parada e focos do mosquito",            "icone": "bug",         "cor": "#E63946", "sla_horas": 12},
        {"nome": "Área verde",          "descricao": "Manutenção de praças e parques",             "icone": "leaf",        "cor": "#52B788", "sla_horas": 48},
        {"nome": "Sinalização",         "descricao": "Placas, semáforos e faixas de pedestre",    "icone": "sign",        "cor": "#F4A261", "sla_horas": 48},
        {"nome": "Animal abandonado",   "descricao": "Animais de rua precisando de ajuda",        "icone": "paw",         "cor": "#E76F51", "sla_horas": 24},
    ]
    result = []
    for d in dados:
        c = Categoria(**d)
        db.add(c)
        result.append(c)
    db.commit()
    print(f"✓ {len(result)} categorias criadas")
    return result


def popular_bairros(db: Session):
    if db.query(Bairro).count() > 0:
        print("⏭️  Bairros já existem — pulando")
        return db.query(Bairro).all()
    print("\n🏘️  Criando bairros...")
    dados = [
        {"nome": "Cidade Velha",    "regiao": "Centro"},
        {"nome": "Campina",         "regiao": "Centro"},
        {"nome": "Nazaré",          "regiao": "Centro"},
        {"nome": "Batista Campos",  "regiao": "Centro"},
        {"nome": "Umarizal",        "regiao": "Oeste"},
        {"nome": "São Brás",        "regiao": "Oeste"},
        {"nome": "Fátima",          "regiao": "Oeste"},
        {"nome": "Marco",           "regiao": "Sul"},
        {"nome": "Pedreira",        "regiao": "Sul"},
        {"nome": "Sacramenta",      "regiao": "Sul"},
        {"nome": "Telégrafo",       "regiao": "Sul"},
        {"nome": "Guamá",           "regiao": "Norte"},
        {"nome": "Terra Firme",     "regiao": "Norte"},
        {"nome": "Canudos",         "regiao": "Norte"},
        {"nome": "Marambaia",       "regiao": "Norte"},
        {"nome": "Cremação",        "regiao": "Leste"},
        {"nome": "Jurunas",         "regiao": "Leste"},
        {"nome": "Condor",          "regiao": "Leste"},
        {"nome": "Reduto",          "regiao": "Centro"},
        {"nome": "Outeiro",         "regiao": "Ilhas"},
    ]
    result = []
    for d in dados:
        b = Bairro(**d)
        db.add(b)
        result.append(b)
    db.commit()
    print(f"✓ {len(result)} bairros criados")
    return result


def popular_usuarios(db: Session):
    emails = [
        "pedro.almeida@email.com",
        "joao.silva@belem.pa.gov.br",
        "carlos.mendes@seurb.belem.pa.gov.br",
        "ana.costa@sesan.belem.pa.gov.br",
        "roberto.lima@semma.belem.pa.gov.br",
        "maria.santos@belem.pa.gov.br",
        "admin@belem.pa.gov.br",
    ]
    existentes = [u.email for u in db.query(Usuario.email).all()]
    if all(e in existentes for e in emails):
        print("⏭️  Usuários já existem — pulando")
        return db.query(Usuario).all()

    print("\n👤 Criando usuários...")
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()

    dados = [
        {"nome": "Pedro Almeida",         "email": "pedro.almeida@email.com",                   "senha": Usuario.hash_senha("senha123"), "cpf": "123.456.789-00", "telefone": "(91) 98888-1111", "tipo": "cidadao"},
        {"nome": "João Silva",             "email": "joao.silva@belem.pa.gov.br",                "senha": Usuario.hash_senha("senha123"), "cpf": "234.567.890-11", "telefone": "(91) 98888-2222", "tipo": "equipe"},
        {"nome": "Carlos Mendes - SEURB",  "email": "carlos.mendes@seurb.belem.pa.gov.br",      "senha": Usuario.hash_senha("senha123"), "cpf": "345.678.901-22", "telefone": "(91) 3242-1500", "tipo": "secretaria", "secretaria_id": seurb.id if seurb else None},
        {"nome": "Ana Costa - SESAN",      "email": "ana.costa@sesan.belem.pa.gov.br",          "senha": Usuario.hash_senha("senha123"), "cpf": "456.789.012-33", "telefone": "(91) 3242-1600", "tipo": "secretaria", "secretaria_id": sesan.id if sesan else None},
        {"nome": "Roberto Lima - SEMMA",   "email": "roberto.lima@semma.belem.pa.gov.br",       "senha": Usuario.hash_senha("senha123"), "cpf": "567.890.123-44", "telefone": "(91) 3242-2100", "tipo": "secretaria", "secretaria_id": semma.id if semma else None},
        {"nome": "Maria Santos - Gestão",  "email": "maria.santos@belem.pa.gov.br",             "senha": Usuario.hash_senha("senha123"), "cpf": "678.901.234-55", "telefone": "(91) 3242-1000", "tipo": "gestor"},
        {"nome": "Administrador",          "email": "admin@belem.pa.gov.br",                    "senha": Usuario.hash_senha("senha123"), "cpf": "789.012.345-66", "telefone": "(91) 3242-1001", "tipo": "admin"},
    ]
    criados = 0
    for d in dados:
        if d["email"] not in existentes:
            db.add(Usuario(**d))
            criados += 1
    db.commit()
    print(f"✓ {criados} usuários criados ({len(existentes)} já existiam)")
    return db.query(Usuario).all()


def popular_chamados(db: Session):
    if db.query(Chamado).count() > 0:
        print("⏭️  Chamados já existem — pulando")
        return
    print("\n📞 Criando chamados de exemplo...")
    categorias = db.query(Categoria).all()
    bairros = db.query(Bairro).all()
    cidadao = db.query(Usuario).filter_by(tipo="cidadao").first()
    if not cidadao or not categorias or not bairros:
        print("⚠️  Dados insuficientes para chamados")
        return
    dados = [
        {"titulo": "Buraco na Av. Presidente Vargas", "descricao": "Buraco de 50cm causando risco aos veículos",  "categoria_id": categorias[0].id, "bairro_id": bairros[1].id, "usuario_id": cidadao.id, "endereco": "Av. Presidente Vargas, 1000", "status": "resolvido",    "prioridade": "alta"},
        {"titulo": "Lixo acumulado na rua",           "descricao": "Acúmulo de lixo há mais de uma semana",       "categoria_id": categorias[3].id, "bairro_id": bairros[2].id, "usuario_id": cidadao.id, "endereco": "Tv. Barão do Triunfo, 234",  "status": "em_andamento", "prioridade": "media"},
        {"titulo": "Poste de iluminação queimado",    "descricao": "Poste apagado há 3 dias deixando a rua escura","categoria_id": categorias[1].id, "bairro_id": bairros[0].id, "usuario_id": cidadao.id, "endereco": "Rua João Diogo, 567",        "status": "aberto",       "prioridade": "alta"},
        {"titulo": "Esgoto estourado na calçada",     "descricao": "Vazamento de esgoto com mau cheiro intenso",  "categoria_id": categorias[4].id, "bairro_id": bairros[4].id, "usuario_id": cidadao.id, "endereco": "Av. Gentil Bittencourt, 320","status": "aberto",       "prioridade": "alta"},
        {"titulo": "Árvore com galhos sobre fios",    "descricao": "Galhos de árvore tocando a fiação elétrica",  "categoria_id": categorias[5].id, "bairro_id": bairros[5].id, "usuario_id": cidadao.id, "endereco": "Tv. 14 de Março, 89",        "status": "aberto",       "prioridade": "media"},
    ]
    for d in dados:
        db.add(Chamado(**d))
    db.commit()
    print(f"✓ {len(dados)} chamados criados")


def main():
    print("🌱 Iniciando seed idempotente...")
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
        print("✅ Seed concluído!")
        print("\n👤 LOGINS (senha: senha123):")
        print("   Cidadão:  pedro.almeida@email.com")
        print("   Admin:    admin@belem.pa.gov.br")
        print("   Gestor:   maria.santos@belem.pa.gov.br")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback; traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
