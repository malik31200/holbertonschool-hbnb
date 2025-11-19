document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errordiv = document.getElementById('error-message');
    const submitBtn = loginForm ? loginForm.querySelector('button[type="submit"]') : null;

    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (errordiv) errordiv.textContent = '';

        if (!loginForm.checkValidity()) {
            loginForm.reportValidity();
            return;
        }

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Connexion...';
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            const payload = await response.json().catch(() => null);

            if (response.ok && payload && payload.access_token) {
                document.cookie = `token=${payload.access_token}; path=/; max-age=86400`;
                console.log('Cookie créé :', document.cookie);

                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 100);
            } else {
                const msg = payload && payload.message ? payload.message : 'login failed';
                if (errordiv) errordiv.textContent = msg;
            }
        } catch (error) {
            console.error('Network error', error);
            if (errordiv) errordiv.textContent = 'Network error: Unable to reach server.';
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Login';
            }
        }
    });
});
