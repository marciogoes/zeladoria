"""
fix_index.py — Corrige, reconstrói e atualiza o frontend/index.html do Zelô
Execute na pasta python-zeladoria/:
    python fix_index.py

Aplica:
  - Reconstrução estrutural (remove duplicatas, restaura loadPropostas)
  - Patches de bugs (avaliacao, previsao style)
  - Sprint 17: paginação nos chamados + timeline de histórico + export CSV
"""
import os, re, urllib.request, sys

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, 'frontend', 'index.html')

# ── 1. Obtém o conteúdo original ────────────────────────────────────────────
GITHUB_RAW = (
    "https://raw.githubusercontent.com/marciogoes/zeladoria/"
    "main/python-zeladoria/frontend/index.html"
)

print("Baixando index.html do GitHub...")
try:
    with urllib.request.urlopen(GITHUB_RAW, timeout=15) as r:
        raw = r.read().decode('utf-8')
    print(f"  OK: {len(raw)} chars baixados")
except Exception as e:
    print(f"  GitHub falhou ({e}), tentando arquivo local...")
    backup_candidates = [
        os.path.join(d, 'frontend', 'index.html.bak'),
        os.path.join(d, '_index_backup.html'),
    ]
    raw = None
    for c in backup_candidates:
        if os.path.exists(c):
            with open(c, 'r', encoding='utf-8') as f:
                raw = f.read()
            print(f"  Usando backup: {c}")
            break
    if raw is None:
        # Tenta ler o arquivo atual (pode ainda ser o bom antes do placeholder)
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            with open(out, 'r', encoding='utf-8') as f:
                raw = f.read()
            print(f"  Usando arquivo atual: {len(raw)} chars")
        else:
            print("ERRO: Não foi possível obter o index.html original.")
            sys.exit(1)

if len(raw) < 50000:
    print(f"ERRO: Arquivo muito pequeno ({len(raw)} chars) — pode ser o placeholder.")
    print("Faça 'git checkout frontend/index.html' para restaurar o original.")
    sys.exit(1)

# ── 2. Reconstrução estrutural ────────────────────────────────────────────────
SCRIPT_START  = '\n<script>\n    const API_BASE'
NAV_LEGACY    = '    // ─── Navigation ──────────────────────────────────\n    document.querySelectorAll'
DATA_LOADING  = '    // ─── Data loading ────────────────────────────────'
ONBOARDING    = '    // ═══════════════════════════════════════════════════\n    // ONBOARDING MODAL'
HTML_CLOSE    = '</html>\n'

main_idx = raw.find(SCRIPT_START)
if main_idx == -1:
    print("ERRO: Marcador de script não encontrado.")
    sys.exit(1)

html_part = raw[:main_idx]
script    = raw[main_idx:]

nav1_idx       = script.find(NAV_LEGACY)
onboard_idx    = script.find(ONBOARDING)
html_close_idx = script.find(HTML_CLOSE)
orphan_start   = html_close_idx + len(HTML_CLOSE)

part1            = script[:nav1_idx]
orphan           = script[orphan_start:]
nav2_idx         = orphan.find(NAV_LEGACY)
orphan_handlers  = orphan[:nav2_idx]
legacy1          = script[nav1_idx:onboard_idx]
utils_section    = legacy1[legacy1.find(DATA_LOADING):]
good_end         = script[onboard_idx:html_close_idx + len(HTML_CLOSE)]

final = html_part + part1 + orphan_handlers + utils_section + good_end

print(f"  Estrutura reconstruída: {len(final)} chars")

