document.addEventListener('DOMContentLoaded', function() {
    console.log('🏎️ Homepage loaded.');
    const startBtn = document.querySelector('.btn-start');
    if (startBtn) {
        startBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('🚗 Journey Started!');
        });
    }
});