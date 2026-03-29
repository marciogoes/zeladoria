// ========== FUNCIONALIDADES AVANÇADAS DO DASHBOARD ========== //

// Variáveis globais para gráficos
let chartInstances = {};

// ========== GRÁFICOS INTERATIVOS COM CHART.JS ========== //

function initChartJS() {
    // Verificar se Chart.js está disponível
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js não está carregado. Pulando inicialização de gráficos avançados.');
        return;
    }

    // Configuração global do Chart.js
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.font.size = 12;
}

// Gráfico de Pizza - Distribuição por Status
function renderPieChartStatus(data) {
    const ctx = document.getElementById('pieChartStatus');
    if (!ctx || typeof Chart === 'undefined') return;

    // Destruir gráfico anterior se existir
    if (chartInstances.pieStatus) {
        chartInstances.pieStatus.destroy();
    }

    const statusData = data.por_status || [];
    const labels = statusData.map(s => formatStatus(s.status));
    const values = statusData.map(s => s.total);
    const colors = ['#3b82f6', '#f59e0b', '#10b981', '#ef4444'];

    chartInstances.pieStatus = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de Linha - Evolução Temporal
function renderLineChartTemporal(data) {
    const ctx = document.getElementById('lineChartTemporal');
    if (!ctx || typeof Chart === 'undefined') return;

    if (chartInstances.lineTemporal) {
        chartInstances.lineTemporal.destroy();
    }

    // Simular dados dos últimos 30 dias
    const dias = [];
    const valores = [];
    const hoje = new Date();
    
    for (let i = 29; i >= 0; i--) {
        const data = new Date(hoje);
        data.setDate(data.getDate() - i);
        dias.push(data.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }));
        valores.push(Math.floor(Math.random() * 20) + 5);
    }

    chartInstances.lineTemporal = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dias,
            datasets: [{
                label: 'Chamados por Dia',
                data: valores,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 6,
                pointBackgroundColor: '#3b82f6'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

// Gráfico de Barras Horizontais - Top Categorias
function renderBarChartCategorias(data) {
    const ctx = document.getElementById('barChartCategorias');
    if (!ctx || typeof Chart === 'undefined') return;

    if (chartInstances.barCategorias) {
        chartInstances.barCategorias.destroy();
    }

    const categorias = data.top_categorias || [];
    const labels = categorias.map(c => c.categoria?.nome || 'N/A');
    const values = categorias.map(c => c.total);

    chartInstances.barCategorias = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Chamados',
                data: values,
                backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6'
                ],
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.x} chamados`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 10
                    }
                }
            }
        }
    });
}

// ========== FILTRO DE DATA PERSONALIZADO ========== //

function initDateFilters() {
    // Adicionar event listeners para filtros de data
    const periodoSelect = document.getElementById('reportPeriodo');
    const customDateContainer = document.getElementById('customDateContainer');
    
    if (periodoSelect) {
        periodoSelect.addEventListener('change', (e) => {
            if (e.target.value === 'custom') {
                showCustomDatePicker();
            } else {
                hideCustomDatePicker();
            }
        });
    }
}

function showCustomDatePicker() {
    const container = document.getElementById('customDateContainer');
    if (!container) {
        // Criar container se não existir
        const reportFilters = document.querySelector('.report-filters .form-row');
        if (reportFilters) {
            const customDiv = document.createElement('div');
            customDiv.id = 'customDateContainer';
            customDiv.style.gridColumn = '1 / -1';
            customDiv.innerHTML = `
                <div class="form-row" style="margin-top: 15px;">
                    <div class="form-group">
                        <label>Data Inicial</label>
                        <input type="date" id="dataInicial" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>Data Final</label>
                        <input type="date" id="dataFinal" class="form-control">
                    </div>
                </div>
            `;
            reportFilters.appendChild(customDiv);
        }
    } else {
        container.style.display = 'block';
    }
}

function hideCustomDatePicker() {
    const container = document.getElementById('customDateContainer');
    if (container) {
        container.style.display = 'none';
    }
}

function getDateRange(periodo) {
    const hoje = new Date();
    let dataInicio, dataFim;

    switch(periodo) {
        case 'hoje':
            dataInicio = new Date(hoje.setHours(0, 0, 0, 0));
            dataFim = new Date(hoje.setHours(23, 59, 59, 999));
            break;
        
        case 'semana':
            const primeiroDia = hoje.getDate() - hoje.getDay();
            dataInicio = new Date(hoje.setDate(primeiroDia));
            dataInicio.setHours(0, 0, 0, 0);
            dataFim = new Date(hoje.setDate(primeiroDia + 6));
            dataFim.setHours(23, 59, 59, 999);
            break;
        
        case 'mes':
            dataInicio = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
            dataFim = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0);
            dataFim.setHours(23, 59, 59, 999);
            break;
        
        case 'trimestre':
            const mesAtual = hoje.getMonth();
            const trimestreInicio = Math.floor(mesAtual / 3) * 3;
            dataInicio = new Date(hoje.getFullYear(), trimestreInicio, 1);
            dataFim = new Date(hoje.getFullYear(), trimestreInicio + 3, 0);
            dataFim.setHours(23, 59, 59, 999);
            break;
        
        case 'ano':
            dataInicio = new Date(hoje.getFullYear(), 0, 1);
            dataFim = new Date(hoje.getFullYear(), 11, 31);
            dataFim.setHours(23, 59, 59, 999);
            break;
        
        case 'custom':
            const dataInicialInput = document.getElementById('dataInicial');
            const dataFinalInput = document.getElementById('dataFinal');
            
            if (dataInicialInput && dataFinalInput && dataInicialInput.value && dataFinalInput.value) {
                dataInicio = new Date(dataInicialInput.value);
                dataFim = new Date(dataFinalInput.value);
                dataFim.setHours(23, 59, 59, 999);
            } else {
                return null;
            }
            break;
        
        default:
            dataInicio = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
            dataFim = new Date(hoje.getFullYear(), hoje.getMonth() + 1, 0);
            dataFim.setHours(23, 59, 59, 999);
    }

    return {
        inicio: dataInicio.toISOString(),
        fim: dataFim.toISOString(),
        inicioFormatado: dataInicio.toLocaleDateString('pt-BR'),
        fimFormatado: dataFim.toLocaleDateString('pt-BR')
    };
}

// ========== COMPARAÇÃO DE PERÍODOS ========== //

async function compararPeriodos() {
    const periodoAtual = document.getElementById('reportPeriodo').value;
    const datas = getDateRange(periodoAtual);
    
    if (!datas) {
        showToast('Selecione um período válido', 'error');
        return;
    }

    try {
        showLoading();
        
        // Buscar dados do período atual
        const responseAtual = await fetch(`${API_URL}/relatorios/periodo?inicio=${datas.inicio}&fim=${datas.fim}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        // Calcular período anterior (mesmo intervalo, mas deslocado para trás)
        const diasDiferenca = Math.ceil((new Date(datas.fim) - new Date(datas.inicio)) / (1000 * 60 * 60 * 24));
        const dataInicioAnterior = new Date(datas.inicio);
        dataInicioAnterior.setDate(dataInicioAnterior.getDate() - diasDiferenca);
        const dataFimAnterior = new Date(datas.inicio);
        dataFimAnterior.setDate(dataFimAnterior.getDate() - 1);
        
        // Buscar dados do período anterior
        const responseAnterior = await fetch(
            `${API_URL}/relatorios/periodo?inicio=${dataInicioAnterior.toISOString()}&fim=${dataFimAnterior.toISOString()}`,
            { headers: { 'Authorization': `Bearer ${authToken}` }}
        );
        
        const dadosAtual = await responseAtual.json();
        const dadosAnterior = await responseAnterior.json();
        
        renderComparacao(dadosAtual, dadosAnterior, datas);
        
        hideLoading();
    } catch (error) {
        console.error('Erro ao comparar períodos:', error);
        showToast('Erro ao comparar períodos. Usando dados simulados.', 'warning');
        
        // Simular comparação
        const dadosAtual = { total_chamados: 120, resolvidos: 85, avaliacaoMedia: 4.6 };
        const dadosAnterior = { total_chamados: 105, resolvidos: 72, avaliacaoMedia: 4.4 };
        renderComparacao(dadosAtual, dadosAnterior, datas);
        
        hideLoading();
    }
}

