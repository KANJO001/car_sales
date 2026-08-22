/* ========================================== */
/*        EDIT_CAR.JS – FORM HANDLING         */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('editForm');
    const submitBtn = document.getElementById('submitBtn');
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imageFeedback = document.getElementById('imageFeedback');

    // ---------- Image Preview ----------
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const files = this.files;
            imagePreviewContainer.innerHTML = '';
            imageFeedback.textContent = '';
            imageFeedback.className = 'feedback';

            if (!files || files.length === 0) return;

            let validCount = 0;
            let errorMessages = [];

            if (files.length > 10) {
                errorMessages.push('Maximum 10 images allowed.');
            }

            for (let i = 0; i < Math.min(files.length, 10); i++) {
                const file = files[i];
                
                if (file.size > 5 * 1024 * 1024) {
                    errorMessages.push(`"${file.name}" is larger than 5MB.`);
                    continue;
                }

                const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
                if (!validTypes.includes(file.type)) {
                    errorMessages.push(`"${file.name}" is not a valid image type.`);
                    continue;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    const div = document.createElement('div');
                    div.className = 'image-preview-item';
                    
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    div.appendChild(img);
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.className = 'remove-image';
                    removeBtn.innerHTML = '×';
                    removeBtn.type = 'button';
                    removeBtn.addEventListener('click', function() {
                        div.remove();
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

    // ---------- Remove Existing Images ----------
    document.querySelectorAll('.btn-remove-existing').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const imageId = this.dataset.id;
            const item = document.getElementById(`image-${imageId}`);
            
            if (!confirm('Remove this image?')) return;
            
            fetch(`/cars/image/${imageId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    item.style.transition = 'all 0.3s ease';
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => item.remove(), 300);
                } else {
                    alert('Could not remove image. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    });

    // ---------- Form Submit ----------
    if (form) {
        form.addEventListener('submit', function(e) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';
        });
    }

    // ---------- Utility: Get CSRF Token ----------
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

    console.log('✏️ Edit Car JS loaded.');
});