"""
Script para verificar dados no banco
"""
from app.database.database import SessionLocal
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.models.chamado import Chamado

def verificar_dados():
    db = SessionLocal()
    
    try:
        print()
        print('=' * 50)
        print('  VERIFICACAO DE DADOS NO BANCO')
        print('=' * 50)
        print()
        
        # Categorias
        categorias_count = db.query(Categoria).count()
        print(f'📂 Categorias: {categorias_count}')
        if categorias_count > 0:
            print('   Exemplos:')
            for cat in db.query(Categoria).limit(3).all():
                print(f'   - {cat.icone} {cat.nome}')
        print()
        
        # Bairros
        bairros_count = db.query(Bairro).count()
        print(f'🏘️  Bairros: {bairros_count}')
        if bairros_count > 0:
            print('   Exemplos:')
            for bairro in db.query(Bairro).limit(3).all():
                print(f'   - {bairro.nome} ({bairro.regiao})')
        print()
        
        # Usuários
        usuarios_count = db.query(Usuario).count()
        print(f'👥 Usuarios: {usuarios_count}')
        if usuarios_count > 0:
            print('   Exemplos:')
            for user in db.query(Usuario).limit(3).all():
                print(f'   - {user.nome} ({user.tipo})')
        print()
        
        # Chamados
        chamados_count = db.query(Chamado).count()
        print(f'📋 Chamados: {chamados_count}')
        if chamados_count > 0:
            print('   Exemplos:')
            for chamado in db.query(Chamado).limit(3).all():
                print(f'   - {chamado.protocolo}: {chamado.titulo}')
        print()
        
        print('=' * 50)
        
        # Avisos
        if categorias_count == 0:
            print('⚠️  AVISO: Nenhuma categoria encontrada!')
            print('   Execute: POPULAR_CATEGORIAS_BAIRROS.bat')
            print()
        
        if bairros_count == 0:
            print('⚠️  AVISO: Nenhum bairro encontrado!')
            print('   Execute: POPULAR_CATEGORIAS_BAIRROS.bat')
            print()
        
        if usuarios_count == 0:
            print('⚠️  AVISO: Nenhum usuario encontrado!')
            print('   Execute: CRIAR_USUARIOS.bat')
            print()
        
        if categorias_count > 0 and bairros_count > 0 and usuarios_count > 0:
            print('✅ Banco de dados pronto para uso!')
            print()
        
    except Exception as e:
        print(f'❌ ERRO: {e}')
        
    finally:
        db.close()

if __name__ == '__main__':
    verificar_dados()
