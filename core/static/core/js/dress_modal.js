// Global variables for image navigation
let currentImages = [];
let currentImageIndex = 0;

function showDressDetails(id, name, price, description, images, sizes) {
    // Store images globally for navigation
    currentImages = images;
    currentImageIndex = 0;

    document.getElementById("dressModalLabel").innerText = name;
    document.getElementById("modalPrice").innerText = "₹" + price;
    document.getElementById("modalDescription").innerText =
        description || "No description available";

    /* IMAGES */
    const imgBox = document.getElementById("modalImages");
    imgBox.innerHTML = "";

    if (images.length > 0) {
        images.forEach((img, index) => {
            const image = document.createElement("img");
            image.src = img;
            image.classList.add("rounded-3");
            image.style.width = "180px";
            image.style.height = "180px";
            image.style.objectFit = "cover";
            image.style.cursor = "pointer";
            image.style.transition = "transform 0.2s";

            // 🔥 CLICK TO MAXIMIZE with index
            image.onclick = () => openImagePreview(index);
            
            // Hover effect
            image.onmouseover = () => image.style.transform = "scale(1.05)";
            image.onmouseout = () => image.style.transform = "scale(1)";

            imgBox.appendChild(image);
        });
    } else {
        imgBox.innerHTML = "<p class='text-muted'>No images available</p>";
    }

    /* SIZES */
    const sizeBox = document.getElementById("modalSizes");
    sizeBox.innerHTML = "";

    if (sizes.length > 0) {
        sizes.forEach(size => {
            const span = document.createElement("span");
            span.className = "size-badge me-1";
            span.innerText = size;
            sizeBox.appendChild(span);
        });
    } else {
        sizeBox.innerHTML = "<span class='text-muted'>No sizes available</span>";
    }

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
    if (currentImageIndex < currentImages.length - 1) {
        currentImageIndex++;
        updatePreviewImage();
    }
}

/* Navigate to previous image */
function prevImage() {
    if (currentImageIndex > 0) {
        currentImageIndex--;
        updatePreviewImage();
    }
}

/* Keyboard navigation */
document.addEventListener("keydown", (e) => {
    const modal = document.getElementById("imagePreviewModal");
    if (modal && modal.classList.contains("show")) {
        if (e.key === "ArrowRight") nextImage();
        if (e.key === "ArrowLeft") prevImage();
    }
});
