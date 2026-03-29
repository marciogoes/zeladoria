// ========== RECLASSIFICAÇÃO ==========
let catalogoCompleto = [];
let chamadoAtualReclassificar = null;
let servicoSelecionado = null;

async function carregarCatalogoCompleto() {
    try {
        const response = await fetch(API_BASE + '/catalogo');
        if (response.ok) {
            catalogoCompleto = await response.json();
            console.log('Catálogo carregado:', catalogoCompleto.length, 'serviços');
            
            // Carregar secretarias no filtro
            const secretarias = [...new Set(catalogoCompleto.map(s => s.secretaria_sigla))];
            const select = document.getElementById('filtro-secretaria-reclassificar');
            if (select) {
                select.innerHTML = '<option value="">Todas as Secretarias</option>';
                secretarias.forEach(sigla => {
                    const servico = catalogoCompleto.find(s => s.secretaria_sigla === sigla);
                    select.innerHTML += `<option value="${sigla}">${sigla} - ${servico.secretaria_nome}</option>`;
                });
            }
        }
    } catch (error) {
        console.error('Erro ao carregar catálogo:', error);
    }
}

async function abrirModalReclassificar(chamadoId) {
    try {
        // Carregar dados do chamado
        const response = await apiRequest(`/chamados/${chamadoId}`);
        const chamado = await response.json();
        
        chamadoAtualReclassificar = chamado;
        
        // Mostrar dados do chamado
        document.getElementById('chamado-atual-dados').innerHTML = `
            <p><strong>Protocolo:</strong> ${chamado.protocolo}</p>
            <p><strong>Título:</strong> ${chamado.titulo}</p>
            <p><strong>Status:</strong> <span class="badge ${chamado.status}">${formatStatus(chamado.status)}</span></p>
            <p><strong>Prioridade Atual:</strong> <span class="badge ${chamado.prioridade}">${formatPrioridade(chamado.prioridade)}</span></p>
        `;
        
        // Limpar busca
        document.getElementById('busca-servico-reclassificar').value = '';
        document.getElementById('filtro-secretaria-reclassificar').value = '';
        document.getElementById('filtro-prioridade-reclassificar').value = '';
        document.getElementById('servicos-lista-reclassificar').innerHTML = '<p style="text-align: center; color: #6c757d;">Digite para buscar serviços...</p>';
        
        // Abrir modal
        document.getElementById('modal-reclassificar').classList.add('active');
    } catch (error) {
        showToast('Erro ao carregar chamado', 'error');
    }
}

function fecharModalReclassificar() {
    document.getElementById('modal-reclassificar').classList.remove('active');
    chamadoAtualReclassificar = null;
    servicoSelecionado = null;
}

