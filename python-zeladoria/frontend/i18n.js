/**
 * Sprint 7 — i18n (internacionalização)
 * Suporte: pt, en, es
 */
const LANGS_CACHE = {};
let _currentLang = localStorage.getItem('zelo_lang') || 'pt';

async function loadLang(lang) {
    if (LANGS_CACHE[lang]) return LANGS_CACHE[lang];
    try {
        const res = await fetch(`/static/i18n/${lang}.json`);
        if (!res.ok) throw new Error();
        LANGS_CACHE[lang] = await res.json();
    } catch {
        // fallback para pt
        if (lang !== 'pt') return loadLang('pt');
        LANGS_CACHE[lang] = {};
    }
    return LANGS_CACHE[lang];
}

async function setLang(lang) {
    _currentLang = lang;
    localStorage.setItem('zelo_lang', lang);
    const dict = await loadLang(lang);
    // Aplica em todos os elementos com data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) el.textContent = dict[key];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) el.placeholder = dict[key];
    });
    // Atualiza seletor de idioma se existir
    const sel = document.getElementById('lang-selector');
    if (sel) sel.value = lang;
    document.documentElement.lang = lang;
}

function t(key) {
    return (LANGS_CACHE[_currentLang] || {})[key] || key;
}

// Auto-init ao carregar
document.addEventListener('DOMContentLoaded', () => setLang(_currentLang));
window.setLang = setLang;
window.t = t;
