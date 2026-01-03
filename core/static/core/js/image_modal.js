function openModal(imgSrc) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImg");

    modalImg.src = imgSrc;
    modal.style.display = "flex";
}

// Close modal
function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}

// Close on ESC key
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        closeModal();
    }
});
