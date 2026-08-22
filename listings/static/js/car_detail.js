/* ========================================== */
/*        CAR_DETAIL.JS – SAVE + TOAST        */
/* ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    const saveBtn = document.getElementById('saveBtn');
    if (!saveBtn) return;

    saveBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const url = this.href;

        this.style.pointerEvents = 'none';
        this.style.opacity = '0.6';

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.style.pointerEvents = 'auto';
            this.style.opacity = '1';

            if (data.saved) {
                this.classList.add('saved');
                this.innerHTML = '<i class="fas fa-heart"></i> Saved';
                showToast('✅ Car saved to wishlist!');
            } else {
                this.classList.remove('saved');
                this.innerHTML = '<i class="fas fa-heart"></i> Save';
                showToast('🗑️ Car removed from wishlist');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.style.pointerEvents = 'auto';
            this.style.opacity = '1';
            showToast('❌ Something went wrong. Please try again.');
        });
    });

    function showToast(message) {
        const oldToast = document.getElementById('customToast');
        if (oldToast) oldToast.remove();

        const toast = document.createElement('div');
        toast.id = 'customToast';
        toast.innerHTML = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #141414;
            color: #ffffff;
            padding: 15px 25px;
            border-radius: 8px;
            border-left: 4px solid #f97316;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            z-index: 9999;
            font-weight: 500;
            font-size: 1rem;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.4s ease, transform 0.4s ease;
            max-width: 400px;
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        }, 50);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }

    console.log('🚗 Car Detail JS with toast loaded.');
});