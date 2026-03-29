"""
Script de População do Banco de Dados (Seed)
Sistema de Zeladoria Urbana - Belém/PA
Com Secretarias Municipais Reais
"""

from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal, Base
from app.models import (
    Usuario, TipoUsuario, Secretaria, Categoria, Bairro,
    Chamado, StatusChamado, PrioridadeChamado, Avaliacao
)

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """Cria hash da senha"""
    return pwd_context.hash(senha)


def limpar_banco():
    """Limpa todas as tabelas (cuidado!)"""
    print("🗑️  Limpando banco de dados...")
    Base.metadata.drop_all(bind=engine)
    print("✓ Banco limpo")


def criar_tabelas():
    """Cria todas as tabelas"""
    print("\n📦 Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas")


def popular_secretarias(db: Session):
    """Popula as Secretarias Municipais de Belém"""
    print("\n🏛️  Criando secretarias municipais...")
    
    secretarias_data = [
        # Administração e Gestão
        {
            "sigla": "SEMAD",
            "nome": "Secretaria Municipal de Administração",
            "descricao": "Responsável pela gestão administrativa da prefeitura",
            "email": "semad@belem.pa.gov.br",
            "telefone": "(91) 3242-1100"
        },
        {
            "sigla": "SEGEP",
            "nome": "Secretaria Municipal de Coordenadoria Geral de Planejamento e Gestão",
            "descricao": "Planejamento estratégico e gestão municipal",
            "email": "segep@belem.pa.gov.br",
            "telefone": "(91) 3242-1200"
        },
        
        # Finanças e Economia
        {
            "sigla": "SEFIN",
            "nome": "Secretaria Municipal de Finanças",
            "descricao": "Gestão financeira e tributária do município",
            "email": "sefin@belem.pa.gov.br",
            "telefone": "(91) 3242-1300"
        },
        {
            "sigla": "SECON",
            "nome": "Secretaria Municipal de Economia",
            "descricao": "Desenvolvimento econômico e empreendedorismo",
            "email": "secon@belem.pa.gov.br",
            "telefone": "(91) 3242-1400"
        },
        
        # Infraestrutura e Urbanismo
        {
            "sigla": "SEURB",
            "nome": "Secretaria Municipal de Urbanismo",
            "descricao": "Planejamento urbano, obras e infraestrutura",
            "email": "seurb@belem.pa.gov.br",
            "telefone": "(91) 3242-1500"
        },
        {
            "sigla": "SESAN",
            "nome": "Secretaria Municipal de Saneamento",
            "descricao": "Saneamento básico, limpeza pública e resíduos",
            "email": "sesan@belem.pa.gov.br",
            "telefone": "(91) 3242-1600"
        },
        {
            "sigla": "SEHAB",
            "nome": "Secretaria Municipal de Habitação",
            "descricao": "Habitação popular e regularização fundiária",
            "email": "sehab@belem.pa.gov.br",
            "telefone": "(91) 3242-1700"
        },
        
        # Saúde e Bem-Estar
        {
            "sigla": "SESMA",
            "nome": "Secretaria Municipal de Saúde",
            "descricao": "Saúde pública e atenção básica",
            "email": "sesma@belem.pa.gov.br",
            "telefone": "(91) 3242-1800"
        },
        {
            "sigla": "SEMULHER",
            "nome": "Secretaria Municipal da Mulher",
            "descricao": "Políticas públicas para mulheres",
            "email": "semulher@belem.pa.gov.br",
            "telefone": "(91) 3242-1900"
        },
        
        # Educação
        {
            "sigla": "SEMEC",
            "nome": "Secretaria Municipal de Educação",
            "descricao": "Educação infantil e fundamental",
            "email": "semec@belem.pa.gov.br",
            "telefone": "(91) 3242-2000"
        },
        
        # Meio Ambiente
        {
            "sigla": "SEMMA",
            "nome": "Secretaria Municipal de Meio Ambiente",
            "descricao": "Preservação ambiental e áreas verdes",
            "email": "semma@belem.pa.gov.br",
            "telefone": "(91) 3242-2100"
        },
        
        # Outras Secretarias
        {
            "sigla": "SEMAJ",
            "nome": "Secretaria Municipal de Assuntos Jurídicos",
            "descricao": "Assessoria jurídica do município",
            "email": "semaj@belem.pa.gov.br",
            "telefone": "(91) 3242-2200"
        },
        {
            "sigla": "SEJEL",
            "nome": "Secretaria Municipal de Esporte, Juventude e Lazer",
            "descricao": "Esportes, juventude e atividades de lazer",
            "email": "sejel@belem.pa.gov.br",
            "telefone": "(91) 3242-2300"
        },
        
        # Órgãos e Autarquias
        {
            "sigla": "GMB",
            "nome": "Guarda Municipal de Belém",
            "descricao": "Segurança patrimonial e comunitária",
            "email": "gmb@belem.pa.gov.br",
            "telefone": "(91) 3242-2400"
        },
        {
            "sigla": "OGM",
            "nome": "Ouvidoria Geral do Município",
            "descricao": "Ouvidoria e atendimento ao cidadão",
            "email": "ouvidoria@belem.pa.gov.br",
            "telefone": "(91) 3242-2500"
        },
    ]
    
    secretarias = []
    for data in secretarias_data:
        secretaria = Secretaria(**data)
        db.add(secretaria)
        secretarias.append(secretaria)
    
    db.commit()
    print(f"✓ {len(secretarias)} secretarias criadas")
    return secretarias


