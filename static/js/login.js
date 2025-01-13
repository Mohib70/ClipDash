document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    let isValid = true;

    // Clear previous error messages
    document.getElementById('username-error').textContent = '';
    document.getElementById('password-error').textContent = '';

    // Validate inputs
    if (username === '') {
        document.getElementById('username-error').textContent = 'Username is required.';
        isValid = false;
    }
    if (password === '') {
        document.getElementById('password-error').textContent = 'Password is required.';
        isValid = false;
    }

    if (isValid) {
        try {
            const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                alert('Login successful! Redirecting to home page...');
                window.location.href = '/'; // Redirect to home page
            } else {
                const errorData = await response.json();
                alert(errorData.detail || 'An error occurred.');
            }
        } catch (error) {
            console.error('Error logging in:', error);
            alert('An unexpected error occurred. Please try again later.');
        }
    }
});
