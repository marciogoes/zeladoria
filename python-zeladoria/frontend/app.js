// Configuração da API
const API_URL = 'http://localhost:8001/api';

// Estado da aplicação
let currentUser = null;
let authToken = null;
let categorias = [];
let bairros = [];
let allChamados = []; // Cache de todos os chamados
let map = null; // Mapa Leaflet
let marker = null; // Marcador no mapa

// Elementos do DOM
const loginScreen = document.getElementById('loginScreen');
const appScreen = document.getElementById('appScreen');
const loading = document.getElementById('loading');
const toast = document.getElementById('toast');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkAuth();
});

// ========== SETUP ========== //
function setupEventListeners() {
    // Tabs de login
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Formulários
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    document.getElementById('novoChamadoForm').addEventListener('submit', handleNovoChamado);

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);

    // Navegação
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    // Filtros
    document.getElementById('filterStatus').addEventListener('change', loadChamados);
    document.getElementById('filterPrioridade').addEventListener('change', loadChamados);
    document.getElementById('searchChamados').addEventListener('input', debounce(loadChamados, 500));

    // Usuários demo
    document.querySelectorAll('.btn-demo').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.getElementById('loginEmail').value = e.target.dataset.email;
            document.getElementById('loginPassword').value = e.target.dataset.senha;
        });
    });

    // Botão de geolocalização
    const btnGeolocation = document.getElementById('btnGeolocation');
    if (btnGeolocation) {
        btnGeolocation.addEventListener('click', getGeolocation);
    }

    // Modal
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    document.getElementById(`${tab}Form`).classList.add('active');
}

function switchView(view) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    
    document.querySelector(`[data-view="${view}"]`).classList.add('active');
    document.getElementById(`view${capitalize(view)}`).classList.add('active');

    if (view === 'chamados') {
        loadChamados();
    } else if (view === 'dashboard') {
        loadDashboard();
    } else if (view === 'novo') {
        // Atualizar título baseado no perfil
        const viewHeader = document.querySelector('#viewNovo .view-header h3');
        if (currentUser.tipo === 'cidadao') {
            viewHeader.textContent = 'Reportar Problema';
        } else {
            viewHeader.textContent = 'Novo Chamado';
        }
        // Inicializar mapa
        setTimeout(() => initMap(), 100);
    }
}

// ========== AUTH ========== //
function checkAuth() {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('currentUser');

    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        showApp();
    } else {
        showLogin();
    }
}

async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const senha = document.getElementById('loginPassword').value;

    try {
        showLoading();
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Erro ao fazer login');
        }

        authToken = data.access_token;
        currentUser = data.usuario;

        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        showToast(`Bem-vindo, ${currentUser.nome}! 👋`, 'success');
        showApp();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const nome = document.getElementById('registerNome').value;
    const email = document.getElementById('registerEmail').value;
    const telefone = document.getElementById('registerTelefone').value;
    const cpf = document.getElementById('registerCpf').value;
    const senha = document.getElementById('registerPassword').value;

    try {
        showLoading();
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, telefone, cpf, senha, tipo: 'cidadao' })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Erro ao cadastrar');
        }

        authToken = data.access_token;
        currentUser = data.usuario;

        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        showToast('Cadastro realizado com sucesso! 🎉', 'success');
        showApp();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function handleLogout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    authToken = null;
    currentUser = null;
    showLogin();
    showToast('Até logo! 👋', 'success');
}

// ========== APP ========== //
async function showApp() {
    loginScreen.classList.remove('active');
    appScreen.classList.add('active');

    // Exibir nome do usuário com emoji do perfil
    const perfilEmoji = {
        'cidadao': '👤',
        'equipe': '👷',
        'gestor': '📊',
        'admin': '🔧'
    };
    document.getElementById('userName').textContent = `${perfilEmoji[currentUser.tipo]} ${currentUser.nome}`;

    // Configurar navegação baseada no perfil
    configureNavigation();

    await loadCategorias();
    await loadBairros();
    await loadChamados();
}

