/* ========================================== */
/*        TEST_DRIVE.JS – FORM HANDLING       */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('testDriveForm');
    const submitBtn = document.getElementById('submitBtn');

    // Set min date to today
    const dateInput = document.getElementById('preferred_date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        // Set default to tomorrow
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        dateInput.value = tomorrow.toISOString().split('T')[0];
    }

    // ---------- Form Submit ----------
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            const name = document.getElementById('name');
            const email = document.getElementById('email');
            const date = document.getElementById('preferred_date');
            const time = document.getElementById('preferred_time');

            // Validate required fields
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

            if (!date.value) {
                date.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                date.style.borderColor = '#2a2a2a';
            }

            if (!time.value) {
                time.style.borderColor = '#dc3545';
                isValid = false;
            } else {
                time.style.borderColor = '#2a2a2a';
            }

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('[style*="border-color: #dc3545;"]');
                if (firstInvalid) firstInvalid.focus();
                return;
            }

            // Disable button to prevent double submission
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
        });
    }

    // ---------- Real-time validation clear ----------
    document.querySelectorAll('#testDriveForm input, #testDriveForm select, #testDriveForm textarea').forEach(function(el) {
        el.addEventListener('input', function() {
            this.style.borderColor = '#2a2a2a';
        });
        el.addEventListener('change', function() {
            this.style.borderColor = '#2a2a2a';
        });
    });

    console.log('🚗 Test Drive JS loaded.');
});