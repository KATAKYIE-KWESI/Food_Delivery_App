// CSRF Token
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

// Update Cart Totals
function updateCartTotals() {
    let subtotal = 0;
    document.querySelectorAll('.cart-item').forEach(item => {
        const quantity = parseInt(item.querySelector('.quantity').textContent);
        const price = parseFloat(item.querySelector('.item-price').textContent.replace('$',''));
        const itemTotal = quantity * price;
        item.querySelector('.item-total p').textContent = `$${itemTotal.toFixed(2)}`;
        subtotal += itemTotal;
    });
    const tax = subtotal * 0.10;
    const deliveryFee = 5.00;
    const total = subtotal + tax + deliveryFee;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('tax').textContent = `$${tax.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

// Quantity buttons
document.querySelectorAll('.plus-btn, .minus-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        const itemId = this.dataset.itemId;
        const cartItem = this.closest('.cart-item');
        const quantityEl = cartItem.querySelector('.quantity');
        let quantity = parseInt(quantityEl.textContent);

        if (this.classList.contains('plus-btn')) quantity++;
        else if (this.classList.contains('minus-btn') && quantity > 1) quantity--;
        else if (quantity === 1 && this.classList.contains('minus-btn')) {
            if (confirm('Remove this item from cart?')) await removeItem(itemId);
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

// Remove item
document.querySelectorAll('.remove-btn').forEach(btn => {
    btn.addEventListener('click', async function() {
        if(confirm('Remove this item from cart?')) {
            await removeItem(this.dataset.itemId);
        }
    });
});

async function removeItem(itemId) {
    const response = await fetch('/cart/remove/', {
        method:'POST',
        headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
        body:JSON.stringify({item_id:itemId})
    });
    if(response.ok){
        const data = await response.json();
        if(data.success) showNotification(data.message);
        document.querySelector(`.cart-item[data-item-id="${itemId}"]`)?.remove();
        updateCartTotals();
    }
}

// Notification
function showNotification(message){
    const notification = document.createElement('div');
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

// Checkout button
document.querySelector('.checkout-btn')?.addEventListener('click', function(){
    const url = this.dataset.url;
    if(url) window.location.href = url;
});

// Delivery Timer with Car Animation
function startDeliveryTimer(durationInMinutes) {
    let timer = durationInMinutes*60;
    const timerDisplay = document.getElementById('timerText');
    const progressBar = document.getElementById('progressBar');
    const carMarker = document.getElementById('carMarker');
    const total = durationInMinutes*60;
    const thankYouMessage = document.getElementById('thankYouMessage');

    if(carMarker) carMarker.style.left = '0%'; // start from left

    const countdown = setInterval(()=>{
        let mins = Math.floor(timer/60);
        let secs = timer % 60;
        if(timerDisplay) timerDisplay.textContent = `${mins < 10 ? '0'+mins : mins}:${secs < 10 ? '0'+secs : secs}`;

        let percentage = ((total - timer)/total)*100; // percentage elapsed
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



// GeoLocation 
function shareLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
            const coords = {
                lat: pos.coords.latitude,
                lon: pos.coords.longitude
            };

            // This sends the GPS to your Django view
            fetch('/update-cart-location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(coords)
            }).then(() => {
                alert("Location shared! Your driver can now find you.");
            });
        });
    }
}