function renderComparacao(dadosAtual, dadosAnterior, datas) {
    const container = document.getElementById('reportResult');
    
    const calcularVariacao = (atual, anterior) => {
        if (anterior === 0) return 0;
        return (((atual - anterior) / anterior) * 100).toFixed(1);
    };
    
    const variacaoTotal = calcularVariacao(dadosAtual.total_chamados, dadosAnterior.total_chamados);
    const variacaoResolvidos = calcularVariacao(dadosAtual.resolvidos, dadosAnterior.resolvidos);
    const variacaoAvaliacao = calcularVariacao(dadosAtual.avaliacaoMedia, dadosAnterior.avaliacaoMedia);
    
    const getIcon = (variacao) => variacao > 0 ? '↗️' : variacao < 0 ? '↘️' : '➡️';
    const getColor = (variacao, inverso = false) => {
        if (inverso) {
            return variacao > 0 ? '#ef4444' : variacao < 0 ? '#10b981' : '#64748b';
        }
        return variacao > 0 ? '#10b981' : variacao < 0 ? '#ef4444' : '#64748b';
    };
    
    container.innerHTML = `
        <div style="padding: 20px;">
            <h3 style="margin-bottom: 20px; color: var(--dark);">📊 Comparação de Períodos</h3>
            
            <div style="display: grid; gap: 15px; margin-bottom: 30px;">
                <div style="background: var(--light); padding: 15px; border-radius: 8px;">
                    <strong>Período Atual:</strong> ${datas.inicioFormatado} - ${datas.fimFormatado}
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div style="font-size: 2em; margin-bottom: 10px;">📞</div>
                    <div class="stat-value">${dadosAtual.total_chamados || 0}</div>
                    <div class="stat-label">Total de Chamados</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: ${getColor(variacaoTotal)};">
                        ${getIcon(variacaoTotal)} ${Math.abs(variacaoTotal)}% vs período anterior
                    </div>
                </div>
                
                <div class="stat-item">
                    <div style="font-size: 2em; margin-bottom: 10px;">✅</div>
                    <div class="stat-value">${dadosAtual.resolvidos || 0}</div>
                    <div class="stat-label">Chamados Resolvidos</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: ${getColor(variacaoResolvidos)};">
                        ${getIcon(variacaoResolvidos)} ${Math.abs(variacaoResolvidos)}% vs período anterior
                    </div>
                </div>
                
                <div class="stat-item">
                    <div style="font-size: 2em; margin-bottom: 10px;">⭐</div>
                    <div class="stat-value">${(dadosAtual.avaliacaoMedia || 0).toFixed(1)}</div>
                    <div class="stat-label">Avaliação Média</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: ${getColor(variacaoAvaliacao)};">
                        ${getIcon(variacaoAvaliacao)} ${Math.abs(variacaoAvaliacao)}% vs período anterior
                    </div>
                </div>
                
                <div class="stat-item">
                    <div style="font-size: 2em; margin-bottom: 10px;">📈</div>
                    <div class="stat-value">
                        ${dadosAtual.total_chamados > 0 ? ((dadosAtual.resolvidos / dadosAtual.total_chamados) * 100).toFixed(1) : 0}%
                    </div>
                    <div class="stat-label">Taxa de Resolução</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: var(--success);">
                        Período atual
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding: 20px; background: #f0f9ff; border-radius: 8px; border-left: 4px solid #3b82f6;">
                <h4 style="margin-bottom: 10px; color: var(--primary);">💡 Insights</h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    ${variacaoTotal > 0 ? 
                        '<li style="padding: 5px 0;">📈 Aumento no volume de chamados - considere alocar mais recursos</li>' : 
                        '<li style="padding: 5px 0;">📉 Redução no volume de chamados - ótimo trabalho!</li>'}
                    ${variacaoResolvidos > 0 ? 
                        '<li style="padding: 5px 0;">✅ Melhora na taxa de resolução - equipe performando bem</li>' : 
                        '<li style="padding: 5px 0;">⚠️ Queda na taxa de resolução - investigar gargalos</li>'}
                    ${variacaoAvaliacao > 0 ? 
                        '<li style="padding: 5px 0;">⭐ Satisfação dos cidadãos aumentou - continue assim!</li>' : 
                        '<li style="padding: 5px 0;">⚠️ Satisfação dos cidadãos diminuiu - avaliar qualidade do atendimento</li>'}
                </ul>
            </div>
        </div>
    `;
}