def popular_categorias(db: Session):
    """Popula as categorias associadas às secretarias"""
    print("\n📦 Criando categorias...")
    
    # Buscar secretarias
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()
    sesma = db.query(Secretaria).filter_by(sigla="SESMA").first()
    sejel = db.query(Secretaria).filter_by(sigla="SEJEL").first()
    gmb = db.query(Secretaria).filter_by(sigla="GMB").first()
    semec = db.query(Secretaria).filter_by(sigla="SEMEC").first()
    sehab = db.query(Secretaria).filter_by(sigla="SEHAB").first()
    
    categorias_data = [
        # SEURB - Urbanismo
        {
            "nome": "Buraco na via",
            "descricao": "Buracos, crateras e problemas no asfalto",
            "icone": "road",
            "cor": "#FF6B6B",
            "secretaria_id": seurb.id,
            "sla_horas": 48
        },
        {
            "nome": "Iluminação pública",
            "descricao": "Lâmpadas queimadas ou postes danificados",
            "icone": "lightbulb",
            "cor": "#FFD93D",
            "secretaria_id": seurb.id,
            "sla_horas": 24
        },
        {
            "nome": "Calçada danificada",
            "descricao": "Calçadas quebradas ou irregulares",
            "icone": "shoe-prints",
            "cor": "#A8DADC",
            "secretaria_id": seurb.id,
            "sla_horas": 72
        },
        {
            "nome": "Sinalização",
            "descricao": "Placas, semáforos e faixas de pedestre",
            "icone": "traffic-light",
            "cor": "#F4A261",
            "secretaria_id": seurb.id,
            "sla_horas": 48
        },
        
        # SESAN - Saneamento
        {
            "nome": "Lixo acumulado",
            "descricao": "Acúmulo de lixo e entulho",
            "icone": "trash",
            "cor": "#6C757D",
            "secretaria_id": sesan.id,
            "sla_horas": 24
        },
        {
            "nome": "Esgoto",
            "descricao": "Problemas com rede de esgoto",
            "icone": "water",
            "cor": "#8B4513",
            "secretaria_id": sesan.id,
            "sla_horas": 12
        },
        {
            "nome": "Coleta de lixo",
            "descricao": "Problemas com coleta de resíduos",
            "icone": "recycle",
            "cor": "#2ECC71",
            "secretaria_id": sesan.id,
            "sla_horas": 24
        },
        
        # SEMMA - Meio Ambiente
        {
            "nome": "Poda de árvore",
            "descricao": "Árvores que precisam de poda",
            "icone": "tree",
            "cor": "#27AE60",
            "secretaria_id": semma.id,
            "sla_horas": 72
        },
        {
            "nome": "Área verde",
            "descricao": "Manutenção de praças e parques",
            "icone": "leaf",
            "cor": "#52B788",
            "secretaria_id": semma.id,
            "sla_horas": 48
        },
        {
            "nome": "Animal abandonado",
            "descricao": "Animais de rua precisando de ajuda",
            "icone": "paw",
            "cor": "#E76F51",
            "secretaria_id": semma.id,
            "sla_horas": 24
        },
        
        # SESMA - Saúde
        {
            "nome": "Foco de dengue",
            "descricao": "Água parada e focos do mosquito",
            "icone": "bug",
            "cor": "#E63946",
            "secretaria_id": sesma.id,
            "sla_horas": 12
        },
        
        # SEJEL - Esporte e Lazer
        {
            "nome": "Equipamento público",
            "descricao": "Equipamentos de praças e academias",
            "icone": "dumbbell",
            "cor": "#457B9D",
            "secretaria_id": sejel.id,
            "sla_horas": 72
        },
        
        # GMB - Guarda Municipal
        {
            "nome": "Segurança pública",
            "descricao": "Questões de segurança e vandalismo",
            "icone": "shield-alt",
            "cor": "#1D3557",
            "secretaria_id": gmb.id,
            "sla_horas": 6
        },
        
        # SEMEC - Educação
        {
            "nome": "Infraestrutura escolar",
            "descricao": "Problemas em escolas municipais",
            "icone": "school",
            "cor": "#4361EE",
            "secretaria_id": semec.id,
            "sla_horas": 48
        },
        
        # SEHAB - Habitação
        {
            "nome": "Habitação irregular",
            "descricao": "Ocupações e regularização fundiária",
            "icone": "home",
            "cor": "#BC6C25",
            "secretaria_id": sehab.id,
            "sla_horas": 168
        },
    ]
    
    categorias = []
    for data in categorias_data:
        categoria = Categoria(**data)
        db.add(categoria)
        categorias.append(categoria)
    
    db.commit()
    print(f"✓ {len(categorias)} categorias criadas")
    return categorias


