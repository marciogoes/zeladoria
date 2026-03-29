"""
TESTAR APIS DO CATÁLOGO DE SERVIÇOS
Teste todas as rotas do sistema de catálogo
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_listar_servicos():
    print_section("TESTE 1: Listar Serviços")
    
    try:
        response = requests.get(f"{API_BASE}/api/servicos")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total de serviços: {data.get('total', 0)}")
            
            if data.get('servicos'):
                servico = data['servicos'][0]
                print(f"\nExemplo de serviço:")
                print(f"  - Código: {servico.get('codigo')}")
                print(f"  - Nome: {servico.get('nome')}")
                print(f"  - SLA: {servico.get('sla_horas')}h")
                print(f"  - Custo: R$ {servico.get('custo', 0):.2f}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Erro de conexão: {str(e)}")
        print("Verifique se o backend está rodando!")

def test_buscar_servico():
    print_section("TESTE 2: Buscar Serviço por ID")
    
    try:
        # Primeiro pegar um ID válido
        response = requests.get(f"{API_BASE}/api/servicos")
        if response.status_code == 200:
            data = response.json()
            if data.get('servicos'):
                servico_id = data['servicos'][0]['id']
                
                # Buscar esse serviço específico
                response2 = requests.get(f"{API_BASE}/api/servicos/{servico_id}")
                print(f"Status: {response2.status_code}")
                
                if response2.status_code == 200:
                    servico = response2.json()
                    print(f"✅ Serviço encontrado:")
                    print(f"  - ID: {servico.get('id')}")
                    print(f"  - Código: {servico.get('codigo')}")
                    print(f"  - Nome: {servico.get('nome')}")
                    print(f"  - Categoria: {servico.get('categoria')}")
                    print(f"  - Prioridade: {servico.get('prioridade')}")
                    print(f"  - SLA: {servico.get('sla_horas')}h")
                else:
                    print(f"❌ Erro: {response2.status_code}")
            else:
                print("⚠️ Nenhum serviço encontrado no banco")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_filtrar_servicos():
    print_section("TESTE 3: Filtrar Serviços")
    
    try:
        # Teste 1: Filtrar por categoria
        print("\n📋 Filtro: Categoria")
        response = requests.get(f"{API_BASE}/api/servicos?categoria=Iluminação")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Serviços de iluminação: {data.get('total', 0)}")
        
        # Teste 2: Filtrar por prioridade
        print("\n🔴 Filtro: Prioridade Alta")
        response = requests.get(f"{API_BASE}/api/servicos?prioridade=alta")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Serviços de alta prioridade: {data.get('total', 0)}")
        
        # Teste 3: Apenas gratuitos
        print("\n💰 Filtro: Apenas Gratuitos")
        response = requests.get(f"{API_BASE}/api/servicos?apenas_gratuitos=true")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Serviços gratuitos: {data.get('total', 0)}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_busca_avancada():
    print_section("TESTE 4: Busca Avançada")
    
    try:
        termos = ["iluminação", "buraco", "limpeza"]
        
        for termo in termos:
            print(f"\n🔍 Buscando: '{termo}'")
            response = requests.get(f"{API_BASE}/api/servicos/buscar/avancada?q={termo}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                resultados = response.json()
                print(f"✅ Encontrados: {len(resultados)} serviço(s)")
                
                for r in resultados[:3]:  # Mostrar só os 3 primeiros
                    print(f"   • {r.get('codigo')} - {r.get('nome')}")
                    print(f"     Relevância: {r.get('relevancia', 0):.2f}")
            else:
                print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_autocomplete():
    print_section("TESTE 5: Autocomplete")
    
    try:
        termo = "rep"
        print(f"\n💡 Autocomplete para: '{termo}'")
        
        response = requests.get(f"{API_BASE}/api/servicos/autocomplete?q={termo}&limite=5")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            sugestoes = data.get('sugestoes', [])
            print(f"✅ Sugestões: {len(sugestoes)}")
            
            for s in sugestoes:
                print(f"   • {s.get('value')} - {s.get('label')}")
                print(f"     Categoria: {s.get('categoria')} | SLA: {s.get('sla')}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_categorias():
    print_section("TESTE 6: Listar Categorias")
    
    try:
        response = requests.get(f"{API_BASE}/api/servicos/categorias/listar")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            categorias = response.json()
            print(f"✅ Total de categorias: {len(categorias)}")
            
            print("\n📁 Categorias disponíveis:")
            for cat in categorias:
                print(f"   • {cat.get('categoria')}: {cat.get('total_servicos')} serviço(s)")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_dashboard():
    print_section("TESTE 7: Dashboard do Catálogo")
    
    try:
        response = requests.get(f"{API_BASE}/api/servicos/dashboard")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📊 KPIs:")
            print(f"   Total de Serviços: {data.get('total_servicos')}")
            print(f"   Serviços Ativos: {data.get('servicos_ativos')}")
            print(f"   Categorias: {data.get('total_categorias')}")
            print(f"   Taxa SLA: {data.get('taxa_cumprimento_sla_geral', 0):.1f}%")
            print(f"   Avaliação Média: {data.get('avaliacao_media_geral', 0):.1f}")
            
            print("\n🔴 Distribuição por Prioridade:")
            for prioridade, total in data.get('por_prioridade', {}).items():
                print(f"   • {prioridade}: {total}")
            
            print("\n📋 Top Categorias Solicitadas:")
            for cat in data.get('categorias_mais_solicitadas', [])[:5]:
                print(f"   • {cat.get('categoria')}: {cat.get('total')} solicitações")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_chamados():
    print_section("TESTE 8: Listar Chamados")
    
    try:
        response = requests.get(f"{API_BASE}/api/chamados")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # O formato pode variar dependendo da API
            if isinstance(data, list):
                chamados = data
                total = len(chamados)
            elif isinstance(data, dict):
                chamados = data.get('chamados', [])
                total = data.get('total', len(chamados))
            
            print(f"✅ Total de chamados: {total}")
            
            if chamados:
                print("\n📞 Exemplos de chamados:")
                for c in chamados[:3]:
                    print(f"\n   Protocolo: {c.get('protocolo')}")
                    print(f"   Título: {c.get('titulo')}")
                    print(f"   Status: {c.get('status')}")
                    
                    # Verificar SLA
                    if c.get('prazo_sla'):
                        print(f"   Prazo SLA: {c.get('prazo_sla')}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def run_all_tests():
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║   🧪 TESTE DAS APIS - CATÁLOGO DE SERVIÇOS            ║")
    print("║   Sistema de Zeladoria Urbana - Belém/PA              ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    print(f"\n🌐 Testando API em: {API_BASE}")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    test_listar_servicos()
    test_buscar_servico()
    test_filtrar_servicos()
    test_busca_avancada()
    test_autocomplete()
    test_categorias()
    test_dashboard()
    test_chamados()
    
    print_section("RESUMO DOS TESTES")
    print("\n✅ Se todos os testes passaram, o sistema está funcionando!")
    print("❌ Se houve erros:")
    print("   1. Verifique se o backend está rodando")
    print("   2. Verifique se o banco tem dados (execute popular_banco.py)")
    print("   3. Verifique a porta (padrão: 8000)")
    print("\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro crítico: {str(e)}")
    
    print("\n" + "="*60)
    input("\nPressione ENTER para sair...")
