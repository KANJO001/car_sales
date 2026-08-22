/* ========================================== */
/*        CONTACT_SELLER.JS – FORM HANDLING   */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');

    // ---------- Form Submit ----------
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            // Simple validation
            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');

            if (!name.value.trim()) {
                name.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                name.style.borderColor = '#2a2a2a';
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                email.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                email.style.borderColor = '#2a2a2a';
            }

            if (!message.value.trim()) {
                message.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                message.style.borderColor = '#2a2a2a';
            }

            if (!isValid) {
                e.preventDefault();
                // Focus first invalid
                const firstInvalid = form.querySelector('[style*="border-color: #dc3545;"]');
                if (firstInvalid) firstInvalid.focus();
                return;
            }

            // Disable button to prevent double submission
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        });
    }

    // ---------- Real-time validation clear ----------
    document.querySelectorAll('#contactForm input, #contactForm textarea').forEach(function(el) {
        el.addEventListener('input', function() {
            this.style.borderColor = '#2a2a2a';
        });
    });

    console.log('📩 Contact Seller JS loaded.');
});