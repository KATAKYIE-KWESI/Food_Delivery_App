const locBtn = document.getElementById("loc-btn");
const checkoutBtn = document.getElementById("checkoutBtn");
const phoneInput = document.getElementById("phone");
const landmarkInput = document.getElementById("landmark");

// Only run this logic if we are on the CART page (where these elements exist)
if (locBtn) {
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

                document.getElementById("id_lat").value = lat;
                document.getElementById("id_lon").value = lon;

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
                    locBtn.textContent = "✓ Location Captured";
                    locBtn.style.backgroundColor = "#27ae60";
                    locBtn.disabled = false;
                    checkReady();
                });
            },
            () => {
                alert("Failed to get location.");
                locBtn.textContent = "📍 Share My Location";
                locBtn.disabled = false;
            }
        );
    });
}

// Check if inputs exist before adding listeners
if (phoneInput) phoneInput.addEventListener("input", checkReady);
if (landmarkInput) landmarkInput.addEventListener("input", checkReady);

if (checkoutBtn) {
    checkoutBtn.addEventListener("click", (e) => {
        e.preventDefault();
        const phone = phoneInput.value;
        const landmark = landmarkInput.value;

        fetch("/save-delivery-details/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ phone: phone, landmark: landmark })
        })
        .then(() => {
            window.location.href = checkoutBtn.getAttribute("data-url");
        });
    });
}

function checkReady() {
    // Optional chaining or null checks here too
    const phoneVal = phoneInput ? phoneInput.value.trim() : "";
    const landmarkVal = landmarkInput ? landmarkInput.value.trim() : "";
    const latInput = document.getElementById("id_lat");
    const latVal = latInput ? latInput.value : "";

    if (phoneVal && landmarkVal && latVal && checkoutBtn) {
        checkoutBtn.disabled = false;
        checkoutBtn.classList.remove("disabled");
        checkoutBtn.textContent = "Proceed to Checkout";
    }
}