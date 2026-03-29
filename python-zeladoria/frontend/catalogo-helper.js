// ==========================================
// SOLUÇÃO PARA O CATÁLOGO
// ==========================================

// Função melhorada para abrir catálogo
function abrirCatalogo() {
    console.log('🚀 Tentando abrir catálogo...');
    
    // Tentar abrir em nova aba
    const novaAba = window.open('catalogo.html', '_blank');
    
    // Se o popup foi bloqueado, mostrar mensagem
    if (!novaAba || novaAba.closed || typeof novaAba.closed == 'undefined') {
        console.warn('⚠️ Popup bloqueado! Mostrando alternativa...');
        
        // Mostrar mensagem de aviso
        const aviso = confirm(
            '🚨 Seu navegador bloqueou a abertura do Catálogo!\n\n' +
            'Clique em OK para abrir na mesma aba.\n' +
            'Ou permita popups e tente novamente.'
        );
        
        if (aviso) {
            // Abrir na mesma aba
            window.location.href = 'catalogo.html';
        } else {
            // Mostrar instruções
            showToast(
                'Permita popups no navegador e tente novamente! ' +
                'Ou copie: ' + window.location.origin + '/static/catalogo.html',
                'warning'
            );
        }
    } else {
        console.log('✅ Catálogo aberto em nova aba!');
        showToast('Catálogo aberto em nova aba!', 'success');
    }
}
