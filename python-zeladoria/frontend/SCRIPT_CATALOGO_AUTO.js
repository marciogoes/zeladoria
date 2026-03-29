// Adicionar ao final do script do index.html
// Abrir catálogo automaticamente ao clicar na tab
document.querySelector('[data-tab="catalogo"]').addEventListener('click', (e) => {
    // Abrir catalogo.html em nova aba
    window.open('catalogo.html', '_blank');
});
