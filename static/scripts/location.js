const locBtn = document.getElementById("loc-btn");
const checkoutBtn = document.getElementById("checkoutBtn");
const checkoutForm = document.getElementById("checkoutForm");

// HELPER: This gets the security token Django needs to accept data
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

locBtn.addEventListener("click", () => {
    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    locBtn.textContent = "⌛ Getting location...";
    locBtn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;

            // 1. Fill the hidden inputs for the form
            document.getElementById("id_lat").value = lat;
            document.getElementById("id_lon").value = lon;

            // 2. SYNC TO SERVER: This makes the map work in Telegram!
            // It sends the numbers to your 'update_cart_location' view in Python
            fetch("/update-cart-location/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ lat: lat, lon: lon })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Location saved to database:", data);
                locBtn.textContent = "✓ Location Captured";
                locBtn.style.backgroundColor = "#27ae60"; // Make it green
                locBtn.disabled = false;
                checkReady();
            })
            .catch(error => {
                console.error("Error saving location:", error);
                locBtn.textContent = "📍 Retry Location";
                locBtn.disabled = false;
            });
        },
        () => {
            alert("Failed to get location. Please enable GPS.");
            locBtn.textContent = "📍 Share My Location";
            locBtn.disabled = false;
        }
    );
});

function checkReady() {
    const phone = document.getElementById("phone").value.trim();
    const landmark = document.getElementById("landmark").value.trim();
    const lat = document.getElementById("id_lat").value;

    if (phone && landmark && lat) {
        checkoutBtn.disabled = false;
        checkoutBtn.classList.remove("disabled");
        checkoutBtn.textContent = "Proceed to Checkout";

        const display = document.getElementById("address-display");
        if (display) {
            display.style.display = "block";
            display.innerHTML = "✓ Delivery details ready";
        }
    }
}

document.getElementById("phone").addEventListener("input", checkReady);
document.getElementById("landmark").addEventListener("input", checkReady);

checkoutBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (checkoutBtn.disabled) return;

    // Before submitting, we save the phone and landmark to the session
    const phone = document.getElementById("phone").value;
    const landmark = document.getElementById("landmark").value;

    fetch("/save-delivery-details/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ phone: phone, landmark: landmark })
    })
    .then(() => {
        // Now that the server knows the location, phone, and landmark...
        // ...we can safely proceed to the payment page.
        window.location.href = checkoutBtn.getAttribute("data-url");
    });
});