# ── 3. Patches de bugs (Sprints anteriores) ───────────────────────────────────
patches = [
    # Bug 7: payload avaliação
    (
        "JSON.stringify({ nota, comentario: document.getElementById('comentario').value })",
        "JSON.stringify({ avaliacao: nota, comentario_avaliacao: document.getElementById('comentario').value || null })"
    ),
    # Bug 8a: c.avaliacao.nota
    ("{'⭐'.repeat(c.avaliacao.nota)}", "{'⭐'.repeat(c.avaliacao || 0)}"),
    # Bug 8b: c.avaliacao.comentario
    (
        "${c.avaliacao.comentario ? `<p style=\"font-size:0.85rem;color:var(--text-secondary);margin-top:6px;\">${c.avaliacao.comentario}</p>` : ''}",
        "${c.comentario_avaliacao ? `<p style=\"font-size:0.85rem;color:var(--text-secondary);margin-top:6px;\">${c.comentario_avaliacao}</p>` : ''}"
    ),
    # Bug 9: loadPrevisao style
    (
        '<div style="font-weight:600;font-size:0.9rem;">${p.bairro} <span style="font-weight:400;color:var(--text-muted);• ${p.regiao}</span></div>',
        '<div style="font-weight:600;font-size:0.9rem;">${p.bairro} <span style="font-weight:400;color:var(--text-muted);">• ${p.regiao || \'\'}</span></div>'
    ),
]

for old, new in patches:
    count = final.count(old)
    if count > 0:
        final = final.replace(old, new)
        print(f"  Bug patch ({count}x): '{old[:55]}...'")

# ── 4. Sprint 17: Paginação nos chamados ──────────────────────────────────────
# Substitui loadChamados para usar paginação da API
OLD_LOAD_CHAMADOS = '''    async function loadChamados() {
        showLoading();
        try {
            const res = await apiRequest('/chamados');
            allChamados = await res.json();
            renderChamados(allChamados);

            const abertos = allChamados.filter(c => c.status === 'aberto').length;
            const badge = document.getElementById('badge-chamados');
            if (abertos > 0) { badge.textContent = abertos; badge.style.display = ''; }
            else badge.style.display = 'none';
        } catch(e) {
            showToast('Erro ao carregar chamados', 'error');
        } finally { hideLoading(); }
    }'''

NEW_LOAD_CHAMADOS = '''    // Sprint 17: Estado de paginação
    let _pagina = 1;
    let _totalPaginas = 1;
    let _totalChamados = 0;
    const _LIMIT = 20;

    async function loadChamados(pagina = 1) {
        showLoading();
        _pagina = pagina;
        try {
            const status = document.getElementById('filter-status')?.value || '';
            const prio   = document.getElementById('filter-prioridade')?.value || '';
            const search = document.getElementById('filter-search')?.value || '';
            let url = `/chamados?pagina=${pagina}&limit=${_LIMIT}`;
            if (status) url += `&status=${status}`;
            if (prio)   url += `&prioridade=${prio}`;
            if (search) url += `&search=${encodeURIComponent(search)}`;

            const res = await apiRequest(url);
            if (!res.ok) { showToast('Erro ao carregar chamados', 'error'); return; }
            const data = await res.json();

            allChamados = data.items || data;
            _totalPaginas = data.paginas || 1;
            _totalChamados = data.total || allChamados.length;

            renderChamados(allChamados);
            renderPaginacao();

            const abertos = allChamados.filter(c => c.status === 'aberto').length;
            const badge = document.getElementById('badge-chamados');
            if (abertos > 0) { badge.textContent = abertos; badge.style.display = ''; }
            else badge.style.display = 'none';
        } catch(e) {
            showToast('Erro ao carregar chamados', 'error');
        } finally { hideLoading(); }
    }

    function renderPaginacao() {
        let el = document.getElementById('paginacao-chamados');
        if (!el) {
            el = document.createElement('div');
            el.id = 'paginacao-chamados';
            el.style.cssText = 'display:flex;align-items:center;gap:8px;justify-content:center;margin-top:20px;flex-wrap:wrap;';
            document.getElementById('chamados-list')?.after(el);
        }
        if (_totalPaginas <= 1) { el.innerHTML = ''; return; }

        const btnStyle = (ativo) => `padding:6px 12px;border-radius:8px;border:1px solid var(--border);background:${ativo?'var(--accent)':'var(--bg-elevated)'};color:${ativo?'#fff':'var(--text-secondary)'};cursor:pointer;font-size:0.82rem;font-weight:600;`;

        let html = `<span style="font-size:0.8rem;color:var(--text-muted);">${_totalChamados} chamados</span>`;
        html += `<button onclick="loadChamados(${_pagina-1})" ${_pagina<=1?'disabled':''} style="${btnStyle(false)}">‹</button>`;

        const start = Math.max(1, _pagina - 2);
        const end   = Math.min(_totalPaginas, _pagina + 2);
        if (start > 1) html += `<button onclick="loadChamados(1)" style="${btnStyle(false)}">1</button>${start>2?'<span style="color:var(--text-muted)">…</span>':''}`;
        for (let p = start; p <= end; p++) {
            html += `<button onclick="loadChamados(${p})" style="${btnStyle(p===_pagina)}">${p}</button>`;
        }
        if (end < _totalPaginas) html += `${end<_totalPaginas-1?'<span style="color:var(--text-muted)">…</span>':''}<button onclick="loadChamados(${_totalPaginas})" style="${btnStyle(false)}">${_totalPaginas}</button>`;
        html += `<button onclick="loadChamados(${_pagina+1})" ${_pagina>=_totalPaginas?'disabled':''} style="${btnStyle(false)}">›</button>`;

        el.innerHTML = html;
    }'''

