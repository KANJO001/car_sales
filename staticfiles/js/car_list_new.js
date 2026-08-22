/* ========================================== */
/*        CAR_LIST.JS – INTERACTIONS          */
/* ========================================== */

console.log('🚗 NEW car_list.js loaded!');

document.addEventListener('DOMContentLoaded', function() {

    // ---------- Auto-submit filter on select change ----------
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(function(select) {
            select.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // ---------- Price range validation ----------
    const minPrice = document.querySelector('input[name="min_price"]');
    const maxPrice = document.querySelector('input[name="max_price"]');

    if (minPrice && maxPrice) {
        minPrice.addEventListener('change', function() {
            const minVal = parseFloat(this.value);
            const maxVal = parseFloat(maxPrice.value);
            if (this.value && maxPrice.value && minVal > maxVal) {
                alert('Minimum price cannot be greater than maximum price.');
                this.value = '';
            }
        });

        maxPrice.addEventListener('change', function() {
            const minVal = parseFloat(minPrice.value);
            const maxVal = parseFloat(this.value);
            if (this.value && minPrice.value && maxVal < minVal) {
                alert('Maximum price cannot be less than minimum price.');
                this.value = '';
            }
        });
    }

    // ---------- Animate car cards on scroll ----------
    const cards = document.querySelectorAll('.car-card');
    if (cards.length > 0) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry, index) {
                if (entry.isIntersecting) {
                    setTimeout(function() {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(function(card, index) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            setTimeout(function() {
                observer.observe(card);
            }, index * 50);
        });
    }

    console.log('✅ Car List JS fully loaded and running!');
});