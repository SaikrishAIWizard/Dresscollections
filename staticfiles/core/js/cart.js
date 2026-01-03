let cart = JSON.parse(localStorage.getItem("cart")) || [];

function renderCart() {
    const box = document.getElementById("cartItems");
    box.innerHTML = "";

    let total = 0;

    if (cart.length === 0) {
        box.innerHTML = "<p>Your cart is empty</p>";
        document.getElementById("totalPrice").innerText = "";
        return;
    }

    cart.forEach((item, i) => {
        total += parseInt(item.price);
        box.innerHTML += `
        <div class="card mb-3">
            <div class="card-body d-flex justify-content-between">
                <div>
                    <h6>${item.name}</h6>
                    <p>Size: ${item.size}</p>
                    <p class="text-success">₹${item.price}</p>
                </div>
                <button class="btn btn-sm btn-danger"
                        onclick="removeItem(${i})">Remove</button>
            </div>
        </div>`;
    });

    document.getElementById("totalPrice").innerText = `Total: ₹${total}`;
}

function removeItem(i) {
    cart.splice(i, 1);
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCart();
}

function checkoutWhatsApp() {
    let msg = "🛍 Order Summary\n\n";
    let total = 0;

    cart.forEach((item, i) => {
        total += parseInt(item.price);
        msg += `${i+1}. ${item.name}\n   Size: ${item.size}\n   ₹${item.price}\n\n`;
    });

    msg += `💰 Total: ₹${total}`;

    const phone = "91XXXXXXXXXX"; // replace
    window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, "_blank");
}

renderCart();
