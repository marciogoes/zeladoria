#!/usr/bin/env python3
"""
Gerenciador do Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA

Script para gerenciar o catálogo de serviços municipais
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.seeds.seed_servicos import seed_servicos


def listar_servicos(secretaria_id=None):
    """Lista serviços do catálogo"""
    db = SessionLocal()
    
    try:
        query = db.query(ServicoSecretaria)
        
        if secretaria_id:
            query = query.filter_by(secretaria_id=secretaria_id)
        
        servicos = query.order_by(ServicoSecretaria.codigo).all()
        
        print(f"\n📋 CATÁLOGO DE SERVIÇOS")
        print("=" * 100)
        print(f"{'Código':<15} {'Nome':<50} {'SLA':<15} {'Prioridade':<15} {'Status'}")
        print("=" * 100)
        
        for s in servicos:
            print(f"{s.codigo:<15} {s.nome[:47]:<50} {s.sla_em_dias:<15} {s.prioridade_label:<15} {s.status.value}")
        
        print("=" * 100)
        print(f"Total: {len(servicos)} serviço(s)")
        
        # Estatísticas
        total_ativos = sum(1 for s in servicos if s.ativo)
        total_gratuitos = sum(1 for s in servicos if s.custo == 0)
        
        print(f"\n📊 Estatísticas:")
        print(f"  • Ativos: {total_ativos}")
        print(f"  • Inativos: {len(servicos) - total_ativos}")
        print(f"  • Gratuitos: {total_gratuitos}")
        print(f"  • Pagos: {len(servicos) - total_gratuitos}")
        
    finally:
        db.close()


def listar_categorias():
    """Lista categorias de serviços"""
    db = SessionLocal()
    
    try:
        from sqlalchemy import func
        
        categorias = db.query(
            ServicoSecretaria.categoria,
            func.count(ServicoSecretaria.id).label("total")
        ).filter(
            ServicoSecretaria.ativo == True
        ).group_by(
            ServicoSecretaria.categoria
        ).order_by(
            func.count(ServicoSecretaria.id).desc()
        ).all()
        
        print(f"\n📁 CATEGORIAS DE SERVIÇOS")
        print("=" * 60)
        print(f"{'Categoria':<40} {'Total':<10}")
        print("=" * 60)
        
        for cat, total in categorias:
            print(f"{cat:<40} {total:<10}")
        
        print("=" * 60)
        print(f"Total de categorias: {len(categorias)}")
        
    finally:
        db.close()


def buscar_servico(termo):
    """Busca serviços por termo"""
    db = SessionLocal()
    
    try:
        from sqlalchemy import or_
        
        busca_filter = f"%{termo}%"
        
        servicos = db.query(ServicoSecretaria).filter(
            or_(
                ServicoSecretaria.codigo.ilike(busca_filter),
                ServicoSecretaria.nome.ilike(busca_filter),
                ServicoSecretaria.descricao.ilike(busca_filter)
            )
        ).all()
        
        print(f"\n🔍 BUSCA: '{termo}'")
        print(f"Encontrado(s): {len(servicos)} serviço(s)")
        print("=" * 100)
        
        for s in servicos:
            print(f"\n{s.codigo} - {s.nome}")
            print(f"  Categoria: {s.categoria}")
            print(f"  SLA: {s.sla_em_dias} | Prioridade: {s.prioridade_label}")
            print(f"  Custo: {s.custo_formatado}")
            if s.descricao:
                print(f"  Descrição: {s.descricao[:100]}...")
        
    finally:
        db.close()


def estatisticas_gerais():
    """Mostra estatísticas gerais do catálogo"""
    db = SessionLocal()
    
    try:
        from sqlalchemy import func
        
        total = db.query(func.count(ServicoSecretaria.id)).scalar()
        ativos = db.query(func.count(ServicoSecretaria.id)).filter_by(ativo=True).scalar()
        
        print(f"\n📊 ESTATÍSTICAS DO CATÁLOGO")
        print("=" * 60)
        print(f"Total de serviços: {total}")
        print(f"Serviços ativos: {ativos}")
        print(f"Serviços inativos: {total - ativos}")
        
        # Por prioridade
        print(f"\n⚡ Por Prioridade:")
        for prioridade in PrioridadeServico:
            count = db.query(func.count(ServicoSecretaria.id))\
                .filter_by(prioridade=prioridade).scalar()
            print(f"  {prioridade.value}: {count}")
        
        # Por status
        print(f"\n📍 Por Status:")
        for status in StatusServico:
            count = db.query(func.count(ServicoSecretaria.id))\
                .filter_by(status=status).scalar()
            print(f"  {status.value}: {count}")
        
        # Custos
        gratuitos = db.query(func.count(ServicoSecretaria.id))\
            .filter_by(custo=0).scalar()
        pagos = total - gratuitos
        
        print(f"\n💰 Custos:")
        print(f"  Gratuitos: {gratuitos}")
        print(f"  Pagos: {pagos}")
        
        # Categorias
        total_categorias = db.query(
            func.count(func.distinct(ServicoSecretaria.categoria))
        ).scalar()
        
        print(f"\n📁 Categorias:")
        print(f"  Total: {total_categorias}")
        
    finally:
        db.close()


def popular_banco():
    """Popula o banco com serviços"""
    print("\n🌱 POPULAR BANCO DE DADOS")
    print("=" * 60)
    print("⚠️  ATENÇÃO: Esta operação vai inserir 100+ serviços no banco")
    print("=" * 60)
    
    confirmacao = input("\nDeseja continuar? (s/N): ")
    
    if confirmacao.lower() != 's':
        print("❌ Operação cancelada")
        return
    
    try:
        seed_servicos()
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")


def menu_principal():
    """Menu principal"""
    while True:
        print("\n" + "=" * 60)
        print("  GERENCIADOR DO CATÁLOGO DE SERVIÇOS")
        print("  Sistema de Zeladoria Urbana - Belém/PA")
        print("=" * 60)
        print("\n1. Listar todos os serviços")
        print("2. Listar categorias")
        print("3. Buscar serviço")
        print("4. Estatísticas gerais")
        print("5. Popular banco de dados")
        print("0. Sair")
        print()
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            listar_servicos()
        elif opcao == "2":
            listar_categorias()
        elif opcao == "3":
            termo = input("Digite o termo de busca: ")
            buscar_servico(termo)
        elif opcao == "4":
            estatisticas_gerais()
        elif opcao == "5":
            popular_banco()
        elif opcao == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == "seed":
            seed_servicos()
        elif comando == "listar":
            listar_servicos()
        elif comando == "categorias":
            listar_categorias()
        elif comando == "stats":
            estatisticas_gerais()
        elif comando == "buscar":
            if len(sys.argv) > 2:
                buscar_servico(sys.argv[2])
            else:
                print("❌ Informe o termo de busca")
        else:
            print(f"❌ Comando '{comando}' não reconhecido")
            print("\nComandos disponíveis:")
            print("  python manage_catalogo.py seed          - Popular banco")
            print("  python manage_catalogo.py listar        - Listar serviços")
            print("  python manage_catalogo.py categorias    - Listar categorias")
            print("  python manage_catalogo.py stats         - Estatísticas")
            print("  python manage_catalogo.py buscar TERMO  - Buscar serviços")
    else:
        menu_principal()