if OLD_LOAD_CHAMADOS in final:
    final = final.replace(OLD_LOAD_CHAMADOS, NEW_LOAD_CHAMADOS)
    print("  Sprint 17: paginação aplicada ✅")
else:
    print("  Sprint 17: padrão de loadChamados não encontrado — paginação não aplicada ⚠️")

# ── 5. Sprint 17: applyFilters chama loadChamados(1) ─────────────────────────
OLD_APPLY = '''    function applyFilters() {
        const search = document.getElementById('filter-search').value.toLowerCase();
        const status = document.getElementById('filter-status').value;
        const prio = document.getElementById('filter-prioridade').value;
        let filtered = allChamados;
        if (search) filtered = filtered.filter(c => c.protocolo.toLowerCase().includes(search) || c.titulo.toLowerCase().includes(search));
        if (status) filtered = filtered.filter(c => c.status === status);
        if (prio) filtered = filtered.filter(c => c.prioridade === prio);
        renderChamados(filtered);
    }'''

NEW_APPLY = '''    function applyFilters() {
        loadChamados(1);  // Sprint 17: filtra server-side com paginação
    }'''

if OLD_APPLY in final:
    final = final.replace(OLD_APPLY, NEW_APPLY)
    print("  Sprint 17: applyFilters atualizado ✅")

# ── 6. Sprint 17: Timeline de histórico no modal de chamado ──────────────────
# Adiciona botão "Timeline" no modal de detalhes após os action buttons
OLD_HISTORICO_SECTION = '                <div style="margin-top:24px; padding-top:20px; border-top:1px solid var(--border);">\n                    <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:12px;">COMENTÁRIOS</div>'
NEW_HISTORICO_SECTION = '''                <div style="margin-top:16px;">
                    <button class="btn-action" onclick="mostrarTimeline(${id})" style="font-size:0.8rem;">
                        📋 Ver Timeline
                    </button>
                    <div id="timeline-container-${id}" style="display:none;margin-top:12px;"></div>
                </div>
                <div style="margin-top:24px; padding-top:20px; border-top:1px solid var(--border);">
                    <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:12px;">COMENTÁRIOS</div>'''

