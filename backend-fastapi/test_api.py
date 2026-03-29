"""
Script de teste para a API de Tarefas
Execute este script após iniciar o servidor
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testando API de Tarefas\n")
    print("=" * 50)
    
    # 1. Health Check
    print("\n1️⃣ Testando Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}\n")
    
    # 2. Criar Tarefa
    print("2️⃣ Criando nova tarefa...")
    new_task = {
        "title": "Aprender FastAPI",
        "description": "Estudar documentação e criar exemplos",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=new_task)
    print(f"Status: {response.status_code}")
    task = response.json()
    print(f"Tarefa criada: {json.dumps(task, indent=2, ensure_ascii=False)}\n")
    task_id = task['id']
    
    # 3. Listar Tarefas
    print("3️⃣ Listando todas as tarefas...")
    response = requests.get(f"{BASE_URL}/tasks/")
    print(f"Status: {response.status_code}")
    tasks = response.json()
    print(f"Total de tarefas: {len(tasks)}")
    print(f"Tarefas: {json.dumps(tasks, indent=2, ensure_ascii=False)}\n")
    
    # 4. Buscar Tarefa por ID
    print(f"4️⃣ Buscando tarefa ID {task_id}...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {response.status_code}")
    print(f"Tarefa: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # 5. Atualizar Tarefa
    print(f"5️⃣ Atualizando tarefa ID {task_id}...")
    update_data = {
        "description": "Descrição atualizada via script de teste"
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Tarefa atualizada: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # 6. Marcar como Concluída
    print(f"6️⃣ Marcando tarefa ID {task_id} como concluída...")
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete")
    print(f"Status: {response.status_code}")
    print(f"Tarefa concluída: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
    
    # 7. Deletar Tarefa
    print(f"7️⃣ Deletando tarefa ID {task_id}...")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {response.status_code}")
    print("Tarefa deletada com sucesso!\n")
    
    print("=" * 50)
    print("✅ Todos os testes concluídos!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("Certifique-se de que o servidor está rodando:")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Erro: {e}")
