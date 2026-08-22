/* ========================================== */
/*        EDIT_CAR.JS – FORM HANDLING         */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('editForm');
    const submitBtn = document.getElementById('submitBtn');
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreview = document.getElementById('imagePreview');
    const imageFeedback = document.getElementById('imageFeedback');

    // ---------- Image Preview ----------
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            imagePreview.innerHTML = '';
            imagePreview.style.display = 'none';
            imageFeedback.textContent = '';
            imageFeedback.className = 'feedback';

            if (!file) return;

            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                imageFeedback.textContent = 'File size must be less than 5MB.';
                imageFeedback.className = 'feedback error';
                this.value = '';
                return;
            }

            // Validate file type
            const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                imageFeedback.textContent = 'Please upload a valid image (JPEG, PNG, WebP, or GIF).';
                imageFeedback.className = 'feedback error';
                this.value = '';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                imagePreview.appendChild(img);
                imagePreview.style.display = 'block';
                imageFeedback.textContent = 'Image uploaded successfully!';
                imageFeedback.className = 'feedback success';
            };
            reader.readAsDataURL(file);
        });
    }

    // ---------- Form Submit ----------
    if (form) {
        form.addEventListener('submit', function(e) {
            // Disable button to prevent double submission
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';
        });
    }

    console.log('✏️ Edit Car JS loaded.');
});