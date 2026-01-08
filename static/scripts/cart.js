// ==============================
// CSRF Token
// ==============================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// ==============================
// Update Cart Totals
// ==============================
function updateCartTotals() {
    // Check how many items are left in the HTML
    const items = document.querySelectorAll('.cart-item');

    // IF NO ITEMS ARE LEFT: Reload the page to trigger Django's {% else %} block
    if (items.length === 0) {
        window.location.reload();
        return; // Stop the rest of the function
    }

    let subtotal = 0;

    // 1. Calculate the subtotal from each item row
    items.forEach(item => {
        const quantity = parseInt(item.querySelector('.quantity').textContent);
        const priceText = item.querySelector('.item-price').textContent;
        const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));

        const itemTotal = quantity * price;

        // Update the individual item total on the right side
        item.querySelector('.item-total p').textContent = `GHS ${itemTotal.toFixed(2)}`;
        subtotal += itemTotal;
    });

    // 2. Constants matching your Python calculate_cart_totals function
    const deliveryFee = 5.00;
    const grandTotal = subtotal + deliveryFee;

    // 3. Update the Summary section on the screen
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');

    if (subtotalEl) subtotalEl.textContent = `GHS ${subtotal.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `GHS ${grandTotal.toFixed(2)}`;
}

// ==============================
// Custom Confirm Modal
// ==============================
async function showConfirmModal(message) {
    return new Promise(resolve => {
        const modal = document.getElementById('confirmModal');
        const msg = document.getElementById('confirmMessage');
        const yesBtn = document.getElementById('confirmYes');
        const noBtn = document.getElementById('confirmNo');

        msg.textContent = message;
        modal.style.display = 'flex';

        function cleanup() {
            modal.style.display = 'none';
            yesBtn.removeEventListener('click', onYes);
            noBtn.removeEventListener('click', onNo);
        }

        function onYes() {
            cleanup();
            resolve(true);
        }

        function onNo() {
            cleanup();
            resolve(false);
        }

        yesBtn.addEventListener('click', onYes);
        noBtn.addEventListener('click', onNo);
    });
}

// ==============================
// Remove Item
// ==============================
async function removeItem(itemId, itemName) {
    const response = await fetch('/cart/remove/', {
        method:'POST',
        headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
        body:JSON.stringify({item_id:itemId})
    });
    if(response.ok){
        const data = await response.json();
        if(data.success) {
            showDeleteNotification(itemName || 'Item');
        }
        document.querySelector(`.cart-item[data-item-id="${itemId}"]`)?.remove();
        updateCartTotals();
    }
}

// ==============================
// Delete Notification
// ==============================
function showDeleteNotification(itemName) {
    const existing = document.querySelectorAll('.cart-notification');
    existing.forEach(n => n.remove());

    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.innerHTML = `<i class="fas fa-trash-alt"></i> <span>${itemName} removed from cart</span>`;
    document.body.appendChild(notification);

    notification.offsetHeight; // force reflow
    setTimeout(() => notification.classList.add('show'), 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// ==============================
// OLD Notification (for compatibility)
// ==============================
function showNotification(message){
    const existing = document.querySelectorAll('.old-notification');
    existing.forEach(n => n.remove());

    const notification = document.createElement('div');
    notification.className = 'old-notification';
    notification.style.cssText = `
        position: fixed; top: 20px; right: 20px;
        background: #4CAF50; color: white; padding: 15px 25px;
        border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000; animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(()=>{
        notification.style.animation='slideOut 0.3s ease';
        setTimeout(()=>notification.remove(),300);
    },2000);
}

// ==============================
// Checkout Button
// ==============================
document.querySelector('.checkout-btn')?.addEventListener('click', async function(){
    const url = this.dataset.url;
    if(!url) return;

    // 1️⃣ Read phone & landmark inputs
    const phone = document.getElementById('phone')?.value.trim() || '';
    const landmark = document.getElementById('landmark')?.value.trim() || '';

    // 2️⃣ Send phone & landmark to backend
    try {
        if(phone || landmark){
            await fetch('/cart/save-delivery-details/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json','X-CSRFToken': csrftoken},
                body: JSON.stringify({phone, landmark})
            });
        }
    } catch (err) {
        console.error("Failed to save delivery details:", err);
    }

    // 3️⃣ Send geolocation if available
    if(navigator.geolocation){
        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {timeout: 10000});
            });
            await fetch('/cart/update-location/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json','X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                })
            });
        } catch (err) {
            console.log("Geolocation not available or denied:", err);
        }
    }

    // 4️⃣ Redirect to payment page only after above steps
    window.location.href = url;
});

// ==============================
// Delivery Timer with Car Animation
// ==============================
function startDeliveryTimer(durationInMinutes) {
    let timer = durationInMinutes*60;
    const timerDisplay = document.getElementById('timerText');
    const progressBar = document.getElementById('progressBar');
    const carMarker = document.getElementById('carMarker');
    const total = durationInMinutes*60;
    const thankYouMessage = document.getElementById('thankYouMessage');

    if(carMarker) carMarker.style.left = '0%';

    const countdown = setInterval(()=>{
        let mins = Math.floor(timer/60);
        let secs = timer % 60;
        if(timerDisplay) timerDisplay.textContent = `${mins < 10 ? '0'+mins : mins}:${secs < 10 ? '0'+secs : secs}`;

        let percentage = ((total - timer)/total)*100;
        if(progressBar) progressBar.style.width = percentage + '%';
        if(carMarker) carMarker.style.left = percentage + '%';

        if(--timer < 0){
            clearInterval(countdown);
            if(document.querySelector('.tracker-status'))
                document.querySelector('.tracker-status').textContent = "Driver has arrived!";
            if(thankYouMessage){
                thankYouMessage.style.display = 'block';
                setTimeout(()=>thankYouMessage.style.display='none', 10000);
            }
        }
    }, 1000);
}
window.startDeliveryTimer = startDeliveryTimer;

// ==============================
// Event Listeners for Quantity & Remove Buttons
// ==============================
document.addEventListener('DOMContentLoaded', () => {

    // Quantity buttons
    document.querySelectorAll('.plus-btn, .minus-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const cartItem = this.closest('.cart-item');
            const quantityEl = cartItem.querySelector('.quantity');
            let quantity = parseInt(quantityEl.textContent);
            const itemId = this.dataset.itemId;

            if (this.classList.contains('plus-btn')) quantity++;
            else if (this.classList.contains('minus-btn') && quantity > 1) quantity--;
            else if (quantity === 1 && this.classList.contains('minus-btn')) {
                const confirmed = await showConfirmModal('Remove this item from cart?');
                if(confirmed) await removeItem(itemId);
                return;
            }

            quantityEl.textContent = quantity;
            updateCartTotals();

            await fetch('/cart/update/', {
                method: 'POST',
                headers: {'Content-Type':'application/json','X-CSRFToken':csrftoken},
                body: JSON.stringify({item_id:itemId, quantity})
            });
        });
    });

    // Remove buttons
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const cartItem = this.closest('.cart-item');
            const itemName = cartItem.querySelector('.item-info h4').textContent;
            const itemId = this.dataset.itemId;

            const confirmed = await showConfirmModal(`Remove ${itemName} from cart?`);
            if(confirmed) await removeItem(itemId, itemName);
        });
    });

});
