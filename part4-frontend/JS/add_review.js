/* =============================================
   add_review.js — Logic for add_review.html
============================================= */

async function submitReview(token, placeId, reviewText, rating) {
    const response = await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating),
            place_id: placeId
        })
    });
    return response;
}

function handleReviewResponse(response, form) {
    const successMsg = document.getElementById('success-msg');
    const errorMsg   = document.getElementById('error-msg');

    if (response.ok) {
        if (successMsg) successMsg.classList.remove('d-none');
        if (errorMsg) errorMsg.classList.add('d-none');
        form.reset();
        const placeId = getPlaceIdFromURL();
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 2000);
    } else {
        if (errorMsg) errorMsg.classList.remove('d-none');
        if (successMsg) successMsg.classList.add('d-none');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const addReviewCard = document.querySelector('.add-review');
    const successMsg = document.getElementById('success-msg');

    if (reviewForm && addReviewCard && successMsg) {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
        }

        checkAuthentication();

        const placeId = getPlaceIdFromURL();
        const backLink = document.querySelector('a[href="place.html"]');
        if (backLink && placeId) {
            backLink.href = `place.html?id=${placeId}`;
        }

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText  = document.getElementById('review-text').value.trim();
            const ratingInput = document.querySelector('input[name="rating"]:checked');
            const ratingError = document.getElementById('rating-error');

            if (!ratingInput) {
                ratingError.classList.remove('d-none');
                return;
            }
            ratingError.classList.add('d-none');

            const rating   = ratingInput.value;
            const response = await submitReview(token, placeId, reviewText, rating);
            handleReviewResponse(response, reviewForm);
        });
    }
});
