"""
Script para diagnosticar problemas no sistema
"""
from app.database.database import SessionLocal
from app.models.usuario import Usuario
from app.models.chamado import Chamado
from app.models.categoria import Categoria
from app.models.bairro import Bairro

def diagnostico():
    db = SessionLocal()
    
    try:
        print()
        print('=' * 60)
        print('  DIAGNOSTICO COMPLETO DO SISTEMA')
        print('=' * 60)
        print()
        
        # 1. USUARIOS
        print('1. USUARIOS NO BANCO')
        print('-' * 60)
        usuarios = db.query(Usuario).all()
        print(f'Total: {len(usuarios)} usuarios')
        print()
        for user in usuarios:
            print(f'   {user.tipo.upper():12} | {user.email:30} | {user.nome}')
        print()
        
        # 2. CATEGORIAS
        print('2. CATEGORIAS')
        print('-' * 60)
        categorias = db.query(Categoria).count()
        print(f'Total: {categorias} categorias')
        if categorias > 0:
            for cat in db.query(Categoria).limit(5).all():
                print(f'   {cat.icone} {cat.nome}')
        print()
        
        # 3. BAIRROS
        print('3. BAIRROS')
        print('-' * 60)
        bairros = db.query(Bairro).count()
        print(f'Total: {bairros} bairros')
        if bairros > 0:
            for b in db.query(Bairro).limit(5).all():
                print(f'   {b.nome} ({b.regiao})')
        print()
        
        # 4. CHAMADOS
        print('4. CHAMADOS')
        print('-' * 60)
        chamados = db.query(Chamado).count()
        print(f'Total: {chamados} chamados')
        if chamados > 0:
            for ch in db.query(Chamado).limit(3).all():
                print(f'   {ch.protocolo} - {ch.titulo} ({ch.status})')
        print()
        
        # 5. VERIFICAR PERMISSOES
        print('5. VERIFICAR ACESSO AO DASHBOARD')
        print('-' * 60)
        tipos_com_acesso = ['gestor', 'admin', 'secretaria', 'equipe']
        for user in usuarios:
            acesso = 'SIM' if user.tipo in tipos_com_acesso else 'NAO'
            simbolo = '✓' if user.tipo in tipos_com_acesso else '✗'
            print(f'   {simbolo} {user.tipo.upper():12} | {user.email:30} | Dashboard: {acesso}')
        print()
        
        # 6. RECOMENDACOES
        print('6. RECOMENDACOES')
        print('-' * 60)
        
        if categorias == 0:
            print('   ⚠️  Execute: POPULAR_CATEGORIAS_BAIRROS.bat')
        if bairros == 0:
            print('   ⚠️  Execute: POPULAR_CATEGORIAS_BAIRROS.bat')
        
        # Verificar se tem usuario com acesso ao dashboard
        usuarios_dashboard = [u for u in usuarios if u.tipo in tipos_com_acesso]
        if not usuarios_dashboard:
            print('   ⚠️  NENHUM usuario com acesso ao Dashboard!')
            print('   Execute: CRIAR_USUARIOS.bat')
        else:
            print('   ✓ Usuarios com acesso ao Dashboard:')
            for u in usuarios_dashboard:
                print(f'      - {u.email} (senha: use a do script)')
        
        print()
        print('=' * 60)
        print('  DIAGNOSTICO CONCLUIDO')
        print('=' * 60)
        print()
        
    except Exception as e:
        print(f'❌ ERRO: {e}')
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == '__main__':
    diagnostico()