def popular_bairros(db: Session):
    """Popula os bairros de Belém"""
    print("\n🏘️  Criando bairros...")
    
    bairros_data = [
        # Região Central
        {"nome": "Cidade Velha", "regiao": "Centro"},
        {"nome": "Campina", "regiao": "Centro"},
        {"nome": "Reduto", "regiao": "Centro"},
        {"nome": "Nazaré", "regiao": "Centro"},
        {"nome": "Batista Campos", "regiao": "Centro"},
        
        # Região Norte
        {"nome": "Marambaia", "regiao": "Norte"},
        {"nome": "Canudos", "regiao": "Norte"},
        {"nome": "Guamá", "regiao": "Norte"},
        {"nome": "Terra Firme", "regiao": "Norte"},
        
        # Região Sul
        {"nome": "Marco", "regiao": "Sul"},
        {"nome": "Pedreira", "regiao": "Sul"},
        {"nome": "Sacramenta", "regiao": "Sul"},
        {"nome": "Telégrafo", "regiao": "Sul"},
        
        # Região Leste
        {"nome": "Cremação", "regiao": "Leste"},
        {"nome": "Jurunas", "regiao": "Leste"},
        {"nome": "Condor", "regiao": "Leste"},
        
        # Região Oeste
        {"nome": "Umarizal", "regiao": "Oeste"},
        {"nome": "São Brás", "regiao": "Oeste"},
        {"nome": "Fátima", "regiao": "Oeste"},
        
        # Região de Outeiro
        {"nome": "Outeiro", "regiao": "Ilhas"},
    ]
    
    bairros = []
    for data in bairros_data:
        bairro = Bairro(**data)
        db.add(bairro)
        bairros.append(bairro)
    
    db.commit()
    print(f"✓ {len(bairros)} bairros criados")
    return bairros