// ========== SISTEMA DE ALERTAS AVANÇADO ========== //

function verificarAlertas() {
    const alertas = [];
    
    // Verificar SLA crítico
    const slaCumprido = parseInt(document.getElementById('slaCumprido')?.textContent || '0');
    if (slaCumprido < 80) {
        alertas.push({
            tipo: 'danger',
            icone: '🚨',
            titulo: 'SLA Crítico',
            mensagem: `SLA está em ${slaCumprido}% (meta: 90%)`,
            acao: 'Priorizar chamados mais antigos'
        });
    }
    
    // Verificar chamados vencidos
    const vencidos = parseInt(document.getElementById('vencidos')?.textContent || '0');
    if (vencidos > 10) {
        alertas.push({
            tipo: 'warning',
            icone: '⚠️',
            titulo: 'Chamados Vencidos',
            mensagem: `${vencidos} chamados fora do prazo`,
            acao: 'Atribuir equipe urgentemente'
        });
    }
    
    // Verificar avaliação baixa
    const avaliacaoMedia = parseFloat(document.getElementById('avaliacaoMedia')?.textContent || '0');
    if (avaliacaoMedia < 4.0) {
        alertas.push({
            tipo: 'warning',
            icone: '⭐',
            titulo: 'Satisfação Baixa',
            mensagem: `Avaliação média: ${avaliacaoMedia.toFixed(1)}/5`,
            acao: 'Revisar qualidade do atendimento'
        });
    }
    
    // Verificar carga de trabalho alta
    const emAndamento = parseInt(document.getElementById('emAndamento')?.textContent || '0');
    if (emAndamento > 50) {
        alertas.push({
            tipo: 'info',
            icone: '👥',
            titulo: 'Carga de Trabalho Alta',
            mensagem: `${emAndamento} chamados em andamento`,
            acao: 'Considerar alocar mais recursos'
        });
    }
    
    return alertas;
}

