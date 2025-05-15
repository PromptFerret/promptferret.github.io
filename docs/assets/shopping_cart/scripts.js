const ENCRYPTED_CSV_URL = "U2FsdGVkX1/7NiSx7Ugsj0XsHxvxjGZJBq/yVSy1T/+bNDHbGnORMUcQpa9AXMVautQ1Gn+8NGt0pdrwsWa3mxuW0yMSo/zV9Q/9hEsfrO5QKbDg13Kd8n1Ka+VUL6TxT+Y+50KCmf47vOqkmfSAqp9+R0H6Kf9fUm98LHmB4D1kKhFlboN6kkpIbhbn3bqhT3TeXyFvYlZJd7wityCOR24ZAjXNhdjwgfff5zVLf6VABmny28jCng0L5XLm5r1g";

const CACHE_BUSTER = Date.now();
const CART_EXPORT_PASSWORD = "cart-export-2024";

function setCookie(name, value, hours) {
    const d = new Date();
    d.setTime(d.getTime() + (hours * 60 * 60 * 1000));
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${d.toUTCString()};path=/;SameSite=Strict`;
}
function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : "";
}

// Helper to encrypt and encode cart JSON
function encryptCart(cartObj) {
    const json = JSON.stringify(cartObj);
    const encrypted = CryptoJS.AES.encrypt(json, CART_EXPORT_PASSWORD).toString();
    return btoa(encrypted);
}

// Helper to decode and decrypt cart JSON
function decryptCart(str) {
    try {
        const encrypted = atob(str);
        const decrypted = CryptoJS.AES.decrypt(encrypted, CART_EXPORT_PASSWORD).toString(CryptoJS.enc.Utf8);
        return JSON.parse(decrypted);
    } catch {
        return null;
    }
}

async function getDecryptedCsvUrl() {
    let tries = 0;
    let password = getCookie("SHOP_PASSWORD") || (typeof window.SHOP_PASSWORD === "string" ? window.SHOP_PASSWORD : "");
    while (tries < 6) {
        if (!password) {
            password = prompt("Enter password to access the item shop:");
            if (password === null) throw new Error("No password entered.");
        }
        try {
            const decrypted = CryptoJS.AES.decrypt(ENCRYPTED_CSV_URL, password).toString(CryptoJS.enc.Utf8);
            if (!decrypted.startsWith("http")) throw new Error("Decryption failed");
            setCookie("SHOP_PASSWORD", password, 6); // Save for 6 hours
            return decrypted;
        } catch {
            tries++;
            password = "";
            document.cookie = "SHOP_PASSWORD=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
            // No alert here, just loop and ask again
        }
    }
    // 6th failure: wipe DOM and show error
    document.body.innerHTML = `
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;">
            <div style="font-size:2rem;color:#c00;margin-bottom:1rem;">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <div style="font-size:1.5rem;font-weight:bold;margin-bottom:0.5rem;">Too many failed attempts</div>
            <div style="font-size:1.1rem;">Access denied. Please reload the page to try again.</div>
        </div>
    `;
    throw new Error("Too many failed password attempts");
}

let allData = [];
let itemsData = [];
let sortCol = null;
let sortAsc = true;
let cart = [];
let selectedRowName = null;

const $ = (selector, ctx = document) => ctx.querySelector(selector);
const $$ = (selector, ctx = document) => Array.from(ctx.querySelectorAll(selector));

// Robust CSV parser for quoted fields
function parseCSV(text) {
    const rows = [];
    let row = [];
    let cell = '';
    let inQuotes = false;
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (char === '"') {
            if (inQuotes && text[i + 1] === '"') {
                cell += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (char === ',' && !inQuotes) {
            row.push(cell);
            cell = '';
        } else if ((char === '\n' || char === '\r') && !inQuotes) {
            if (cell !== '' || row.length > 0) row.push(cell);
            if (row.length) rows.push(row.map(c => c.trim()));
            row = [];
            cell = '';
            if (char === '\r' && text[i + 1] === '\n') i++; // handle \r\n
        } else {
            cell += char;
        }
    }
    if (cell !== '' || row.length > 0) row.push(cell);
    if (row.length) rows.push(row.map(c => c.trim()));
    return rows;
}

async function fetchCSV(url) {
    const sep = url.includes('?') ? '&' : '?';
    const res = await fetch(url + sep + 'v=' + CACHE_BUSTER);
    const text = await res.text();
    return parseCSV(text);
}

async function fetchJSON(url) {
    const sep = url.includes('?') ? '&' : '?';
    const res = await fetch(url + sep + 'v=' + CACHE_BUSTER);
    return res.json();
}

async function tryFetchJSON(url) {
    try {
        return await fetchJSON(url);
    } catch (e) {
        // Optionally log: console.warn(`Could not load ${url}:`, e);
        return null;
    }
}

const ITEM_JSON_FILES = [
    'items.json',
    'items-base.json',
    // Add more file names here as needed
];

const KNOWN_ARRAY_KEYS = ['item', 'baseitem'];

async function loadAllBatchedJsonData() {
    let loadedCount = 0;
    for (const file of ITEM_JSON_FILES) {
        const data = await tryFetchJSON(`assets/shopping_cart/${file}`);
        let arr = [];
        if (Array.isArray(data)) {
            arr = data;
        } else if (data && typeof data === 'object') {
            for (const key of KNOWN_ARRAY_KEYS) {
                if (Array.isArray(data[key])) {
                    arr = data[key];
                    break;
                }
            }
        }
        if (arr.length) {
            itemsData.push(...arr);
            loadedCount += arr.length;
            console.log(`Loaded ${file}: ${arr.length} items`);
        } else {
            console.log(`${file} not loaded or not an array`);
        }
    }
    console.log(`Total loaded items: ${loadedCount}`);
}

async function loadData() {
    try {
        const CSV_URL = await getDecryptedCsvUrl();
        const csvRows = await fetchCSV(CSV_URL);
        allData = csvRows.slice(1);

        // --- Sort by tier: -1 first, then 0, then ascending ---
        allData.sort((a, b) => {
            const ta = parseInt(a[0], 10);
            const tb = parseInt(b[0], 10);
            // -1 always first
            if (ta === -1 && tb !== -1) return -1;
            if (tb === -1 && ta !== -1) return 1;
            // then 0, then ascending
            if (ta === 0 && tb !== 0) return -1;
            if (tb === 0 && ta !== 0) return 1;
            return ta - tb;
        });

        itemsData = [];
        populateFilters();
        setupEvents();
        applyFilters();
    } catch (err) {
        console.error("Failed to load data:", err);
    }
}

function uniqueSorted(arr) {
    return Array.from(new Set(arr.flat())).sort((a, b) => {
        const na = parseInt(a), nb = parseInt(b);
        if (!isNaN(na) && !isNaN(nb)) return na - nb;
        return String(a).localeCompare(String(b));
    });
}

function populateCheckboxMatrix(containerId, values) {
    const container = $(containerId);
    container.innerHTML = '';
    const items = uniqueSorted(values);
    items.forEach(val => {
        const label = document.createElement('label');
        label.className = "mb-0";
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.value = val;
        input.name = containerId.replace('#filter-', '');
        label.appendChild(input);
        // Use displayTier for tier filter, "None" for blank rarity, otherwise show raw value
        if (containerId === '#filter-tier') {
            label.append(' ' + displayTier(val));
        } else if (containerId === '#filter-rarity') {
            label.append(' ' + (val === "" ? "None" : val));
        } else {
            label.append(' ' + val);
        }
        container.appendChild(label);
    });
}

function populateFilters() {
    // Ensure correct columns: 0 = Tier, 1 = Type, 7 = Rarity
    const tierSet = allData.map(row => row[0]);
    const typeSet = allData.map(row => row[1]);
    const raritySet = allData.map(row => normalizeRarity(row[7])).flat();

    populateCheckboxMatrix('#filter-tier', tierSet);
    populateCheckboxMatrix('#filter-type', typeSet);
    populateCheckboxMatrix('#filter-rarity', raritySet);
}

function normalizeRarity(val) {
    if (val === "Very Rare (S)") return "Very Rare";
    if (val === "Very Rare/Rare") return ["Very Rare", "Rare"];
    return val;
}

function tokenizeMatch(text, query) {
    if (!query.trim()) return true;
    const tokens = query.toLowerCase().split(/\s+/);
    const field = (text || "").toLowerCase();
    return tokens.every(t => field.includes(t));
}

function applyFilters() {
    const tiers = $$('#filter-tier input:checked').map(el => el.value);
    const types = $$('#filter-type input:checked').map(el => el.value);
    const rarities = $$('#filter-rarity input:checked').map(el => el.value);
    const nameQ = $('#filter-name').value;
    const atn = $('#filter-atn').value;
    const session = $('#filter-session').value;
    const itemTypeQ = $('#filter-itemtype').value;
    const bookQ = $('#filter-book').value;
    const notesQ = $('#filter-notes').value;
    const costMin = parseInt($('#filter-cost-min').value) || 0;
    const costMax = parseInt($('#filter-cost-max').value) || 20000000;

    let data = allData.filter(row => {
        const [tier, type, name, atnVal, sessVal, itemType, cost, rawRarity, book, notes] = row;
        const costVal = parseInt((cost || '').replace(/[^0-9]/g, '')) || 0;
        const normRarity = normalizeRarity(rawRarity);
        const rarityMatch = Array.isArray(normRarity)
            ? normRarity.some(r => rarities.includes(r))
            : (rarities.length === 0 || rarities.includes(normRarity));

        return (
            (tiers.length === 0 || tiers.includes(tier)) &&
            (types.length === 0 || types.includes(type)) &&
            tokenizeMatch(name, nameQ) &&
            (atn === "" || (atn === "yes" && atnVal) || (atn === "no" && !atnVal)) &&
            (session === "" || (session === "yes" && sessVal) || (session === "no" && !sessVal)) &&
            tokenizeMatch(itemType, itemTypeQ) &&
            (costVal >= costMin && costVal <= costMax) &&
            rarityMatch &&
            tokenizeMatch(book, bookQ) &&
            tokenizeMatch(notes, notesQ)
        );
    });

    if (sortCol !== null) {
        data.sort((a, b) => {
            let vA = a[sortCol], vB = b[sortCol];
            // Try numeric sort if both are numbers
            const nA = parseFloat(vA), nB = parseFloat(vB);
            if (!isNaN(nA) && !isNaN(nB)) {
                return sortAsc ? nA - nB : nB - nA;
            }
            return sortAsc ? String(vA).localeCompare(String(vB)) : String(vB).localeCompare(String(vA));
        });
    }

    renderTable(data);
}

function renderTable(data) {
    const tbody = $('#itemsTable tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'item-row';
        tr.dataset.row = JSON.stringify(row);

        if (selectedRowName && row[2] === selectedRowName) {
            tr.classList.add('selected-row');
        }

        const [tier, type, name, atnVal, sessVal, itemType, cost, rarity, book, notes, link] = row;
        const inCart = isInCart(name);

        const showBase = typeof cost === "string" && cost.includes('+');
        let btnHtml = '';
        if (inCart) {
            btnHtml = `<button class="btn btn-secondary btn-sm" disabled title="Already in Cart"><i class="fa fa-cart-plus"></i></button>`;
        } else {
            btnHtml = `<button class="btn btn-primary btn-sm add-table-cart" data-name="${encodeURIComponent(name)}" data-base="${showBase ? 1 : 0}" title="Add to Cart"><i class="fa fa-cart-plus"></i></button>`;
        }
        btnHtml += `
            <button class="btn btn-primary btn-sm ms-1 table-share-btn" data-name="${encodeURIComponent(name)}" title="Share item">
                <i class="fa-solid fa-share-nodes"></i>
            </button>
        `;
        if (link && link.trim() !== "") {
            btnHtml += `
                <a href="${link}" target="_blank" rel="noopener" class="btn btn-primary btn-sm ms-1 table-link-btn" title="Open item link">
                    <i class="fa-solid fa-up-right-from-square"></i>
                </a>
            `;
        }

        const tdBtn = document.createElement('td');
        tdBtn.className = 'action-col';
        tdBtn.innerHTML = btnHtml;
        tr.appendChild(tdBtn);

        row.slice(0, 10).forEach((col, i) => {
            const td = document.createElement('td');
            if (i === 0) {
                td.textContent = displayTier(col);
            } else if (i === 6) { // Cost column
                // Remove non-numeric chars, parse, and format with commas if valid
                const num = parseInt((col || '').replace(/[^0-9]/g, ''));
                td.textContent = !isNaN(num) && num > 0 ? num.toLocaleString() : (col || '');
            } else {
                td.textContent = col || '';
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    // Add event listeners for the new buttons
    tbody.querySelectorAll('.add-table-cart').forEach(btn => {
        btn.addEventListener('click', e => {
            e.stopPropagation();
            const name = decodeURIComponent(btn.getAttribute('data-name'));
            addToCart(name);
            applyFilters();
        });
    });

    // Share button event listener
    tbody.querySelectorAll('.table-share-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.stopPropagation();
            const name = decodeURIComponent(btn.getAttribute('data-name'));
            const url = new URL(window.location.href);
            url.search = `?v=${toBase64(name)}`;
            url.hash = "";
            navigator.clipboard.writeText(url.toString()).then(() => {
                const rect = btn.getBoundingClientRect();
                showCopyToast('Share URL copied!', rect.left + rect.width / 2, rect.top - 20 + window.scrollY);
            });
        });
    });

    // Always re-sync sticky scrollbar after table changes
    if (typeof setupStickyScrollbar === "function") setupStickyScrollbar();
}

function formatBatchedJsonTags(text) {
    if (!text) return "";
    // Match both {@tag ...} and {#tag ...}
    return text.replace(/\{[@#]\w+\s+([^}]+)\}/g, (match, content) => {
        const parsed = content.split('|')[0].trim();
        return `<span class="parsed-BatchedJson-tag">${parsed}</span>`;
    });
}

function formatEntry(entry) {
    if (typeof entry === "string") {
        return formatBatchedJsonTags(entry);
    } else if (entry && typeof entry === "object") {
        let html = "";
        if (entry.name) {
            html += `<b>${entry.name}:</b> `;
        }
        if (entry.type === "list" && Array.isArray(entry.items)) {
            html += "<ul>" + entry.items.map(item => `<li>${formatEntry(item)}</li>`).join("") + "</ul>";
        } else if (entry.type === "table" && Array.isArray(entry.rows)) {
            html += "<table class='table table-sm mb-2'>";
            if (entry.colLabels) {
                html += "<thead><tr>" + entry.colLabels.map(label => `<th>${formatBatchedJsonTags(label)}</th>`).join("") + "</tr></thead>";
            }
            html += "<tbody>";
            for (const row of entry.rows) {
                html += "<tr>" + row.map(cell => `<td>${formatEntry(cell)}</td>`).join("") + "</tr>";
            }
            html += "</tbody></table>";
        } else if (Array.isArray(entry.entries)) {
            html += entry.entries.map(formatEntry).join(" ");
        }
        return html;
    }
    return "";
}

function toBase64(str) {
    return btoa(unescape(encodeURIComponent(str)));
}
function fromBase64(str) {
    try {
        return decodeURIComponent(escape(atob(str)));
    } catch {
        return "";
    }
}

// Replace the entire renderDetails function with this:
function renderDetails(rowData) {
    const [tier, type, name, atnVal, sessVal, itemType, cost, rarity, book, notes, link] = rowData;
    const item = itemsData.find(i => normalizeItemName(i.name) === normalizeItemName(name));

    // Helper to wrap any value as copyable
    const copy = v => `<span class="copyable">${v ?? ''}</span>`;

    let html = `
        <div class="item-title">
            ${copy(name)}
            <span class="item-source">${copy(book)}</span>
        </div>
        <div class="item-type">${copy(itemType)}</div>
        <div><b>Tier:</b> ${copy(displayTier(tier))}</div>
        <div><b>Type:</b> ${copy(type)}</div>
        <div><b>Rarity:</b> ${copy(rarity)}</div>
        <div><b>Cost:</b> ${copy(cost)}</div>
        <div><b>Requires Attunement:</b> ${copy(atnVal ? 'Yes' : 'No')}</div>
        <div><b>Session Required:</b> ${copy(sessVal ? 'Yes' : 'No')}</div>
    `;

    // Only include notes if present
    if (notes && notes.trim()) {
        html += `<div class="item-desc">${formatBatchedJsonTags(notes)}</div>`;
    }

    if (item && item.entries) {
        html += `<div class="item-desc">${item.entries.map(formatEntry).join(" ")}</div>`;
    }

    // Render into modal content
    const modalContent = document.getElementById('itemDetailModalContent');
    if (modalContent) modalContent.innerHTML = html;

    // Update modal Add to Cart button
    updateAddToCartBtnModal(name);

    // Update modal link/share buttons
    updateItemLinkBtnModal(name, link);

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('itemDetailsModal'));
    modal.show();
}

// Add these helper functions:
function updateAddToCartBtnModal(name) {
    const btn = document.getElementById('add-to-cart-btn-modal');
    if (!btn) return;
    if (isInCart(name)) {
        btn.innerHTML = `
            <span title="Already in Cart">
                <button class="btn btn-secondary btn-sm" tabindex="-1" style="pointer-events:none; opacity:0.65;">
                    <i class="fa-solid fa-cart-shopping"></i>
                </button>
            </span>
        `;
    } else {
        btn.innerHTML = `
            <button class="btn btn-primary btn-sm" title="Add to Cart">
                <i class="fa-solid fa-cart-plus"></i>
            </button>
        `;
        btn.querySelector('button').onclick = () => {
            addToCart(name);
            updateAddToCartBtnModal(name);
        };
    }
}

function updateItemLinkBtnModal(name, link) {
    const linkBtn = document.getElementById('item-link-btn-modal');
    if (!linkBtn) return;
    let shareHtml = `
        <button id="item-share-btn-modal" class="btn btn-primary btn-sm ms-2" title="Share item">
            <i class="fa-solid fa-share-nodes"></i>
        </button>
    `;
    let linkHtml = "";
    if (link && link.trim() !== "") {
        linkHtml = `
            <a href="${link}" target="_blank" rel="noopener" class="ms-2 btn btn-primary btn-sm" title="Open item link">
                <i class="fa-solid fa-up-right-from-square"></i>
            </a>
        `;
    }
    linkBtn.innerHTML = shareHtml + linkHtml;

    // Add share button event
    const shareBtn = document.getElementById('item-share-btn-modal');
    if (shareBtn) {
        shareBtn.onclick = () => {
            const url = new URL(window.location.href);
            url.search = `?v=${toBase64(name)}`;
            url.hash = "";
            navigator.clipboard.writeText(url.toString()).then(() => {
                const rect = shareBtn.getBoundingClientRect();
                showCopyToast('Share URL copied!', rect.left + rect.width / 2, rect.top - 20 + window.scrollY);
            });
        };
    }
}

// Enhance copyable: show "Copied to clipboard" as a tip
document.addEventListener('click', e => {
    if (e.target.classList.contains('copyable')) {
        const text = e.target.innerText;
        navigator.clipboard.writeText(text).then(() => {
            const rect = e.target.getBoundingClientRect();
            showCopyToast('Copied to clipboard', rect.left + rect.width / 2, rect.top - 20 + window.scrollY);
        });
    }
});

function showCopyToast(text, x, y) {
    let toast = $('#copyToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'copyToast';
        toast.className = 'copy-toast';
        document.body.appendChild(toast);
    }
    toast.textContent = text;
    toast.style.left = `${x}px`;
    toast.style.top = `${y}px`;
    toast.style.opacity = 1;
    toast.style.transform = "translateY(-20px)";
    setTimeout(() => {
        toast.style.opacity = 0;
        toast.style.transform = "translateY(-10px)";
    }, 1200);
}

function setBootstrapTheme(dark) {
    // Remove table from DOM to avoid repaint cost
    const tableWrapper = document.getElementById('tableWrapper');
    let parent, next;
    if (tableWrapper) {
        parent = tableWrapper.parentNode;
        next = tableWrapper.nextSibling;
        parent.removeChild(tableWrapper);
    }

    document.documentElement.setAttribute('data-bs-theme', dark ? 'dark' : 'light');
    const themeBtn = document.querySelector('.toggle-theme');
    if (themeBtn) {
        themeBtn.innerHTML = dark
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
    }

    // Re-insert table after a short delay to allow repaint
    setTimeout(() => {
        if (parent && tableWrapper) {
            if (next) {
                parent.insertBefore(tableWrapper, next);
            } else {
                parent.appendChild(tableWrapper);
            }
            setupStickyScrollbar(); // <-- Add this line
        }
    }, 50);
}

function setupEvents() {
    // Filter controls
    $$('.filters input, .filters select').forEach(el =>
        el.addEventListener('input', applyFilters)
    );
    // Table sorting
    $$('#itemsTable thead th').forEach((th, idx) =>
        th.addEventListener('click', () => {
            sortAsc = (sortCol === idx) ? !sortAsc : true;
            sortCol = idx;
            applyFilters();
        })
    );
    // Row click
    $('#itemsTable tbody').addEventListener('click', e => {
        const tr = e.target.closest('tr');
        if (tr && tr.dataset.row) {
            const rowData = JSON.parse(tr.dataset.row);
            selectedRowName = rowData[2]; // Use the Name column as unique identifier
            renderDetails(rowData); // Now opens modal
            applyFilters(); // Re-render table to update selected row highlight
        }
    });
    // Theme toggle
    const themeBtn = document.querySelector('.toggle-theme');
    let dark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    themeBtn.addEventListener('click', () => {
        dark = !dark;
        setBootstrapTheme(dark);
    });
    setBootstrapTheme(dark);
    document.getElementById('cart-btn').addEventListener('click', () => {
        if (cart.length === 0) return;
        renderCart();
        const modal = new bootstrap.Modal(document.getElementById('cartModal'));
        modal.show();
    });
    document.getElementById('order-btn').addEventListener('click', () => {
        // Filter out items with blank or 0 quantity
        const filtered = cart.filter(item => {
            // Remove if quantity is blank, 0, or not a number
            const qty = parseInt(item.quantity, 10);
            return !isNaN(qty) && qty > 0;
        });

        // Check for missing base values
        let missingBaseOrName = false;
        filtered.forEach(item => {
            const row = allData.find(row => row[2] === item.name);
            let costField = row ? (row[6] || '') : '';
            if (costField.includes('+')) {
                // Needs base and custom name
                if (
                    item.base === '' || item.base === null || isNaN(item.base) || Number(item.base) === 0 ||
                    !item.customName || !item.customName.trim()
                ) {
                    missingBaseOrName = true;
                }
            }
        });

        if (missingBaseOrName) {
            alert('Please enter a base value and a name for all items that require them.');
            return;
        }

        // Prepare output
        let total = 0;
        let lines = [];
        filtered.forEach(item => {
            const row = allData.find(row => row[2] === item.name);
            let costField = row ? (row[6] || '') : '';
            let showBase = costField.includes('+');
            let costDisplay = showBase ? costField.slice(0, costField.indexOf('+')).trim() : costField.trim();
            let cost = parseInt(costDisplay.replace(/[^0-9]/g, '')) || 0;
            let base = showBase ? (parseInt(item.base, 10) || 0) : 0;
            let qty = parseInt(item.quantity, 10);
            let perItem = cost + base;
            let itemTotal = perItem * qty;
            total += itemTotal;
            const displayName = showBase
                ? (item.customName && item.customName.trim()
                    ? `${item.name} (${item.customName.trim()})`
                    : item.name)
                : item.name;
            lines.push(`     ${displayName} ${perItem.toLocaleString()} x${qty} - ${itemTotal.toLocaleString()} GP`);
        });

        let output = `discordName as characterName buys:\n${lines.join('\n')}\nTotal ${total.toLocaleString()} GP`;

        // Copy to clipboard
        const orderBtn = document.getElementById('order-btn');
        navigator.clipboard.writeText(output).then(() => {
            const original = orderBtn.textContent;
            orderBtn.textContent = "Copied!";
            setTimeout(() => {
                orderBtn.textContent = original;
            }, 1500);
        }, () => {
            orderBtn.textContent = "Copy failed";
            setTimeout(() => {
                orderBtn.textContent = "Order";
            }, 1500);
        });
    });
    document.getElementById('clear-cart-btn').addEventListener('click', () => {
        if (cart.length === 0) return;
        if (confirm("Clear all items from your cart?")) {
            cart = [];
            updateCartCount();
            renderCart();
            applyFilters();
        }
    });

    // Import/Export button opens modal
    const importExportBtn = document.getElementById('import-export-btn');
    const importExportModal = document.getElementById('importExportModal');
    const importExportTextarea = document.getElementById('importExportTextarea');
    const copyBtn = document.getElementById('copy-import-export-btn');
    const shareBtn = document.getElementById('share-import-export-btn');
    const cancelBtn = document.getElementById('cancel-import-export-btn');
    const updateBtn = document.getElementById('update-import-export-btn');

    if (importExportBtn && importExportModal) {
        importExportBtn.addEventListener('click', () => {
            // If cart is not empty, show encrypted+base64 JSON
            if (cart.length) {
                importExportTextarea.value = encryptCart(cart);
            } else {
                importExportTextarea.value = '';
            }
            const modal = new bootstrap.Modal(importExportModal);
            modal.show();
        });
    }

    // Copy button
    if (copyBtn && importExportTextarea) {
        copyBtn.addEventListener('click', () => {
            importExportTextarea.select();
            document.execCommand('copy');
            copyBtn.textContent = "Copied!";
            setTimeout(() => { copyBtn.textContent = "Copy"; }, 1200);
        });
    }
    // Cancel button just closes modal (handled by data-bs-dismiss)

    // Update button (for now, just closes modal)
    if (updateBtn && importExportModal && importExportTextarea) {
        updateBtn.addEventListener('click', () => {
            const val = importExportTextarea.value.trim();
            if (val) {
                const imported = decryptCart(val);
                if (imported && Array.isArray(imported)) {
                    cart = imported;
                    updateCartCount();
                    renderCart();
                    applyFilters();
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(importExportModal);
                    if (modal) modal.hide();
                } else {
                    alert("Invalid or corrupted import data.");
                }
            } else {
                // Just close modal if textarea is empty
                const modal = bootstrap.Modal.getInstance(importExportModal);
                if (modal) modal.hide();
            }
        });
    }
}

function isInCart(name) {
    return cart.some(item => item.name === name);
}

function addToCart(name) {
    if (!isInCart(name)) {
        // Find the row to check if it needs a base
        const row = allData.find(row => row[2] === name);
        let costField = row ? (row[6] || '') : '';
        let needsBase = costField.includes('+');
        cart.push({
            name,
            quantity: 1,
            base: 0,
            ...(needsBase ? { customName: "" } : {})
        });
        updateAddToCartBtn(name);
        updateCartCount();
        applyFilters(); // Re-render table to update buttons
    }
}

function updateAddToCartBtn(name) {
    const btn = document.getElementById('add-to-cart-btn');
    if (!btn) return;
    if (isInCart(name)) {
        btn.innerHTML = `
            <span title="Already in Cart">
                <button class="btn btn-secondary btn-sm" tabindex="-1" style="pointer-events:none; opacity:0.65;">
                    <i class="fa-solid fa-cart-shopping"></i>
                </button>
            </span>
        `;
    } else {
        btn.innerHTML = `
            <button class="btn btn-primary btn-sm" title="Add to Cart">
                <i class="fa-solid fa-cart-plus"></i>
            </button>
        `;
        btn.querySelector('button').onclick = () => addToCart(name);
    }
}

function updateCartCount() {
    const count = cart.length;
    const badge = document.getElementById('cart-count');
    if (badge) badge.textContent = count;
    const cartBtn = document.getElementById('cart-btn');
    if (cartBtn) cartBtn.disabled = count === 0;
}

function renderCart() {
    const container = document.getElementById('cart-contents');
    if (!container) return;

    // --- Save scroll position ---
    const scrollY = container.scrollTop;

    // --- Save focus and cursor position ---
    const active = document.activeElement;
    let focusInfo = null;
    if (active && (active.classList.contains('cart-qty') || active.classList.contains('cart-base'))) {
        focusInfo = {
            className: active.classList.contains('cart-qty') ? 'cart-qty' : 'cart-base',
            idx: active.dataset.idx,
            selectionStart: active.selectionStart,
            selectionEnd: active.selectionEnd
        };
    }

    if (cart.length === 0) {
        container.innerHTML = '<div class="p-3 text-center text-muted">Your cart is empty.</div>';
        // Also clear total in footer if present
        const totalEl = document.getElementById('cart-total');
        if (totalEl) totalEl.textContent = "Total: 0 GP";
        return;
    }
    let html = `<table class="table table-sm align-middle mb-0">
        <thead>
            <tr>
                <th>Name</th>
                <th>Qty</th>
                <th>Base</th>
                <th>Per Item Price</th>
                <th>Total</th>
                <th></th>
            </tr>
        </thead>
        <tbody>`;
    let grandTotal = 0;
    cart.forEach((item, idx) => {
        // Find item data for price
        const row = allData.find(row => row[2] === item.name);
        let cost = 0, baseCost = item.base || 0, showBase = false, costDisplay = '';
        if (row) {
            let costField = row[6] || '';
            const plusIdx = costField.indexOf('+');
            if (plusIdx !== -1) {
                showBase = true;
                costDisplay = costField.slice(0, plusIdx).trim();
            } else {
                costDisplay = costField.trim();
            }
            cost = parseInt(costDisplay.replace(/[^0-9]/g, '')) || 0;
        }
        const perItem = cost + (showBase ? baseCost : 0);
        const total = perItem * (parseInt(item.quantity) || 0);
        grandTotal += total;
        html += `<tr>
            <td>${item.name}</td>
            <td>
                <input type="text" inputmode="numeric" pattern="[0-9]*"
                    class="form-control form-control-sm cart-qty"
                    style="max-width: 60px; min-width: 40px; display:inline-block;"
                    data-idx="${idx}" value="${item.quantity ?? ''}">
            </td>
            <td>
                ${showBase ? `<input type="text" inputmode="numeric" pattern="[0-9]*"
                    class="form-control form-control-sm cart-base"
                    style="max-width: 60px; min-width: 40px; display:inline-block;"
                    data-idx="${idx}" value="${item.base ?? ''}">` : ''}
            </td>
            <td>
                ${showBase ? `<input type="text"
                    class="form-control form-control-sm cart-custom-name"
                    style="max-width: 100px; min-width: 60px; display:inline-block;"
                    data-idx="${idx}" value="${item.customName ?? ''}" placeholder="Type">` : ''}
            </td>
            <td>${costDisplay ? (parseInt(costDisplay.replace(/[^0-9]/g, '')) || 0).toLocaleString() : perItem.toLocaleString()}</td>
            <td>${total.toLocaleString()}</td>
            <td>
                <button class="btn btn-danger btn-sm cart-delete" data-idx="${idx}" title="Remove"><i class="fa fa-trash"></i></button>
            </td>
        </tr>`;
    });
    html += `</tbody></table>`;
    container.innerHTML = html;

    // Show total in modal footer
    let totalEl = document.getElementById('cart-total');
    if (!totalEl) {
        // Insert total span if not present
        const footer = document.querySelector('#cartModal .modal-footer');
        if (footer) {
            totalEl = document.createElement('span');
            totalEl.id = 'cart-total';
            totalEl.className = 'ms-auto me-2 fw-bold';
            footer.insertBefore(totalEl, footer.querySelector('#order-btn'));
        }
    }
    if (totalEl) totalEl.textContent = `Total: ${grandTotal.toLocaleString()} GP`;

    // Quantity change
    container.querySelectorAll('.cart-qty').forEach(input => {
        input.addEventListener('input', e => {
            const idx = +input.dataset.idx;
            const raw = input.value.replace(/\D/g, '');
            if (raw === '') {
                // Allow blank while editing, don't update cart yet
                cart[idx].quantity = '';
            } else {
                let val = parseInt(raw, 10);
                if (val < 0) val = 0;
                cart[idx].quantity = val;
            }
            renderCart();
            updateCartCount();
        });
    });
    // Base change
    container.querySelectorAll('.cart-base').forEach(input => {
        input.addEventListener('input', e => {
            const idx = +input.dataset.idx;
            const raw = input.value.replace(/\D/g, '');
            if (raw === '') {
                cart[idx].base = '';
            } else {
                let val = parseInt(raw, 10);
                if (val < 0) val = 0;
                cart[idx].base = val;
            }
            renderCart();
        });
    });
    // Delete
    container.querySelectorAll('.cart-delete').forEach(btn => {
        btn.addEventListener('click', e => {
            const idx = +btn.dataset.idx;
            const removed = cart[idx];
            cart.splice(idx, 1);
            renderCart();
            updateCartCount();
            updateAddToCartBtn(removed.name); // Update item details button
            applyFilters(); // Re-render table to update buttons
            // Hide modal if cart is empty
            if (cart.length === 0) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('cartModal'));
                if (modal) modal.hide();
            }
        });
    });
    // Name change
    container.querySelectorAll('.cart-custom-name').forEach(input => {
        input.addEventListener('input', e => {
            const idx = +input.dataset.idx;
            cart[idx].customName = input.value;
        });
    });

    // --- Restore focus and cursor position ---
    if (focusInfo) {
        const input = container.querySelector(`.${focusInfo.className}[data-idx="${focusInfo.idx}"]`);
        if (input) {
            input.focus();
            input.setSelectionRange(focusInfo.selectionStart, focusInfo.selectionEnd);
        }
    }

    // Restore scroll position
    container.scrollTop = scrollY;
}

// Initial load
async function initialLoad() {
    await loadData(); // loads CSV and sets up allData, filters, etc.
    await loadAllBatchedJsonData(); // loads all JSON files into itemsData
    applyFilters(); // now safe to use itemsData

    // --- Check for ?v=BASE64 in URL (after all data is loaded) ---
    const params = new URLSearchParams(window.location.search);
    const vParam = params.get('v');
    if (vParam) {
        const decodedName = fromBase64(vParam);
        const row = allData.find(r => r[2] === decodedName);
        if (row) {
            renderDetails(row);
        }
    }
    // Any other initialization that needs itemsData
}

initialLoad();

function setupStickyScrollbar() {
    const tableWrapper = document.querySelector('.table-responsive-custom');
    const stickyScrollbar = document.querySelector('.sticky-table-scrollbar');
    if (!tableWrapper || !stickyScrollbar) return;
    const table = tableWrapper.querySelector('table');
    if (!table) return;

    // Set sticky scrollbar width to match table
    stickyScrollbar.firstElementChild.style.width = table.scrollWidth + 'px';

    // Remove previous event handlers
    stickyScrollbar.onscroll = null;
    tableWrapper.onscroll = null;

    // Always sync, all sizes
    stickyScrollbar.onscroll = () => {
        tableWrapper.scrollLeft = stickyScrollbar.scrollLeft;
    };
    tableWrapper.onscroll = () => {
        stickyScrollbar.scrollLeft = tableWrapper.scrollLeft;
    };
}

document.addEventListener('DOMContentLoaded', () => {
    // Import/Export button opens modal
    const importExportBtn = document.getElementById('import-export-btn');
    const importExportModal = document.getElementById('importExportModal');
    const importExportTextarea = document.getElementById('importExportTextarea');
    const copyBtn = document.getElementById('copy-import-export-btn');
    const shareBtn = document.getElementById('share-import-export-btn');
    const cancelBtn = document.getElementById('cancel-import-export-btn');
    const updateBtn = document.getElementById('update-import-export-btn');

    if (importExportBtn && importExportModal) {
        importExportBtn.addEventListener('click', () => {
            // If cart is not empty, show encrypted+base64 JSON
            if (cart.length) {
                importExportTextarea.value = encryptCart(cart);
            } else {
                importExportTextarea.value = '';
            }
            const modal = new bootstrap.Modal(importExportModal);
            modal.show();
        });
    }

    // Copy button
    if (copyBtn && importExportTextarea) {
        copyBtn.addEventListener('click', () => {
            importExportTextarea.select();
            document.execCommand('copy');
            copyBtn.textContent = "Copied!";
            setTimeout(() => { copyBtn.textContent = "Copy"; }, 1200);
        });
    }

    // Share button (uses Web Share API if available)
    if (shareBtn && importExportTextarea) {
        shareBtn.addEventListener('click', () => {
            const text = importExportTextarea.value;
            if (navigator.share) {
                navigator.share({ text }).catch(() => {});
            } else {
                alert("Sharing is not supported in this browser.");
            }
        });
    }

    // Cancel button just closes modal (handled by data-bs-dismiss)

    // Update button (for now, just closes modal)
    if (updateBtn && importExportModal && importExportTextarea) {
        updateBtn.addEventListener('click', () => {
            const val = importExportTextarea.value.trim();
            if (val) {
                const imported = decryptCart(val);
                if (imported && Array.isArray(imported)) {
                    cart = imported;
                    updateCartCount();
                    renderCart();
                    applyFilters();
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(importExportModal);
                    if (modal) modal.hide();
                } else {
                    alert("Invalid or corrupted import data.");
                }
            } else {
                // Just close modal if textarea is empty
                const modal = bootstrap.Modal.getInstance(importExportModal);
                if (modal) modal.hide();
            }
        });
    }
});

function displayTier(tier) {
    if (tier === "-1" || tier === -1) return "Mundane";
    if (!isNaN(tier)) return `Tier ${tier}`;
    return tier;
}

function normalizeItemName(name) {
    // Remove all trailing parenthetical groups and convert to lowercase
    return name.replace(/(\s*\([^)]+\))+$/g, '').trim().toLowerCase();
}