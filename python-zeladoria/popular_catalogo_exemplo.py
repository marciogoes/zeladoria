"""
POPULAR CATÁLOGO DE SERVIÇOS COM DADOS DE EXEMPLO
Sistema de Zeladoria Urbana - Belém/PA
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.models_secretarias import Secretaria
from app.database.database import Base
import random

def criar_tabelas():
    """Cria tabelas se não existirem"""
    print("📊 Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas!")

def verificar_secretarias(db: Session):
    """Verifica se existem secretarias, se não, cria algumas"""
    count = db.query(Secretaria).count()
    
    if count == 0:
        print("\n⚠️ Nenhuma secretaria encontrada. Criando secretarias padrão...")
        
        secretarias = [
            {
                "sigla": "SEURB",
                "nome": "Secretaria Municipal de Urbanismo",
                "tipo": "infraestrutura",
                "email": "seurb@belem.pa.gov.br",
                "telefone": "(91) 3184-1000"
            },
            {
                "sigla": "SESAN",
                "nome": "Secretaria Municipal de Saneamento",
                "tipo": "infraestrutura",
                "email": "sesan@belem.pa.gov.br",
                "telefone": "(91) 3184-2000"
            },
            {
                "sigla": "SEMOB",
                "nome": "Secretaria Municipal de Mobilidade",
                "tipo": "infraestrutura",
                "email": "semob@belem.pa.gov.br",
                "telefone": "(91) 3184-3000"
            }
        ]
        
        for sec_data in secretarias:
            sec = Secretaria(**sec_data)
            db.add(sec)
        
        db.commit()
        print(f"✅ {len(secretarias)} secretarias criadas!")
    else:
        print(f"✅ Encontradas {count} secretaria(s)")
    
    return db.query(Secretaria).all()

def popular_servicos(db: Session):
    """Popula banco com serviços de exemplo"""
    
    # Verificar se já existem serviços
    count = db.query(ServicoSecretaria).count()
    if count > 0:
        print(f"\n⚠️ Já existem {count} serviços no banco.")
        resposta = input("Deseja adicionar mais serviços? (s/n): ")
        if resposta.lower() != 's':
            return
    
    secretarias = verificar_secretarias(db)
    
    if not secretarias:
        print("❌ Nenhuma secretaria disponível para vincular serviços!")
        return
    
    print(f"\n📋 Populando catálogo de serviços...")
    
    # SEURB - Urbanismo
    servicos_seurb = [
        {
            "codigo": "SEURB-001",
            "nome": "Reparo de Iluminação Pública",
            "descricao": "Reparo de postes, lâmpadas e outros componentes de iluminação pública",
            "categoria": "Iluminação",
            "subcategoria": "Manutenção",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "custo": 0.0,
            "documentos_necessarios": "Localização precisa do problema",
            "requisitos": "Descrever qual tipo de defeito (lâmpada queimada, fiação, poste danificado)",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-002",
            "nome": "Tapa-buraco em Via Pública",
            "descricao": "Reparo de buracos em ruas, avenidas e calçadas",
            "categoria": "Pavimentação",
            "subcategoria": "Manutenção",
            "sla_horas": 96,
            "prioridade": PrioridadeServico.MEDIA,
            "custo": 0.0,
            "documentos_necessarios": "Localização e foto do buraco",
            "requisitos": "Informar dimensões aproximadas e profundidade",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-003",
            "nome": "Poda de Árvore em Via Pública",
            "descricao": "Poda de árvores que estejam obstruindo vias ou oferecendo risco",
            "categoria": "Arborização",
            "subcategoria": "Manutenção",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "custo": 0.0,
            "documentos_necessarios": "Localização da árvore",
            "requisitos": "Informar se há risco iminente",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-004",
            "nome": "Remoção de Árvore em Risco",
            "descricao": "Remoção emergencial de árvores com risco de queda",
            "categoria": "Arborização",
            "subcategoria": "Emergência",
            "sla_horas": 8,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "custo": 0.0,
            "documentos_necessarios": "Localização precisa e fotos",
            "requisitos": "Laudo técnico ou avaliação de risco",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-005",
            "nome": "Reparo de Calçada",
            "descricao": "Reparo de calçadas danificadas ou irregulares",
            "categoria": "Pavimentação",
            "subcategoria": "Manutenção",
            "sla_horas": 120,
            "prioridade": PrioridadeServico.BAIXA,
            "custo": 0.0,
            "documentos_necessarios": "Localização e fotos",
            "requisitos": "Área de calçada a ser reparada",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": False,
        },
    ]
    
    # SESAN - Saneamento
    servicos_sesan = [
        {
            "codigo": "SESAN-001",
            "nome": "Desobstrução de Bueiro",
            "descricao": "Limpeza e desobstrução de bueiros e bocas de lobo",
            "categoria": "Drenagem",
            "subcategoria": "Manutenção",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "custo": 0.0,
            "documentos_necessarios": "Localização do bueiro",
            "requisitos": "Informar se há alagamento",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SESAN-002",
            "nome": "Coleta de Lixo Especial",
            "descricao": "Coleta de móveis velhos, entulho e objetos grandes",
            "categoria": "Limpeza",
            "subcategoria": "Coleta",
            "sla_horas": 168,
            "prioridade": PrioridadeServico.AGENDAVEL,
            "custo": 0.0,
            "documentos_necessarios": "Endereço completo",
            "requisitos": "Agendar com 72h de antecedência",
            "atendimento_presencial": False,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SESAN-003",
            "nome": "Limpeza de Via Pública",
            "descricao": "Limpeza de ruas, praças e espaços públicos",
            "categoria": "Limpeza",
            "subcategoria": "Manutenção",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "custo": 0.0,
            "documentos_necessarios": "Localização",
            "requisitos": "Descrever tipo de sujeira ou lixo",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SESAN-004",
            "nome": "Vazamento de Água em Via",
            "descricao": "Reparo de vazamentos em tubulações de água",
            "categoria": "Água",
            "subcategoria": "Emergência",
            "sla_horas": 12,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "custo": 0.0,
            "documentos_necessarios": "Localização precisa",
            "requisitos": "Informar se é vazamento grande ou pequeno",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
    ]
    
    # SEMOB - Mobilidade
    servicos_semob = [
        {
            "codigo": "SEMOB-001",
            "nome": "Instalação de Sinalização",
            "descricao": "Instalação de placas, faixas de pedestre e outros sinais de trânsito",
            "categoria": "Sinalização",
            "subcategoria": "Implantação",
            "sla_horas": 240,
            "prioridade": PrioridadeServico.BAIXA,
            "custo": 0.0,
            "documentos_necessarios": "Localização e justificativa",
            "requisitos": "Aprovação técnica necessária",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": False,
        },
        {
            "codigo": "SEMOB-002",
            "nome": "Reparo de Semáforo",
            "descricao": "Manutenção e reparo de semáforos",
            "categoria": "Sinalização",
            "subcategoria": "Manutenção",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.ALTA,
            "custo": 0.0,
            "documentos_necessarios": "Localização do semáforo",
            "requisitos": "Informar o tipo de problema",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEMOB-003",
            "nome": "Pintura de Faixa de Pedestre",
            "descricao": "Pintura ou repintura de faixas de pedestre",
            "categoria": "Sinalização",
            "subcategoria": "Manutenção",
            "sla_horas": 120,
            "prioridade": PrioridadeServico.MEDIA,
            "custo": 0.0,
            "documentos_necessarios": "Localização",
            "requisitos": "Faixa deve estar apagada ou danificada",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": False,
        },
    ]
    
    # Vincular serviços às secretarias
    servicos_por_secretaria = {
        "SEURB": servicos_seurb,
        "SESAN": servicos_sesan,
        "SEMOB": servicos_semob,
    }
    
    total_adicionados = 0
    
    for secretaria in secretarias:
        if secretaria.sigla in servicos_por_secretaria:
            servicos = servicos_por_secretaria[secretaria.sigla]
            
            for serv_data in servicos:
                # Adicionar dados calculados
                serv_data['secretaria_id'] = secretaria.id
                serv_data['sla_dias'] = serv_data['sla_horas'] / 24
                serv_data['status'] = StatusServico.ATIVO
                serv_data['ativo'] = True
                
                # Dados aleatórios de estatística (para exemplo)
                serv_data['total_solicitacoes'] = random.randint(0, 100)
                serv_data['taxa_cumprimento_sla'] = random.uniform(75, 98)
                serv_data['avaliacao_media'] = random.uniform(3.5, 5.0)
                serv_data['tempo_medio_atendimento'] = random.randint(
                    int(serv_data['sla_horas'] * 0.5),
                    int(serv_data['sla_horas'] * 0.9)
                )
                
                servico = ServicoSecretaria(**serv_data)
                db.add(servico)
                total_adicionados += 1
            
            print(f"✅ {len(servicos)} serviços adicionados para {secretaria.sigla}")
    
    db.commit()
    print(f"\n🎉 Total de {total_adicionados} serviços adicionados ao catálogo!")

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║   📋 POPULAR CATÁLOGO DE SERVIÇOS                      ║")
    print("║   Sistema de Zeladoria Urbana - Belém/PA              ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    try:
        criar_tabelas()
        
        db = SessionLocal()
        
        try:
            popular_servicos(db)
            
            # Mostrar resumo
            print("\n" + "="*60)
            print("📊 RESUMO DO CATÁLOGO")
            print("="*60)
            
            total = db.query(ServicoSecretaria).count()
            ativos = db.query(ServicoSecretaria).filter(ServicoSecretaria.ativo == True).count()
            
            print(f"\nTotal de serviços: {total}")
            print(f"Serviços ativos: {ativos}")
            
            # Contar por secretaria
            print("\n📁 Por Secretaria:")
            secretarias = db.query(Secretaria).all()
            for sec in secretarias:
                count = db.query(ServicoSecretaria).filter(
                    ServicoSecretaria.secretaria_id == sec.id
                ).count()
                if count > 0:
                    print(f"   • {sec.sigla}: {count} serviço(s)")
            
            # Contar por prioridade
            print("\n🔴 Por Prioridade:")
            for prioridade in PrioridadeServico:
                count = db.query(ServicoSecretaria).filter(
                    ServicoSecretaria.prioridade == prioridade
                ).count()
                if count > 0:
                    print(f"   • {prioridade.value}: {count} serviço(s)")
            
            print("\n✅ Catálogo populado com sucesso!")
            print("\n💡 Próximos passos:")
            print("   1. Inicie o backend: INICIAR_BACKEND.bat")
            print("   2. Inicie o frontend: INICIAR_FRONTEND.bat")
            print("   3. Acesse: http://localhost:5173")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()
