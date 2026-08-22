/* ========================================== */
/*        DASHBOARD.JS – INTERACTIONS         */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ---------- Delete Car (with confirmation) ----------
    const deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const carId = this.dataset.id;
            const carName = this.dataset.name;

            if (confirm(`Are you sure you want to delete "${carName}"?`)) {
                // Send DELETE request to the server
                fetch(`/cars/${carId}/delete/`, {
                    method: 'DELETE',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // Remove the card from the DOM
                        const card = this.closest('.listing-card');
                        card.style.transition = 'all 0.3s ease';
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            card.remove();
                            // Update stats or show empty state if needed
                            location.reload(); // Simple reload to refresh stats
                        }, 300);
                    } else {
                        alert('Something went wrong. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            }
        });
    });

    // ---------- Remove Saved Car ----------
    const removeSavedButtons = document.querySelectorAll('.btn-remove-saved');

    removeSavedButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const carId = this.dataset.id;
            const card = this.closest('.saved-card');

            if (confirm('Remove this car from your wishlist?')) {
                fetch(`/cars/${carId}/save/`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.saved === false) {
                        card.style.transition = 'all 0.3s ease';
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            card.remove();
                            location.reload();
                        }, 300);
                    } else {
                        alert('Could not remove. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            }
        });
    });

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

    console.log('📊 Dashboard JS loaded.');
});