# Também adiciona a função mostrarTimeline após showDetails
OLD_CLOSE_MODAL = '''    function closeModal() { document.getElementById('modal-detalhes').classList.remove('active'); }'''
NEW_CLOSE_MODAL = '''    function closeModal() { document.getElementById('modal-detalhes').classList.remove('active'); }

    async function mostrarTimeline(id) {
        const container = document.getElementById(`timeline-container-${id}`);
        if (!container) return;
        if (container.style.display === 'block') { container.style.display = 'none'; return; }
        container.style.display = 'block';
        container.innerHTML = '<p style="color:var(--text-muted);font-size:0.82rem;">Carregando...</p>';
        try {
            const res = await apiRequest(`/chamados/${id}/historico`);
            if (!res.ok) { container.innerHTML = '<p style="color:var(--danger);font-size:0.82rem;">Erro ao carregar timeline</p>'; return; }
            const hist = await res.json();
            if (!hist.length) { container.innerHTML = '<p style="color:var(--text-muted);font-size:0.82rem;">Nenhum registro de histórico</p>'; return; }
            const CAMPO_LABEL = { criacao:'Abertura', status:'Status', prioridade:'Prioridade', responsavel:'Responsável', avaliacao:'Avaliação', reclassificacao:'Reclassificação' };
            container.innerHTML = `<div style="border-left:2px solid var(--border);padding-left:12px;display:flex;flex-direction:column;gap:8px;">
                ${hist.map(h => `
                <div style="position:relative;">
                    <div style="position:absolute;left:-17px;top:4px;width:8px;height:8px;border-radius:50%;background:var(--accent);"></div>
                    <div style="font-size:0.72rem;color:var(--text-muted);">${new Date(h.criado_em).toLocaleString('pt-BR')} · ${h.usuario}</div>
                    <div style="font-size:0.82rem;"><strong>${CAMPO_LABEL[h.campo]||h.campo}:</strong> ${h.valor_anterior?`${h.valor_anterior} → `:''}${h.valor_novo}</div>
                    ${h.observacao?`<div style="font-size:0.78rem;color:var(--text-muted);">${h.observacao}</div>`:''}
                </div>`).join('')}
            </div>`;
        } catch(e) { container.innerHTML = '<p style="color:var(--danger);font-size:0.82rem;">Erro ao carregar timeline</p>'; }
    }'''

if OLD_CLOSE_MODAL in final:
    final = final.replace(OLD_CLOSE_MODAL, NEW_CLOSE_MODAL)
    print("  Sprint 17: timeline de histórico aplicada ✅")

# ── 7. Sprint 17: Botão Export CSV no painel de gestor ───────────────────────
OLD_PAGE_HEADER_CHAMADOS = '''            <div class="page-header">
                <div>
                    <h1 id="chamados-title">Chamados</h1>
                    <p id="chamados-subtitle">Gerencie os chamados da sua área</p>
                </div>
            </div>'''

NEW_PAGE_HEADER_CHAMADOS = '''            <div class="page-header">
                <div>
                    <h1 id="chamados-title">Chamados</h1>
                    <p id="chamados-subtitle">Gerencie os chamados da sua área</p>
                </div>
                <div id="btn-export-csv-container" style="display:none;">
                    <button class="btn-secondary" onclick="exportarCSV()" style="font-size:0.82rem;">
                        📥 Exportar CSV
                    </button>
                </div>
            </div>'''

if OLD_PAGE_HEADER_CHAMADOS in final:
    final = final.replace(OLD_PAGE_HEADER_CHAMADOS, NEW_PAGE_HEADER_CHAMADOS)
    print("  Sprint 17: botão export CSV aplicado ✅")

# Adiciona função exportarCSV e show/hide do botão de export
OLD_SETUP_NAV = '    function setupNavPorPerfil(tipo) {'
NEW_SETUP_NAV = '''    async function exportarCSV() {
        const status = document.getElementById('filter-status')?.value || '';
        let url = `${API_BASE}/chamados/export/csv`;
        if (status) url += `?status=${status}`;
        try {
            const res = await apiRequest(url.replace(API_BASE, ''));
            if (!res.ok) { showToast('Sem permissão para exportar', 'error'); return; }
            const blob = await res.blob();
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `chamados_${new Date().toISOString().slice(0,10)}.csv`;
            a.click();
            URL.revokeObjectURL(a.href);
            showToast('CSV exportado com sucesso! 📥');
        } catch(e) { showToast('Erro ao exportar', 'error'); }
    }

    function setupNavPorPerfil(tipo) {'''

if OLD_SETUP_NAV in final:
    final = final.replace(OLD_SETUP_NAV, NEW_SETUP_NAV)
    # Mostra botão export apenas para gestor/admin/secretaria
    final = final.replace(
        "if (u.tipo === 'cidadao') {",
        "if (['gestor','admin','secretaria'].includes(u.tipo)) { document.getElementById('btn-export-csv-container').style.display=''; }\n        if (u.tipo === 'cidadao') {"
    )
    print("  Sprint 17: exportarCSV + visibilidade do botão ✅")

