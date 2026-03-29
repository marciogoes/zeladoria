"""
🎯 SCRIPT DE POPULAÇÃO DO BANCO DE DADOS - VERSÃO PARA APRESENTAÇÃO
Sistema de Zeladoria Urbana - Belém/PA

Este script popula o banco de dados com MUITOS dados realistas para apresentação.
"""

from datetime import datetime, timedelta
import random
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    Usuario, TipoUsuario, Secretaria, Categoria, Bairro,
    Chamado, StatusChamado, PrioridadeChamado, Comentario, Avaliacao
)

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_hash_senha(senha: str) -> str:
    """Cria hash da senha"""
    return pwd_context.hash(senha)

# ========================================
# DADOS PARA POPULAR
# ========================================

USUARIOS_DEMO = [
    # Cidadãos
    {"nome": "Maria Silva Santos", "email": "maria.silva@email.com", "telefone": "(91) 98765-4321", "tipo": TipoUsuario.CIDADAO, "cpf": "111.111.111-11"},
    {"nome": "João Pereira Costa", "email": "joao.pereira@email.com", "telefone": "(91) 98765-1234", "tipo": TipoUsuario.CIDADAO, "cpf": "222.222.222-22"},
    {"nome": "Ana Paula Souza", "email": "ana.souza@email.com", "telefone": "(91) 98765-5678", "tipo": TipoUsuario.CIDADAO, "cpf": "333.333.333-33"},
    {"nome": "Carlos Eduardo Lima", "email": "carlos.lima@email.com", "telefone": "(91) 98765-8765", "tipo": TipoUsuario.CIDADAO, "cpf": "444.444.444-44"},
    {"nome": "Fernanda Oliveira", "email": "fernanda.oliveira@email.com", "telefone": "(91) 98765-4567", "tipo": TipoUsuario.CIDADAO, "cpf": "555.555.555-55"},
    {"nome": "Roberto Almeida", "email": "roberto.almeida@email.com", "telefone": "(91) 98765-9876", "tipo": TipoUsuario.CIDADAO, "cpf": "666.666.666-66"},
    {"nome": "Juliana Martins", "email": "juliana.martins@email.com", "telefone": "(91) 98765-3456", "tipo": TipoUsuario.CIDADAO, "cpf": "777.777.777-77"},
    # Equipes
    {"nome": "Pedro Santos (Equipe SEURB)", "email": "pedro.santos@seurb.belem.pa.gov.br", "telefone": "(91) 3344-5566", "tipo": TipoUsuario.EQUIPE, "cpf": "888.888.888-88"},
    {"nome": "Juliana Costa (Equipe SESAN)", "email": "juliana.costa@sesan.belem.pa.gov.br", "telefone": "(91) 3344-5577", "tipo": TipoUsuario.EQUIPE, "cpf": "999.999.999-99"},
    {"nome": "Roberto Alves (Equipe SEMMA)", "email": "roberto.alves@semma.belem.pa.gov.br", "telefone": "(91) 3344-5588", "tipo": TipoUsuario.EQUIPE, "cpf": "101.010.101-01"},
]

TITULOS_CHAMADOS = [
    "Buraco na pista da Av. Almirante Barroso",
    "Semáforo com defeito na Av. Nazaré",
    "Lixo acumulado na Rua dos Mundurucus",
    "Iluminação pública queimada",
    "Árvore caída bloqueando via",
    "Calçada quebrada em frente à escola",
    "Vazamento de água na rua",
    "Poda de árvore necessária",
    "Entulho abandonado em terreno",
    "Falta de sinalização em cruzamento",
    "Bueiro entupido causando alagamento",
    "Poste com risco de queda",
    "Esgoto a céu aberto",
    "Praça com equipamentos danificados",
    "Falta de coleta de lixo há 3 dias",
    "Ponto de ônibus destruído",
    "Mato alto em área pública",
    "Calçada irregular causa acidentes",
    "Faixa de pedestre apagada",
    "Parque infantil com brinquedos quebrados"
]

DESCRICOES_MODELO = [
    "Há um grande buraco na pista que está causando risco para motoristas e pedestres. Precisa de reparo urgente.",
    "O equipamento não está funcionando, causando transtornos no trânsito e risco de acidentes.",
    "Grande acúmulo de lixo está causando mau cheiro e atraindo animais. Situação insalubre.",
    "A iluminação está completamente apagada, deixando a área escura e insegura à noite.",
    "Árvore de grande porte caiu e está impedindo o trânsito de veículos e pedestres.",
    "A calçada está muito danificada, com risco de quedas, especialmente para idosos.",
    "Vazamento significativo está desperdiçando água e alagando a via pública.",
    "Árvore com galhos muito baixos está prejudicando a passagem e a visibilidade.",
    "Material de construção abandonado representa risco e atrai descarte irregular.",
    "Cruzamento perigoso sem nenhuma sinalização adequada para motoristas e pedestres."
]

