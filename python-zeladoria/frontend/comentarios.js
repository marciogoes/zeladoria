// ========================================
// 💬 SISTEMA DE COMENTÁRIOS
// ========================================

async function carregarComentarios(chamadoId) {
    try {
        const response = await apiRequest(`/chamados/${chamadoId}/comentarios`);
        
        if (!response.ok) {
            console.error('Erro ao carregar comentários');
            return [];
        }
        
        const comentarios = await response.json();
        return comentarios;
    } catch (error) {
        console.error('Erro ao carregar comentários:', error);
        return [];
    }
}

function renderizarComentarios(comentarios, chamadoId) {
    if (comentarios.length === 0) {
        return `
            <div style="text-align: center; padding: 30px; color: var(--secondary);">
                <div style="font-size: 3rem; margin-bottom: 10px;">💬</div>
                <p>Nenhum comentário ainda</p>
                <p style="font-size: 0.9rem;">Seja o primeiro a comentar sobre este chamado!</p>
            </div>
        `;
    }
    
    return comentarios.map(c => {
        const data = new Date(c.data_criacao);
        const dataFormatada = formatDate(data);
        
        // Ícones por tipo de usuário
        const iconeUsuario = {
            'cidadao': '👤',
            'equipe': '👷',
            'gestor': '📊',
            'secretaria': '🏛️',
            'admin': '🔧',
            'sistema': '🤖'
        }[c.usuario_tipo] || '👤';
        
        // Cor por tipo de comentário
        const corTipo = {
            'atualizacao': '#dbeafe',
            'observacao': '#fef3c7', 
            'resolucao': '#d1fae5'
        }[c.tipo] || '#f1f5f9';
        
        const labelTipo = {
            'atualizacao': '📝 Atualização',
            'observacao': '💡 Observação',
            'resolucao': '✅ Resolução'
        }[c.tipo] || '💬 Comentário';
        
        const podeEditar = currentUser && 
                          (c.usuario_id === currentUser.id || 
                           ['admin', 'gestor'].includes(currentUser.tipo));
        
        return `
            <div class="comentario-item" style="background: white; border-left: 4px solid ${corTipo}; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 5px;">
                            <span style="font-size: 1.2rem;">${iconeUsuario}</span>
                            <strong>${c.usuario_nome}</strong>
                            <span style="background: ${corTipo}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                                ${labelTipo}
                            </span>
                            ${!c.visivel_cidadao ? '<span style="background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">🔒 Interno</span>' : ''}
                        </div>
                        <div style="font-size: 0.85rem; color: var(--secondary);">
                            ${dataFormatada}
                        </div>
                    </div>
                    ${podeEditar ? `
                    <div style="display: flex; gap: 5px;">
                        <button onclick="editarComentario(${chamadoId}, ${c.id}, '${c.comentario.replace(/'/g, "\\'")}', '${c.tipo}', ${c.visivel_cidadao})" 
                                class="btn-icon" title="Editar">
                            ✏️
                        </button>
                        <button onclick="deletarComentario(${chamadoId}, ${c.id})" 
                                class="btn-icon" title="Deletar">
                            🗑️
                        </button>
                    </div>
                    ` : ''}
                </div>
                <div style="white-space: pre-wrap; color: var(--dark); line-height: 1.5;">
                    ${c.comentario}
                </div>
            </div>
        `;
    }).join('');
}

async function adicionarComentario(chamadoId) {
    const comentarioTexto = document.getElementById('novo-comentario-texto').value.trim();
    const tipo = document.getElementById('novo-comentario-tipo').value;
    const visivelCidadao = document.getElementById('novo-comentario-visivel').checked;
    
    if (!comentarioTexto) {
        showToast('Digite um comentário', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await apiRequest(`/chamados/${chamadoId}/comentarios`, {
            method: 'POST',
            body: JSON.stringify({
                comentario: comentarioTexto,
                tipo: tipo,
                visivel_cidadao: visivelCidadao
            })
        });
        
        if (response.ok) {
            showToast('Comentário adicionado com sucesso!');
            
            // Limpar formulário
            document.getElementById('novo-comentario-texto').value = '';
            document.getElementById('novo-comentario-tipo').value = 'atualizacao';
            document.getElementById('novo-comentario-visivel').checked = true;
            
            // Recarregar comentários
            await atualizarComentariosModal(chamadoId);
        } else {
            const data = await response.json();
            showToast(data.detail || 'Erro ao adicionar comentário', 'error');
        }
    } catch (error) {
        showToast('Erro: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function atualizarComentariosModal(chamadoId) {
    const comentarios = await carregarComentarios(chamadoId);
    const container = document.getElementById('comentarios-container');
    
    if (container) {
        container.innerHTML = renderizarComentarios(comentarios, chamadoId);
    }
}

async function deletarComentario(chamadoId, comentarioId) {
    if (!confirm('Tem certeza que deseja deletar este comentário?')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await apiRequest(`/chamados/${chamadoId}/comentarios/${comentarioId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Comentário deletado com sucesso!');
            await atualizarComentariosModal(chamadoId);
        } else {
            const data = await response.json();
            showToast(data.detail || 'Erro ao deletar comentário', 'error');
        }
    } catch (error) {
        showToast('Erro: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function editarComentario(chamadoId, comentarioId, comentarioAtual, tipoAtual, visivelAtual) {
    const novoComentario = prompt('Editar comentário:', comentarioAtual);
    
    if (novoComentario === null || novoComentario.trim() === '') {
        return;
    }
    
    showLoading();
    
    try {
        const response = await apiRequest(`/chamados/${chamadoId}/comentarios/${comentarioId}`, {
            method: 'PATCH',
            body: JSON.stringify({
                comentario: novoComentario.trim(),
                tipo: tipoAtual,
                visivel_cidadao: visivelAtual
            })
        });
        
        if (response.ok) {
            showToast('Comentário atualizado com sucesso!');
            await atualizarComentariosModal(chamadoId);
        } else {
            const data = await response.json();
            showToast(data.detail || 'Erro ao atualizar comentário', 'error');
        }
    } catch (error) {
        showToast('Erro: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Adicionar CSS para botões de ícone
const style = document.createElement('style');
style.textContent = `
    .btn-icon {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        padding: 4px 8px;
        border-radius: 4px;
        transition: all 0.2s;
    }
    
    .btn-icon:hover {
        background: var(--light);
        transform: scale(1.1);
    }
    
    .comentarios-secao {
        border-top: 2px solid var(--border);
        margin-top: 20px;
        padding-top: 20px;
    }
    
    .form-comentario {
        background: var(--light);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
`;
document.head.appendChild(style);
