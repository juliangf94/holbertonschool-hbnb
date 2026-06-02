# HBnB Evolution — Part 4: Frontend

> Vanilla JS single-page frontend for the HBnB REST API — browse places, filter by price, log in with JWT, and leave reviews.

---

## Description

Part 4 is the client-side layer of HBnB Evolution. It consumes the Part 3 REST API using the Fetch API (no frameworks), manages authentication via JWT stored in cookies, and dynamically renders places, details, and reviews.

**Objectives:**
- Implement JWT-based authentication flow in the browser
- Dynamically fetch and display data from the REST API
- Allow authenticated users to submit reviews
- Apply client-side price filtering without a page reload

---

## Technologies

| Technology | Version | Purpose |
|---|---|---|
| HTML5 | — | Page structure |
| CSS3 | — | Styling |
| Bootstrap | 5.3.0 | Layout and components |
| Vanilla JavaScript | ES6+ | DOM manipulation, Fetch API, cookie management |
| HBnB Part 3 API | — | Backend data source |

---

## Prerequisites

- A modern browser (Chrome, Firefox, Edge)
- [HBnB Part 3 backend](../part3-backend/) running at `http://127.0.0.1:5000`
- Python 3 (optional — only if serving via `http.server`)

---

## Installation

No build step or package manager required.

1. Make sure the Part 3 API is running:

```bash
cd ../part3-backend
source .venv/bin/activate
python3 run.py
```

2. Serve the frontend:

```bash
cd part4-frontend
python3 -m http.server 8080
```

3. Open `http://localhost:8080` in your browser.

Alternatively, open `index.html` directly in the browser if CORS is not an issue.

---

## Usage

### Browse places

The home page lists all available places fetched from the API. Use the **Max Price** input to filter results client-side.

### Log in

Navigate to `login.html` or click the **Login** button. Enter valid credentials (default admin: `admin@hbnb.io` / `admin1234`). A JWT token is stored in a cookie on success and used for all subsequent authenticated requests.

### View place details

Click **View Details** on any place card to see the full description, amenities, and reviews.

### Leave a review

When logged in, a review form appears on the place detail page. Submit it to POST to `POST /api/v1/reviews/`.

---

## Pages

| File | Description |
|---|---|
| `index.html` | Home — place listing with price filter |
| `login.html` | Login form — obtains JWT token |
| `place.html` | Place detail — amenities, images, reviews |
| `add_review.html` | Review submission form |

## JavaScript modules

| File | Responsibility |
|---|---|
| `JS/common.js` | Cookie helpers, `checkAuthentication()`, shared API URL |
| `JS/index.js` | Fetch and render place list, client-side filter |
| `JS/login.js` | Login form submit, token storage |
| `JS/place.js` | Fetch and render place detail, reviews |
| `JS/add_review.js` | Review form submit |

---

## Features

- **JWT auth** — login/logout flow; protected sections hidden when unauthenticated
- **Dynamic rendering** — places and reviews built from API responses, no static HTML
- **Client-side price filter** — filters without a round-trip to the server
- **Responsive layout** — Bootstrap 5 grid, mobile-friendly
- **WebP images** — optimized place photos served as `.webp` for performance

---

## Acknowledgments

Part of the [HBnB Evolution](../README.md) project — Holberton School, 2025-2026.

- **Julian** — frontend implementation, image optimization, UI design
- **Fabien** — JWT authentication (Part 3 backend)
- **Georgia** — SQLAlchemy persistence (Part 3 backend)
