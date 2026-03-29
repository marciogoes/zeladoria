"""
Seed de Secretarias
Sistema de Zeladoria Urbana - Belém/PA

Popular banco de dados com todas as secretarias da Prefeitura de Belém
"""

from app.database.database import SessionLocal, engine, Base
from app.models_secretarias import Secretaria, TipoSecretaria

# Criar tabelas
Base.metadata.create_all(bind=engine)

def seed_secretarias():
    """Popular banco com secretarias da Prefeitura de Belém"""
    
    db = SessionLocal()
    
    try:
        print("🏛️  Criando Secretarias da Prefeitura de Belém...")
        
        secretarias = [
            # ==========================================
            # ADMINISTRAÇÃO E GESTÃO
            # ==========================================
            {
                "nome": "Secretaria Municipal de Administração",
                "sigla": "SEMAD",
                "descricao": "Responsável pela gestão administrativa, recursos humanos e patrimônio público",
                "tipo": TipoSecretaria.ADMINISTRACAO,
                "email": "semad@belem.pa.gov.br",
                "telefone": "(91) 3073-3000",
                "responsavel": "Secretário Municipal de Administração",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal de Coordenadoria Geral de Planejamento e Gestão",
                "sigla": "SEGEP",
                "descricao": "Planejamento estratégico, orçamento e gestão municipal",
                "tipo": TipoSecretaria.ADMINISTRACAO,
                "email": "segep@belem.pa.gov.br",
                "telefone": "(91) 3073-3100",
                "responsavel": "Secretário de Planejamento",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Gabinete do Prefeito",
                "sigla": "GABPREF",
                "descricao": "Gabinete do Prefeito e Vice-Prefeita",
                "tipo": TipoSecretaria.ADMINISTRACAO,
                "email": "gabinete@belem.pa.gov.br",
                "telefone": "(91) 3073-2000",
                "responsavel": "Chefe de Gabinete",
                "cargo_responsavel": "Chefe de Gabinete",
            },
            
            # ==========================================
            # FINANÇAS E ECONOMIA
            # ==========================================
            {
                "nome": "Secretaria Municipal de Finanças",
                "sigla": "SEFIN",
                "descricao": "Gestão financeira, tributos e arrecadação municipal",
                "tipo": TipoSecretaria.FINANCAS,
                "email": "sefin@belem.pa.gov.br",
                "telefone": "(91) 3073-3200",
                "responsavel": "Secretário Municipal de Finanças",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal de Economia",
                "sigla": "SECON",
                "descricao": "Desenvolvimento econômico, emprego e renda",
                "tipo": TipoSecretaria.FINANCAS,
                "email": "secon@belem.pa.gov.br",
                "telefone": "(91) 3073-3300",
                "responsavel": "Secretário Municipal de Economia",
                "cargo_responsavel": "Secretário",
            },
            
            # ==========================================
            # INFRAESTRUTURA E URBANISMO
            # ==========================================
            {
                "nome": "Secretaria Municipal de Urbanismo",
                "sigla": "SEURB",
                "descricao": "Planejamento urbano, obras, vias públicas e infraestrutura urbana",
                "tipo": TipoSecretaria.INFRAESTRUTURA,
                "email": "seurb@belem.pa.gov.br",
                "telefone": "(91) 3073-3400",
                "responsavel": "Secretário Municipal de Urbanismo",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal de Saneamento",
                "sigla": "SESAN",
                "descricao": "Saneamento básico, drenagem, água e esgoto",
                "tipo": TipoSecretaria.INFRAESTRUTURA,
                "email": "sesan@belem.pa.gov.br",
                "telefone": "(91) 3073-3500",
                "responsavel": "Secretário Municipal de Saneamento",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal de Habitação",
                "sigla": "SEHAB",
                "descricao": "Política habitacional, regularização fundiária e moradia popular",
                "tipo": TipoSecretaria.INFRAESTRUTURA,
                "email": "sehab@belem.pa.gov.br",
                "telefone": "(91) 3073-3600",
                "responsavel": "Secretário Municipal de Habitação",
                "cargo_responsavel": "Secretário",
            },
            
            # ==========================================
            # SAÚDE E BEM-ESTAR
            # ==========================================
            {
                "nome": "Secretaria Municipal de Saúde",
                "sigla": "SESMA",
                "descricao": "Saúde pública, postos de saúde, hospitais e programas de saúde",
                "tipo": TipoSecretaria.SAUDE,
                "email": "sesma@belem.pa.gov.br",
                "telefone": "(91) 3073-3700",
                "responsavel": "Secretário Municipal de Saúde",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal da Mulher",
                "sigla": "SEMULHER",
                "descricao": "Políticas para mulheres, combate à violência e igualdade de gênero",
                "tipo": TipoSecretaria.SAUDE,
                "email": "semulher@belem.pa.gov.br",
                "telefone": "(91) 3073-3800",
                "responsavel": "Secretária Municipal da Mulher",
                "cargo_responsavel": "Secretária",
            },
            
            # ==========================================
            # EDUCAÇÃO
            # ==========================================
            {
                "nome": "Secretaria Municipal de Educação",
                "sigla": "SEMEC",
                "descricao": "Educação municipal, escolas, creches e programas educacionais",
                "tipo": TipoSecretaria.EDUCACAO,
                "email": "semec@belem.pa.gov.br",
                "telefone": "(91) 3073-3900",
                "responsavel": "Secretário Municipal de Educação",
                "cargo_responsavel": "Secretário",
            },
            
            # ==========================================
            # MEIO AMBIENTE
            # ==========================================
            {
                "nome": "Secretaria Municipal de Meio Ambiente",
                "sigla": "SEMMA",
                "descricao": "Meio ambiente, áreas verdes, arborização e fiscalização ambiental",
                "tipo": TipoSecretaria.MEIO_AMBIENTE,
                "email": "semma@belem.pa.gov.br",
                "telefone": "(91) 3073-4000",
                "responsavel": "Secretário Municipal de Meio Ambiente",
                "cargo_responsavel": "Secretário",
            },
            
            # ==========================================
            # OUTRAS SECRETARIAS
            # ==========================================
            {
                "nome": "Secretaria Municipal de Assuntos Jurídicos",
                "sigla": "SEMAJ",
                "descricao": "Assuntos jurídicos, legislação e consultoria legal",
                "tipo": TipoSecretaria.OUTRAS,
                "email": "semaj@belem.pa.gov.br",
                "telefone": "(91) 3073-4100",
                "responsavel": "Secretário Municipal de Assuntos Jurídicos",
                "cargo_responsavel": "Secretário",
            },
            {
                "nome": "Secretaria Municipal de Esporte, Juventude e Lazer",
                "sigla": "SEJEL",
                "descricao": "Esporte, lazer, juventude e equipamentos esportivos",
                "tipo": TipoSecretaria.OUTRAS,
                "email": "sejel@belem.pa.gov.br",
                "telefone": "(91) 3073-4200",
                "responsavel": "Secretário Municipal de Esporte",
                "cargo_responsavel": "Secretário",
            },
            
            # ==========================================
            # ÓRGÃOS E AUTARQUIAS
            # ==========================================
            {
                "nome": "Procuradoria-Geral do Município",
                "sigla": "PGM",
                "descricao": "Procuradoria, defesa jurídica e consultoria do município",
                "tipo": TipoSecretaria.ORGAO,
                "email": "pgm@belem.pa.gov.br",
                "telefone": "(91) 3073-4300",
                "responsavel": "Procurador-Geral do Município",
                "cargo_responsavel": "Procurador-Geral",
            },
            {
                "nome": "Auditoria Geral do Município",
                "sigla": "AGM",
                "descricao": "Auditoria, controle interno e fiscalização",
                "tipo": TipoSecretaria.ORGAO,
                "email": "agm@belem.pa.gov.br",
                "telefone": "(91) 3073-4400",
                "responsavel": "Auditor-Geral do Município",
                "cargo_responsavel": "Auditor-Geral",
            },
            {
                "nome": "Ouvidoria Geral do Município",
                "sigla": "OGM",
                "descricao": "Ouvidoria, atendimento ao cidadão e mediação de conflitos",
                "tipo": TipoSecretaria.ORGAO,
                "email": "ogm@belem.pa.gov.br",
                "telefone": "(91) 3073-4500",
                "responsavel": "Ouvidor-Geral do Município",
                "cargo_responsavel": "Ouvidor-Geral",
            },
            {
                "nome": "Guarda Municipal de Belém",
                "sigla": "GMB",
                "descricao": "Segurança municipal, patrimônio público e ordem urbana",
                "tipo": TipoSecretaria.ORGAO,
                "email": "gmb@belem.pa.gov.br",
                "telefone": "(91) 3073-4600",
                "responsavel": "Comandante da Guarda Municipal",
                "cargo_responsavel": "Comandante",
            },
            {
                "nome": "Companhia de Desenvolvimento e Administração da Área Metropolitana de Belém",
                "sigla": "CODEM",
                "descricao": "Desenvolvimento metropolitano, feiras e mercados públicos",
                "tipo": TipoSecretaria.ORGAO,
                "email": "codem@belem.pa.gov.br",
                "telefone": "(91) 3073-4700",
                "responsavel": "Diretor-Presidente da CODEM",
                "cargo_responsavel": "Diretor-Presidente",
            },
        ]
        
        # Limpar secretarias existentes (opcional)
        db.query(Secretaria).delete()
        
        # Criar secretarias
        for sec_data in secretarias:
            secretaria = Secretaria(**sec_data)
            db.add(secretaria)
        
        db.commit()
        
        count = db.query(Secretaria).count()
        print(f"✓ {count} secretarias criadas com sucesso!")
        
        # Mostrar resumo
        print("\n" + "="*60)
        print("SECRETARIAS CADASTRADAS:")
        print("="*60)
        
        for tipo in TipoSecretaria:
            secs = db.query(Secretaria).filter(Secretaria.tipo == tipo).all()
            if secs:
                print(f"\n📁 {tipo.value.upper().replace('_', ' ')}:")
                for sec in secs:
                    print(f"   • {sec.sigla} - {sec.nome}")
        
        print("\n" + "="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar secretarias: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seed de Secretarias - Prefeitura de Belém\n")
    seed_secretarias()
    print("\n✅ Seed concluído!")