function configureNavigation() {
    const dashboardBtn = document.getElementById('dashboardBtn');
    const viewHeader = document.querySelector('#viewChamados .view-header h3');

    if (currentUser.tipo === 'cidadao') {
        // CIDADÃO: Apenas seus chamados
        dashboardBtn.style.display = 'none';
        viewHeader.textContent = 'Meus Chamados';
    } else if (currentUser.tipo === 'equipe') {
        // EQUIPE: Todos os chamados, sem dashboard
        dashboardBtn.style.display = 'none';
        viewHeader.textContent = 'Todos os Chamados';
    } else if (['gestor', 'admin'].includes(currentUser.tipo)) {
        // GESTOR/ADMIN: Tudo
        dashboardBtn.style.display = 'block';
        viewHeader.textContent = 'Todos os Chamados';
    }
}

function showLogin() {
    loginScreen.classList.add('active');
    appScreen.classList.remove('active');
}

// ========== CHAMADOS ========== //
async function loadChamados() {
    try {
        const status = document.getElementById('filterStatus').value;
        const prioridade = document.getElementById('filterPrioridade').value;
        const search = document.getElementById('searchChamados').value;

        let url = `${API_URL}/chamados?`;
        if (status) url += `status=${status}&`;
        if (prioridade) url += `prioridade=${prioridade}&`;
        if (search) url += `search=${search}&`;

        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        allChamados = await response.json();

        // Filtrar por perfil
        let chamadosFiltrados = allChamados;
        if (currentUser.tipo === 'cidadao') {
            // Cidadão vê apenas seus chamados
            chamadosFiltrados = allChamados.filter(c => c.usuario_id === currentUser.id);
        }
        // Equipe e Gestor veem todos

        renderChamados(chamadosFiltrados);
    } catch (error) {
        showToast('Erro ao carregar chamados', 'error');
        console.error(error);
    }
}

