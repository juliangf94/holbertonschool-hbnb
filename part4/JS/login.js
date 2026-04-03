/* =============================================
   login.js — Logic for login.html
============================================= */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    return response;
}

document.addEventListener('DOMContentLoaded', () => {

    /* --- Toggle password visibility --- */
    const togglePassword = document.getElementById('toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const passwordInput = document.getElementById('password');
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';
            togglePassword.textContent = isPassword ? '🙈' : '👁';
        });
    }

    /* --- Login form --- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorMsg = document.getElementById('login-error');

            try {
                const response = await loginUser(email, password);
                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token, 1);
                    window.location.href = 'index.html';
                } else {
                    if (errorMsg) {
                        errorMsg.textContent = 'Invalid email or password. Please try again.';
                        errorMsg.classList.remove('d-none');
                    }
                }
            } catch (error) {
                if (errorMsg) {
                    errorMsg.textContent = 'Connection error. Make sure the API is running.';
                    errorMsg.classList.remove('d-none');
                }
            }
        });
    }
});
