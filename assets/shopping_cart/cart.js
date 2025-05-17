let cart = [];

function isInCart(name) {
    return cart.some(item => item.name === name);
}
function addToCart(name) {
    if (!isInCart(name)) {
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
        applyFilters();
    }
}
function updateCartCount() {
    const count = cart.length;
    const badge = document.getElementById('cart-count');
    if (badge) badge.textContent = count;
    const cartBtn = document.getElementById('cart-btn');
    if (cartBtn) cartBtn.disabled = count === 0;
}