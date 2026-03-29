"""
Script para adicionar funcionalidade de Reclassificação ao index.html
Adiciona automaticamente o modal e o código JavaScript
"""

import os
import re

FRONTEND_PATH = "frontend"
INDEX_FILE = os.path.join(FRONTEND_PATH, "index.html")
RECLASSIFICACAO_JS = os.path.join(FRONTEND_PATH, "reclassificacao.js")

def adicionar_reclassificacao():
    print("=" * 60)
    print("  ADICIONAR RECLASSIFICAÇÃO AO INDEX.HTML")
    print("=" * 60)
    print()
    
    # Verificar se arquivos existem
    if not os.path.exists(INDEX_FILE):
        print(f"❌ Erro: {INDEX_FILE} não encontrado!")
        input("\nPressione ENTER para sair...")
        return
    
    if not os.path.exists(RECLASSIFICACAO_JS):
        print(f"❌ Erro: {RECLASSIFICACAO_JS} não encontrado!")
        input("\nPressione ENTER para sair...")
        return
    
    # Ler arquivos
    print("📖 Lendo arquivos...")
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    with open(RECLASSIFICACAO_JS, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Verificar se já foi adicionado
    if 'modal-reclassificar' in html_content:
        print("⚠️  Reclassificação já foi adicionada anteriormente!")
        print("    Removendo versão antiga...")
        
        # Remover modal antigo
        html_content = re.sub(
            r'<!-- MODAL RECLASSIFICAÇÃO -->.*?</div>\s*</div>\s*</div>',
            '',
            html_content,
            flags=re.DOTALL
        )
    
    print("✏️  Adicionando modal de reclassificação...")
    
    # HTML do modal
    modal_html = '''
    <!-- MODAL RECLASSIFICAÇÃO -->
    <div class="modal" id="modal-reclassificar">
        <div class="modal-content" style="max-width: 900px;">
            <div class="modal-header">
                <h2>🔄 Reclassificar Chamado</h2>
                <button class="btn-close" onclick="fecharModalReclassificar()">&times;</button>
            </div>
            <div class="modal-body">
                <div id="chamado-atual-info" style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h4>Chamado Atual:</h4>
                    <div id="chamado-atual-dados"></div>
                </div>
                
                <h4>Buscar Serviço no Catálogo:</h4>
                <div class="form-group">
                    <input 
                        type="text" 
                        id="busca-servico-reclassificar" 
                        placeholder="Digite para buscar serviço..." 
                        style="width: 100%;"
                        oninput="buscarServicosReclassificar()"
                    >
                </div>
                
                <div class="form-group">
                    <label>Filtrar por Secretaria:</label>
                    <select id="filtro-secretaria-reclassificar" onchange="buscarServicosReclassificar()">
                        <option value="">Todas as Secretarias</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Filtrar por Prioridade:</label>
                    <select id="filtro-prioridade-reclassificar" onchange="buscarServicosReclassificar()">
                        <option value="">Todas</option>
                        <option value="emergencial">⚠️ Emergencial</option>
                        <option value="alta">🔴 Alta</option>
                        <option value="media">🟡 Média</option>
                        <option value="baixa">🟢 Baixa</option>
                        <option value="agendavel">📅 Agendável</option>
                    </select>
                </div>
                
                <div id="servicos-lista-reclassificar" style="max-height: 400px; overflow-y: auto;">
                    <p style="text-align: center; color: #6c757d;">Digite para buscar serviços...</p>
                </div>
            </div>
        </div>
    </div>
'''
    
    # Adicionar modal antes do fechamento do body
    html_content = html_content.replace('</body>', modal_html + '\n</body>')
    
    print("✏️  Adicionando código JavaScript...")
    
    # Extrair apenas o código JavaScript do arquivo (remover comentários de bloco)
    js_lines = []
    in_comment = False
    for line in js_content.split('\n'):
        line = line.strip()
        if line.startswith('/*'):
            in_comment = True
        if not in_comment and line and not line.startswith('//'):
            js_lines.append(line)
        if '*/' in line:
            in_comment = False
    
    js_code = '\n'.join(js_lines)
    
    # Adicionar JavaScript antes do fechamento do </script>
    html_content = html_content.replace(
        '</script>\n</body>',
        f'\n        // ========== RECLASSIFICAÇÃO ==========\n{js_code}\n    </script>\n</body>'
    )
    
    # Adicionar botão de reclassificar no showDetails
    # Procurar pelo trecho onde há os botões de atualizar status
    pattern = r"(<button class=\"btn btn-success\" onclick=\"updateStatus\(\$\{id\}, 'resolvido'\)\">[\s\S]*?</button>)"
    replacement = r'''\1
                                <button class="btn" style="background: var(--info); color: white;" onclick="closeModal(); abrirModalReclassificar(${id})">
                                    🔄 Reclassificar
                                </button>'''
    
    if re.search(pattern, html_content):
        html_content = re.sub(pattern, replacement, html_content)
        print("✅ Botão de reclassificar adicionado!")
    else:
        print("⚠️  Não foi possível adicionar o botão automaticamente")
    
    # Adicionar carregamento do catálogo no DOMContentLoaded
    pattern = r"(if \(token && userStr\) \{[\s\S]*?loadMainApp\(\);[\s\S]*?\})"
    replacement = r'''\1
            
            // Carregar catálogo completo
            carregarCatalogoCompleto();'''
    
    if re.search(pattern, html_content):
        html_content = re.sub(pattern, replacement, html_content)
        print("✅ Carregamento do catálogo adicionado!")
    
    # Salvar backup
    backup_file = INDEX_FILE + '.backup'
    print(f"💾 Criando backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Salvar arquivo atualizado
    print(f"💾 Salvando {INDEX_FILE}...")
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print()
    print("=" * 60)
    print("✅ SUCESSO! RECLASSIFICAÇÃO ADICIONADA!")
    print("=" * 60)
    print()
    print("📋 O que foi adicionado:")
    print("  ✓ Modal de reclassificação")
    print("  ✓ Código JavaScript completo")
    print("  ✓ Botão 'Reclassificar' no modal de detalhes")
    print("  ✓ Carregamento automático do catálogo")
    print()
    print("🧪 Próximos passos:")
    print("  1. Inicie o backend: INICIAR_BACKEND.bat")
    print("  2. Acesse: http://localhost:8001/static/index.html")
    print("  3. Faça login como gestor/admin")
    print("  4. Abra um chamado e clique em 'Reclassificar'")
    print()
    print(f"💡 Backup salvo em: {backup_file}")
    print()
    
    input("Pressione ENTER para sair...")

if __name__ == "__main__":
    adicionar_reclassificacao()
