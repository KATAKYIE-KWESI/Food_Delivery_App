const locBtn = document.getElementById("loc-btn");
const checkoutBtn = document.getElementById("checkoutBtn");

locBtn.addEventListener("click", () => {
    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    locBtn.textContent = "Getting location...";
    locBtn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            document.getElementById("id_lat").value = pos.coords.latitude;
            document.getElementById("id_lon").value = pos.coords.longitude;
            locBtn.textContent = "✓ Location Captured";
            locBtn.disabled = false;
            checkReady();
        },
        () => {
            alert("Failed to get location");
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

        document.getElementById("address-display").style.display = "block";
        document.getElementById("address-display").innerHTML =
            "✓ Delivery details saved";
    }
}

document.getElementById("phone").addEventListener("input", checkReady);
document.getElementById("landmark").addEventListener("input", checkReady);

checkoutBtn.addEventListener("click", () => {
    if (checkoutBtn.disabled) return;
    window.location.href = checkoutBtn.dataset.url;
});