def popular_usuarios(db: Session):
    """Popula usuários de teste"""
    print("\n👤 Criando usuários...")
    
    # Buscar secretarias
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()
    
    usuarios_data = [
        # Cidadão
        {
            "nome": "Pedro Almeida",
            "email": "pedro.almeida@email.com",
            "senha": criar_hash_senha("senha123"),
            "cpf": "123.456.789-00",
            "telefone": "(91) 98888-1111",
            "tipo": TipoUsuario.CIDADAO
        },
        
        # Equipe de campo
        {
            "nome": "João Silva",
            "email": "joao.silva@belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "234.567.890-11",
            "telefone": "(91) 98888-2222",
            "tipo": TipoUsuario.EQUIPE
        },
        
        # Usuário da SEURB (Secretaria)
        {
            "nome": "Carlos Mendes - SEURB",
            "email": "carlos.mendes@seurb.belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "345.678.901-22",
            "telefone": "(91) 3242-1500",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": seurb.id
        },
        
        # Usuário da SESAN (Secretaria)
        {
            "nome": "Ana Costa - SESAN",
            "email": "ana.costa@sesan.belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "456.789.012-33",
            "telefone": "(91) 3242-1600",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": sesan.id
        },
        
        # Usuário da SEMMA (Secretaria)
        {
            "nome": "Roberto Lima - SEMMA",
            "email": "roberto.lima@semma.belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "567.890.123-44",
            "telefone": "(91) 3242-2100",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": semma.id
        },
        
        # Gestor (Prefeito/Coordenador Geral)
        {
            "nome": "Maria Santos - Gestão",
            "email": "maria.santos@belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "678.901.234-55",
            "telefone": "(91) 3242-1000",
            "tipo": TipoUsuario.GESTOR
        },
        
        # Admin
        {
            "nome": "Administrador",
            "email": "admin@belem.pa.gov.br",
            "senha": criar_hash_senha("senha123"),
            "cpf": "789.012.345-66",
            "telefone": "(91) 3242-1001",
            "tipo": TipoUsuario.ADMIN
        },
    ]
    
    usuarios = []
    for data in usuarios_data:
        usuario = Usuario(**data)
        db.add(usuario)
        usuarios.append(usuario)
    
    db.commit()
    print(f"✓ {len(usuarios)} usuários criados")
    return usuarios