COMENTARIOS_MODELO = [
    "Equipe técnica realizou vistoria no local. Problema confirmado.",
    "Solicitação de orçamento enviada ao setor responsável.",
    "Material necessário já foi requisitado ao almoxarifado.",
    "Serviço programado para execução na próxima semana.",
    "Equipe iniciou os trabalhos no local.",
    "Problema parcialmente resolvido. Aguardando conclusão.",
    "Serviço concluído com sucesso. Área normalizada.",
    "Moradores da região agradecem pela rapidez no atendimento.",
    "Situação monitorada para garantir que não haja reincidência.",
    "Documentação fotográfica do serviço anexada ao processo."
]

def criar_usuarios(db: Session):
    """Cria usuários de demonstração"""
    print("\n👥 Criando usuários...")
    
    usuarios_criados = []
    
    for user_data in USUARIOS_DEMO:
        # Verificar se já existe
        usuario_existe = db.query(Usuario).filter_by(email=user_data["email"]).first()
        
        if not usuario_existe:
            senha_hash = criar_hash_senha("demo123")
            usuario = Usuario(
                nome=user_data["nome"],
                email=user_data["email"],
                telefone=user_data["telefone"],
                senha_hash=senha_hash,
                cpf=user_data["cpf"],
                tipo=user_data["tipo"],
                ativo=True
            )
            db.add(usuario)
            usuarios_criados.append(usuario)
    
    db.commit()
    print(f"   ✅ {len(usuarios_criados)} usuários criados!")
    return usuarios_criados

def criar_chamados_realistas(db: Session):
    """Cria chamados com dados realistas"""
    print("\n📞 Criando chamados...")
    
    # Buscar entidades necessárias
    usuarios = db.query(Usuario).filter_by(tipo=TipoUsuario.CIDADAO).all()
    categorias = db.query(Categoria).all()
    bairros = db.query(Bairro).all()
    equipes = db.query(Usuario).filter_by(tipo=TipoUsuario.EQUIPE).all()
    
    if not usuarios or not categorias or not bairros:
        print("   ⚠️  Faltam dados base. Execute primeiro o seed.py")
        return []
    
    chamados_criados = []
    
    # Criar 50 chamados variados
    for i in range(50):
        # Data aleatória nos últimos 90 dias
        dias_atras = random.randint(0, 90)
        data_abertura = datetime.utcnow() - timedelta(days=dias_atras)
        
        # Coordenadas próximas a Belém
        lat_base = -1.4558
        lng_base = -48.4902
        latitude = lat_base + random.uniform(-0.1, 0.1)
        longitude = lng_base + random.uniform(-0.1, 0.1)
        
        # Selecionar dados aleatórios
        usuario = random.choice(usuarios)
        categoria = random.choice(categorias)
        bairro = random.choice(bairros)
        titulo = random.choice(TITULOS_CHAMADOS)
        descricao = random.choice(DESCRICOES_MODELO)
        
        # Status distribuído realisticamente
        status_weights = [(StatusChamado.ABERTO, 0.15), (StatusChamado.EM_ANDAMENTO, 0.35), 
                         (StatusChamado.RESOLVIDO, 0.45), (StatusChamado.CANCELADO, 0.05)]
        status = random.choices([s[0] for s in status_weights], weights=[s[1] for s in status_weights])[0]
        
        # Prioridade distribuída
        prioridade_weights = [(PrioridadeChamado.BAIXA, 0.30), (PrioridadeChamado.MEDIA, 0.45),
                             (PrioridadeChamado.ALTA, 0.20), (PrioridadeChamado.CRITICA, 0.05)]
        prioridade = random.choices([p[0] for p in prioridade_weights], weights=[p[1] for p in prioridade_weights])[0]
        
        # Criar protocolo único
        protocolo = f"BEL{data_abertura.year}{data_abertura.month:02d}{random.randint(1000, 9999)}"
        
        chamado_data = {
            "protocolo": protocolo,
            "titulo": titulo,
            "descricao": descricao,
            "latitude": latitude,
            "longitude": longitude,
            "endereco": f"Rua {random.choice(['A', 'B', 'C', 'Principal', 'Central'])}, {bairro.nome}, Belém-PA",
            "status": status,
            "prioridade": prioridade,
            "cidadao_id": usuario.id,
            "categoria_id": categoria.id,
            "bairro_id": bairro.id,
            "data_abertura": data_abertura
        }
        
        # Se atribuído, definir equipe e datas
        if status in [StatusChamado.EM_ANDAMENTO, StatusChamado.RESOLVIDO] and equipes:
            chamado_data["operador_id"] = random.choice(equipes).id
            chamado_data["data_atribuicao"] = data_abertura + timedelta(days=random.randint(1, 3))
            chamado_data["data_inicio_atendimento"] = chamado_data["data_atribuicao"] + timedelta(hours=random.randint(2, 24))
        
        # Se resolvido, adicionar data de resolução
        if status == StatusChamado.RESOLVIDO:
            dias_resolucao = random.randint(1, 30)
            chamado_data["data_resolucao"] = data_abertura + timedelta(days=dias_resolucao)
        
        chamado = Chamado(**chamado_data)
        db.add(chamado)
        chamados_criados.append(chamado)
    
    db.commit()
    print(f"   ✅ {len(chamados_criados)} chamados criados!")
    return chamados_criados

