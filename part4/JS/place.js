/* =============================================
   place.js — Logic for place.html
============================================= */

async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.status);
        }
    } catch (error) {
        console.error('Connection error:', error);
    }
}

function displayPlaceDetails(place) {
    const placeInfo = document.querySelector('#place-details .place-info');
    const reviewsSection = document.getElementById('reviews');
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!placeInfo) return;

    const amenityIcons = {
        'WiFi': '📶', 'Pool': '🏊', 'Kitchen': '🍳',
        'Heating': '🔥', 'Pet Friendly': '🐾', 'Parking': '🚗',
        'Air Conditioning': '❄️', 'Lake View': '🏞️',
        'Private Garden': '🌿', 'Forest Access': '🌲',
        'Train': '🚂', 'Quidditch Field': '🧹', 'Library': '📚',
        'Desert View': '🏜️', 'Stargazing Deck': '🌌'
    };

    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<span class="amenity-badge">${amenityIcons[a.name] || '✓'} ${a.name}</span>`).join('')
        : '<span class="text-muted">No amenities listed.</span>';

    const heroPositions = {
        'images/Rennes/3.jpg': 'center 70%',
        'images/Tatooine/2.jpg': 'center 80%',
        'images/Hogwarts/header.jpg': 'center 60%',
    };

    const heroUrl = (place.images && place.images.length > 0)
        ? place.images[place.images.length - 1].image_url
        : place.image_url;
    const heroPosition = heroPositions[heroUrl] || 'center';
    const heroImg = heroUrl
        ? `<div class="place-hero" style="background-image: url('${heroUrl}'); background-position: ${heroPosition};"></div>`
        : '';

    const thumbImg = place.image_url
        ? `<img src="${place.image_url}" alt="${place.title}" class="place-thumb">`
        : '';

    placeInfo.innerHTML = `
        ${heroImg}
        <div class="place-body-layout">
            ${thumbImg ? `<div class="place-thumb-col">${thumbImg}</div>` : ''}
            <div class="place-info-col">
                <h1 class="place-title">${place.title}</h1>
                <p class="price-badge">$${place.price} / night</p>
                <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
                <p class="mt-2">${place.description || 'No description available.'}</p>
                <div class="mt-3">
                    <strong>Amenities:</strong>
                    <div class="mt-2">${amenitiesHTML}</div>
                </div>
            </div>
        </div>
    `;

    // Gallery of additional images
    const gallerySection = document.getElementById('place-gallery');
    if (gallerySection) {
        gallerySection.innerHTML = '';
        if (place.images && place.images.length > 0) {
            gallerySection.innerHTML = `<h3 class="mb-3">Photos</h3>`;
            const grid = document.createElement('div');
            grid.className = 'gallery-grid';
            place.images.forEach(img => {
                const item = document.createElement('div');
                item.className = 'gallery-item';
                const image = document.createElement('img');
                image.src = img.image_url;
                image.alt = 'Place photo';
                image.className = 'gallery-img';
                image.loading = 'lazy';
                image.style.cursor = 'zoom-in';
                image.addEventListener('click', () => openLightbox(img.image_url));
                item.appendChild(image);
                grid.appendChild(item);
            });
            gallerySection.appendChild(grid);
        }
    }

    if (reviewsSection) {
        reviewsSection.querySelectorAll('.review-card, .review-summary').forEach(el => el.remove());

        if (place.reviews && place.reviews.length > 0) {
            // Average rating + count
            const avg = (place.reviews.reduce((sum, r) => sum + r.rating, 0) / place.reviews.length).toFixed(1);
            const summary = document.createElement('div');
            summary.className = 'review-summary';
            summary.innerHTML = `<span class="review-avg-stars">★</span> <strong>${avg}</strong> · ${place.reviews.length} review${place.reviews.length > 1 ? 's' : ''}`;
            reviewsSection.appendChild(summary);

            // Sort newest first (by id as proxy, or just reverse)
            const sorted = [...place.reviews].reverse();

            sorted.forEach(async review => {
                const card = document.createElement('div');
                card.classList.add('review-card');

                let userName = 'Anonymous';
                try {
                    const userResponse = await fetch(`${API_URL}/users/${review.user_id}`);
                    if (userResponse.ok) {
                        const user = await userResponse.json();
                        userName = `${user.first_name} ${user.last_name}`;
                    }
                } catch (e) {
                    console.error('Could not fetch user:', e);
                }

                const initials = userName === 'Anonymous' ? '?' : userName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
                const date = review.created_at ? new Date(review.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : '';

                card.innerHTML = `
                    <div class="review-header">
                        <div class="reviewer-info">
                            <div class="reviewer-avatar">${initials}</div>
                            <div>
                                <span class="reviewer-name">${userName}</span>
                                ${date ? `<span class="review-date">${date}</span>` : ''}
                            </div>
                        </div>
                        <span class="stars">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                    </div>
                    <p class="review-text">${review.text}</p>
                `;
                reviewsSection.appendChild(card);
            });
        } else {
            const noReviews = document.createElement('p');
            noReviews.classList.add('text-muted');
            noReviews.textContent = 'No reviews yet. Be the first to review!';
            reviewsSection.appendChild(noReviews);
        }
    }

    if (token && addReviewSection) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentUserId = payload.sub;
        const alreadyReviewed = place.reviews && place.reviews.some(r => r.user_id === currentUserId);
        const isOwner = place.owner && place.owner.id === currentUserId;
        if (alreadyReviewed || isOwner) {
            addReviewSection.style.display = 'none';
        }
    }
}

function openLightbox(src) {
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    img.src = src;
    lightbox.style.display = 'flex';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'none';
    document.getElementById('lightbox-img').src = '';
}

document.addEventListener('DOMContentLoaded', () => {
    const lightbox = document.getElementById('lightbox');
    if (lightbox) {
        lightbox.addEventListener('click', closeLightbox);
        document.getElementById('lightbox-close').addEventListener('click', closeLightbox);
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeLightbox();
        });
    }

    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        checkAuthentication();
        const token = getCookie('token');
        const placeId = getPlaceIdFromURL();

        if (placeId) fetchPlaceDetails(token, placeId);

        const addReviewLink = document.getElementById('add-review-link');
        if (addReviewLink && placeId) {
            addReviewLink.href = `add_review.html?id=${placeId}`;
        }
    }
});