function renderAlertas() {
    const alertas = verificarAlertas();
    const container = document.getElementById('alertasContainer');
    
    if (!container || alertas.length === 0) return;
    
    const corMap = {
        'danger': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6',
        'success': '#10b981'
    };
    
    container.innerHTML = alertas.map(alerta => `
        <div style="background: white; border-left: 4px solid ${corMap[alerta.tipo]}; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: start; gap: 15px;">
                <div style="font-size: 2em;">${alerta.icone}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0; color: var(--dark);">${alerta.titulo}</h4>
                    <p style="margin: 0 0 10px 0; color: var(--secondary);">${alerta.mensagem}</p>
                    <div style="padding: 8px 12px; background: var(--light); border-radius: 6px; font-size: 0.9em;">
                        <strong>Ação recomendada:</strong> ${alerta.acao}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Criar container de alertas se não existir
function initAlertasContainer() {
    const visaoGeral = document.getElementById('tabVisaoGeral');
    if (visaoGeral && !document.getElementById('alertasContainer')) {
        const alertasDiv = document.createElement('div');
        alertasDiv.innerHTML = `
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h4 style="margin-bottom: 20px; color: var(--dark);">🔔 Alertas e Ações Recomendadas</h4>
                <div id="alertasContainer"></div>
            </div>
        `;
        
        const dashboardCards = visaoGeral.querySelector('.dashboard-cards');
        if (dashboardCards) {
            dashboardCards.parentNode.insertBefore(alertasDiv, dashboardCards.nextSibling);
        }
    }
}

// ========== EXPORTAÇÃO AVANÇADA ========== //

window.exportarRelatorioCompleto = async function() {
    try {
        showLoading();
        
        const periodo = document.getElementById('reportPeriodo').value;
        const tipo = document.getElementById('reportTipo').value;
        const datas = getDateRange(periodo);
        
        if (!datas && periodo === 'custom') {
            showToast('Selecione as datas inicial e final', 'error');
            hideLoading();
            return;
        }
        
        // Simular dados para exportação
        const csvData = [
            ['Relatório de Chamados - Sistema de Zeladoria Urbana'],
            ['Período:', `${datas.inicioFormatado} - ${datas.fimFormatado}`],
            ['Tipo:', capitalize(tipo)],
            ['Gerado em:', new Date().toLocaleString('pt-BR')],
            [''],
            ['Protocolo', 'Título', 'Status', 'Categoria', 'Bairro', 'Data Abertura', 'Avaliação'],
            ['2025001', 'Lâmpada queimada', 'Resolvido', 'Iluminação', 'Centro', '18/10/2025', '5'],
            ['2025002', 'Buraco na via', 'Em Andamento', 'Pavimentação', 'Nazaré', '18/10/2025', '-'],
            ['2025003', 'Lixo acumulado', 'Aberto', 'Limpeza', 'Umarizal', '18/10/2025', '-']
        ];
        
        const csvContent = csvData.map(row => row.join(';')).join('\n');
        const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', `relatorio_zeladoria_${periodo}_${new Date().getTime()}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showToast('Relatório exportado com sucesso! 💾', 'success');
        hideLoading();
    } catch (error) {
        console.error('Erro ao exportar:', error);
        showToast('Erro ao exportar relatório', 'error');
        hideLoading();
    }
};

// ========== INICIALIZAÇÃO ========== //

// Adicionar ao evento DOMContentLoaded existente
document.addEventListener('DOMContentLoaded', () => {
    initChartJS();
    initDateFilters();
    initAlertasContainer();
});

// Atualizar função loadVisaoGeral para incluir alertas
const loadVisaoGeralOriginal = loadVisaoGeral;
if (typeof loadVisaoGeralOriginal === 'function') {
    loadVisaoGeral = async function() {
        await loadVisaoGeralOriginal();
        setTimeout(() => {
            renderAlertas();
        }, 500);
    };
}

// Adicionar botão de comparação de períodos
window.addEventListener('load', () => {
    const reportActions = document.querySelector('.report-actions');
    if (reportActions && !document.getElementById('btnComparar')) {
        const btnComparar = document.createElement('button');
        btnComparar.id = 'btnComparar';
        btnComparar.className = 'btn btn-secondary';
        btnComparar.innerHTML = '📊 Comparar Períodos';
        btnComparar.onclick = compararPeriodos;
        reportActions.appendChild(btnComparar);
    }
});

console.log('✅ Funcionalidades avançadas do dashboard carregadas!');
