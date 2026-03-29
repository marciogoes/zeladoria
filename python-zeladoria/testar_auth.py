"""
Script para testar autenticacao e permissoes
"""
from app.database.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.auth import create_access_token, verify_token
import bcrypt

def testar_auth():
    db = SessionLocal()
    
    try:
        print()
        print('=' * 60)
        print('  TESTE DE AUTENTICACAO E PERMISSOES')
        print('=' * 60)
        print()
        
        # Buscar usuario SEURB
        email = 'seurb@zeladoria.com'
        print(f'1. Buscando usuario: {email}')
        print('-' * 60)
        
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        
        if not usuario:
            print(f'ERRO: Usuario {email} nao encontrado!')
            return
        
        print(f'Usuario encontrado:')
        print(f'   ID: {usuario.id}')
        print(f'   Nome: {usuario.nome}')
        print(f'   Email: {usuario.email}')
        print(f'   Tipo: {usuario.tipo}')
        print(f'   Ativo: {usuario.ativo}')
        print()
        
        # Verificar senha
        print('2. Testando senha')
        print('-' * 60)
        senha_teste = 'seurb123'
        senha_correta = usuario.verificar_senha(senha_teste)
        print(f'Senha "{senha_teste}": {"✓ CORRETA" if senha_correta else "✗ INCORRETA"}')
        print()
        
        # Criar token
        print('3. Criando token JWT')
        print('-' * 60)
        token = create_access_token(data={"sub": str(usuario.id)})
        print(f'Token gerado: {token[:50]}...')
        print()
        
        # Verificar token
        print('4. Verificando token')
        print('-' * 60)
        user_id = verify_token(token)
        print(f'User ID do token: {user_id}')
        print()
        
        # Verificar permissoes
        print('5. Verificando permissoes para Dashboard')
        print('-' * 60)
        perfis_permitidos = ['gestor', 'admin', 'secretaria', 'equipe']
        tem_permissao = usuario.tipo in perfis_permitidos
        
        print(f'Perfis com acesso ao Dashboard: {", ".join(perfis_permitidos)}')
        print(f'Tipo do usuario: "{usuario.tipo}"')
        print(f'Tem permissao: {"✓ SIM" if tem_permissao else "✗ NAO"}')
        print()
        
        # Verificar se o tipo esta exatamente igual
        print('6. Verificacao detalhada do tipo')
        print('-' * 60)
        print(f'Tipo do usuario (repr): {repr(usuario.tipo)}')
        print(f'Tipo esperado: "secretaria"')
        print(f'Sao iguais: {usuario.tipo == "secretaria"}')
        print(f'Tamanho do tipo: {len(usuario.tipo)} caracteres')
        print()
        
        # Testar cada perfil
        print('7. Testando cada perfil individualmente')
        print('-' * 60)
        for perfil in perfis_permitidos:
            resultado = usuario.tipo == perfil
            print(f'   {perfil:15} == {usuario.tipo:15} : {resultado}')
        print()
        
        print('=' * 60)
        print('  TESTE CONCLUIDO')
        print('=' * 60)
        print()
        
        if tem_permissao:
            print('✓ Usuario DEVE ter acesso ao Dashboard!')
        else:
            print('✗ Usuario NAO deve ter acesso ao Dashboard')
            print(f'  Tipo atual: "{usuario.tipo}"')
            print(f'  Tipos permitidos: {perfis_permitidos}')
        
        print()
        
    except Exception as e:
        print(f'ERRO: {e}')
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == '__main__':
    testar_auth()
