document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const message = document.getElementById('message');

            // Reset border colors
            [name, email, message].forEach(field => {
                if (field) field.style.borderColor = '#2a2a2a';
            });

            if (!name.value.trim()) {
                name.style.borderColor = '#dc3545';
                isValid = false;
            }

            if (!email.value.trim() || !email.value.includes('@')) {
                email.style.borderColor = '#dc3545';
                isValid = false;
            }

            if (!message.value.trim()) {
                message.style.borderColor = '#dc3545';
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('[style*="border-color: #dc3545;"]');
                if (firstInvalid) firstInvalid.focus();
                return;
            }

            // Disable button
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            // If the form submission is successful, the page will reload with messages.
            // The celebration will be triggered by the script in contact_seller.html.
        });
    }

    // Real-time validation clear
    document.querySelectorAll('#contactForm input, #contactForm textarea').forEach(function(el) {
        el.addEventListener('input', function() {
            if (this.style.borderColor === '#dc3545' && this.value.trim()) {
                this.style.borderColor = '#2a2a2a';
            }
        });
    });

    console.log('📩 Contact Seller JS loaded.');
});