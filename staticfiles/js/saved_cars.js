/* ========================================== */
/*        SAVED_CARS.JS – REMOVE HANDLER      */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const removeButtons = document.querySelectorAll('.remove-btn');

    removeButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const carId = this.dataset.car;
            const savedId = this.dataset.id;
            const item = this.closest('.saved-item');

            if (!confirm('Remove this car from your wishlist?')) return;

            const originalHtml = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.disabled = true;

            fetch(`/cars/${carId}/save/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.saved === false) {
                    item.classList.add('removing');
                    setTimeout(function() {
                        item.remove();
                        if (document.querySelectorAll('.saved-item').length === 0) {
                            location.reload();
                        }
                    }, 300);
                } else {
                    alert('Could not remove. Please try again.');
                    this.innerHTML = originalHtml;
                    this.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.innerHTML = originalHtml;
                this.disabled = false;
                alert('An error occurred. Please try again.');
            });
        });
    });

    console.log('❤️ Saved Cars JS loaded.');
});