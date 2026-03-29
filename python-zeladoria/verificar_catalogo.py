"""
Verificar servicos no catalogo
"""
from app.database.database import SessionLocal
from app.models_servicos import ServicoSecretaria, PrioridadeServico

def verificar_servicos():
    db = SessionLocal()
    
    try:
        print()
        print('=' * 80)
        print('  CATALOGO DE SERVICOS')
        print('=' * 80)
        print()
        
        # Total
        total = db.query(ServicoSecretaria).count()
        print(f'📊 Total de servicos: {total}')
        print()
        
        if total == 0:
            print('⚠️  NENHUM SERVICO ENCONTRADO!')
            print('Execute: POPULAR_CATALOGO_SERVICOS.bat')
            print()
            return
        
        # Por Secretaria
        print('📂 Servicos por Secretaria')
        print('-' * 80)
        
        secretarias_ids = db.query(ServicoSecretaria.secretaria_id).distinct().all()
        
        for (sec_id,) in secretarias_ids:
            if sec_id:
                count = db.query(ServicoSecretaria).filter_by(secretaria_id=sec_id).count()
                print(f'   Secretaria {sec_id}: {count} servicos')
        print()
        
        # Por Prioridade
        print('⚠️  Servicos por Prioridade')
        print('-' * 80)
        
        for prioridade in PrioridadeServico:
            count = db.query(ServicoSecretaria).filter_by(prioridade=prioridade).count()
            emoji = {
                'emergencial': '🚨',
                'alta': '🔴',
                'media': '🟡',
                'baixa': '🟢',
                'agendavel': '📅'
            }.get(prioridade.value, '')
            
            print(f'   {emoji} {prioridade.value.capitalize()}: {count} servicos')
        print()
        
        # Exemplos
        print('📋 Exemplos de Servicos')
        print('-' * 80)
        
        servicos = db.query(ServicoSecretaria).limit(10).all()
        
        for servico in servicos:
            print(f'   {servico.codigo}: {servico.nome}')
            print(f'      SLA: {servico.sla_em_dias} | Prioridade: {servico.prioridade_label}')
            print()
        
        print('=' * 80)
        print()
        
    except Exception as e:
        print(f'❌ ERRO: {e}')
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == '__main__':
    verificar_servicos()