function renderChamados(chamados) {
    const container = document.getElementById('chamadosList');

    if (chamados.length === 0) {
        const mensagem = currentUser.tipo === 'cidadao' 
            ? 'Você ainda não tem chamados. Clique em "Novo Chamado" para reportar um problema!'
            : 'Nenhum chamado encontrado';
        
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>${mensagem}</p>
            </div>
        `;
        return;
    }

    container.innerHTML = chamados.map(chamado => `
        <div class="chamado-card" onclick="showChamadoDetails(${chamado.id})">
            <div class="chamado-header">
                <div>
                    <div class="chamado-titulo">${chamado.titulo}</div>
                    <div class="chamado-protocolo">📋 Protocolo: ${chamado.protocolo}</div>
                </div>
                <div class="chamado-badges">
                    <span class="badge badge-${chamado.status}">${formatStatus(chamado.status)}</span>
                    <span class="badge badge-${chamado.prioridade}">${capitalize(chamado.prioridade)}</span>
                </div>
            </div>
            <div class="chamado-body">
                <div class="chamado-descricao">${chamado.descricao}</div>
                <div class="chamado-endereco">📍 ${chamado.endereco}</div>
            </div>
            <div class="chamado-footer">
                <div class="chamado-categoria">
                    <span>${chamado.categoria?.icone || '📌'}</span>
                    <span>${chamado.categoria?.nome || 'N/A'}</span>
                </div>
                <div class="chamado-data">
                    ${formatDate(chamado.created_at)}
                </div>
            </div>
        </div>
    `).join('');
}

async function showChamadoDetails(id) {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/chamados/${id}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        const chamado = await response.json();

        const modal = document.getElementById('chamadoModal');
        const detalhes = document.getElementById('chamadoDetalhes');

        // Botões de ação baseados no perfil
        let acoesHTML = '';
        
        if (currentUser.tipo === 'equipe' || currentUser.tipo === 'gestor' || currentUser.tipo === 'admin') {
            // EQUIPE/GESTOR: Pode atualizar status
            acoesHTML = `
                <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid var(--border);">
                    <h4 style="margin-bottom: 15px;">⚙️ Ações da Equipe</h4>
                    <div style="display: grid; gap: 10px;">
                        <select id="modalStatus" style="padding: 10px; border: 2px solid var(--border); border-radius: 8px;">
                            <option value="aberto" ${chamado.status === 'aberto' ? 'selected' : ''}>Aberto</option>
                            <option value="em_andamento" ${chamado.status === 'em_andamento' ? 'selected' : ''}>Em Andamento</option>
                            <option value="resolvido" ${chamado.status === 'resolvido' ? 'selected' : ''}>Resolvido</option>
                            <option value="cancelado" ${chamado.status === 'cancelado' ? 'selected' : ''}>Cancelado</option>
                        </select>
                        <button onclick="atualizarStatus(${chamado.id})" class="btn btn-primary">
                            💾 Atualizar Status
                        </button>
                    </div>
                </div>
            `;
        } else if (currentUser.tipo === 'cidadao' && chamado.status === 'resolvido' && !chamado.avaliacao) {
            // CIDADÃO: Pode avaliar quando resolvido
            acoesHTML = `
                <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid var(--border);">
                    <h4 style="margin-bottom: 15px;">⭐ Avaliar Atendimento</h4>
                    <div style="display: grid; gap: 10px;">
                        <div style="display: flex; gap: 10px; justify-content: center; font-size: 2em;">
                            <span onclick="setAvaliacao(1)" style="cursor: pointer;" data-star="1">⭐</span>
                            <span onclick="setAvaliacao(2)" style="cursor: pointer;" data-star="2">⭐</span>
                            <span onclick="setAvaliacao(3)" style="cursor: pointer;" data-star="3">⭐</span>
                            <span onclick="setAvaliacao(4)" style="cursor: pointer;" data-star="4">⭐</span>
                            <span onclick="setAvaliacao(5)" style="cursor: pointer;" data-star="5">⭐</span>
                        </div>
                        <input type="hidden" id="modalAvaliacao" value="5">
                        <textarea id="modalComentario" placeholder="Comentário (opcional)" rows="3" style="padding: 10px; border: 2px solid var(--border); border-radius: 8px;"></textarea>
                        <button onclick="avaliarChamado(${chamado.id})" class="btn btn-primary">
                            📤 Enviar Avaliação
                        </button>
                    </div>
                </div>
            `;
        }

        detalhes.innerHTML = `
            <h2>${chamado.titulo}</h2>
            <p><strong>📋 Protocolo:</strong> ${chamado.protocolo}</p>
            <p><strong>📊 Status:</strong> <span class="badge badge-${chamado.status}">${formatStatus(chamado.status)}</span></p>
            <p><strong>🚨 Prioridade:</strong> <span class="badge badge-${chamado.prioridade}">${capitalize(chamado.prioridade)}</span></p>
            <p><strong>📂 Categoria:</strong> ${chamado.categoria?.icone} ${chamado.categoria?.nome}</p>
            ${chamado.bairro ? `<p><strong>🏘️ Bairro:</strong> ${chamado.bairro.nome}</p>` : ''}
            <p><strong>📍 Endereço:</strong> ${chamado.endereco}</p>
            <p><strong>📝 Descrição:</strong> ${chamado.descricao}</p>
            ${chamado.usuario ? `<p><strong>👤 Solicitante:</strong> ${chamado.usuario.nome}</p>` : ''}
            ${chamado.responsavel ? `<p><strong>👷 Responsável:</strong> ${chamado.responsavel.nome}</p>` : ''}
            ${chamado.foto_antes ? `<p><strong>📸 Foto:</strong><br><img src="${chamado.foto_antes}" style="max-width: 100%; border-radius: 8px; margin-top: 10px;"></p>` : ''}
            ${chamado.foto_depois ? `<p><strong>📸 Foto Depois:</strong><br><img src="${chamado.foto_depois}" style="max-width: 100%; border-radius: 8px; margin-top: 10px;"></p>` : ''}
            ${chamado.avaliacao ? `<p><strong>⭐ Avaliação:</strong> ${'⭐'.repeat(chamado.avaliacao)} (${chamado.avaliacao}/5)</p>` : ''}
            ${chamado.comentario_avaliacao ? `<p><strong>💬 Comentário:</strong> ${chamado.comentario_avaliacao}</p>` : ''}
            <p><strong>🕒 Criado em:</strong> ${formatDate(chamado.created_at)}</p>
            ${chamado.data_resolucao ? `<p><strong>✅ Resolvido em:</strong> ${formatDate(chamado.data_resolucao)}</p>` : ''}
            ${acoesHTML}
        `;

        modal.classList.add('active');
        hideLoading();
    } catch (error) {
        showToast('Erro ao carregar detalhes', 'error');
        hideLoading();
    }
}

// Função para atualizar status (EQUIPE/GESTOR)
window.atualizarStatus = async function(chamadoId) {
    const novoStatus = document.getElementById('modalStatus').value;
    
    try {
        showLoading();
        const response = await fetch(`${API_URL}/chamados/${chamadoId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: novoStatus })
        });

        if (!response.ok) {
            throw new Error('Erro ao atualizar status');
        }

        showToast('Status atualizado com sucesso! ✅', 'success');
        closeModal();
        await loadChamados();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
};

