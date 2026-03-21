/* ============================================================
           BCV Monitor — Frontend Script
           Fetches exchange rates from the API and updates the DOM.
        ============================================================ */

        const API_ENDPOINT = '/api/rates';

        const elements = {
            usdPrice: document.getElementById('usd-price'),
            eurPrice: document.getElementById('eur-price'),
            timestamp: document.getElementById('timestamp'),
            refreshBtn: document.getElementById('btn-refresh'),
        };

        /**
         * Format a number as a Venezuelan Bolívares rate string.
         * @param {number} value
         * @returns {string}
         */
        function formatRate(value) {
            return value.toLocaleString('es-VE', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 4,
            });
        }

        /**
         * Format an ISO date string to a readable Spanish locale string.
         * @param {string} isoString
         * @returns {string}
         */
        function formatDate(isoString) {
            const date = new Date(isoString);
            return date.toLocaleDateString('es-VE', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            });
        }

        /**
         * Update a price element with the given value.
         * @param {HTMLElement} el
         * @param {number} value
         */
        function renderPrice(el, value) {
            el.innerHTML = `${formatRate(value)} <span class="rate-card__price-unit">Bs.</span>`;
        }

        /**
         * Fetch rates from the API and update all UI elements.
         */
        async function fetchRates() {
            elements.refreshBtn.disabled = true;
            elements.refreshBtn.classList.add('btn-refresh--loading');

            try {
                const response = await fetch(API_ENDPOINT);

                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }

                const { success, rates, error } = await response.json();

                if (!success) {
                    throw new Error(error || 'Error desconocido en la API.');
                }

                const usd = rates.find(r => r.nombre === 'Dólar');
                const eur = rates.find(r => r.nombre === 'Euro');

                if (usd) renderPrice(elements.usdPrice, usd.promedio);
                if (eur) renderPrice(elements.eurPrice, eur.promedio);

                const dateSource = usd?.fechaActualizacion || eur?.fechaActualizacion;
                if (dateSource) {
                    elements.timestamp.textContent = `Actualizado: ${formatDate(dateSource)}`;
                }

            } catch (err) {
                console.error('[BCV Monitor] Error al obtener tasas:', err);
                elements.timestamp.textContent = 'No se pudieron cargar los datos.';
            } finally {
                elements.refreshBtn.disabled = false;
                elements.refreshBtn.classList.remove('btn-refresh--loading');
            }
        }

        // Event listeners
        elements.refreshBtn.addEventListener('click', fetchRates);

        // ── Code-example tab switching ─────────────────────────────────
        document.querySelectorAll('.tabs__btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tabs__btn').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');
                document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
            });
        });

        // ── Endpoint switcher ──────────────────────────────────────────
        /**
         * Config for each endpoint: url, description, and code snippets per language.
         */
        const ENDPOINTS = {
            all: {
                url: '/api/rates',
                desc: 'Devuelve el Dólar y el Euro en un mismo array.',
                code: {
                    curl: `<span class="code--var">curl</span> https://tu-dominio.vercel.app/api/rates`,
                    js: `<span class="code--keyword">const</span> <span class="code--var">res</span>  = <span class="code--keyword">await</span> <span class="code--fn">fetch</span>(<span class="code--str">'/api/rates'</span>);\n<span class="code--keyword">const</span> <span class="code--var">data</span> = <span class="code--keyword">await</span> <span class="code--var">res</span>.<span class="code--fn">json</span>();\n<span class="code--var">console</span>.<span class="code--fn">log</span>(<span class="code--var">data</span>);`,
                    php: `<span class="code--var">$json</span> = <span class="code--fn">file_get_contents</span>(<span class="code--str">'/api/rates'</span>);\n<span class="code--var">$data</span> = <span class="code--fn">json_decode</span>(<span class="code--var">$json</span>, <span class="code--bool">true</span>);\n<span class="code--fn">print_r</span>(<span class="code--var">$data</span>);`,
                    python: `<span class="code--keyword">import</span> requests\n\n<span class="code--var">r</span>    = requests.<span class="code--fn">get</span>(<span class="code--str">'/api/rates'</span>)\n<span class="code--var">data</span> = <span class="code--var">r</span>.<span class="code--fn">json</span>()\n<span class="code--fn">print</span>(<span class="code--var">data</span>)`,
                },
            },
            dolar: {
                url: '/api/rates/dolar',
                desc: 'Devuelve únicamente la tasa oficial del Dólar Americano.',
                code: {
                    curl: `<span class="code--var">curl</span> https://tu-dominio.vercel.app/api/rates/dolar`,
                    js: `<span class="code--keyword">const</span> <span class="code--var">res</span>  = <span class="code--keyword">await</span> <span class="code--fn">fetch</span>(<span class="code--str">'/api/rates/dolar'</span>);\n<span class="code--keyword">const</span> <span class="code--var">data</span> = <span class="code--keyword">await</span> <span class="code--var">res</span>.<span class="code--fn">json</span>();\n<span class="code--var">console</span>.<span class="code--fn">log</span>(<span class="code--var">data</span>);`,
                    php: `<span class="code--var">$json</span> = <span class="code--fn">file_get_contents</span>(<span class="code--str">'/api/rates/dolar'</span>);\n<span class="code--var">$data</span> = <span class="code--fn">json_decode</span>(<span class="code--var">$json</span>, <span class="code--bool">true</span>);\n<span class="code--fn">print_r</span>(<span class="code--var">$data</span>);`,
                    python: `<span class="code--keyword">import</span> requests\n\n<span class="code--var">r</span>    = requests.<span class="code--fn">get</span>(<span class="code--str">'/api/rates/dolar'</span>)\n<span class="code--var">data</span> = <span class="code--var">r</span>.<span class="code--fn">json</span>()\n<span class="code--fn">print</span>(<span class="code--var">data</span>)`,
                },
            },
            euro: {
                url: '/api/rates/euro',
                desc: 'Devuelve únicamente la tasa oficial del Euro.',
                code: {
                    curl: `<span class="code--var">curl</span> https://tu-dominio.vercel.app/api/rates/euro`,
                    js: `<span class="code--keyword">const</span> <span class="code--var">res</span>  = <span class="code--keyword">await</span> <span class="code--fn">fetch</span>(<span class="code--str">'/api/rates/euro'</span>);\n<span class="code--keyword">const</span> <span class="code--var">data</span> = <span class="code--keyword">await</span> <span class="code--var">res</span>.<span class="code--fn">json</span>();\n<span class="code--var">console</span>.<span class="code--fn">log</span>(<span class="code--var">data</span>);`,
                    php: `<span class="code--var">$json</span> = <span class="code--fn">file_get_contents</span>(<span class="code--str">'/api/rates/euro'</span>);\n<span class="code--var">$data</span> = <span class="code--fn">json_decode</span>(<span class="code--var">$json</span>, <span class="code--bool">true</span>);\n<span class="code--fn">print_r</span>(<span class="code--var">$data</span>);`,
                    python: `<span class="code--keyword">import</span> requests\n\n<span class="code--var">r</span>    = requests.<span class="code--fn">get</span>(<span class="code--str">'/api/rates/euro'</span>)\n<span class="code--var">data</span> = <span class="code--var">r</span>.<span class="code--fn">json</span>()\n<span class="code--fn">print</span>(<span class="code--var">data</span>)`,
                },
            },
        };

        /**
         * Switch the docs panel to the given endpoint key.
         * @param {'all'|'dolar'|'euro'} key
         */
        function switchEndpoint(key) {
            const cfg = ENDPOINTS[key];

            // Update description
            document.getElementById('ep-desc').textContent = cfg.desc;

            // Update endpoint row URL
            document.getElementById('ep-url').innerHTML =
                cfg.url.replace('/api/rates', '/api/<strong>rates</strong>') +
                (key !== 'all' ? `/<strong>${key}</strong>` : '');

            // Update Try button link
            document.getElementById('ep-try-link').href = cfg.url;

            // Update code examples
            document.getElementById('code-curl').innerHTML = cfg.code.curl;
            document.getElementById('code-js').innerHTML = cfg.code.js;
            document.getElementById('code-php').innerHTML = cfg.code.php;
            document.getElementById('code-python').innerHTML = cfg.code.python;

            // Show/hide schema panels
            ['all', 'dolar', 'euro'].forEach(k => {
                document.getElementById('schema-' + k).style.display = (k === key) ? 'block' : 'none';
            });
        }

        document.querySelectorAll('.ep-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.ep-btn').forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');
                switchEndpoint(btn.dataset.ep);
            });
        });

        // Initial load
        switchEndpoint('all');
        fetchRates();

        // ── Copy to clipboard ──────────────────────────────────────────
        document.querySelectorAll('.btn-copy').forEach(btn => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('data-target');
                // Extract plain text and clean up extra spaces
                const targetEl = document.getElementById(targetId);
                const textToCopy = targetEl.innerText.trim();
                
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalHTML = btn.innerHTML;
                    btn.classList.add('copied');
                    btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
                    
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btn.innerHTML = originalHTML;
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        });