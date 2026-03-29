"""
Script de Migração do Banco de Dados
De: Sistema sem Secretarias
Para: Sistema com Secretarias Municipais

Execute este script para adicionar as secretarias ao banco existente
"""

import os
import shutil
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import Secretaria, Categoria, Usuario, TipoUsuario
from seed import criar_hash_senha


def fazer_backup():
    """Faz backup do banco de dados atual"""
    print("💾 Fazendo backup do banco de dados...")
    
    if os.path.exists("zeladoria.db"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backups/zeladoria_antes_migr_{timestamp}.db"
        
        # Criar diretório se não existir
        os.makedirs("backups", exist_ok=True)
        
        # Copiar banco
        shutil.copy2("zeladoria.db", backup_name)
        print(f"✅ Backup criado: {backup_name}")
        return backup_name
    else:
        print("⚠️  Banco de dados não encontrado. Criando novo...")
        return None


def criar_secretarias(db: Session):
    """Cria as secretarias municipais"""
    print("\n🏛️  Criando secretarias municipais...")
    
    # Verificar se já existem secretarias
    count = db.query(Secretaria).count()
    if count > 0:
        print(f"⚠️  Já existem {count} secretarias no banco.")
        resposta = input("Deseja recriar? (s/n): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada")
            return []
    
    secretarias_data = [
        # Administração e Gestão
        {"sigla": "SEMAD", "nome": "Secretaria Municipal de Administração", 
         "email": "semad@belem.pa.gov.br", "telefone": "(91) 3242-1100"},
        {"sigla": "SEGEP", "nome": "Secretaria Municipal de Coordenadoria Geral de Planejamento e Gestão", 
         "email": "segep@belem.pa.gov.br", "telefone": "(91) 3242-1200"},
        
        # Finanças
        {"sigla": "SEFIN", "nome": "Secretaria Municipal de Finanças", 
         "email": "sefin@belem.pa.gov.br", "telefone": "(91) 3242-1300"},
        {"sigla": "SECON", "nome": "Secretaria Municipal de Economia", 
         "email": "secon@belem.pa.gov.br", "telefone": "(91) 3242-1400"},
        
        # Infraestrutura
        {"sigla": "SEURB", "nome": "Secretaria Municipal de Urbanismo", 
         "email": "seurb@belem.pa.gov.br", "telefone": "(91) 3242-1500"},
        {"sigla": "SESAN", "nome": "Secretaria Municipal de Saneamento", 
         "email": "sesan@belem.pa.gov.br", "telefone": "(91) 3242-1600"},
        {"sigla": "SEHAB", "nome": "Secretaria Municipal de Habitação", 
         "email": "sehab@belem.pa.gov.br", "telefone": "(91) 3242-1700"},
        
        # Saúde
        {"sigla": "SESMA", "nome": "Secretaria Municipal de Saúde", 
         "email": "sesma@belem.pa.gov.br", "telefone": "(91) 3242-1800"},
        {"sigla": "SEMULHER", "nome": "Secretaria Municipal da Mulher", 
         "email": "semulher@belem.pa.gov.br", "telefone": "(91) 3242-1900"},
        
        # Educação
        {"sigla": "SEMEC", "nome": "Secretaria Municipal de Educação", 
         "email": "semec@belem.pa.gov.br", "telefone": "(91) 3242-2000"},
        
        # Meio Ambiente
        {"sigla": "SEMMA", "nome": "Secretaria Municipal de Meio Ambiente", 
         "email": "semma@belem.pa.gov.br", "telefone": "(91) 3242-2100"},
        
        # Outras
        {"sigla": "SEMAJ", "nome": "Secretaria Municipal de Assuntos Jurídicos", 
         "email": "semaj@belem.pa.gov.br", "telefone": "(91) 3242-2200"},
        {"sigla": "SEJEL", "nome": "Secretaria Municipal de Esporte, Juventude e Lazer", 
         "email": "sejel@belem.pa.gov.br", "telefone": "(91) 3242-2300"},
        
        # Órgãos
        {"sigla": "GMB", "nome": "Guarda Municipal de Belém", 
         "email": "gmb@belem.pa.gov.br", "telefone": "(91) 3242-2400"},
        {"sigla": "OGM", "nome": "Ouvidoria Geral do Município", 
         "email": "ouvidoria@belem.pa.gov.br", "telefone": "(91) 3242-2500"},
    ]
    
    secretarias = []
    for data in secretarias_data:
        secretaria = Secretaria(**data)
        db.add(secretaria)
        secretarias.append(secretaria)
    
    db.commit()
    print(f"✅ {len(secretarias)} secretarias criadas")
    return secretarias


def associar_categorias(db: Session):
    """Associa categorias existentes às secretarias"""
    print("\n🔗 Associando categorias às secretarias...")
    
    # Buscar secretarias
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()
    sesma = db.query(Secretaria).filter_by(sigla="SESMA").first()
    sejel = db.query(Secretaria).filter_by(sigla="SEJEL").first()
    gmb = db.query(Secretaria).filter_by(sigla="GMB").first()
    semec = db.query(Secretaria).filter_by(sigla="SEMEC").first()
    sehab = db.query(Secretaria).filter_by(sigla="SEHAB").first()
    
    # Mapeamento: nome da categoria -> secretaria
    mapeamento = {
        "Buraco na via": seurb,
        "Iluminação pública": seurb,
        "Iluminacao publica": seurb,
        "Calçada danificada": seurb,
        "Calcada danificada": seurb,
        "Sinalização": seurb,
        "Sinalizacao": seurb,
        
        "Lixo acumulado": sesan,
        "Esgoto": sesan,
        "Coleta de lixo": sesan,
        
        "Poda de árvore": semma,
        "Poda de arvore": semma,
        "Área verde": semma,
        "Area verde": semma,
        "Animal abandonado": semma,
        
        "Foco de dengue": sesma,
        
        "Equipamento público": sejel,
        "Equipamento publico": sejel,
        
        "Segurança pública": gmb,
        "Seguranca publica": gmb,
        
        "Infraestrutura escolar": semec,
        
        "Habitação irregular": sehab,
        "Habitacao irregular": sehab,
    }
    
    # Atualizar categorias
    count = 0
    for nome, secretaria in mapeamento.items():
        if secretaria:
            categoria = db.query(Categoria).filter_by(nome=nome).first()
            if categoria:
                categoria.secretaria_id = secretaria.id
                count += 1
    
    db.commit()
    print(f"✅ {count} categorias associadas")


def criar_usuarios_secretarias(db: Session):
    """Cria usuários de exemplo para as secretarias"""
    print("\n👤 Criando usuários das secretarias...")
    
    # Buscar secretarias
    seurb = db.query(Secretaria).filter_by(sigla="SEURB").first()
    sesan = db.query(Secretaria).filter_by(sigla="SESAN").first()
    semma = db.query(Secretaria).filter_by(sigla="SEMMA").first()
    
    usuarios_data = [
        {
            "nome": "Carlos Mendes - SEURB",
            "email": "carlos.mendes@seurb.belem.pa.gov.br",
            "senha_hash": criar_hash_senha("senha123"),
            "cpf": "345.678.901-22",
            "telefone": "(91) 3242-1500",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": seurb.id if seurb else None
        },
        {
            "nome": "Ana Costa - SESAN",
            "email": "ana.costa@sesan.belem.pa.gov.br",
            "senha_hash": criar_hash_senha("senha123"),
            "cpf": "456.789.012-33",
            "telefone": "(91) 3242-1600",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": sesan.id if sesan else None
        },
        {
            "nome": "Roberto Lima - SEMMA",
            "email": "roberto.lima@semma.belem.pa.gov.br",
            "senha_hash": criar_hash_senha("senha123"),
            "cpf": "567.890.123-44",
            "telefone": "(91) 3242-2100",
            "tipo": TipoUsuario.SECRETARIA,
            "secretaria_id": semma.id if semma else None
        },
    ]
    
    count = 0
    for data in usuarios_data:
        # Verificar se já existe
        existe = db.query(Usuario).filter_by(email=data["email"]).first()
        if not existe:
            usuario = Usuario(**data)
            db.add(usuario)
            count += 1
    
    db.commit()
    print(f"✅ {count} usuários de secretarias criados")


def main():
    """Função principal da migração"""
    print("=" * 60)
    print("🔄 MIGRAÇÃO DO BANCO DE DADOS")
    print("Sistema de Zeladoria Urbana - Belém/PA")
    print("Adicionando Secretarias Municipais")
    print("=" * 60)
    print()
    
    # Fazer backup
    backup_file = fazer_backup()
    
    if backup_file:
        print(f"\n⚠️  ATENÇÃO: Backup criado em {backup_file}")
        print("Se algo der errado, você pode restaurar este backup.")
    
    print("\n⚠️  Esta operação irá modificar o banco de dados.")
    resposta = input("Deseja continuar? (s/n): ")
    
    if resposta.lower() != 's':
        print("\n❌ Migração cancelada pelo usuário")
        return
    
    # Criar tabelas se não existirem
    print("\n📦 Verificando estrutura do banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Estrutura verificada")
    
    # Criar sessão
    db = SessionLocal()
    
    try:
        # Executar migração
        secretarias = criar_secretarias(db)
        
        if secretarias:
            associar_categorias(db)
            criar_usuarios_secretarias(db)
        
        print("\n" + "=" * 60)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n👤 NOVOS USUÁRIOS (SECRETARIAS):\n")
        print("   SEURB: carlos.mendes@seurb.belem.pa.gov.br / senha123")
        print("   SESAN: ana.costa@sesan.belem.pa.gov.br / senha123")
        print("   SEMMA: roberto.lima@semma.belem.pa.gov.br / senha123")
        print("\n🏛️  15 secretarias municipais adicionadas")
        print("🔗 Categorias associadas às secretarias")
        print("\n💡 Próximos passos:")
        print("   1. Reinicie o backend: stop.bat && start.bat")
        print("   2. Teste o login com usuários das secretarias")
        print("   3. Verifique o dashboard específico de cada secretaria")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {e}")
        print("\n💡 Para restaurar o backup:")
        if backup_file:
            print(f"   copy {backup_file} zeladoria.db")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
