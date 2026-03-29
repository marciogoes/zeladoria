/**
 * CATÁLOGO DE SERVIÇOS - PREFEITURA DE BELÉM
 * Sistema de Zeladoria Urbana
 */

console.log('🚀 Catálogo de Serviços carregado!');

// ============================================
// VARIÁVEIS GLOBAIS
// ============================================

let secretarias = [];
let servicos = [];
let servicosFiltrados = [];
const API_BASE_URL = 'http://localhost:8001/api';

// ============================================
// INICIALIZAÇÃO
// ============================================

window.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM carregado');
    inicializar();
});

async function inicializar() {
    try {
        // Tentar carregar do backend
        await carregarDados();
    } catch (error) {
        console.warn('⚠️ Backend indisponível, usando dados de exemplo');
        // Usar dados mock
        secretarias = gerarSecretariasMock();
        servicos = gerarServicosMock();
    }
    
    atualizarEstatisticas();
    popularFiltroSecretarias();
    configurarEventListeners();
    aplicarFiltros();
    
    console.log('✅ Catálogo inicializado!');
}

async function carregarDados() {
    try {
        const [resSecretarias, resServicos] = await Promise.all([
            fetch(`${API_BASE_URL}/secretarias`),
            fetch(`${API_BASE_URL}/servicos`)
        ]);
        
        if (resSecretarias.ok) {
            secretarias = await resSecretarias.json();
            console.log(`✅ ${secretarias.length} secretarias carregadas`);
        } else {
            throw new Error('API não disponível');
        }
        
        if (resServicos.ok) {
            servicos = await resServicos.json();
            console.log(`✅ ${servicos.length} serviços carregados`);
        } else {
            throw new Error('API não disponível');
        }
    } catch (error) {
        console.warn('Usando dados mock:', error.message);
        throw error;
    }
}

// ============================================
// EVENT LISTENERS
// ============================================

function configurarEventListeners() {
    document.getElementById('busca').addEventListener('input', aplicarFiltros);
    document.getElementById('filtro-secretaria').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-prioridade').addEventListener('change', aplicarFiltros);
    document.getElementById('filtro-status').addEventListener('change', aplicarFiltros);
}

// ============================================
// FILTROS E ORDENAÇÃO
// ============================================

function aplicarFiltros() {
    const busca = document.getElementById('busca').value.toLowerCase();
    const secretaria = document.getElementById('filtro-secretaria').value;
    const prioridade = document.getElementById('filtro-prioridade').value;
    const status = document.getElementById('filtro-status').value;

    servicosFiltrados = servicos.filter(s => {
        const matchBusca = !busca || 
            s.nome.toLowerCase().includes(busca) || 
            s.descricao.toLowerCase().includes(busca) ||
            s.categoria.toLowerCase().includes(busca);
        const matchSec = !secretaria || s.secretaria_id == secretaria;
        const matchPrio = !prioridade || s.prioridade === prioridade;
        const matchStatus = !status || s.status === status;
        return matchBusca && matchSec && matchPrio && matchStatus;
    });

    aplicarOrdenacao();
}

function aplicarOrdenacao() {
    const ord = document.getElementById('ordenacao').value;
    servicosFiltrados.sort((a, b) => {
        if (ord === 'nome-asc') return a.nome.localeCompare(b.nome);
        if (ord === 'nome-desc') return b.nome.localeCompare(a.nome);
        if (ord === 'sla-asc') return a.sla_horas - b.sla_horas;
        if (ord === 'sla-desc') return b.sla_horas - a.sla_horas;
        return 0;
    });
    renderizar();
}

function limparFiltros() {
    document.getElementById('busca').value = '';
    document.getElementById('filtro-secretaria').value = '';
    document.getElementById('filtro-prioridade').value = '';
    document.getElementById('filtro-status').value = '';
    document.getElementById('ordenacao').value = 'nome-asc';
    aplicarFiltros();
}

// ============================================
// RENDERIZAÇÃO
// ============================================

function renderizar() {
    const grid = document.getElementById('servicos-grid');
    const empty = document.getElementById('empty-state');
    const contador = document.getElementById('contador');

    contador.textContent = `${servicosFiltrados.length} ${servicosFiltrados.length === 1 ? 'serviço' : 'serviços'}`;

    if (servicosFiltrados.length === 0) {
        grid.innerHTML = '';
        empty.style.display = 'block';
        return;
    }

    empty.style.display = 'none';
    grid.innerHTML = servicosFiltrados.map(s => criarCardHTML(s)).join('');
    
    console.log(`✅ ${servicosFiltrados.length} serviços renderizados`);
}

function criarCardHTML(s) {
    const sec = secretarias.find(sec => sec.id === s.secretaria_id);
    const slaTexto = formatarSLA(s.sla_horas);
    
    return `
        <div class="servico-card" onclick="abrirModal(${s.id})">
            <div class="servico-header">
                <div class="servico-codigo">${s.codigo}</div>
                <span class="badge-status ${s.status || 'ativo'}">${s.status || 'ativo'}</span>
            </div>
            <h3 class="servico-titulo">${s.nome}</h3>
            <div class="servico-secretaria">
                <span>🏛️</span>
                <span>${sec ? sec.nome : 'Secretaria não encontrada'}</span>
            </div>
            <p class="servico-descricao">${s.descricao}</p>
            <div class="servico-categorias">
                <span class="categoria-tag">📁 ${s.categoria}</span>
                ${s.subcategoria ? `<span class="categoria-tag">📂 ${s.subcategoria}</span>` : ''}
            </div>
            <div class="servico-footer">
                <div class="sla-info">
                    <div class="sla-label">SLA de Atendimento</div>
                    <div class="sla-valor">⏱️ ${slaTexto}</div>
                </div>
                <span class="prioridade-badge ${s.prioridade || 'media'}">${s.prioridade || 'media'}</span>
            </div>
        </div>
    `;
}

