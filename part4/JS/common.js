/* =============================================
   common.js — Shared utilities across all pages
============================================= */

const API_URL = 'http://127.0.0.1:5000/api/v1';

function setCookie(name, value, days = 1) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

function isAuthenticated() {
    return getCookie('token') !== null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const userNameSpan = document.getElementById('user-name');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    if (token && userNameSpan) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        fetch(`${API_URL}/users/${payload.sub}`)
            .then(res => {
                if (!res.ok) throw new Error('User not found');
                return res.json();
            })
            .then(user => {
                if (user.first_name && user.last_name) {
                    userNameSpan.textContent = `${user.first_name} ${user.last_name}`;
                    const dropdown = document.getElementById('user-dropdown');
                    if (dropdown) dropdown.style.display = 'inline';
                    const logoutBtn = document.getElementById('logout-btn');
                    if (logoutBtn) {
                        logoutBtn.addEventListener('click', (e) => {
                            e.preventDefault();
                            setCookie('token', '', -1);
                            window.location.href = 'index.html';
                        });
                    }
                }
            })
            .catch(() => {});
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }
}
