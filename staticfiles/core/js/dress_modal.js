// Global variables for image navigation
let currentImages = [];
let currentImageIndex = 0;
let cart = JSON.parse(localStorage.getItem("cart")) || [];
updateCartCount();
let currentDress = {};
let selectedSize = null;

function showDressDetails(id, name, price, description, images, sizes) {
    currentDress = { id, name, price };
    currentImages = images || [];
    currentImageIndex = 0;
    selectedSize = null;

    document.getElementById("dressModalLabel").innerText = name;
    document.getElementById("modalPrice").innerText = "₹" + price;
    document.getElementById("modalDescription").innerText =
        description || "No description available";

    /* ================= IMAGES ================= */
    const imgBox = document.getElementById("modalImages");
    imgBox.innerHTML = "";

    currentImages.forEach((img, index) => {
        const image = document.createElement("img");
        image.src = img;
        image.style.width = "180px";
        image.style.height = "180px";
        image.style.objectFit = "cover";
        image.style.cursor = "pointer";
        image.className = "rounded-3 me-2";

        image.onclick = () => openImagePreview(index);
        imgBox.appendChild(image);
    });

    /* ================= SIZES (FIXED) ================= */
    const sizeBox = document.getElementById("modalSizes");
    sizeBox.innerHTML = "";

    sizes.forEach(size => {
        const span = document.createElement("span");
        span.className = "size-badge";
        span.innerText = size;

        span.addEventListener("click", () => {
            // ✅ FIX: scope selection to modalSizes only
            sizeBox.querySelectorAll(".size-badge")
                   .forEach(s => s.classList.remove("active"));

            span.classList.add("active");
            selectedSize = size;

            console.log("Selected size:", selectedSize);
        });

        sizeBox.appendChild(span);
    });

    new bootstrap.Modal(document.getElementById("dressModal")).show();
}





/* FULLSCREEN IMAGE FUNCTION */
function openImagePreview(index) {
    currentImageIndex = index || 0;
    updatePreviewImage();
    new bootstrap.Modal(document.getElementById("imagePreviewModal")).show();
}

/* Update preview image and counter */
function updatePreviewImage() {
    if (currentImages.length === 0) return;
    
    document.getElementById("previewImage").src = currentImages[currentImageIndex];
    document.getElementById("imageCounter").textContent = `${currentImageIndex + 1} / ${currentImages.length}`;
    
    // Show/hide navigation buttons
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    
    if (prevBtn) prevBtn.style.display = currentImageIndex === 0 ? "none" : "block";
    if (nextBtn) nextBtn.style.display = currentImageIndex === currentImages.length - 1 ? "none" : "block";
}

/* Navigate to next image */
function nextImage() {
    if (currentImages.length === 0) return;

    currentImageIndex = (currentImageIndex + 1) % currentImages.length;
    document.getElementById("previewImage").src = currentImages[currentImageIndex];
    document.getElementById("imageCounter").innerText =
        `${currentImageIndex + 1} / ${currentImages.length}`;
}

function prevImage() {
    if (currentImages.length === 0) return;

    currentImageIndex =
        (currentImageIndex - 1 + currentImages.length) % currentImages.length;
    document.getElementById("previewImage").src = currentImages[currentImageIndex];
    document.getElementById("imageCounter").innerText =
        `${currentImageIndex + 1} / ${currentImages.length}`;
}


/* Keyboard navigation */
document.addEventListener("keydown", (e) => {
    const modal = document.getElementById("imagePreviewModal");
    if (modal && modal.classList.contains("show")) {
        if (e.key === "ArrowRight") nextImage();
        if (e.key === "ArrowLeft") prevImage();
    }
});