// ============================================
// MODAL
// ============================================

function abrirModal(id) {
    const s = servicos.find(serv => serv.id === id);
    if (!s) return;
    
    const sec = secretarias.find(sec => sec.id === s.secretaria_id);
    const slaTexto = formatarSLA(s.sla_horas);

    document.getElementById('modal-codigo').textContent = s.codigo;
    document.getElementById('modal-titulo').textContent = s.nome;
    document.getElementById('modal-secretaria').textContent = '🏛️ ' + (sec ? sec.nome : 'N/A');
    document.getElementById('modal-descricao').textContent = s.descricao;
    document.getElementById('modal-sla').textContent = slaTexto;
    document.getElementById('modal-categoria').textContent = s.categoria;
    document.getElementById('modal-subcategoria').textContent = s.subcategoria || 'N/A';
    document.getElementById('modal-prioridade').innerHTML = `<span class="prioridade-badge ${s.prioridade || 'media'}">${s.prioridade || 'media'}</span>`;

    document.getElementById('modal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function fecharModal() {
    document.getElementById('modal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function solicitarServico() {
    alert('🚀 Redirecionando para criar chamado...');
    window.location.href = 'index.html';
}

// ============================================
// ESTATÍSTICAS
// ============================================

function atualizarEstatisticas() {
    document.getElementById('total-secretarias').textContent = secretarias.length;
    document.getElementById('total-servicos').textContent = servicos.length;
    
    const emergenciais = servicos.filter(s => s.prioridade === 'emergencial').length;
    document.getElementById('servicos-emergenciais').textContent = emergenciais;
    
    const slaTotal = servicos.reduce((sum, s) => sum + (s.sla_horas || 0), 0);
    const slaMedio = servicos.length > 0 ? Math.floor(slaTotal / servicos.length) : 0;
    document.getElementById('sla-medio').textContent = formatarSLA(slaMedio);
}

function popularFiltroSecretarias() {
    const select = document.getElementById('filtro-secretaria');
    secretarias.forEach(sec => {
        const option = document.createElement('option');
        option.value = sec.id;
        option.textContent = (sec.sigla || '') + ' - ' + sec.nome;
        select.appendChild(option);
    });
}

// ============================================
// UTILIDADES
// ============================================

function formatarSLA(horas) {
    if (!horas) return 'N/A';
    if (horas < 24) return horas + 'h';
    const dias = Math.floor(horas / 24);
    const horasRestantes = horas % 24;
    return horasRestantes > 0 ? `${dias}d ${horasRestantes}h` : `${dias} dias`;
}

// ============================================
// DADOS MOCK (FALLBACK)
// ============================================

function gerarSecretariasMock() {
    return [
        { id: 1, sigla: 'SEURB', nome: 'Secretaria de Urbanismo' },
        { id: 2, sigla: 'SESAN', nome: 'Secretaria de Saneamento' },
        { id: 3, sigla: 'SECON', nome: 'Secretaria de Economia' },
        { id: 4, sigla: 'SESMA', nome: 'Secretaria de Saúde' },
        { id: 5, sigla: 'SEMEC', nome: 'Secretaria de Educação' }
    ];
}

function gerarServicosMock() {
    return [
        {
            id: 1,
            codigo: 'SEURB-001',
            nome: 'Reparo de Iluminação Pública',
            descricao: 'Solicitação de reparo ou substituição de postes e luminárias de iluminação pública',
            categoria: 'Iluminação',
            subcategoria: 'Manutenção',
            secretaria_id: 1,
            sla_horas: 48,
            prioridade: 'alta',
            status: 'ativo'
        },
        {
            id: 2,
            codigo: 'SEURB-002',
            nome: 'Tapa-buraco em Via Pública',
            descricao: 'Solicitação de correção de buracos em vias públicas',
            categoria: 'Pavimentação',
            subcategoria: 'Emergencial',
            secretaria_id: 1,
            sla_horas: 24,
            prioridade: 'emergencial',
            status: 'ativo'
        },
        {
            id: 3,
            codigo: 'SESAN-001',
            nome: 'Limpeza de Terreno Baldio',
            descricao: 'Limpeza e remoção de lixo e entulho em terrenos baldios',
            categoria: 'Limpeza Urbana',
            subcategoria: 'Terrenos',
            secretaria_id: 2,
            sla_horas: 120,
            prioridade: 'media',
            status: 'ativo'
        },
        {
            id: 4,
            codigo: 'SESAN-002',
            nome: 'Coleta de Lixo Irregular',
            descricao: 'Solicitação de coleta especial de lixo acumulado',
            categoria: 'Coleta de Resíduos',
            subcategoria: 'Coleta Especial',
            secretaria_id: 2,
            sla_horas: 72,
            prioridade: 'media',
            status: 'ativo'
        },
        {
            id: 5,
            codigo: 'SEURB-003',
            nome: 'Poda de Árvore',
            descricao: 'Solicitação de poda ou remoção de árvores em áreas públicas',
            categoria: 'Arborização',
            subcategoria: 'Manutenção',
            secretaria_id: 1,
            sla_horas: 168,
            prioridade: 'baixa',
            status: 'ativo'
        },
        {
            id: 6,
            codigo: 'SECON-001',
            nome: 'Emissão de Alvará',
            descricao: 'Solicitação de alvará de funcionamento para estabelecimentos comerciais',
            categoria: 'Licenciamento',
            subcategoria: 'Alvará',
            secretaria_id: 3,
            sla_horas: 240,
            prioridade: 'agendavel',
            status: 'ativo'
        }
    ];
}

console.log('✅ Script do Catálogo carregado!');
