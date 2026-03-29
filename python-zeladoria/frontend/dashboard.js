// Função melhorada de dashboard com tratamento de erros
async function loadDashboard() {
    showLoading();
    
    try {
        console.log('🔍 Carregando dashboard...');
        
        const response = await apiRequest('/relatorios/dashboard');
        
        console.log('📊 Status da resposta:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('❌ Erro do servidor:', errorData);
            throw new Error(errorData.detail || 'Erro ao carregar dashboard');
        }
        
        const data = await response.json();
        console.log('✅ Dados recebidos:', data);
        
        // Total de chamados
        document.getElementById('stat-total').textContent = data.total_chamados || 0;
        
        // Em andamento
        const emAndamento = data.por_status?.find(s => s.status === 'em_andamento');
        document.getElementById('stat-andamento').textContent = emAndamento?.total || 0;
        
        // Resolvidos
        const resolvidos = data.por_status?.find(s => s.status === 'resolvido');
        document.getElementById('stat-resolvidos').textContent = resolvidos?.total || 0;
        
        // Avaliação média
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
            categoriasContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhuma categoria com chamados ainda</p>';
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
            bairrosContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 20px;">Nenhum bairro com chamados ainda</p>';
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
            recentesContainer.innerHTML = '<p style="text-align: center; color: var(--secondary); padding: 40px;">Nenhum chamado ainda. Crie o primeiro!</p>';
        }
        
        console.log('✅ Dashboard carregado com sucesso!');
        
    } catch (error) {
        console.error('❌ Erro ao carregar dashboard:', error);
        showToast('Erro ao carregar dashboard: ' + error.message, 'error');
        
        // Mostrar mensagem de erro na página
        document.getElementById('chart-categorias').innerHTML = 
            `<p style="text-align: center; color: #ef4444; padding: 20px;">
                ❌ Erro ao carregar dados do dashboard.<br>
                ${error.message}<br><br>
                <button class="btn btn-primary" onclick="loadDashboard()">🔄 Tentar Novamente</button>
            </p>`;
    } finally {
        hideLoading();
    }
}
