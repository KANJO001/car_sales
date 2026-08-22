/* ========================================== */
/*        REGISTER.JS – FORM INTERACTION      */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const form = document.querySelector('.register-form');
    const submitBtn = document.querySelector('.btn-register');

    // Password strength indicator (simple)
    const passwordInput = document.getElementById('id_password1');
    const confirmInput = document.getElementById('id_password2');

    // Real-time password match check
    if (passwordInput && confirmInput) {
        confirmInput.addEventListener('input', function() {
            if (this.value.length > 0 && this.value !== passwordInput.value) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#2a2a2a';
            }
        });
    }

    // Prevent double submission
    if (form) {
        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
        });
    }

    console.log('📝 Register JS loaded.');
});