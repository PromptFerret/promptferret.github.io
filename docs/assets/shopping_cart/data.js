const ENCRYPTED_CSV_URL = "U2FsdGVkX1/7NiSx7Ugsj0XsHxvxjGZJBq/yVSy1T/+bNDHbGnORMUcQpa9AXMVautQ1Gn+8NGt0pdrwsWa3mxuW0yMSo/zV9Q/9hEsfrO5QKbDg13Kd8n1Ka+VUL6TxT+Y+50KCmf47vOqkmfSAqp9+R0H6Kf9fUm98LHmB4D1kKhFlboN6kkpIbhbn3bqhT3TeXyFvYlZJd7wityCOR24ZAjXNhdjwgfff5zVLf6VABmny28jCng0L5XLm5r1g";
const CACHE_BUSTER = Date.now();
const CART_EXPORT_PASSWORD = "cart-export-2024";

let allData = [];
let itemsData = [];
let sortCol = null;
let sortAsc = true;
let selectedRowName = null;

function setCookie(name, value, hours) {
    const d = new Date();
    d.setTime(d.getTime() + (hours * 60 * 60 * 1000));
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${d.toUTCString()};path=/;SameSite=Strict`;
}
function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : "";
}
function encryptCart(cartObj) {
    const json = JSON.stringify(cartObj);
    const encrypted = CryptoJS.AES.encrypt(json, CART_EXPORT_PASSWORD).toString();
    return btoa(encrypted);
}
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
            setCookie("SHOP_PASSWORD", password, 6);
            return decrypted;
        } catch {
            tries++;
            password = "";
            document.cookie = "SHOP_PASSWORD=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
        }
    }
    document.body.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;"><div style="font-size:2rem;color:#c00;margin-bottom:1rem;"><i class="fa-solid fa-triangle-exclamation"></i></div><div style="font-size:1.5rem;font-weight:bold;margin-bottom:0.5rem;">Too many failed attempts</div><div style="font-size:1.1rem;">Access denied. Please reload the page to try again.</div></div>`;
    throw new Error("Too many failed password attempts");
}
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
            if (char === '\r' && text[i + 1] === '\n') i++;
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
        return null;
    }
}
const ITEM_JSON_FILES = [
    'https://raw.githubusercontent.com/5etools-mirror-3/5etools-2014-src/refs/heads/main/data/items.json',
    'https://raw.githubusercontent.com/5etools-mirror-3/5etools-2014-src/refs/heads/main/data/items-base.json',
];
const KNOWN_ARRAY_KEYS = ['item', 'baseitem'];
async function loadAllBatchedJsonData() {
    let loadedCount = 0;
    for (const file of ITEM_JSON_FILES) {
        const data = await tryFetchJSON(file);
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
        }
    }
}
async function loadData() {
    try {
        const CSV_URL = await getDecryptedCsvUrl();
        const csvRows = await fetchCSV(CSV_URL);
        allData = csvRows.slice(1);
        allData.sort((a, b) => {
            const ta = parseInt(a[0], 10);
            const tb = parseInt(b[0], 10);
            if (ta === -1 && tb !== -1) return -1;
            if (tb === -1 && ta !== -1) return 1;
            if (ta === 0 && tb !== 0) return -1;
            if (tb === 0 && ta !== 0) return 1;
            return ta - tb;
        });
        itemsData = [];
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
function normalizeRarity(val) {
    if (val === "Very Rare (S)") return "Very Rare";
    if (val === "Very Rare/Rare") return ["Very Rare", "Rare"];
    return val;
}