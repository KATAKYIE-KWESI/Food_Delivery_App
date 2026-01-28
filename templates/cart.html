{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shopping Cart - JollyFoods</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="{% static 'homepage.css' %}">
    <link rel="stylesheet" href="{% static 'cart.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>

<div class="navbar">
    <a href="{% url 'homepage' %}" class="home-button">
        <i class="fa-solid fa-house"></i>
    </a>
    <a href="{% url 'homepage' %}" class="logo">JollyFoods.</a>
    <ul class="navbar-menu">
        <li><a href="{% url 'homepage' %}">Home</a></li>
        <li><a href="{% url 'homepage' %}#food-display">Menu</a></li>
        <li><a href="{% url 'homepage' %}#contact">Contact</a></li>
    </ul>
</div>
<div class="cart-container">

    {% if paid %}
    <div class="cart-content">

        <div id="activeTrackerSection">
            <div class="delivery-tracker" style="text-align: center; margin-bottom: 20px;">
                <p style="color: #666; margin-bottom: 5px;">Share this code with your driver:</p>
                <h2 style="font-size: 36px; letter-spacing: 5px; color: #ff4d4d;">{{ delivery.token }}</h2>
            </div>

            {% if delivery.driver %}
            <div class="driver-info-card" style="background: #fdf2f2; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #ffcccc; display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 24px; color: #ff4d4d;"><i class="fa-solid fa-motorcycle"></i></div>
                <div style="flex-grow: 1; text-align: left;">
                    <h4 style="margin: 0; font-size: 16px;">{{ delivery.driver.user.username }}</h4>
                    <p style="margin: 0; font-family: monospace; font-weight: bold; color: #333;">
                        {{ delivery.driver.vehicle_plate }}
                    </p>
                </div>
                <a href="tel:{{ delivery.driver.phone_number }}" style="background: #27ae60; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none;">
                    <i class="fa-solid fa-phone"></i>
                </a>
            </div>
            {% endif %}

            <div class="tracker-bar">
                <div id="progressBar" class="progress"></div>
                <div id="carMarker" class="car-marker">🚗</div>
            </div>

            <div class="tracker-info" style="display: flex; justify-content: space-between; margin-top: 15px; margin-bottom: 30px;">
                <span id="timerText" style="font-weight: bold; font-size: 18px; color: #e67e22;">02:00</span>
                <span class="tracker-status" style="font-weight: 500;">
                    {% if delivery.driver %} Driver is on the way! {% else %} Waiting for driver... {% endif %}
                </span>
            </div>
        </div>

        <div id="thankYouSection" style="display: none; text-align: center; padding: 50px 20px;">
            <i class="fa-solid fa-circle-check" style="color: #27ae60; font-size: 80px; margin-bottom: 20px;"></i>
            <h2 style="font-size: 28px; color: #333;">Thank you for choosing JollyFoods!</h2>
            <p style="color: #666; font-size: 18px; margin-bottom: 30px;">Your meal has been safely delivered. Enjoy!</p>

            <a href="{% url 'homepage' %}" class="browse-menu-btn" style="background: #ff4d4d; color: white; padding: 15px 40px; text-decoration: none; border-radius: 30px; font-weight: bold; display: inline-block;">
                <i class="fa-solid fa-utensils"></i> Browse More
            </a>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <a href="{% url 'homepage' %}" style="color: #333; text-decoration: none; font-size: 14px;">
                <i class="fa-solid fa-house"></i> Return to Home
            </a>
        </div>
    </div>

    {% elif cart_items %}
    <div class="cart-content">
        <div class="cart-items-section">
            <h2>Your Items</h2>
            {% for item in cart_items %}
            <div class="cart-item" data-item-id="{{ item.id }}">
                <img src="{% static 'assets/' %}{{ item.food_image }}" alt="{{ item.food_name }}">
                <div class="item-info">
                    <h4>{{ item.food_name }}</h4>
                    <p class="item-price">GHS {{ item.food_price }}</p>
                </div>
                <div class="item-quantity">
                    <button class="qty-btn minus-btn" data-item-id="{{ item.id }}">−</button>
                    <span class="quantity">{{ item.quantity }}</span>
                    <button class="qty-btn plus-btn" data-item-id="{{ item.id }}">+</button>
                </div>
                <div class="item-total"><p>GHS {{ item.get_total_price }}</p></div>
                <button class="remove-btn" data-item-id="{{ item.id }}"><i class="fa-solid fa-trash"></i></button>
            </div>
            {% endfor %}
        </div>

        <div class="order-summary-container">
            <div class="summary-row"><span>Subtotal</span><span id="subtotal">GHS {{ cart_total }}</span></div>
            <div class="summary-row"><span>Delivery</span><span>GHS 5.00</span></div>
            <div class="summary-row total"><strong>Total</strong><strong id="total">GHS {{ grand_total|floatformat:2 }}</strong></div>
        </div>

        <div class="delivery-location-section">
            <div class="section-header"><div class="delivery-icon">🚚</div><h3>Delivery Details</h3></div>
            <button id="loc-btn" class="quick-location-btn">📍 Share My Location</button>
            <div class="form-group"><label>Phone Number *</label><input type="tel" id="phone" placeholder="24 123 4567"></div>
            <div class="form-group"><label>Nearby Landmark *</label><input type="text" id="landmark" placeholder="e.g. Near the Total Filling Station"></div>
        </div>

        <button id="checkoutBtn" class="checkout-btn disabled" data-url="{% url 'payment' %}" disabled>
            Enter details to checkout
        </button>
    </div>

    {% else %}
    <div class="empty-cart-card">
        <div class="empty-cart-body" style="text-align: center; padding: 50px 20px;">
            <i class="fa-solid fa-utensils empty-icon" style="font-size: 60px; color: #ccc; margin-bottom: 20px;"></i>
            <h2>Your cart is empty!</h2>
            <p style="color: #666; margin-bottom: 25px;">Looks like you haven't added any delicious meals yet.</p>
            <a href="{% url 'homepage' %}" class="browse-menu-btn" style="background: #ff4d4d; color: white; padding: 12px 30px; text-decoration: none; border-radius: 30px;">Browse Menu</a>
        </div>
    </div>
    {% endif %}

</div>

<div id="confirmModal" class="confirm-modal" style="display:none;">
    <div class="confirm-modal-content">
        <p id="confirmMessage">Are you sure you want to remove this item?</p>
        <div class="confirm-modal-buttons">
            <button id="confirmYes">Yes</button>
            <button id="confirmNo">No</button>
        </div>
    </div>
</div>

<input type="hidden" id="id_lat">
<input type="hidden" id="id_lon">

<script src="{% static 'scripts/cart.js' %}"></script>
<script src="{% static 'scripts/location.js' %}"></script>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // We use the variables passed from your Python view
        const isPaid = "{{ paid }}" === "True";

        if (isPaid) {
            // Start 2-minute delivery timer
            if (typeof startDeliveryTimer === "function") {
                startDeliveryTimer(2);
            }

            // Disable cart buttons while delivery is in progress
            document.querySelectorAll('.plus-btn, .minus-btn, .remove-btn').forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = "0.5";
                btn.style.cursor = "not-allowed";
            });

            // Hide the location and checkout buttons since order is already placed
            const checkoutBtn = document.getElementById('checkoutBtn');
            const locationSection = document.querySelector('.delivery-location-section');
            if(checkoutBtn) checkoutBtn.style.display = 'none';
            if(locationSection) locationSection.style.display = 'none';
        }
    });
</script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const isPaid = "{{ paid }}" === "True";
    const deliveryId = "{{ delivery_id }}";

    if (isPaid && deliveryId) {
        const checkStatus = setInterval(() => {
            fetch(`/check-delivery-status/${deliveryId}/`)
                .then(response => response.json())
                .then(data => {
                    // NEW: If a driver is assigned but NOT yet shown on screen, reload the page
                    const driverCardExists = document.querySelector('.driver-info-card');
                    if (data.driver_assigned && !driverCardExists) {
                        location.reload();
                    }

                    // If delivered, show thank you
                    if (data.status === 'delivered') {
                        document.getElementById('activeTrackerSection').style.display = 'none';
                        document.getElementById('thankYouSection').style.display = 'block';
                        clearInterval(checkStatus);
                    }
                })
                .catch(err => console.error("Error checking status:", err));
        }, 5000); // Check every 5 seconds
    }
});

</script>

</body>
</html>