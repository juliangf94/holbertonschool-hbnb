/* =============================================
   index.js — Logic for index.html
============================================= */

async function fetchPlaces(token) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`${API_URL}/places/`, { headers });
        if (response.ok) {
            const places = await response.json();
            window.allPlaces = places;
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.status);
        }
    } catch (error) {
        console.error('Connection error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';
    places.sort((a, b) => a.price - b.price);

    if (places.length === 0) {
        placesList.innerHTML = '<p class="text-muted">No places found.</p>';
        return;
    }

    places.forEach((place, index) => {
        const card = document.createElement('div');
        card.classList.add('col-md-3', `card-gradient-${index % 4}`);
        card.dataset.price = place.price;

        const imgPosition = place.image_url && place.image_url.includes('Hogwarts') ? '50% 30%' : 'center';
        const imageContent = place.image_url
            ? `<img src="${place.image_url}" alt="${place.title}" class="place-card-photo" style="object-position: ${imgPosition};">`
            : `<span class="place-card-initial">${place.title.charAt(0).toUpperCase()}</span>`;

        card.innerHTML = `
            <article class="place-card">
                <div class="place-card-img">
                    ${imageContent}
                </div>
                <div class="place-card-body">
                    <h2>${place.title}</h2>
                    <p class="price-tag">$${place.price} <span>/ night</span></p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                </div>
            </article>
        `;
        placesList.appendChild(card);
    });
}

function filterPlaces(maxPrice) {
    const scrollY = window.scrollY;
    const cards = document.querySelectorAll('#places-list .col-md-3');
    const limit = maxPrice === 'all' ? Infinity : parseFloat(maxPrice);
    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (price <= limit) ? 'block' : 'none';
    });
    window.scrollTo({ top: scrollY, behavior: 'instant' });
}

document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
        const token = getCookie('token');
        fetchPlaces(token);

        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('input', (event) => {
                event.preventDefault();
                const val = event.target.value.trim();
                filterPlaces(val === '' ? 'all' : val);
            });
            priceFilter.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') event.preventDefault();
            });
        }
    }
});
