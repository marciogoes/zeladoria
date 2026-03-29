// ==========================================
// DASHBOARD EXECUTIVO - ADMIN E GESTOR
// ==========================================

async function loadDashboardExecutivo() {
    showLoading();
    
    try {
        console.log('🔍 Carregando dashboard executivo...');
        
        const response = await apiRequest('/relatorios/dashboard');
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro ao carregar dashboard');
        }
        
        const data = await response.json();
        console.log('✅ Dados recebidos:', data);
        
        // ========== ESTATÍSTICAS PRINCIPAIS ==========
        document.getElementById('stat-total').textContent = data.total_chamados || 0;
        
        const emAndamento = data.por_status?.find(s => s.status === 'em_andamento');
        document.getElementById('stat-andamento').textContent = emAndamento?.total || 0;
        
        const resolvidos = data.por_status?.find(s => s.status === 'resolvido');
        document.getElementById('stat-resolvidos').textContent = resolvidos?.total || 0;
        
        document.getElementById('stat-avaliacao').textContent = (data.avaliacao_media || 0).toFixed(1);
        
        // ========== MÉTRICAS EXECUTIVAS ==========
        
        // Taxa de resolução
        const taxaResolucao = data.total_chamados > 0 
            ? ((resolvidos?.total || 0) / data.total_chamados * 100).toFixed(1)
            : 0;
        document.getElementById('stat-taxa-resolucao').textContent = taxaResolucao + '%';
        
        // Chamados abertos
        const abertos = data.por_status?.find(s => s.status === 'aberto');
        document.getElementById('stat-abertos').textContent = abertos?.total || 0;
        
        // Tempo médio de resolução (estimado - 3 dias por chamado resolvido)
        const tempoMedio = (resolvidos?.total || 0) > 0 ? 3 : 0;
        document.getElementById('stat-tempo-medio').textContent = tempoMedio + ' dias';
        
        // Chamados críticos
        const criticos = data.por_prioridade?.find(p => p.prioridade === 'critica');
        document.getElementById('stat-criticos').textContent = criticos?.total || 0;
        
        // ========== GRÁFICO: EVOLUÇÃO MENSAL ==========
        renderGraficoEvolucao(data);
        
        // ========== GRÁFICO: STATUS ==========
        renderGraficoStatus(data);
        
        // ========== GRÁFICO: PRIORIDADES ==========
        renderGraficoPrioridades(data);
        
        // ========== TOP CATEGORIAS ==========
        const categoriasContainer = document.getElementById('chart-categorias');
        if (data.top_categorias && data.top_categorias.length > 0) {
            const categoriasHtml = data.top_categorias.map(item => {
                const percentage = data.total_chamados > 0 
                    ? (item.total / data.total_chamados * 100).toFixed(1) 
                    : 0;
                return `
                    <div class="chart-item">
                        <div class="chart-label">
                            <span>${item.categoria.icone || '📌'} ${item.categoria.nome}</span>
                            <span><strong>${item.total}</strong> (${percentage}%)</span>
                        </div>
                        <div class="chart-bar">
                            <div class="chart-fill" style="width: ${percentage}%; background: #3b82f6;"></div>
                        </div>
                    </div>
                `;
            }).join('');
            categoriasContainer.innerHTML = categoriasHtml;
        } else {
            categoriasContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhuma categoria com chamados</p>';
        }
        
        // ========== TOP BAIRROS ==========
        const bairrosContainer = document.getElementById('chart-bairros');
        if (data.top_bairros && data.top_bairros.length > 0) {
            const bairrosHtml = data.top_bairros.map(item => {
                const percentage = data.total_chamados > 0 
                    ? (item.total / data.total_chamados * 100).toFixed(1) 
                    : 0;
                return `
                    <div class="chart-item">
                        <div class="chart-label">
                            <span>🏘️ ${item.bairro.nome}</span>
                            <span><strong>${item.total}</strong> (${percentage}%)</span>
                        </div>
                        <div class="chart-bar">
                            <div class="chart-fill" style="width: ${percentage}%; background: #10b981;"></div>
                        </div>
                    </div>
                `;
            }).join('');
            bairrosContainer.innerHTML = bairrosHtml;
        } else {
            bairrosContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhum bairro com chamados</p>';
        }
        
        // ========== CHAMADOS RECENTES ==========
        const recentesContainer = document.getElementById('chamados-recentes');
        if (data.recentes && data.recentes.length > 0) {
            const recentesHtml = data.recentes.slice(0, 6).map(chamado => `
                <div class="card" onclick="showDetails(${chamado.id})" style="cursor: pointer;">
                    <div class="card-header">
                        <div>
                            <div class="card-title">${chamado.titulo}</div>
                            <div class="card-protocolo">${chamado.protocolo}</div>
                        </div>
                        <span class="badge ${chamado.status}">${formatStatus(chamado.status)}</span>
                    </div>
                    <div class="card-info">
                        <div>
                            <span>🏷️</span>
                            <span>${chamado.categoria?.nome || 'N/A'}</span>
                        </div>
                        <div>
                            <span>⚠️</span>
                            <span class="badge ${chamado.prioridade}">${formatPrioridade(chamado.prioridade)}</span>
                        </div>
                        <div>
                            <span>📅</span>
                            <span>${formatDate(chamado.created_at || chamado.data_criacao)}</span>
                        </div>
                    </div>
                </div>
            `).join('');
            recentesContainer.innerHTML = recentesHtml;
        } else {
            recentesContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 40px;">Nenhum chamado ainda</p>';
        }
        
        console.log('✅ Dashboard executivo carregado!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar dashboard:', error);
        showToast('Erro ao carregar dashboard: ' + error.message, 'error');
        
        document.getElementById('chart-categorias').innerHTML = 
            `<p style="text-align: center; color: #ef4444; padding: 20px;">
                ❌ Erro ao carregar dados.<br>
                ${error.message}<br><br>
                <button class="btn btn-primary" onclick="loadDashboard()">🔄 Tentar Novamente</button>
            </p>`;
    } finally {
        hideLoading();
    }
}

