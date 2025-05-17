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
    const descQ = $('#filter-description') ? $('#filter-description').value.trim().toLowerCase() : ""; // <-- Add this
    const costMin = parseInt($('#filter-cost-min').value) || 0;
    const costMax = parseInt($('#filter-cost-max').value) || 20000000;

    let data = allData.filter(row => {
        const [tier, type, name, atnVal, sessVal, itemType, cost, rawRarity, book, notes] = row;
        const costVal = parseInt((cost || '').replace(/[^0-9]/g, '')) || 0;
        const normRarity = normalizeRarity(rawRarity);
        const rarityMatch = Array.isArray(normRarity)
            ? normRarity.some(r => rarities.includes(r))
            : (rarities.length === 0 || rarities.includes(normRarity));

        // --- Description filter logic ---
        let descMatch = true;
        if (descQ) {
            const item = Object.entries(item_data).find(
                ([key]) => key.toLowerCase() === name.toLowerCase()
            )?.[1];
            descMatch = !!(item && Array.isArray(item.entries) && item.entries.some(e =>
                typeof e === "string" && tokenizeMatch(e, descQ)
            ));
        }

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
            tokenizeMatch(notes, notesQ) &&
            descMatch // <-- Add this
        );
    });

    // If no filters are selected and no search fields are filled, show all data
    const noFilters =
        tiers.length === 0 &&
        types.length === 0 &&
        rarities.length === 0 &&
        !nameQ && !atn && !session && !itemTypeQ && !bookQ && !notesQ && !descQ &&
        (costMin === 0 && costMax === 20000000);

    if (data.length === 0 && noFilters) {
        data = allData;
    }

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

        // --- FIX: Append action column first ---
        const tdBtn = document.createElement('td');
        tdBtn.className = 'action-col';
        tdBtn.innerHTML = btnHtml;
        tr.appendChild(tdBtn);

        // --- FIX: Append exactly 10 data columns to match thead ---
        [tier, type, name, atnVal, sessVal, itemType, cost, rarity, book, notes].forEach((col, i) => {
            const td = document.createElement('td');
            if (i === 0) {
                td.textContent = displayTier(col);
            } else if (i === 6) { // Cost column
                const num = parseInt((col || '').replace(/[^0-9]/g, ''));
                td.textContent = !isNaN(num) && num > 0 ? num.toLocaleString() : (col || '');
            } else {
                td.textContent = col || '';
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    // --- ADD THIS: Attach row click event after rendering ---
    tbody.querySelectorAll('tr').forEach(tr => {
        tr.addEventListener('click', e => {
            // Prevent button clicks from triggering row click
            if (e.target.closest('button, a')) return;
            const rowData = JSON.parse(tr.dataset.row);
            selectedRowName = rowData[2];
            renderDetails(rowData);
            applyFilters();
        });
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

function formatBatchedJsonTags(text, item) {
    if (!text) return "";

    // Replace {=variable} with value from item or item.inherits, styled like batched JSON tags
    text = text.replace(/\{=([a-zA-Z0-9_]+)\}/g, (match, varName) => {
        let val = match;
        if (item && varName in item) val = item[varName];
        else if (item && item.inherits && varName in item.inherits) val = item.inherits[varName];
        return `<span class="parsed-BatchedJson-tag">${val}</span>`;
    });

    // Recursively replace batched JSON tags, handling nested tags
    return text.replace(/\{([@#][^\s}]+)\s+([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g, (match, tag, content) => {
        // Recursively process the content for nested tags
        const parsed = formatBatchedJsonTags(content.split('|')[0].trim(), item);
        return `<span class="parsed-BatchedJson-tag">${parsed}</span>`;
    });
}

function formatEntry(entry, item) {
    if (typeof entry === "string") {
        return formatBatchedJsonTags(entry, item);
    } else if (entry && typeof entry === "object") {
        let html = "";
        if (entry.name) {
            html += `<b>${entry.name}:</b> `;
        }
        if (entry.type === "list" && Array.isArray(entry.items)) {
            html += "<ul>" + entry.items.map(e => `<li>${formatEntry(e, item)}</li>`).join("") + "</ul>";
        } else if (entry.type === "table" && Array.isArray(entry.rows)) {
            html += "<table class='table table-sm mb-2'>";
            if (entry.colLabels) {
                html += "<thead><tr>" + entry.colLabels.map(label => `<th>${formatBatchedJsonTags(label, item)}</th>`).join("") + "</tr></thead>";
            }
            html += "<tbody>";
            for (const row of entry.rows) {
                html += "<tr>" + row.map(cell => `<td>${formatEntry(cell, item)}</td>`).join("") + "</tr>";
            }
            html += "</tbody></table>";
        } else if (Array.isArray(entry.entries)) {
            html += entry.entries.map(e => formatEntry(e, item)).join(" ");
        }
        return html;
    }
    return "";
}


// Replace the entire renderDetails function with this:
function renderDetails(rowData) {
    if (isAnyModalOpen()) return;
    const [tier, type, name, atnVal, sessVal, itemType, cost, rarity, book, notes, link] = rowData;
    const item = Object.entries(item_data).find(
        ([key]) => key.toLowerCase() === name.toLowerCase()
    )?.[1];

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
        html += `<div class="item-notes mb-2"><i class="fa-solid fa-circle-info me-1"></i>${formatBatchedJsonTags(notes)}</div>`;
    }

    if (item && item.entries) {
        html += `<div class="item-desc">${item.entries.map(e => formatEntry(e, item)).join(" ")}</div>`;
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
        if (isAnyModalOpen()) return;
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
    const updateBtn = document.getElementById('update-import-export-btn');

    if (importExportBtn && importExportModal && importExportTextarea) {
        importExportBtn.addEventListener('click', () => {
            if (isAnyModalOpen()) return;
            importExportTextarea.value = cart.length ? encryptCart(cart) : '';
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

    // Update button (import cart)
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

    // --- Sort cart by per-item cost descending ---
    const sortedCart = [...cart].sort((a, b) => {
        // Find item data for price and base
        const rowA = allData.find(row => row[2] === a.name);
        const rowB = allData.find(row => row[2] === b.name);
        let costA = 0, baseA = a.base || 0, showBaseA = false;
        let costB = 0, baseB = b.base || 0, showBaseB = false;
        if (rowA) {
            let costFieldA = rowA[6] || '';
            showBaseA = costFieldA.includes('+');
            costA = parseInt((showBaseA ? costFieldA.slice(0, costFieldA.indexOf('+')).trim() : costFieldA.trim()).replace(/[^0-9]/g, '')) || 0;
        }
        if (rowB) {
            let costFieldB = rowB[6] || '';
            showBaseB = costFieldB.includes('+');
            costB = parseInt((showBaseB ? costFieldB.slice(0, costFieldB.indexOf('+')).trim() : costFieldB.trim()).replace(/[^0-9]/g, '')) || 0;
        }
        const perItemA = costA + (showBaseA ? baseA : 0);
        const perItemB = costB + (showBaseB ? baseB : 0);
        return perItemB - perItemA;
    });

    let html = `<table class="table table-sm align-middle mb-0">
        <thead>
            <tr>
                <th>Name</th>
                <th>Qty</th>
                <th></th>
                <th>Per Item Price</th>
                <th>Total</th>
                <th></th>
            </tr>
        </thead>
        <tbody>`;
    let grandTotal = 0;
    sortedCart.forEach((item, idx) => {
        // Find the original index in the cart array
        const originalIdx = cart.findIndex(c => c.name === item.name);

        // Find item data for price and link
        const row = allData.find(row => row[2] === item.name);
        let cost = 0, baseCost = item.base || 0, showBase = false, costDisplay = '';
        let link = '';
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
            link = row[10] || ''; // 11th column is link
        }
        const perItem = cost + (showBase ? baseCost : 0);
        const total = perItem * (parseInt(item.quantity) || 0);
        grandTotal += total;
        html += `<tr>
            <td>${
                link && link.trim()
                    ? `<a href="${link}" target="_blank" rel="noopener">${item.name}</a>`
                    : item.name
            }</td>
            <td>
                <input type="text" inputmode="numeric" pattern="[0-9]*"
                    class="form-control form-control-sm cart-qty"
                    style="max-width: 60px; min-width: 40px; display:inline-block;"
                    data-idx="${originalIdx}" value="${item.quantity ?? ''}">
            </td>
            <td>
                ${showBase ? `
                    <input type="text" inputmode="numeric" pattern="[0-9]*"
                        class="form-control form-control-sm cart-base"
                        style="max-width: 60px; min-width: 40px; display:inline-block; margin-right: 4px;"
                        data-idx="${originalIdx}" value="${item.base === 0 || item.base === '' || item.base == null ? '' : item.base}" placeholder="Cost">
                    <input type="text"
                        class="form-control form-control-sm cart-custom-name"
                        style="max-width: 100px; min-width: 60px; display:inline-block;"
                        data-idx="${originalIdx}" value="${item.customName ?? ''}" placeholder="Type">
                ` : ''}
            </td>
            <td>${costDisplay ? (parseInt(costDisplay.replace(/[^0-9]/g, '')) || 0).toLocaleString() : perItem.toLocaleString()}</td>
            <td>${total.toLocaleString()}</td>
            <td>
                <button class="btn btn-danger btn-sm cart-delete" data-idx="${originalIdx}" title="Remove"><i class="fa fa-trash"></i></button>
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
    await setupMappingConfig();
    await loadData();

    populateFilters();
    setupEvents();

    setTimeout(() => {
        applyFilters();
    }, 50);

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
}

// --- ADD THIS: Sticky scrollbar for table ---
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

initialLoad();