# ── 8. Sprint 17: Tempo médio de resolução no dashboard ───────────────────────
OLD_STAT_AVALIACAO = "document.getElementById('stat-avaliacao').textContent = (data.avaliacao_media || 0).toFixed(1);"
NEW_STAT_AVALIACAO = """document.getElementById('stat-avaliacao').textContent = (data.avaliacao_media || 0).toFixed(1);

            // Sprint 17: Tempo médio de resolução
            if (data.tempo_medio_resolucao_horas !== null && data.tempo_medio_resolucao_horas !== undefined) {
                const tmEl = document.getElementById('stat-tempo-medio');
                if (tmEl) {
                    const h = data.tempo_medio_resolucao_horas;
                    tmEl.textContent = h >= 24 ? `${(h/24).toFixed(1)}d` : `${h}h`;
                }
            }"""

if OLD_STAT_AVALIACAO in final:
    final = final.replace(OLD_STAT_AVALIACAO, NEW_STAT_AVALIACAO)
    print("  Sprint 17: tempo médio resolução no dashboard ✅")

# Adiciona card de tempo médio no HTML do dashboard stats
OLD_STAT_CARDS = '''<div class="stat-card blue">
                    <div class="stat-label">Avaliação Média</div>
                    <div class="stat-value" id="stat-avaliacao">—</div>
                </div>
            </div>'''
NEW_STAT_CARDS = '''<div class="stat-card blue">
                    <div class="stat-label">Avaliação Média</div>
                    <div class="stat-value" id="stat-avaliacao">—</div>
                </div>
                <div class="stat-card teal">
                    <div class="stat-label">Tempo Médio Resolução</div>
                    <div class="stat-value" id="stat-tempo-medio">—</div>
                </div>
            </div>'''

if OLD_STAT_CARDS in final:
    final = final.replace(OLD_STAT_CARDS, NEW_STAT_CARDS)
    print("  Sprint 17: card tempo médio adicionado ao dashboard ✅")

# ── 9. Verificações ────────────────────────────────────────────────────────────
print("\nVerificando resultado:")
checks = [
    ("HTML completo",           final.endswith('</html>\n')),
    ("Bug 7 corrigido",         "avaliacao: nota, comentario_avaliacao:" in final),
    ("Bug 7 antigo removido",   "{ nota, comentario: document.getElementById" not in final),
    ("Bug 8a corrigido",        "repeat(c.avaliacao || 0)" in final),
    ("Bug 8b corrigido",        "c.comentario_avaliacao ?" in final),
    ("showDetails única (1x)",  final.count("async function showDetails") == 1),
    ("loadChamados única (1x)", final.count("async function loadChamados") == 1),
    ("DOMContentLoaded 1x",     final.count("window.addEventListener('DOMContentLoaded'") == 1),
    ("loadMainApp().then OK",   "loadMainApp().then(" in final),
    ("loadPropostas completa",  "filter(Boolean).join(' • ')" in final),
    ("setupNavPorPerfil OK",    "function setupNavPorPerfil" in final),
    ("Sprint 17: paginação",    "_totalPaginas" in final),
    ("Sprint 17: renderPaginacao", "renderPaginacao" in final),
    ("Sprint 17: timeline",     "mostrarTimeline" in final),
    ("Sprint 17: exportarCSV",  "exportarCSV" in final),
    ("Sprint 17: tempo médio",  "stat-tempo-medio" in final),
]

all_ok = True
for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")
    if not ok: all_ok = False

if all_ok:
    with open(out, 'w', encoding='utf-8') as f:
        f.write(final)
    print(f"\n✅ index.html atualizado: {len(final)} chars → {out}")
    print("   Agora faça: git add . && git commit -m 'feat: sprint 17'")
else:
    print("\n⚠️  Algumas verificações falharam — arquivo salvo mesmo assim para inspeção.")
    with open(out, 'w', encoding='utf-8') as f:
        f.write(final)
    print(f"   Arquivo salvo: {len(final)} chars")
