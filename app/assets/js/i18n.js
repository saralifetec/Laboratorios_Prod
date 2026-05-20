const i18n = {
    currentLang: localStorage.getItem('app_language') || 'pt',
    translations: {},

    async init() {
        await this.loadLanguage(this.currentLang);
        this.applyTranslations();
        this.updateLanguageSelector();

        
        const btn = document.getElementById("abrirPastaBtn");
        if (btn) {
            btn.setAttribute("title", this.t("action.open_folder"));
        }

        traduzirMeses();

    },

    async loadLanguage(lang) {
        try {
            const response = await fetch(`/assets/i18n/${lang}.json`);
            this.translations = await response.json();
            this.currentLang = lang;
            localStorage.setItem('app_language', lang);
            document.documentElement.lang = lang;
        } catch (error) {
            console.error('Erro ao carregar traduções:', error);
        }
    },




    t(key, defaultValue = key, params = {}) {
        let text = this.translations[key] ?? defaultValue;

        Object.entries(params).forEach(([name, value]) => {
            text = String(text).replaceAll(`{${name}}`, value ?? '');
        });

        return text;
    },

    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.t(key, el.textContent.trim());

            const attr = el.getAttribute('data-i18n-attr');
            if (attr) {
                attr.split(',').map(a => a.trim()).filter(Boolean).forEach(name => {
                    el.setAttribute(name, translation);
                });
            } else {
                el.textContent = translation;
            }
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key, el.placeholder || '');
        });

        const titleKey = document.querySelector('[data-i18n-title]');
        if (titleKey) {
            document.title = this.t(
                titleKey.getAttribute('data-i18n-title'),
                document.title
            );
        }
    },

    async switchLanguage(lang) {
        await this.loadLanguage(lang);
        this.applyTranslations();
        this.updateLanguageSelector();
        window.location.reload();
    },

    updateLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = this.currentLang;
        }
    },

    getDataTablesLanguageUrl() {
        const map = {
            pt: '/assets/js/plugin/datatables/Portuguese.json',
            es: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
            en: '//cdn.datatables.net/plug-ins/1.13.6/i18n/en-GB.json'
        };

        return map[this.currentLang] || map.pt;
    }
};

function traduzirMeses() {
  const select = document.getElementById("mes");
  if (!select) return;

  select.querySelectorAll("option").forEach(opt => {
    const month = parseInt(opt.value, 10);
    if (month >= 1 && month <= 12) {
      opt.textContent = i18n.t(`month.${month}`);
    }
  });
}



document.addEventListener('DOMContentLoaded', () => i18n.init());