document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login_form');
    const registrationForm = document.getElementById('registration_form');
    const showRegistrationLink = document.getElementById('show_registration');
    const showLoginLink = document.getElementById('show_login');
    
    // Toggle to registration form
    showRegistrationLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginForm.classList.add('hidden');
        registrationForm.classList.remove('hidden');
        
        // Update URL without reloading the page
        window.history.pushState({}, '', '/register');
    });
    
    // Toggle to login form
    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        registrationForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        
        // Update URL without reloading the page
        window.history.pushState({}, '', '/login');
    });
    
    // Registration form validation
    const registrationFormElement = document.getElementById('registration_form_element');
    registrationFormElement.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('reg_email').value;
        const password = document.getElementById('reg_password').value;
        const confirmPassword = document.getElementById('reg_confirm_password').value;
        
        // Remove any existing error messages
        const existingError = document.querySelector('.error_message');
        if (existingError) existingError.remove();
        
        // Validate password match
        if (password !== confirmPassword) {
            const errorMessage = document.createElement('p');
            errorMessage.classList.add('error_message');
            errorMessage.textContent = 'Пароли не совпадают';
            registrationFormElement.appendChild(errorMessage);
            return;
        }
        
        // Create form data for submission
        const formData = {
            email: email,
            password: password
        };
        
        // Submit registration data to the API
        fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                // Registration successful
                const successMessage = document.createElement('p');
                successMessage.classList.add('success_message');
                successMessage.textContent = 'Регистрация успешна! Перенаправление на страницу входа...';
                registrationFormElement.appendChild(successMessage);
                
                // Redirect to login after a short delay
                setTimeout(() => {
                    registrationForm.classList.add('hidden');
                    loginForm.classList.remove('hidden');
                    window.history.pushState({}, '', '/login');
                }, 2000);
            } else {
                // Registration failed
                const errorMessage = document.createElement('p');
                errorMessage.classList.add('error_message');
                errorMessage.textContent = data.detail || 'Ошибка при регистрации';
                registrationFormElement.appendChild(errorMessage);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.createElement('p');
            errorMessage.classList.add('error_message');
            errorMessage.textContent = 'Произошла ошибка при отправке запроса';
            registrationFormElement.appendChild(errorMessage);
        });
    });
});