// Função para avaliar chamado (CIDADÃO)
window.avaliarChamado = async function(chamadoId) {
    const avaliacao = parseInt(document.getElementById('modalAvaliacao').value);
    const comentario = document.getElementById('modalComentario').value;
    
    try {
        showLoading();
        const response = await fetch(`${API_URL}/chamados/${chamadoId}/avaliar`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                avaliacao: avaliacao,
                comentario_avaliacao: comentario || null
            })
        });

        if (!response.ok) {
            throw new Error('Erro ao avaliar chamado');
        }

        showToast('Avaliação enviada com sucesso! ⭐', 'success');
        closeModal();
        await loadChamados();
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
};

// Função para selecionar estrelas
window.setAvaliacao = function(nota) {
    document.getElementById('modalAvaliacao').value = nota;
    
    // Destacar estrelas selecionadas
    document.querySelectorAll('[data-star]').forEach(star => {
        const starNum = parseInt(star.dataset.star);
        if (starNum <= nota) {
            star.style.opacity = '1';
            star.style.filter = 'brightness(1.2)';
        } else {
            star.style.opacity = '0.3';
            star.style.filter = 'grayscale(1)';
        }
    });
};

async function handleNovoChamado(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('titulo', document.getElementById('chamadoTitulo').value);
    formData.append('descricao', document.getElementById('chamadoDescricao').value);
    formData.append('endereco', document.getElementById('chamadoEndereco').value);
    formData.append('categoria_id', document.getElementById('chamadoCategoria').value);

    const bairroId = document.getElementById('chamadoBairro').value;
    if (bairroId) formData.append('bairro_id', bairroId);

    const latitude = document.getElementById('chamadoLatitude').value;
    if (latitude) formData.append('latitude', latitude);

    const longitude = document.getElementById('chamadoLongitude').value;
    if (longitude) formData.append('longitude', longitude);

    const foto = document.getElementById('chamadoFoto').files[0];
    if (foto) formData.append('foto', foto);

    try {
        showLoading();
        const response = await fetch(`${API_URL}/chamados`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao criar chamado');
        }

        const chamado = await response.json();
        
        showToast(`Chamado criado! 📋 Protocolo: ${chamado.protocolo}`, 'success');
        document.getElementById('novoChamadoForm').reset();
        switchView('chamados');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// ========== CATEGORIAS E BAIRROS ========== //
async function loadCategorias() {
    try {
        const response = await fetch(`${API_URL}/categorias`);
        categorias = await response.json();

        const select = document.getElementById('chamadoCategoria');
        select.innerHTML = '<option value="">Selecione...</option>' +
            categorias.map(c => `<option value="${c.id}">${c.icone} ${c.nome}</option>`).join('');
    } catch (error) {
        console.error('Erro ao carregar categorias:', error);
    }
}

async function loadBairros() {
    try {
        const response = await fetch(`${API_URL}/bairros`);
        bairros = await response.json();

        const select = document.getElementById('chamadoBairro');
        select.innerHTML = '<option value="">Selecione...</option>' +
            bairros.map(b => `<option value="${b.id}">${b.nome}</option>`).join('');
    } catch (error) {
        console.error('Erro ao carregar bairros:', error);
    }
}

// ========== DASHBOARD (GESTOR) ========== //
async function loadDashboard() {
    try {
        // Carregar a tab "Visão Geral" do dashboard.js
        await loadVisaoGeral();
    } catch (error) {
        showToast('Erro ao carregar dashboard', 'error');
        console.error(error);
    }
}

// ========== UTILITIES ========== //
function showLoading() {
    loading.classList.add('active');
}

function hideLoading() {
    loading.classList.remove('active');
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function closeModal() {
    document.getElementById('chamadoModal').classList.remove('active');
}

function formatStatus(status) {
    const statusMap = {
        'aberto': 'Aberto',
        'em_andamento': 'Em Andamento',
        'resolvido': 'Resolvido',
        'cancelado': 'Cancelado'
    };
    return statusMap[status] || status;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========== GEOLOCALIZAÇÃO ========== //

// Inicializar Mapa
function initMap() {
    // Se o mapa já existe, não criar de novo
    if (map) {
        map.invalidateSize();
        return;
    }

    // Coordenadas de Belém, PA
    const belemLat = -1.4558;
    const belemLng = -48.4902;

    // Criar mapa
    map = L.map('map').setView([belemLat, belemLng], 13);

    // Adicionar camada do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Ícone customizado para o marcador
    const customIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    // Adicionar marcador inicial (Belém centro)
    marker = L.marker([belemLat, belemLng], {
        icon: customIcon,
        draggable: true
    }).addTo(map);

    marker.bindPopup('📍 Arraste o marcador ou clique no mapa para escolher a localização').openPopup();

    // Evento ao arrastar o marcador
    marker.on('dragend', function(e) {
        const position = marker.getLatLng();
        updateLocation(position.lat, position.lng);
    });

    // Evento ao clicar no mapa
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Mover marcador
        marker.setLatLng([lat, lng]);
        marker.bindPopup('📍 Localização selecionada').openPopup();
        
        // Atualizar campos
        updateLocation(lat, lng);
    });
}

// Atualizar localização no formulário
async function updateLocation(lat, lng) {
    // Preencher campos
    document.getElementById('chamadoLatitude').value = lat.toFixed(6);
    document.getElementById('chamadoLongitude').value = lng.toFixed(6);

    // Atualizar instruções
    const instructions = document.getElementById('mapInstructions');
    instructions.innerHTML = '✅ Localização selecionada no mapa!';
    instructions.classList.add('success');

    // Tentar obter endereço
    try {
        const endereco = await reverseGeocode(lat, lng);
        if (endereco) {
            document.getElementById('chamadoEndereco').value = endereco;
            showToast('📍 Localização atualizada!', 'success');
        }
    } catch (error) {
        console.log('Não foi possível obter o endereço automaticamente');
    }
}

function getGeolocation() {
    const locationStatus = document.getElementById('locationStatus');
    const btnGeolocation = document.getElementById('btnGeolocation');
    
    // Verificar se o navegador suporta geolocalização
    if (!navigator.geolocation) {
        showToast('🚫 Seu navegador não suporta geolocalização', 'error');
        return;
    }

    // Atualizar UI
    btnGeolocation.disabled = true;
    btnGeolocation.textContent = '📍 Obtendo localização...';
    locationStatus.textContent = 'Aguarde, obtendo sua localização...';
    locationStatus.style.color = 'var(--info)';

    // Obter posição
    navigator.geolocation.getCurrentPosition(
        async function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const accuracy = position.coords.accuracy;

            // Preencher campos
            document.getElementById('chamadoLatitude').value = lat.toFixed(6);
            document.getElementById('chamadoLongitude').value = lng.toFixed(6);

            // Atualizar mapa
            if (map && marker) {
                map.setView([lat, lng], 16); // Zoom mais próximo
                marker.setLatLng([lat, lng]);
                marker.bindPopup('🎯 Sua localização atual').openPopup();
            }

            // Tentar obter endereço
            try {
                const endereco = await reverseGeocode(lat, lng);
                if (endereco) {
                    document.getElementById('chamadoEndereco').value = endereco;
                }
                
                locationStatus.textContent = `✅ Localização obtida! (precisão: ${Math.round(accuracy)}m)`;
                locationStatus.style.color = 'var(--success)';
                showToast('🎯 Localização obtida com sucesso!', 'success');
            } catch (error) {
                locationStatus.textContent = `✅ Coordenadas obtidas! (${lat.toFixed(4)}, ${lng.toFixed(4)})`;
                locationStatus.style.color = 'var(--success)';
                showToast('📍 Coordenadas obtidas! Preencha o endereço manualmente.', 'success');
            }

            // Restaurar botão
            btnGeolocation.disabled = false;
            btnGeolocation.textContent = '📍 Usar Minha Localização Atual';
        },
        function(error) {
            let errorMessage = '❌ Erro ao obter localização: ';
            
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage += 'Permissão negada. Permita o acesso à localização nas configurações do navegador.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage += 'Localização indisponível. Verifique se o GPS está ativado.';
                    break;
                case error.TIMEOUT:
                    errorMessage += 'Tempo esgotado. Tente novamente.';
                    break;
                default:
                    errorMessage += 'Erro desconhecido.';
            }

            locationStatus.textContent = errorMessage;
            locationStatus.style.color = 'var(--danger)';
            showToast(errorMessage, 'error');

            // Restaurar botão
            btnGeolocation.disabled = false;
            btnGeolocation.textContent = '📍 Usar Minha Localização Atual';
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

// Reverse Geocoding - Converte coordenadas em endereço
async function reverseGeocode(lat, lng) {
    try {
        // Usando Nominatim (OpenStreetMap) - gratuito e sem API key
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`,
            {
                headers: {
                    'User-Agent': 'Sistema-Zeladoria-Belem'
                }
            }
        );

        if (!response.ok) {
            throw new Error('Erro ao buscar endereço');
        }

        const data = await response.json();
        
        // Montar endereço brasileiro
        const address = data.address;
        let endereco = '';

        if (address.road) {
            endereco += address.road;
            if (address.house_number) {
                endereco += ', ' + address.house_number;
            }
        } else if (address.pedestrian) {
            endereco += address.pedestrian;
        } else if (address.neighbourhood) {
            endereco += address.neighbourhood;
        }

        if (address.suburb) {
            endereco += ' - ' + address.suburb;
        } else if (address.neighbourhood && !endereco.includes(address.neighbourhood)) {
            endereco += ' - ' + address.neighbourhood;
        }

        if (address.city) {
            endereco += ', ' + address.city;
        }

        if (address.state) {
            endereco += ' - ' + address.state;
        }

        return endereco || data.display_name;
    } catch (error) {
        console.error('Erro no reverse geocoding:', error);
        return null;
    }
}
