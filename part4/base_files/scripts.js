function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }

    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    const errordiv = document.getElementById('error-message');
    const submitBtn = loginForm ? loginForm.querySelector('button[type="submit"]') : null;

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
                console.log('Cookie created :', document.cookie);

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

document.addEventListener('DOMContentLoaded', async () => {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    checkAuthentication();

    const token = getCookie('token');
    if (!token) return;

    try{
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            console.error('Failed to fetch places');
            return;
        }
        
        const places = await response.json();

        displayPlaces(places);
        setupPriceFilter();
    } catch (error) {
        console.error('Error fetching places:', error);
    }
});

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    list.innerHTML = "";

    places.forEach(place => {
        const div = document.createElement('div');
        div.className = "place-card";
        div.dataset.price = place.price;

        div.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p><strong>Price:</strong>${place.price}€/night</p>
            <p><strong>Location:</strong>${place.location}</p>
            <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
        `;

        list.appendChild(div);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener("change", () => {
        const maxPrice = filter.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);

            if (maxPrice === 'all' || price <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