def criar_comentarios(db: Session, chamados):
    """Cria comentários em vários chamados"""
    print("\n💬 Criando comentários...")
    
    equipes = db.query(Usuario).filter(Usuario.tipo.in_([TipoUsuario.EQUIPE, TipoUsuario.GESTOR, TipoUsuario.ADMIN])).all()
    
    if not equipes:
        print("   ⚠️  Nenhuma equipe encontrada.")
        return
    
    comentarios_criados = 0
    
    # Adicionar comentários em 60% dos chamados
    chamados_com_comentarios = random.sample(chamados, min(int(len(chamados) * 0.6), len(chamados)))
    
    for chamado in chamados_com_comentarios:
        # Cada chamado recebe de 1 a 5 comentários
        num_comentarios = random.randint(1, 5)
        
        for i in range(num_comentarios):
            dias_depois = random.randint(1, 15)
            data_comentario = chamado.data_abertura + timedelta(days=dias_depois)
            
            comentario = Comentario(
                chamado_id=chamado.id,
                usuario_id=random.choice(equipes).id,
                comentario=random.choice(COMENTARIOS_MODELO),
                tipo=random.choice(['atualizacao', 'observacao', 'resolucao']),
                visivel_cidadao=random.choice([True, True, False]),  # 66% visível
                data_criacao=data_comentario
            )
            db.add(comentario)
            comentarios_criados += 1
    
    db.commit()
    print(f"   ✅ {comentarios_criados} comentários criados!")

def criar_avaliacoes(db: Session, chamados):
    """Cria avaliações para chamados resolvidos"""
    print("\n⭐ Criando avaliações...")
    
    chamados_resolvidos = [c for c in chamados if c.status == StatusChamado.RESOLVIDO]
    
    avaliacoes_criadas = 0
    
    # 70% dos chamados resolvidos têm avaliação
    chamados_avaliar = random.sample(
        chamados_resolvidos, 
        min(int(len(chamados_resolvidos) * 0.7), len(chamados_resolvidos))
    )
    
    comentarios_avaliacao = [
        "Serviço muito bem executado! Parabéns à equipe.",
        "Atendimento rápido e eficiente.",
        "Resolveram o problema rapidamente.",
        "Ótimo trabalho da equipe!",
        "Muito satisfeito com o resultado.",
        "Problema totalmente resolvido.",
        "Equipe educada e profissional.",
        "Demorou um pouco mas foi bem feito.",
        "Atendimento adequado às expectativas.",
        "Excelente! Muito obrigado!"
    ]
    
    for chamado in chamados_avaliar:
        # Nota distribuída realisticamente (tendência positiva)
        nota_weights = [(1, 0.05), (2, 0.05), (3, 0.15), (4, 0.35), (5, 0.40)]
        nota = random.choices([n[0] for n in nota_weights], weights=[n[1] for n in nota_weights])[0]
        
        # 80% das avaliações têm comentário
        comentario = random.choice(comentarios_avaliacao) if random.random() < 0.8 else None
        
        avaliacao = Avaliacao(
            chamado_id=chamado.id,
            cidadao_id=chamado.cidadao_id,
            nota=nota,
            comentario=comentario,
            data_avaliacao=chamado.data_resolucao + timedelta(days=random.randint(1, 7))
        )
        db.add(avaliacao)
        avaliacoes_criadas += 1
    
    db.commit()
    print(f"   ✅ {avaliacoes_criadas} avaliações criadas!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🎯 POPULAÇÃO DO BANCO DE DADOS")
    print("Sistema de Zeladoria Urbana - Belém/PA")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. Criar usuários
        usuarios = criar_usuarios(db)
        
        # 2. Criar chamados
        chamados = criar_chamados_realistas(db)
        
        # 3. Criar comentários
        criar_comentarios(db, chamados)
        
        # 4. Criar avaliações
        criar_avaliacoes(db, chamados)
        
        print("\n" + "=" * 60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("=" * 60)
        print("\n📊 RESUMO:")
        print(f"   • Usuários criados: {len(usuarios)}")
        print(f"   • Chamados criados: {len(chamados)}")
        print("\n💡 Dados prontos para apresentação!")
        print("\n🚀 Você pode fazer login com:")
        print("   📧 maria.silva@email.com / demo123 (Cidadão)")
        print("   📧 pedro.santos@seurb.belem.pa.gov.br / demo123 (Equipe)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
