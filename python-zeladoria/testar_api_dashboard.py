"""
Teste direto da API - Simula login e acesso ao dashboard
"""
import requests
import json

API_BASE = 'http://localhost:8001/api'

def testar_dashboard():
    print()
    print('=' * 70)
    print('  TESTE DIRETO DA API - DASHBOARD')
    print('=' * 70)
    print()
    
    # 1. Fazer login
    print('1. Fazendo login com seurb@zeladoria.com')
    print('-' * 70)
    
    try:
        response = requests.post(
            f'{API_BASE}/auth/login',
            json={
                'email': 'seurb@zeladoria.com',
                'senha': 'seurb123'
            }
        )
        
        print(f'Status: {response.status_code}')
        
        if response.status_code != 200:
            print(f'ERRO no login: {response.text}')
            return
        
        data = response.json()
        token = data['access_token']
        usuario = data['usuario']
        
        print(f'✓ Login realizado com sucesso!')
        print(f'  Nome: {usuario["nome"]}')
        print(f'  Tipo: {usuario["tipo"]}')
        print(f'  Token: {token[:50]}...')
        print()
        
        # 2. Acessar dashboard
        print('2. Acessando /api/relatorios/dashboard')
        print('-' * 70)
        
        response = requests.get(
            f'{API_BASE}/relatorios/dashboard',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        
        print(f'Status: {response.status_code}')
        print(f'Headers da resposta:')
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'content-length']:
                print(f'  {key}: {value}')
        print()
        
        if response.status_code == 200:
            print('✓ SUCESSO! Dashboard acessado!')
            data = response.json()
            print(f'  Total de chamados: {data.get("total_chamados", 0)}')
            print()
            
        elif response.status_code == 403:
            print('✗ ERRO 403 - ACESSO NEGADO!')
            print(f'  Resposta: {response.text}')
            print()
            print('DIAGNOSTICO:')
            print(f'  - Usuario tipo: {usuario["tipo"]}')
            print(f'  - Perfis que deveriam ter acesso: gestor, admin, secretaria, equipe')
            print()
            print('POSSIVEL CAUSA:')
            print('  - A API nao foi reiniciada apos as correcoes')
            print('  - O codigo ainda esta usando a versao antiga')
            print()
            
        elif response.status_code == 401:
            print('✗ ERRO 401 - NAO AUTORIZADO!')
            print(f'  Resposta: {response.text}')
            print()
            print('POSSIVEL CAUSA:')
            print('  - Token invalido ou expirado')
            print()
            
        else:
            print(f'✗ ERRO {response.status_code}')
            print(f'  Resposta: {response.text}')
            print()
        
    except requests.exceptions.ConnectionError:
        print('✗ ERRO DE CONEXAO!')
        print('  A API nao esta rodando ou nao esta na porta 8001')
        print()
        print('SOLUCAO:')
        print('  Execute: INICIAR_API_8001.bat')
        print()
        
    except Exception as e:
        print(f'✗ ERRO INESPERADO: {e}')
        import traceback
        traceback.print_exc()
        print()
    
    print('=' * 70)
    print('  TESTE CONCLUIDO')
    print('=' * 70)
    print()

if __name__ == '__main__':
    testar_dashboard()
