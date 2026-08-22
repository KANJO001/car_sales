/* ========================================== */
/*        SELL_CAR.JS – FORM HANDLING         */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('sellForm');
    const submitBtn = document.getElementById('submitBtn');
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imageFeedback = document.getElementById('imageFeedback');

    // ---------- Multiple Image Preview ----------
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const files = this.files;
            imagePreviewContainer.innerHTML = '';
            imageFeedback.textContent = '';
            imageFeedback.className = 'feedback';

            if (!files || files.length === 0) return;

            let validCount = 0;
            let errorMessages = [];

            // Limit to 10 images
            if (files.length > 10) {
                errorMessages.push('Maximum 10 images allowed.');
            }

            // Validate each file
            const maxFiles = Math.min(files.length, 10);
            for (let i = 0; i < maxFiles; i++) {
                const file = files[i];
                
                // Validate file size (max 5MB each)
                if (file.size > 5 * 1024 * 1024) {
                    errorMessages.push(`"${file.name}" is larger than 5MB.`);
                    continue;
                }

                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
                if (!validTypes.includes(file.type)) {
                    errorMessages.push(`"${file.name}" is not a valid image type.`);
                    continue;
                }

                // Create preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    const div = document.createElement('div');
                    div.className = 'image-preview-item';
                    
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    div.appendChild(img);
                    
                    // Add remove button
                    const removeBtn = document.createElement('button');
                    removeBtn.className = 'remove-image';
                    removeBtn.innerHTML = '×';
                    removeBtn.type = 'button';
                    removeBtn.addEventListener('click', function() {
                        div.remove();
                        // Update files list (remove this file)
                        const dt = new DataTransfer();
                        for (let j = 0; j < imageInput.files.length; j++) {
                            if (j !== i) {
                                dt.items.add(imageInput.files[j]);
                            }
                        }
                        imageInput.files = dt.files;
                    });
                    div.appendChild(removeBtn);
                    
                    imagePreviewContainer.appendChild(div);
                };
                reader.readAsDataURL(file);
                validCount++;
            }

            // Show feedback
            if (validCount > 0) {
                imageFeedback.textContent = `${validCount} image(s) uploaded successfully!`;
                imageFeedback.className = 'feedback success';
            }

            if (errorMessages.length > 0) {
                imageFeedback.textContent = errorMessages.join(' ');
                imageFeedback.className = 'feedback error';
            }
        });
    }

    // ---------- Form Submit ----------
    if (form) {
        form.addEventListener('submit', function(e) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
        });
    }

    console.log('🚗 Sell Car JS loaded.');
});