function addToCartFromModal() {
    if (!selectedSize) {
        new bootstrap.Modal(
            document.getElementById("sizeAlertModal")
        ).show();
        return;
    }

    // Add current dress with selected size to cart and persist
    cart = JSON.parse(localStorage.getItem("cart")) || cart;
    cart.push({ ...currentDress, size: selectedSize });
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();

    // Close the dress modal
    const dm = document.getElementById("dressModal");
    const modalInstance = bootstrap.Modal.getInstance(dm);
    if (modalInstance) modalInstance.hide();

    // ✅ Styled success feedback (REPLACES alert)
    const successModalEl = document.getElementById("cartSuccessModal");
    const successModal = new bootstrap.Modal(successModalEl);
    successModal.show();

    // Optional: auto-close after 2 seconds
    setTimeout(() => {
        successModal.hide();
    }, 2000);
}


// UPDATE CART COUNT
function updateCartCount() {
    const cartCount = document.getElementById("cartCount");
    if (!cartCount) return;

    if (cart.length > 0) {
        cartCount.innerText = cart.length;
        cartCount.style.display = "inline-block";
    } else {
        cartCount.style.display = "none";
    }
}


// BUY NOW → WhatsApp
function buyNow() {
    cart = JSON.parse(localStorage.getItem("cart")) || [];
    if (cart.length === 0) {
        alert("Cart is empty");
        return;
    }

    let msg = "🛍️ *Order Details*%0A%0A";
    let total = 0;

    cart.forEach((item, i) => {
        msg += `${i + 1}. ${item.name}%0A`;
        msg += `Size: ${item.size}%0A`;
        msg += `Price: ₹${item.price}%0A%0A`;
        total += item.price;
    });

    msg += `💰 *Total: ₹${total}*`;

    const phone = "919553501265"; // change this
    window.open(`https://wa.me/${phone}?text=${msg}`, "_blank");
    
}


function sendCartToWhatsApp() {
    let cartItems = JSON.parse(localStorage.getItem("cart")) || [];

    if (cartItems.length === 0) {
        alert("Your cart is empty");
        return;
    }

    let message = "🛒 *Cart Items*%0A%0A";
    let total = 0;

    cartItems.forEach((item, index) => {
        message += `${index + 1}. ${item.name}%0A`;
        message += `Size: ${item.size}%0A`;
        message += `Price: ₹${item.price}%0A%0A`;
        total += item.price;
    });

    message += `💰 *Total Amount: ₹${total}*`;

    const phoneNumber = "919553501265"; // replace with your WhatsApp number
    const whatsappURL = `https://wa.me/${phoneNumber}?text=${message}`;

    window.open(whatsappURL, "_blank");
}

// Show cart modal and render items
function showCartModal() {
    cart = JSON.parse(localStorage.getItem("cart")) || [];
    renderCart();
    new bootstrap.Modal(document.getElementById("cartModal")).show();
}

// Render cart items inside the cart modal
function renderCart() {
    const box = document.getElementById("cartItems");
    if (!box) return;

    box.innerHTML = "";
    let total = 0;

    if (!cart || cart.length === 0) {
        box.innerHTML = "<p>Your cart is empty</p>";
        const tp = document.getElementById("totalPrice");
        if (tp) tp.innerText = "";
        return;
    }

    cart.forEach((item, i) => {
        total += parseInt(item.price) || 0;
        box.innerHTML += `
        <div class="card mb-3">
            <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                    <h6>${item.name}</h6>
                    <p class="mb-0">Size: ${item.size}</p>
                    <p class="text-success mb-0">₹${item.price}</p>
                </div>
                <button class="btn btn-sm btn-danger" onclick="removeItem(${i})">Remove</button>
            </div>
        </div>`;
    });

    const tp = document.getElementById("totalPrice");
    if (tp) tp.innerText = `Total: ₹${total}`;
}

// Remove item from cart by index
function removeItem(i) {
    cart.splice(i, 1);
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

function toggleDescription() {
    document.getElementById("descriptionBlock").classList.toggle("d-none");
}

function openImagePreviewFromHome(event, images) {
    event.stopPropagation(); // prevents dress modal opening

    if (!images || images.length === 0) {
        console.error("No images found");
        return;
    }

    currentImages = images;
    currentImageIndex = 0;

    document.getElementById("previewImage").src = images[0];
    document.getElementById("imageCounter").innerText = `1 / ${images.length}`;

    new bootstrap.Modal(document.getElementById("imagePreviewModal")).show();
}



