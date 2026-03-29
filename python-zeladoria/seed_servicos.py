"""
Seed de Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA

Popular banco com catálogo completo de serviços de cada secretaria
com SLA (Service Level Agreement) definido
"""

from app.database.database import SessionLocal, engine, Base
from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.models_secretarias import Secretaria

# Criar tabelas
Base.metadata.create_all(bind=engine)

def seed_servicos():
    """Popular banco com catálogo de serviços das secretarias"""
    
    db = SessionLocal()
    
    try:
        print("📋 Criando Catálogo de Serviços...")
        print("="*70)
        
        # Buscar secretarias
        secretarias = {sec.sigla: sec for sec in db.query(Secretaria).all()}
        
        if not secretarias:
            print("❌ Erro: Execute seed_secretarias.py primeiro!")
            return False
        
        servicos_count = 0
        
        # ==========================================
        # SEURB - SECRETARIA DE URBANISMO
        # ==========================================
        if "SEURB" in secretarias:
            print("\n🏗️  SEURB - Urbanismo")
            seurb_servicos = [
                {
                    "codigo": "SEURB-001",
                    "nome": "Reparo de Iluminação Pública",
                    "descricao": "Conserto ou troca de lâmpadas, luminárias e postes de iluminação",
                    "categoria": "Iluminação",
                    "subcategoria": "Reparo",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                    "documentos_necessarios": "Endereço do local, referências",
                    "requisitos": "Informar localização exata do problema",
                },
                {
                    "codigo": "SEURB-002",
                    "nome": "Tapa-Buraco em Via Pública",
                    "descricao": "Fechamento de buracos e crateras em ruas e avenidas",
                    "categoria": "Pavimentação",
                    "subcategoria": "Tapa-Buraco",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.ALTA,
                    "tempo_medio_atendimento": 36,
                },
                {
                    "codigo": "SEURB-003",
                    "nome": "Recapeamento de Via",
                    "descricao": "Recapeamento completo de ruas e avenidas",
                    "categoria": "Pavimentação",
                    "subcategoria": "Recapeamento",
                    "sla_horas": 720,  # 30 dias
                    "prioridade": PrioridadeServico.AGENDAVEL,
                },
                {
                    "codigo": "SEURB-004",
                    "nome": "Reparo de Calçada",
                    "descricao": "Conserto de calçadas danificadas",
                    "categoria": "Calçadas",
                    "subcategoria": "Reparo",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEURB-005",
                    "nome": "Instalação de Sinalização",
                    "descricao": "Instalação de placas, faixas e sinalizações de trânsito",
                    "categoria": "Sinalização",
                    "subcategoria": "Instalação",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEURB-006",
                    "nome": "Reparo de Sinalização Danificada",
                    "descricao": "Conserto ou substituição de sinalizações danificadas",
                    "categoria": "Sinalização",
                    "subcategoria": "Reparo",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEURB-007",
                    "nome": "Pintura de Faixa de Pedestre",
                    "descricao": "Pintura ou repintura de faixas de pedestres",
                    "categoria": "Sinalização",
                    "subcategoria": "Pintura",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEURB-008",
                    "nome": "Instalação de Lombada",
                    "descricao": "Instalação de lombadas eletrônicas ou físicas",
                    "categoria": "Sinalização",
                    "subcategoria": "Lombada",
                    "sla_horas": 168,  # 7 dias
                    "prioridade": PrioridadeServico.AGENDAVEL,
                },
                {
                    "codigo": "SEURB-009",
                    "nome": "Limpeza de Via Pública",
                    "descricao": "Limpeza de ruas após obras ou eventos",
                    "categoria": "Limpeza",
                    "subcategoria": "Via Pública",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEURB-010",
                    "nome": "Fiscalização de Obra Irregular",
                    "descricao": "Vistoria e fiscalização de construções irregulares",
                    "categoria": "Fiscalização",
                    "subcategoria": "Obra",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
            ]
            
            for servico in seurb_servicos:
                servico["secretaria_id"] = secretarias["SEURB"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(seurb_servicos)} serviços cadastrados")
        
        # ==========================================
        # SESAN - SECRETARIA DE SANEAMENTO
        # ==========================================
        if "SESAN" in secretarias:
            print("\n💧 SESAN - Saneamento")
            sesan_servicos = [
                {
                    "codigo": "SESAN-001",
                    "nome": "Desobstrução de Esgoto",
                    "descricao": "Desentupimento de redes de esgoto",
                    "categoria": "Esgoto",
                    "subcategoria": "Desobstrução",
                    "sla_horas": 12,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                    "tempo_medio_atendimento": 8,
                },
                {
                    "codigo": "SESAN-002",
                    "nome": "Reparo de Vazamento de Água",
                    "descricao": "Conserto de vazamentos na rede pública",
                    "categoria": "Água",
                    "subcategoria": "Vazamento",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                    "tempo_medio_atendimento": 18,
                },
                {
                    "codigo": "SESAN-003",
                    "nome": "Limpeza de Bueiro",
                    "descricao": "Limpeza e desobstrução de bueiros",
                    "categoria": "Drenagem",
                    "subcategoria": "Bueiro",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SESAN-004",
                    "nome": "Atendimento a Alagamento",
                    "descricao": "Ação emergencial em casos de alagamento",
                    "categoria": "Drenagem",
                    "subcategoria": "Alagamento",
                    "sla_horas": 6,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                },
                {
                    "codigo": "SESAN-005",
                    "nome": "Instalação de Ligação de Água",
                    "descricao": "Nova ligação de água para imóvel",
                    "categoria": "Água",
                    "subcategoria": "Instalação",
                    "sla_horas": 240,  # 10 dias
                    "prioridade": PrioridadeServico.AGENDAVEL,
                    "custo": 150.00,
                },
                {
                    "codigo": "SESAN-006",
                    "nome": "Instalação de Ligação de Esgoto",
                    "descricao": "Nova ligação de esgoto para imóvel",
                    "categoria": "Esgoto",
                    "subcategoria": "Instalação",
                    "sla_horas": 240,
                    "prioridade": PrioridadeServico.AGENDAVEL,
                    "custo": 200.00,
                },
                {
                    "codigo": "SESAN-007",
                    "nome": "Limpeza de Fossa",
                    "descricao": "Limpeza de fossas sépticas",
                    "categoria": "Esgoto",
                    "subcategoria": "Fossa",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                    "custo": 300.00,
                },
                {
                    "codigo": "SESAN-008",
                    "nome": "Reparo de Tampa de Bueiro",
                    "descricao": "Troca ou reparo de tampas de bueiro danificadas",
                    "categoria": "Drenagem",
                    "subcategoria": "Bueiro",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
            ]
            
            for servico in sesan_servicos:
                servico["secretaria_id"] = secretarias["SESAN"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(sesan_servicos)} serviços cadastrados")
        
        # ==========================================
        # SEMMA - SECRETARIA DE MEIO AMBIENTE
        # ==========================================
        if "SEMMA" in secretarias:
            print("\n🌳 SEMMA - Meio Ambiente")
            semma_servicos = [
                {
                    "codigo": "SEMMA-001",
                    "nome": "Coleta de Lixo Não Realizada",
                    "descricao": "Atendimento a locais onde coleta não foi realizada",
                    "categoria": "Coleta",
                    "subcategoria": "Lixo Residencial",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEMMA-002",
                    "nome": "Poda de Árvore",
                    "descricao": "Poda de árvores em áreas públicas",
                    "categoria": "Arborização",
                    "subcategoria": "Poda",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEMMA-003",
                    "nome": "Remoção de Árvore Caída",
                    "descricao": "Remoção emergencial de árvores caídas",
                    "categoria": "Arborização",
                    "subcategoria": "Remoção",
                    "sla_horas": 12,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                },
                {
                    "codigo": "SEMMA-004",
                    "nome": "Remoção de Entulho",
                    "descricao": "Recolhimento de entulho e materiais de construção",
                    "categoria": "Coleta",
                    "subcategoria": "Entulho",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEMMA-005",
                    "nome": "Limpeza de Lixo Acumulado",
                    "descricao": "Limpeza de pontos de acúmulo irregular de lixo",
                    "categoria": "Limpeza",
                    "subcategoria": "Lixo",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEMMA-006",
                    "nome": "Combate a Foco de Dengue",
                    "descricao": "Ação de combate a focos de dengue",
                    "categoria": "Saúde Ambiental",
                    "subcategoria": "Dengue",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                },
                {
                    "codigo": "SEMMA-007",
                    "nome": "Capina de Terreno",
                    "descricao": "Capina e limpeza de terrenos públicos",
                    "categoria": "Limpeza",
                    "subcategoria": "Capina",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.BAIXA,
                },
                {
                    "codigo": "SEMMA-008",
                    "nome": "Plantio de Árvore",
                    "descricao": "Plantio de mudas em áreas públicas",
                    "categoria": "Arborização",
                    "subcategoria": "Plantio",
                    "sla_horas": 240,
                    "prioridade": PrioridadeServico.AGENDAVEL,
                },
                {
                    "codigo": "SEMMA-009",
                    "nome": "Fiscalização Ambiental",
                    "descricao": "Vistoria de denúncias ambientais",
                    "categoria": "Fiscalização",
                    "subcategoria": "Ambiental",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEMMA-010",
                    "nome": "Licenciamento Ambiental",
                    "descricao": "Emissão de licenças ambientais",
                    "categoria": "Licenciamento",
                    "subcategoria": "Ambiental",
                    "sla_horas": 720,  # 30 dias
                    "prioridade": PrioridadeServico.AGENDAVEL,
                    "custo": 500.00,
                },
            ]
            
            for servico in semma_servicos:
                servico["secretaria_id"] = secretarias["SEMMA"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(semma_servicos)} serviços cadastrados")
        
        # ==========================================
        # SESMA - SECRETARIA DE SAÚDE
        # ==========================================
        if "SESMA" in secretarias:
            print("\n🏥 SESMA - Saúde")
            sesma_servicos = [
                {
                    "codigo": "SESMA-001",
                    "nome": "Marcação de Consulta",
                    "descricao": "Agendamento de consulta médica em postos de saúde",
                    "categoria": "Atendimento",
                    "subcategoria": "Consulta",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SESMA-002",
                    "nome": "Vacinação",
                    "descricao": "Aplicação de vacinas do calendário nacional",
                    "categoria": "Prevenção",
                    "subcategoria": "Vacina",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SESMA-003",
                    "nome": "Atendimento de Urgência",
                    "descricao": "Atendimento de urgência e emergência",
                    "categoria": "Atendimento",
                    "subcategoria": "Urgência",
                    "sla_horas": 1,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                },
                {
                    "codigo": "SESMA-004",
                    "nome": "Exames Laboratoriais",
                    "descricao": "Realização de exames laboratoriais",
                    "categoria": "Diagnóstico",
                    "subcategoria": "Laboratorial",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SESMA-005",
                    "nome": "Controle de Pragas",
                    "descricao": "Controle de ratos, mosquitos e outras pragas",
                    "categoria": "Vigilância Sanitária",
                    "subcategoria": "Pragas",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SESMA-006",
                    "nome": "Fiscalização Sanitária",
                    "descricao": "Vistoria sanitária em estabelecimentos",
                    "categoria": "Fiscalização",
                    "subcategoria": "Sanitária",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
            ]
            
            for servico in sesma_servicos:
                servico["secretaria_id"] = secretarias["SESMA"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(sesma_servicos)} serviços cadastrados")
        
        # ==========================================
        # SEMEC - SECRETARIA DE EDUCAÇÃO
        # ==========================================
        if "SEMEC" in secretarias:
            print("\n📚 SEMEC - Educação")
            semec_servicos = [
                {
                    "codigo": "SEMEC-001",
                    "nome": "Matrícula Escolar",
                    "descricao": "Matrícula de alunos na rede municipal",
                    "categoria": "Matrícula",
                    "subcategoria": "Escola",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEMEC-002",
                    "nome": "Transferência Escolar",
                    "descricao": "Transferência de aluno entre escolas",
                    "categoria": "Matrícula",
                    "subcategoria": "Transferência",
                    "sla_horas": 72,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEMEC-003",
                    "nome": "Matrícula em Creche",
                    "descricao": "Matrícula de crianças em creches municipais",
                    "categoria": "Matrícula",
                    "subcategoria": "Creche",
                    "sla_horas": 240,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEMEC-004",
                    "nome": "Transporte Escolar",
                    "descricao": "Solicitação de transporte escolar",
                    "categoria": "Transporte",
                    "subcategoria": "Escolar",
                    "sla_horas": 168,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEMEC-005",
                    "nome": "Reclamação sobre Merenda",
                    "descricao": "Reclamação ou solicitação sobre merenda escolar",
                    "categoria": "Alimentação",
                    "subcategoria": "Merenda",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "SEMEC-006",
                    "nome": "Manutenção de Escola",
                    "descricao": "Solicitação de reparo em estrutura escolar",
                    "categoria": "Infraestrutura",
                    "subcategoria": "Manutenção",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.MEDIA,
                },
            ]
            
            for servico in semec_servicos:
                servico["secretaria_id"] = secretarias["SEMEC"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(semec_servicos)} serviços cadastrados")
        
        # ==========================================
        # SEJEL - SECRETARIA DE ESPORTE E LAZER
        # ==========================================
        if "SEJEL" in secretarias:
            print("\n⚽ SEJEL - Esporte e Lazer")
            sejel_servicos = [
                {
                    "codigo": "SEJEL-001",
                    "nome": "Manutenção de Praça",
                    "descricao": "Reparo e manutenção de praças públicas",
                    "categoria": "Infraestrutura",
                    "subcategoria": "Praça",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEJEL-002",
                    "nome": "Reparo de Quadra Esportiva",
                    "descricao": "Conserto de quadras esportivas públicas",
                    "categoria": "Infraestrutura",
                    "subcategoria": "Quadra",
                    "sla_horas": 168,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "SEJEL-003",
                    "nome": "Agendamento de Espaço Esportivo",
                    "descricao": "Reserva de quadras e espaços para eventos",
                    "categoria": "Agendamento",
                    "subcategoria": "Esporte",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.AGENDAVEL,
                },
                {
                    "codigo": "SEJEL-004",
                    "nome": "Manutenção de Parque",
                    "descricao": "Manutenção de parques públicos",
                    "categoria": "Infraestrutura",
                    "subcategoria": "Parque",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.BAIXA,
                },
            ]
            
            for servico in sejel_servicos:
                servico["secretaria_id"] = secretarias["SEJEL"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(sejel_servicos)} serviços cadastrados")
        
        # ==========================================
        # GMB - GUARDA MUNICIPAL
        # ==========================================
        if "GMB" in secretarias:
            print("\n👮 GMB - Guarda Municipal")
            gmb_servicos = [
                {
                    "codigo": "GMB-001",
                    "nome": "Atendimento de Emergência",
                    "descricao": "Atendimento emergencial da Guarda Municipal",
                    "categoria": "Segurança",
                    "subcategoria": "Emergência",
                    "sla_horas": 1,
                    "prioridade": PrioridadeServico.EMERGENCIAL,
                },
                {
                    "codigo": "GMB-002",
                    "nome": "Fiscalização de Patrimônio",
                    "descricao": "Fiscalização e proteção do patrimônio público",
                    "categoria": "Fiscalização",
                    "subcategoria": "Patrimônio",
                    "sla_horas": 24,
                    "prioridade": PrioridadeServico.ALTA,
                },
                {
                    "codigo": "GMB-003",
                    "nome": "Solicitação de Ronda",
                    "descricao": "Solicitação de ronda em local específico",
                    "categoria": "Segurança",
                    "subcategoria": "Ronda",
                    "sla_horas": 12,
                    "prioridade": PrioridadeServico.ALTA,
                },
            ]
            
            for servico in gmb_servicos:
                servico["secretaria_id"] = secretarias["GMB"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(gmb_servicos)} serviços cadastrados")
        
        # ==========================================
        # CODEM
        # ==========================================
        if "CODEM" in secretarias:
            print("\n🏪 CODEM - Feiras e Mercados")
            codem_servicos = [
                {
                    "codigo": "CODEM-001",
                    "nome": "Solicitação de Box em Feira",
                    "descricao": "Solicitação de espaço em feiras municipais",
                    "categoria": "Feira",
                    "subcategoria": "Box",
                    "sla_horas": 240,
                    "prioridade": PrioridadeServico.AGENDAVEL,
                    "custo": 100.00,
                },
                {
                    "codigo": "CODEM-002",
                    "nome": "Manutenção de Feira",
                    "descricao": "Reparo e manutenção de estrutura de feiras",
                    "categoria": "Infraestrutura",
                    "subcategoria": "Feira",
                    "sla_horas": 120,
                    "prioridade": PrioridadeServico.MEDIA,
                },
                {
                    "codigo": "CODEM-003",
                    "nome": "Fiscalização de Comércio Ambulante",
                    "descricao": "Fiscalização de comércio ambulante irregular",
                    "categoria": "Fiscalização",
                    "subcategoria": "Ambulante",
                    "sla_horas": 48,
                    "prioridade": PrioridadeServico.MEDIA,
                },
            ]
            
            for servico in codem_servicos:
                servico["secretaria_id"] = secretarias["CODEM"].id
                servico["sla_dias"] = servico["sla_horas"] / 24
                db.add(ServicoSecretaria(**servico))
                servicos_count += 1
            
            print(f"   ✓ {len(codem_servicos)} serviços cadastrados")
        
        # Commit de todos os serviços
        db.commit()
        
        print("\n" + "="*70)
        print(f"✅ Total: {servicos_count} serviços cadastrados com sucesso!")
        print("="*70)
        
        # Estatísticas
        print("\n📊 ESTATÍSTICAS:")
        print(f"   • Total de serviços: {servicos_count}")
        print(f"   • Serviços emergenciais (< 12h): {db.query(ServicoSecretaria).filter(ServicoSecretaria.prioridade == PrioridadeServico.EMERGENCIAL).count()}")
        print(f"   • Serviços de alta prioridade: {db.query(ServicoSecretaria).filter(ServicoSecretaria.prioridade == PrioridadeServico.ALTA).count()}")
        print(f"   • Serviços gratuitos: {db.query(ServicoSecretaria).filter(ServicoSecretaria.custo == 0).count()}")
        print(f"   • Serviços pagos: {db.query(ServicoSecretaria).filter(ServicoSecretaria.custo > 0).count()}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao criar serviços: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🌱 Seed de Catálogo de Serviços - Prefeitura de Belém\n")
    seed_servicos()
    print("\n✅ Seed concluído!\n")
