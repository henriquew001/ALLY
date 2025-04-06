// ally/static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    const passwordToggles = document.querySelectorAll('.password-toggle');
    console.log('passwordToggles:', passwordToggles);

    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            console.log('Toggle clicked:', this);
            // Find the password input field by traversing the DOM
            const passwordField = this.closest('.password-input-container').querySelector('input');
            console.log('passwordField:', passwordField);

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });
});
