document.getElementById('register-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    let isValid = true;

    // Clear previous error messages
    document.getElementById('username-error').textContent = '';
    document.getElementById('email-error').textContent = '';
    document.getElementById('password-error').textContent = '';

    // Validate inputs
    if (username === '') {
        document.getElementById('username-error').textContent = 'Username is required.';
        isValid = false;
    }
    if (email === '') {
        document.getElementById('email-error').textContent = 'Email is required.';
        isValid = false;
    }
    if (password === '') {
        document.getElementById('password-error').textContent = 'Password is required.';
        isValid = false;
    }

    if (isValid) {
        // Create the data object for the API request
        const userData = {
            username: username,
            email: email,
            password: password
        };

        // Send data to the backend API using fetch
        fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                // If registration is successful, handle the response (e.g., show a success message or redirect)
                alert('Registration successful');
            } else {
                // Handle errors (e.g., username/email already exists)
                console.log('Error:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
