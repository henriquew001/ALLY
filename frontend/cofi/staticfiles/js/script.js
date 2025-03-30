 // cofi/static/js/script.js
 document.addEventListener('DOMContentLoaded', function() {
     const passwordToggles = document.querySelectorAll('.password-toggle');

     passwordToggles.forEach(toggle => {
         toggle.addEventListener('click', function() {
             const passwordFieldId = this.id.replace('toggle-', '');
             const passwordField = document.getElementById(passwordFieldId);

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