def popular_chamados(db: Session):
    """Popula chamados de exemplo"""
    print("\n📞 Criando chamados de exemplo...")
    
    # Buscar dados
    categorias = db.query(Categoria).all()
    bairros = db.query(Bairro).all()
    cidadao = db.query(Usuario).filter_by(tipo=TipoUsuario.CIDADAO).first()
    operador = db.query(Usuario).filter_by(tipo=TipoUsuario.EQUIPE).first()
    
    chamados_data = [
        # Chamado resolvido
        {
            "protocolo": "2025001",
            "titulo": "Buraco grande na Av. Presidente Vargas",
            "descricao": "Buraco de aproximadamente 50cm de diâmetro causando risco aos veículos",
            "categoria_id": categorias[0].id if categorias else 1,
            "bairro_id": bairros[1].id if len(bairros) > 1 else 1,
            "cidadao_id": cidadao.id,
            "operador_id": operador.id,
            "endereco": "Av. Presidente Vargas, 1000",
            "latitude": -1.4558,
            "longitude": -48.4902,
            "status": StatusChamado.RESOLVIDO,
            "prioridade": PrioridadeChamado.ALTA,
            "data_abertura": datetime.utcnow() - timedelta(days=5),
            "data_atribuicao": datetime.utcnow() - timedelta(days=4),
            "data_inicio_atendimento": datetime.utcnow() - timedelta(days=3),
            "data_resolucao": datetime.utcnow() - timedelta(days=1),
        },
        
        # Chamado em andamento
        {
            "protocolo": "2025002",
            "titulo": "Lixo acumulado na rua",
            "descricao": "Acúmulo de lixo há mais de uma semana",
            "categoria_id": categorias[4].id if len(categorias) > 4 else 2,
            "bairro_id": bairros[2].id if len(bairros) > 2 else 2,
            "cidadao_id": cidadao.id,
            "operador_id": operador.id,
            "endereco": "Travessa Barão do Triunfo, 234",
            "status": StatusChamado.EM_ANDAMENTO,
            "prioridade": PrioridadeChamado.MEDIA,
            "data_abertura": datetime.utcnow() - timedelta(days=2),
            "data_atribuicao": datetime.utcnow() - timedelta(days=1),
            "data_inicio_atendimento": datetime.utcnow(),
        },
        
        # Chamado aberto
        {
            "protocolo": "2025003",
            "titulo": "Poste de iluminação queimado",
            "descricao": "Poste apagado há 3 dias deixando a rua escura",
            "categoria_id": categorias[1].id if len(categorias) > 1 else 3,
            "bairro_id": bairros[0].id if bairros else 1,
            "cidadao_id": cidadao.id,
            "endereco": "Rua João Diogo, 567",
            "status": StatusChamado.ABERTO,
            "prioridade": PrioridadeChamado.ALTA,
            "data_abertura": datetime.utcnow() - timedelta(hours=12),
        },
    ]
    
    chamados = []
    for data in chamados_data:
        chamado = Chamado(**data)
        db.add(chamado)
        chamados.append(chamado)
    
    db.commit()
    print(f"✓ {len(chamados)} chamados criados")
    return chamados


def popular_avaliacoes(db: Session):
    """Popula avaliações de exemplo"""
    print("\n⭐ Criando avaliações...")
    
    # Buscar chamados resolvidos
    chamado_resolvido = db.query(Chamado).filter_by(status=StatusChamado.RESOLVIDO).first()
    
    if chamado_resolvido:
        avaliacao = Avaliacao(
            chamado_id=chamado_resolvido.id,
            cidadao_id=chamado_resolvido.cidadao_id,
            nota=5,
            comentario="Excelente atendimento! Problema resolvido rapidamente."
        )
        db.add(avaliacao)
        db.commit()
        print("✓ 1 avaliação criada")
    else:
        print("⚠️  Nenhum chamado resolvido para avaliar")


def main():
    """Função principal do seed"""
    print("🌱 Iniciando seed do banco de dados...")
    print("=" * 60)
    
    # Limpar banco (CUIDADO!)
    # limpar_banco()
    
    # Criar tabelas
    criar_tabelas()
    
    # Criar sessão
    db = SessionLocal()
    
    try:
        # Popular dados
        secretarias = popular_secretarias(db)
        categorias = popular_categorias(db)
        bairros = popular_bairros(db)
        usuarios = popular_usuarios(db)
        chamados = popular_chamados(db)
        popular_avaliacoes(db)
        
        print("\n" + "=" * 60)
        print("✅ Seed concluído com sucesso!")
        print("\n" + "=" * 60)
        print("👤 USUÁRIOS CRIADOS:\n")
        print("   Cidadão:        pedro.almeida@email.com / senha123")
        print("   Equipe:         joao.silva@belem.pa.gov.br / senha123")
        print("   SEURB:          carlos.mendes@seurb.belem.pa.gov.br / senha123")
        print("   SESAN:          ana.costa@sesan.belem.pa.gov.br / senha123")
        print("   SEMMA:          roberto.lima@semma.belem.pa.gov.br / senha123")
        print("   Gestor:         maria.santos@belem.pa.gov.br / senha123")
        print("   Admin:          admin@belem.pa.gov.br / senha123")
        print("=" * 60)
        print("\n🏛️  SECRETARIAS CRIADAS:")
        for sec in secretarias[:5]:
            print(f"   {sec.sigla}: {sec.nome}")
        print(f"   ... e mais {len(secretarias) - 5} secretarias")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao popular banco: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
