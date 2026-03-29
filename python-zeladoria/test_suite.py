#!/usr/bin/env python3
"""
Suite de Testes Automatizados
Sistema de Zeladoria Urbana - Belém/PA
Versão: 2.0.0
"""

import sys
import time
import requests
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Configurações
API_URL = "http://localhost:8001"
FRONTEND_URL = f"{API_URL}/static/index.html"

# Estatísticas
tests_passed = 0
tests_failed = 0
tests_skipped = 0

def print_header(text):
    """Imprime um cabeçalho formatado"""
    print(f"\n{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{text.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}\n")

def print_test(name):
    """Imprime o nome do teste"""
    print(f"{Fore.YELLOW}[TEST]{Style.RESET_ALL} {name}...", end=" ")

def print_success(message="OK"):
    """Imprime mensagem de sucesso"""
    global tests_passed
    tests_passed += 1
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_failure(message="FALHOU"):
    """Imprime mensagem de falha"""
    global tests_failed
    tests_failed += 1
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_skip(message="PULADO"):
    """Imprime mensagem de teste pulado"""
    global tests_skipped
    tests_skipped += 1
    print(f"{Fore.CYAN}⊘ {message}{Style.RESET_ALL}")

def print_info(message):
    """Imprime mensagem informativa"""
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

def print_warning(message):
    """Imprime mensagem de aviso"""
    print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {message}")

def test_backend_health():
    """Testa se o backend está respondendo"""
    print_test("Backend Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success()
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_failure("Backend não está rodando")
        return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_api_docs():
    """Testa se a documentação da API está acessível"""
    print_test("API Docs (/docs)")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success()
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_frontend():
    """Testa se o frontend está acessível"""
    print_test("Frontend (index.html)")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            # Verificar se contém elementos esperados
            if "Sistema de Zeladoria" in response.text:
                print_success()
            else:
                print_failure("Conteúdo inválido")
                return False
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_auth_login():
    """Testa o endpoint de login"""
    print_test("Auth - Login")
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json={
                "email": "maria.santos@belem.pa.gov.br",
                "senha": "senha123"
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data and "usuario" in data:
                print_success()
                return data["access_token"]
            else:
                print_failure("Resposta inválida")
                return None
        else:
            print_failure(f"Status {response.status_code}")
            return None
    except Exception as e:
        print_failure(str(e))
        return None

def test_categorias(token=None):
    """Testa o endpoint de categorias"""
    print_test("API - Listar Categorias")
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{API_URL}/api/categorias", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print_success(f"{len(data)} categorias")
            else:
                print_failure("Nenhuma categoria encontrada")
                return False
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_bairros(token=None):
    """Testa o endpoint de bairros"""
    print_test("API - Listar Bairros")
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{API_URL}/api/bairros", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print_success(f"{len(data)} bairros")
            else:
                print_failure("Nenhum bairro encontrado")
                return False
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_chamados(token):
    """Testa o endpoint de chamados"""
    print_test("API - Listar Chamados")
    try:
        if not token:
            print_skip("Token não disponível")
            return False
            
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/chamados", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_success(f"{len(data)} chamados")
            else:
                print_failure("Resposta inválida")
                return False
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_dashboard(token):
    """Testa o endpoint do dashboard"""
    print_test("API - Dashboard")
    try:
        if not token:
            print_skip("Token não disponível")
            return False
            
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/relatorios/dashboard", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Verificar campos esperados
            expected_fields = ["total_chamados", "por_status", "top_categorias"]
            if all(field in data for field in expected_fields):
                print_success()
            else:
                print_failure("Campos obrigatórios ausentes")
                return False
        else:
            print_failure(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_cors():
    """Testa configuração CORS"""
    print_test("CORS Headers")
    try:
        response = requests.options(f"{API_URL}/api/categorias", timeout=5)
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        ]
        
        if all(header in response.headers for header in cors_headers):
            print_success()
        else:
            print_warning("Alguns headers CORS ausentes")
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_static_files():
    """Testa arquivos estáticos"""
    files = [
        ("app.js", "/static/app.js"),
        ("dashboard.js", "/static/dashboard.js"),
        ("dashboard-advanced.js", "/static/dashboard-advanced.js")
    ]
    
    for name, path in files:
        print_test(f"Static File - {name}")
        try:
            response = requests.get(f"{API_URL}{path}", timeout=5)
            if response.status_code == 200:
                print_success()
            else:
                print_failure(f"Status {response.status_code}")
        except Exception as e:
            print_failure(str(e))

def test_database():
    """Testa conexão com o banco de dados"""
    print_test("Database Connection")
    try:
        from app.database import engine
        connection = engine.connect()
        connection.close()
        print_success()
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def test_response_time():
    """Testa tempo de resposta"""
    print_test("Response Time")
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/api/categorias", timeout=5)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # em ms
        
        if response_time < 1000:  # < 1 segundo
            print_success(f"{response_time:.2f}ms")
        elif response_time < 2000:  # < 2 segundos
            print_warning(f"{response_time:.2f}ms (lento)")
        else:
            print_failure(f"{response_time:.2f}ms (muito lento)")
            return False
    except Exception as e:
        print_failure(str(e))
        return False
    return True

def print_summary():
    """Imprime resumo dos testes"""
    total = tests_passed + tests_failed + tests_skipped
    
    print(f"\n{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'RESUMO DOS TESTES'.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}\n")
    
    print(f"Total de testes: {total}")
    print(f"{Fore.GREEN}✓ Passaram: {tests_passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ Falharam: {tests_failed}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⊘ Pulados: {tests_skipped}{Style.RESET_ALL}")
    
    if tests_failed == 0:
        print(f"\n{Fore.GREEN}{'🎉 TODOS OS TESTES PASSARAM! 🎉'.center(60)}{Style.RESET_ALL}\n")
        return 0
    else:
        success_rate = (tests_passed / (tests_passed + tests_failed)) * 100
        print(f"\n{Fore.YELLOW}Taxa de sucesso: {success_rate:.1f}%{Style.RESET_ALL}\n")
        return 1

def main():
    """Função principal"""
    print_header("SUITE DE TESTES AUTOMATIZADOS")
    print_info("Sistema de Zeladoria Urbana - Belém/PA")
    print_info("Versão: 2.0.0")
    print_info(f"API URL: {API_URL}\n")
    
    # Testes de Infraestrutura
    print_header("TESTES DE INFRAESTRUTURA")
    
    backend_ok = test_backend_health()
    if not backend_ok:
        print_warning("Backend não está rodando. Pulando testes que dependem dele.")
        print_info("Execute: python main.py")
        return 1
    
    test_api_docs()
    test_frontend()
    test_database()
    test_response_time()
    
    # Testes de API - Autenticação
    print_header("TESTES DE AUTENTICAÇÃO")
    token = test_auth_login()
    
    # Testes de API - Endpoints
    print_header("TESTES DE ENDPOINTS")
    test_categorias(token)
    test_bairros(token)
    test_chamados(token)
    test_dashboard(token)
    
    # Testes de Configuração
    print_header("TESTES DE CONFIGURAÇÃO")
    test_cors()
    test_static_files()
    
    # Resumo
    return print_summary()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Testes interrompidos pelo usuário{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Fore.RED}[✗] Erro fatal: {e}{Style.RESET_ALL}")
        sys.exit(1)