// ==========================================
// GRÁFICOS EXECUTIVOS
// ==========================================

function renderGraficoStatus(data) {
    const container = document.getElementById('grafico-status');
    if (!container) return;
    
    const statusData = data.por_status || [];
    const total = data.total_chamados || 0;
    
    if (statusData.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #6c757d;">Sem dados</p>';
        return;
    }
    
    const statusColors = {
        'aberto': '#3b82f6',
        'em_andamento': '#f59e0b',
        'resolvido': '#10b981',
        'cancelado': '#ef4444'
    };
    
    const html = statusData.map(item => {
        const percentage = total > 0 ? (item.total / total * 100).toFixed(1) : 0;
        const color = statusColors[item.status] || '#6c757d';
        
        return `
            <div class="chart-item">
                <div class="chart-label">
                    <span>${formatStatus(item.status)}</span>
                    <span><strong>${item.total}</strong> (${percentage}%)</span>
                </div>
                <div class="chart-bar">
                    <div class="chart-fill" style="width: ${percentage}%; background: ${color};"></div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

function renderGraficoPrioridades(data) {
    const container = document.getElementById('grafico-prioridades');
    if (!container) return;
    
    const prioridadeData = data.por_prioridade || [];
    const total = data.total_chamados || 0;
    
    if (prioridadeData.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #6c757d;">Sem dados</p>';
        return;
    }
    
    const prioridadeColors = {
        'critica': '#ef4444',
        'alta': '#f97316',
        'media': '#f59e0b',
        'baixa': '#3b82f6',
        'agendavel': '#6c757d'
    };
    
    const prioridadeOrder = ['critica', 'alta', 'media', 'baixa', 'agendavel'];
    const sortedData = prioridadeData.sort((a, b) => {
        return prioridadeOrder.indexOf(a.prioridade) - prioridadeOrder.indexOf(b.prioridade);
    });
    
    const html = sortedData.map(item => {
        const percentage = total > 0 ? (item.total / total * 100).toFixed(1) : 0;
        const color = prioridadeColors[item.prioridade] || '#6c757d';
        
        return `
            <div class="chart-item">
                <div class="chart-label">
                    <span>${formatPrioridade(item.prioridade)}</span>
                    <span><strong>${item.total}</strong> (${percentage}%)</span>
                </div>
                <div class="chart-bar">
                    <div class="chart-fill" style="width: ${percentage}%; background: ${color};"></div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

function renderGraficoEvolucao(data) {
    const container = document.getElementById('grafico-evolucao');
    if (!container) return;
    
    // Dados simulados de evolução mensal
    // Em produção, isso viria do backend
    const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'];
    const valores = [12, 19, 15, 25, 22, (data.total_chamados || 0)];
    const maxValor = Math.max(...valores);
    
    const html = meses.map((mes, index) => {
        const valor = valores[index];
        const percentage = maxValor > 0 ? (valor / maxValor * 100).toFixed(1) : 0;
        
        return `
            <div style="display: flex; flex-direction: column; align-items: center; gap: 8px; flex: 1;">
                <div style="width: 100%; height: 150px; background: #f1f5f9; border-radius: 8px; position: relative; display: flex; align-items: flex-end; justify-content: center;">
                    <div style="width: 60%; height: ${percentage}%; background: linear-gradient(180deg, #3b82f6 0%, #1e40af 100%); border-radius: 8px 8px 0 0; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600;">
                        ${valor > 0 ? valor : ''}
                    </div>
                </div>
                <span style="font-size: 0.85rem; color: #6c757d; font-weight: 500;">${mes}</span>
            </div>
        `;
    }).join('');
    
    container.innerHTML = `<div style="display: flex; gap: 12px; align-items: flex-end;">${html}</div>`;
}

// ==========================================
// VERIFICAR TIPO DE USUÁRIO E CARREGAR DASHBOARD APROPRIADO
// ==========================================

function loadDashboard() {
    // Verificar se é admin ou gestor
    if (currentUser && (currentUser.tipo === 'admin' || currentUser.tipo === 'gestor')) {
        console.log('👑 Carregando dashboard executivo para', currentUser.tipo);
        loadDashboardExecutivo();
    } else {
        console.log('👤 Carregando dashboard padrão');
        loadDashboardPadrao();
    }
}

// Dashboard padrão para outros usuários
async function loadDashboardPadrao() {
    showLoading();
    
    try {
        const response = await apiRequest('/relatorios/dashboard');
        
        if (!response.ok) {
            throw new Error('Erro ao carregar dashboard');
        }
        
        const data = await response.json();
        
        // Estatísticas básicas
        document.getElementById('stat-total').textContent = data.total_chamados || 0;
        
        const emAndamento = data.por_status?.find(s => s.status === 'em_andamento');
        document.getElementById('stat-andamento').textContent = emAndamento?.total || 0;
        
        const resolvidos = data.por_status?.find(s => s.status === 'resolvido');
        document.getElementById('stat-resolvidos').textContent = resolvidos?.total || 0;
        
        document.getElementById('stat-avaliacao').textContent = (data.avaliacao_media || 0).toFixed(1);
        
        // Top Categorias
        const categoriasContainer = document.getElementById('chart-categorias');
        if (data.top_categorias && data.top_categorias.length > 0) {
            const categoriasHtml = data.top_categorias.map(item => {
                const percentage = data.total_chamados > 0 
                    ? (item.total / data.total_chamados * 100).toFixed(1) 
                    : 0;
                return `
                    <div class="chart-item">
                        <div class="chart-label">
                            <span>${item.categoria.icone || '📌'} ${item.categoria.nome}</span>
                            <span><strong>${item.total}</strong> (${percentage}%)</span>
                        </div>
                        <div class="chart-bar">
                            <div class="chart-fill" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
            categoriasContainer.innerHTML = categoriasHtml;
        } else {
            categoriasContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhum dado disponível</p>';
        }
        
        // Top Bairros
        const bairrosContainer = document.getElementById('chart-bairros');
        if (data.top_bairros && data.top_bairros.length > 0) {
            const bairrosHtml = data.top_bairros.map(item => {
                const percentage = data.total_chamados > 0 
                    ? (item.total / data.total_chamados * 100).toFixed(1) 
                    : 0;
                return `
                    <div class="chart-item">
                        <div class="chart-label">
                            <span>🏘️ ${item.bairro.nome}</span>
                            <span><strong>${item.total}</strong> (${percentage}%)</span>
                        </div>
                        <div class="chart-bar">
                            <div class="chart-fill" style="width: ${percentage}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
            bairrosContainer.innerHTML = bairrosHtml;
        } else {
            bairrosContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhum dado disponível</p>';
        }
        
        // Chamados Recentes
        const recentesContainer = document.getElementById('chamados-recentes');
        if (data.recentes && data.recentes.length > 0) {
            const recentesHtml = data.recentes.slice(0, 6).map(chamado => `
                <div class="card" onclick="showDetails(${chamado.id})">
                    <div class="card-header">
                        <div>
                            <div class="card-title">${chamado.titulo}</div>
                            <div class="card-protocolo">${chamado.protocolo}</div>
                        </div>
                        <span class="badge ${chamado.status}">${formatStatus(chamado.status)}</span>
                    </div>
                    <div class="card-info">
                        <div>
                            <span>🏷️</span>
                            <span>${chamado.categoria?.nome || 'N/A'}</span>
                        </div>
                        <div>
                            <span>📅</span>
                            <span>${formatDate(chamado.created_at || chamado.data_criacao)}</span>
                        </div>
                    </div>
                </div>
            `).join('');
            recentesContainer.innerHTML = recentesHtml;
        } else {
            recentesContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 40px;">Nenhum chamado recente</p>';
        }
        
    } catch (error) {
        console.error('❌ Erro ao carregar dashboard:', error);
        showToast('Erro ao carregar dashboard: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}