function buscarServicosReclassificar() {
    const busca = document.getElementById('busca-servico-reclassificar').value.toLowerCase();
    const secretaria = document.getElementById('filtro-secretaria-reclassificar').value;
    const prioridade = document.getElementById('filtro-prioridade-reclassificar').value;
    
    if (busca.length < 2 && !secretaria && !prioridade) {
        document.getElementById('servicos-lista-reclassificar').innerHTML = '<p style="text-align: center; color: #6c757d;">Digite ao menos 2 caracteres para buscar...</p>';
        return;
    }
    
    // Filtrar serviços
    let servicosFiltrados = catalogoCompleto;
    
    if (busca.length >= 2) {
        servicosFiltrados = servicosFiltrados.filter(s => 
            s.nome.toLowerCase().includes(busca) ||
            s.descricao.toLowerCase().includes(busca) ||
            s.codigo.toLowerCase().includes(busca) ||
            s.categoria.toLowerCase().includes(busca)
        );
    }
    
    if (secretaria) {
        servicosFiltrados = servicosFiltrados.filter(s => s.secretaria_sigla === secretaria);
    }
    
    if (prioridade) {
        servicosFiltrados = servicosFiltrados.filter(s => s.prioridade === prioridade);
    }
    
    // Mostrar resultados
    const container = document.getElementById('servicos-lista-reclassificar');
    
    if (servicosFiltrados.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #6c757d;">Nenhum serviço encontrado.</p>';
        return;
    }
    
    container.innerHTML = servicosFiltrados.slice(0, 20).map(servico => `
        <div class="card" onclick="selecionarServico(${servico.id})" style="margin-bottom: 10px; cursor: pointer;" id="servico-card-${servico.id}">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0; color: #1e40af;">${servico.codigo}</h4>
                    <h5 style="margin: 0 0 10px 0;">${servico.nome}</h5>
                    <p style="margin: 0; font-size: 0.9rem; color: #64748b;">${servico.descricao.substring(0, 150)}...</p>
                    <div style="margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap;">
                        <span class="badge" style="background: #e0e7ff; color: #4338ca;">${servico.secretaria_sigla}</span>
                        <span class="badge ${servico.prioridade}">${formatPrioridade(servico.prioridade)}</span>
                        <span style="font-size: 0.85rem; color: #64748b;">⏱️ SLA: ${servico.sla_horas}h</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    if (servicosFiltrados.length > 20) {
        container.innerHTML += `<p style="text-align: center; color: #6c757d; margin-top: 10px;">Mostrando 20 de ${servicosFiltrados.length} resultados. Refine sua busca.</p>`;
    }
}

function selecionarServico(servicoId) {
    // Remover seleção anterior
    document.querySelectorAll('[id^="servico-card-"]').forEach(card => {
        card.style.border = '';
        card.style.background = '';
    });
    
    // Selecionar novo
    const card = document.getElementById(`servico-card-${servicoId}`);
    if (card) {
        card.style.border = '3px solid #10b981';
        card.style.background = '#f0fdf4';
    }
    
    servicoSelecionado = catalogoCompleto.find(s => s.id === servicoId);
    
    // Mostrar botão de confirmar
    const container = document.getElementById('servicos-lista-reclassificar');
    
    // Remover botão anterior se existir
    const botaoAnterior = document.getElementById('btn-confirmar-reclassificacao');
    if (botaoAnterior) {
        botaoAnterior.remove();
    }
    
    // Adicionar novo botão
    const botao = document.createElement('div');
    botao.id = 'btn-confirmar-reclassificacao';
    botao.style.cssText = 'position: sticky; bottom: 0; background: white; padding: 15px; border-top: 2px solid #e2e8f0; margin-top: 20px; text-align: center;';
    botao.innerHTML = `
        <button class="btn btn-success" onclick="confirmarReclassificacao()" style="font-size: 1.1rem; padding: 15px 30px;">
            ✅ Confirmar Reclassificação para: ${servicoSelecionado.codigo}
        </button>
    `;
    container.appendChild(botao);
}

async function confirmarReclassificacao() {
    if (!servicoSelecionado || !chamadoAtualReclassificar) {
        showToast('Erro: Selecione um serviço', 'error');
        return;
    }
    
    if (!confirm(`Confirma reclassificação para:\n\n${servicoSelecionado.codigo} - ${servicoSelecionado.nome}\n\nPrioridade será alterada para: ${formatPrioridade(servicoSelecionado.prioridade)}\nSLA: ${servicoSelecionado.sla_horas}h`)) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await apiRequest(`/chamados/${chamadoAtualReclassificar.id}/reclassificar`, {
            method: 'PATCH',
            body: JSON.stringify({
                servico_codigo: servicoSelecionado.codigo,
                servico_nome: servicoSelecionado.nome,
                categoria: servicoSelecionado.categoria,
                sla_horas: servicoSelecionado.sla_horas,
                prioridade: servicoSelecionado.prioridade
            })
        });
        
        if (response.ok) {
            showToast('✅ Chamado reclassificado com sucesso!');
            fecharModalReclassificar();
            await loadChamados();
        } else {
            const data = await response.json();
            showToast(data.detail || 'Erro ao reclassificar', 'error');
        }
    } catch (error) {
        showToast('Erro: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Fechar modal ao clicar fora
document.getElementById('modal-reclassificar')?.addEventListener('click', (e) => {
    if (e.target.id === 'modal-reclassificar') {
        fecharModalReclassificar();
    }
});
