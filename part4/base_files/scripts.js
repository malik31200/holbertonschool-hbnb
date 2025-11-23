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
        loginLink.textContent = 'Login';
        loginLink.onclick = () => {
            window.location.href = 'login.html';
        };
    } else {
        loginLink.textContent = 'Logout';
        loginLink.onclick = () => {
            document.cookie = 'token=; path=/; max=age=0';
            window.location.reload();
        }
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
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">Details</button>
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

function  getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id')
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (!res.ok) {
            console.error('Failed to fetch place details', res.status);
            return null;
        }
        const data = await res.json();
        return data;
    } catch (err) {
        console.error('Error fetching place details:', err);
    }
}

function displayPlaceDetails(place) {
    const titleElt = document.getElementById('place-title');
    const detailsElt = document.getElementById('place-details')
    if (!detailsElt) return;

    if (titleElt) titleElt.textContent = place.title || 'Place';

    const ownerName = place.owner ? `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim() : 'Unknown';
    const amenities = Array.isArray(place.amenities) ? place.amenities.map(a => a.name).join(', ') : '';

    detailsElt.innerHTML = `
        <div class = "place-details">
            <div style="flex:1">
                <p class="place-info"><strong>Host: </strong>${ownerName}</p>
                <p class="place-info"><strong>Price: </strong>${place.price ?? 'N/A'}€</p>
                <p class="place-info"><strong>Description: </strong>${place.description ?? ''}</p>
                <p class="place-info"><strong>Rooms : </strong>${place.rooms ?? 'N/A'}</p>
                <p class="place-info"><strong>Capacity : </strong>${place.capacity ?? 'N/A'}</p>
                <p class="place-info"><strong>Surface : </strong>${place.surface ?? 'N/A'}m²</p>
                <p class="place-info"><strong>Amenities : </strong>${amenities}</p>
            </div>
        </div>
    `;

    let reviewsContainer = document.getElementById('reviews');
    if (!reviewsContainer) {
        reviewsContainer = document.createElement('div');
        reviewsContainer.id = 'reviews';
        detailsElt.insertAdjacentElement('afterend', reviewsContainer);
    }
    reviewsContainer.innerHTML = '<h2>Reviews</h2>';

    console.log('Place reviews:', place.reviews);

    if(!place.reviews || place.reviews.length === 0) {
        reviewsContainer.innerHTML = '<p> No reviews yet.</p>';

    } else {
        place.reviews.forEach(review => {
            console.log('Review data:', review);

            const rev = document.createElement('div');
            rev.className = 'review-card';

            let userName = 'Anonymous';

            if (review.author) {
                if (typeof review.author === 'object') {
                    userName = `${review.author.first_name || ''} ${review.author.last_name || ''}`.trim() || 'Anonymous';
                } else {
                    userName = review.author;
                }
            } else if (review.user) {
                if (typeof review.user === 'object') {
                    userName = `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim() || 'Anonymous';
                } else {
                    userName = review.user;
                }
            }

            const ratingValue = review.rating ?? 0;
            const star = '★'.repeat(Math.max(0, Math.min(5, ratingValue))) + '☆'.repeat(Math.max(0, 5 - ratingValue));
            
            rev.innerHTML = `
                <p><strong>User: </strong>${userName}</p>
                <p>Rating: ${star}</p>
                <p>${review.text ?? review.title ?? ''}</p>
            `;
            reviewsContainer.appendChild(rev);
        })
    }
}

function toggleAddReviewVisibility() {
    const token = getCookie('token');
    const addReviewElt = document.getElementById('add-review');
    if(!addReviewElt) return;

    if (token) {
        addReviewElt.style.display = 'block';
    } else {
        addReviewElt.style.display = 'none';
    }
}

function setupAddReviewButton() {
    const addReviewBtn = document.getElementById('add-review-btn');
    if (addReviewBtn) {
        addReviewBtn.addEventListener('click', () => {
            const placeId = getPlaceIdFromURL();
            window.location.href = `add_review.html?id=${placeId}`;
        });
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const placeId = getPlaceIdFromURL();
    if(!placeId) return;

    checkAuthentication();
    toggleAddReviewVisibility();
    setupAddReviewButton();

    const token = getCookie('token');

    const place = await fetchPlaceDetails(token, placeId);
    if (place) {
        displayPlaceDetails(place);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.querySelector('.add-review');
    if (!reviewForm) return;

    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review');
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('No place ID found');
        window.location.href = 'index.html';
        return;
    }

    checkAuthentication();

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const rating = document.querySelector('input[name="rating"]:checked');
        const comment = document.getElementById('comment').value.trim();

        console.log('Rating:', rating ? rating.value : 'NONE');
        console.log('Comment:', comment);
        console.log('Comment length:', comment.length);
        console.log('Place ID:', placeId);

        if (!rating) {
            alert('Please select a rating.');
            return;
        }

        if (!comment) {
            alert('Please enter a comment')
            return;
        }

        const submitBtn = reviewForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
        }

        const payload = {
            text: comment,
            rating: parseInt(rating.value),
            place_id: placeId
        };

        console.log('Payload to send:', JSON.stringify(payload, null, 2));

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            console.log('Response status:', response.status);

            const responseData = await response.json().catch(() => null);
            console.log('Response data:', responseData);
        
            if (response.ok) {
                alert('Review submitted successfully!')
                reviewForm.reset();

                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 500);
            } else {
                const errorData = await response.json().catch(() => null);
                const errorMessage = errorData?.error || 'Failed to submit review';
                alert(errorMessage);
                console.error('API error:', errorData);
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Network error: Unable to reach server.');
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit';
            }
        }
    });
});
