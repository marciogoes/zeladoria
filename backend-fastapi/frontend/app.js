// Configuração da API
const API_URL = 'http://localhost:8000';

// Estado da aplicação
let tasks = [];
let editingTaskId = null;
let currentFilter = 'all';

// Elementos do DOM
const taskForm = document.getElementById('taskForm');
const titleInput = document.getElementById('title');
const descriptionInput = document.getElementById('description');
const tasksList = document.getElementById('tasksList');
const taskCount = document.getElementById('taskCount');
const loading = document.getElementById('loading');
const toast = document.getElementById('toast');
const btnText = document.getElementById('btnText');
const cancelBtn = document.getElementById('cancelBtn');
const filterBtns = document.querySelectorAll('.filter-btn');

// Inicializar aplicação
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    taskForm.addEventListener('submit', handleSubmit);
    cancelBtn.addEventListener('click', cancelEdit);
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTasks();
        });
    });
}

// Carregar tarefas da API
async function loadTasks() {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/tasks/`);
        if (!response.ok) throw new Error('Erro ao carregar tarefas');
        tasks = await response.json();
        renderTasks();
        hideLoading();
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao carregar tarefas!', 'error');
        hideLoading();
    }
}

// Renderizar tarefas
function renderTasks() {
    const filteredTasks = filterTasks();
    
    if (filteredTasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>Nenhuma tarefa encontrada</p>
            </div>
        `;
    } else {
        tasksList.innerHTML = filteredTasks.map(task => createTaskCard(task)).join('');
    }
    
    updateTaskCount();
}

// Filtrar tarefas
function filterTasks() {
    switch (currentFilter) {
        case 'completed':
            return tasks.filter(task => task.completed);
        case 'pending':
            return tasks.filter(task => !task.completed);
        default:
            return tasks;
    }
}

// Criar card de tarefa
function createTaskCard(task) {
    const date = new Date(task.created_at).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
    
    return `
        <div class="task-card ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <input 
                type="checkbox" 
                class="task-checkbox" 
                ${task.completed ? 'checked' : ''}
                onchange="toggleTask(${task.id})"
            >
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                <div class="task-date">📅 Criada em ${date}</div>
            </div>
            <div class="task-actions">
                <button class="task-btn task-btn-edit" onclick="editTask(${task.id})" title="Editar">
                    ✏️
                </button>
                <button class="task-btn task-btn-delete" onclick="deleteTask(${task.id})" title="Excluir">
                    🗑️
                </button>
            </div>
        </div>
    `;
}

// Atualizar contador
function updateTaskCount() {
    const filteredCount = filterTasks().length;
    const totalCount = tasks.length;
    const completedCount = tasks.filter(t => t.completed).length;
    
    taskCount.textContent = currentFilter === 'all' 
        ? `${totalCount} tarefa${totalCount !== 1 ? 's' : ''} (${completedCount} concluída${completedCount !== 1 ? 's' : ''})`
        : `${filteredCount} tarefa${filteredCount !== 1 ? 's' : ''}`;
}

// Handle form submit
async function handleSubmit(e) {
    e.preventDefault();
    
    const taskData = {
        title: titleInput.value.trim(),
        description: descriptionInput.value.trim() || null,
        completed: false
    };
    
    if (editingTaskId) {
        await updateTask(editingTaskId, taskData);
    } else {
        await createTask(taskData);
    }
}

// Criar nova tarefa
async function createTask(taskData) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/tasks/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) throw new Error('Erro ao criar tarefa');
        
        const newTask = await response.json();
        tasks.unshift(newTask);
        renderTasks();
        resetForm();
        showToast('Tarefa criada com sucesso!', 'success');
        hideLoading();
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao criar tarefa!', 'error');
        hideLoading();
    }
}

// Atualizar tarefa
async function updateTask(id, taskData) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) throw new Error('Erro ao atualizar tarefa');
        
        const updatedTask = await response.json();
        const index = tasks.findIndex(t => t.id === id);
        tasks[index] = updatedTask;
        renderTasks();
        resetForm();
        showToast('Tarefa atualizada com sucesso!', 'success');
        hideLoading();
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao atualizar tarefa!', 'error');
        hideLoading();
    }
}

// Alternar status da tarefa
async function toggleTask(id) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}/complete`, {
            method: 'PATCH'
        });
        
        if (!response.ok) throw new Error('Erro ao atualizar tarefa');
        
        const updatedTask = await response.json();
        const index = tasks.findIndex(t => t.id === id);
        tasks[index] = updatedTask;
        renderTasks();
        showToast(updatedTask.completed ? 'Tarefa concluída! 🎉' : 'Tarefa reaberta!', 'success');
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao atualizar tarefa!', 'error');
        loadTasks(); // Recarregar para sincronizar
    }
}

// Editar tarefa
function editTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    
    editingTaskId = id;
    titleInput.value = task.title;
    descriptionInput.value = task.description || '';
    btnText.textContent = '💾 Salvar Alterações';
    cancelBtn.style.display = 'block';
    
    // Scroll para o formulário
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

// Cancelar edição
function cancelEdit() {
    resetForm();
}

// Deletar tarefa
async function deleteTask(id) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    
    try {
        showLoading();
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Erro ao deletar tarefa');
        
        tasks = tasks.filter(t => t.id !== id);
        renderTasks();
        showToast('Tarefa excluída com sucesso!', 'success');
        hideLoading();
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro ao deletar tarefa!', 'error');
        hideLoading();
    }
}

// Resetar formulário
function resetForm() {
    taskForm.reset();
    editingTaskId = null;
    btnText.textContent = '➕ Adicionar Tarefa';
    cancelBtn.style.display = 'none';
}

// Mostrar loading
function showLoading() {
    loading.style.display = 'flex';
}

// Esconder loading
function hideLoading() {
    loading.style.display = 'none';
}

// Mostrar toast
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
