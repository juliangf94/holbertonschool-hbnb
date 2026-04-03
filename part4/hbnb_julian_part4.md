# HBnB Part 4 — Simple Web Client
## Tecnologías utilizadas

- **HTML5** — estructura semántica de las páginas
- **CSS3** — estilos y diseño visual
- **Bootstrap 5.3** — framework CSS para diseño responsivo
- **JavaScript ES6** — lógica del cliente y llamadas a la API
- **Fetch API** — comunicación con el backend
- **Cookies** — almacenamiento del JWT token

---

## Paleta de colores

| Variable | Color | Uso |
|---|---|---|
| `--navy` | `#1a2e4a` | Header, footer, títulos |
| `--blue` | `#2563eb` | Botones principales, links |
| `--gold` | `#f59e0b` | Ratings, detalles |
| `--bg` | `#f8f9fa` | Fondo de las páginas |
| `--border` | `#ddd` | Bordes de cards |

---

## Estructura del proyecto

```
part4/
├── index.html          # Lista de lugares
├── login.html          # Formulario de login
├── place.html          # Detalle de un lugar
├── add_review.html     # Formulario para agregar una review
├── styles.css          # Estilos globales
├── scripts.js          # Lógica JavaScript
└── images/
    └── logo.png        # Logo de la aplicación
```

---
---

# Task 0 — Design
## Objetivo
Crear las 4 páginas HTML con estructura semántica y estilos CSS que respeten las especificaciones del enunciado.

## Páginas creadas

| Página | Descripción |
|---|---|
| `login.html` | Formulario con campos email y password |
| `index.html` | Lista de places como cards con botón "View Details" |
| `place.html` | Detalle de un lugar con reviews y formulario |
| `add_review.html` | Formulario para agregar una review (solo usuarios autenticados) |

## Parámetros fijos (obligatorios del enunciado)

Todos los cards respetan estos valores sin excepción:

```css
.place-card, .review-card {
    margin: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
}
```

## Clases obligatorias implementadas

| Clase | Elemento | Archivo |
|---|---|---|
| `logo` | Logo en el header | Todas las páginas |
| `login-button` | Botón/link de login | Todas las páginas |
| `place-card` | Card de cada lugar | `index.html` |
| `details-button` | Botón "View Details" | `index.html` |
| `place-details` | Sección de detalle | `place.html` |
| `place-info` | Info del lugar | `place.html` |
| `review-card` | Card de cada review | `place.html` |
| `add-review` | Sección del formulario | `place.html`, `add_review.html` |
| `form` | Formulario de review | `place.html`, `add_review.html` |

## Estructura del Header (igual en todas las páginas)

```html
<header class="hbnb-header">
    <div class="container d-flex justify-content-between align-items-center py-3">
        <img src="images/logo.png" alt="HBnB Logo" class="logo">
        <nav class="d-flex align-items-center gap-3">
            <a href="index.html" class="nav-link-custom">Home</a>
            <a href="login.html" class="btn btn-login login-button">Login</a>
        </nav>
    </div>
</header>
```

## Estructura del Footer (igual en todas las páginas)

```html
<footer class="hbnb-footer">
    <div class="container text-center py-3">
        <p class="mb-0">All rights reserved © 2026 HBnB</p>
    </div>
</footer>
```

## Bootstrap

Importado via CDN — no requiere instalación:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Bootstrap** se usa para el grid (`container`, `row`, `col-md-*`), utilidades de espaciado (`d-flex`, `gap-3`, `mb-4`) y componentes base que luego se personalizan con `styles.css`.

Las clases más importantes que usamos
Layout y espaciado:
| Clase | Qué hace |
| :... | :... |
| container | Centra el contenido con margen automático |
| d-flex | Activa flexbox |
| justify-content-between | Separa los elementos al máximo |
| align-items-center | Centra verticalmente |
| gap-3 | Espacio de 1rem entre elementos flex |
| mb-4 | Margin bottom de 1.5rem |
| py-3 | Padding arriba y abajo de 1rem |
| mt-5, my-5 | Margin top / margin vertical |

Grid (sistema de columnas):
```html
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
```
Esto significa: en pantallas medianas ocupá 8 columnas de 12, en pantallas grandes ocupá 6.  
Bootstrap divide la pantalla en 12 columnas — es responsivo automáticamente.

Componentes:
| Clase | Qué hace |
| :... | :... |
| btn | Estilo base de botón |
| btn-lg | Botón grande |
| btn-outline-secondary | Botón con borde gris |
| alert alert-success | Caja verde de éxito |
| alert alert-danger | Caja roja de error |
| form-control | Estilo para inputs y textareas |
| form-label | Estilo para label |
| sd-none | Oculta un elemento (display: none) |
| d-grid | Para que el botón ocupe el ancho completo |
| text-muted | Texto gris claro |
| fw-semibold | Texto semi-negrita |


## Validación W3C

Todas las páginas deben ser validadas en https://validator.w3.org/

Puntos clave para pasar la validación:
- `<!DOCTYPE html>` al inicio de cada archivo
- `lang="en"` en el tag `<html>`
- `alt` en todas las imágenes
- No usar atributos `style=""` inline — todo en `styles.css`
- Cerrar todos los tags correctamente

---
---

# Task 1 — Login
## Objetivo
Implementar el login con la API usando Fetch y guardar el token JWT en una cookie.

---

## Servidores
1. Correr la API (**`http://127.0.0.1:5000/api/v1/`**):
```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3
source .venv/bin/activate
pip install flask-cors
python3 run.py
```
2. Un servidor para el frontend (**`http://localhost:5500/base_files/login.html`**):
```bash
cd ~/holberton_projects/holbertonschool-hbnb/part4
python3 -m http.server 5500
```

---

## CORS — ¿Qué es y por qué lo necesitamos?
CORS (Cross-Origin Resource Sharing) es una política de seguridad de los navegadores.  
Cuando el frontend (`http://127.0.0.1:5500`) intenta hacer una petición a la API (`http://127.0.0.1:5000`), el navegador lo bloquea porque son orígenes distintos (puertos diferentes).

```
Frontend: http://127.0.0.1:5500  ←→  API: http://127.0.0.1:5000
                        ↑
              Bloqueado por CORS ❌
```
Para solucionarlo instalamos `flask-cors` y lo configuramos en `__init__.py`:

```bash
pip install flask-cors
```

Agregado en `requirements.txt`:
```
flask-cors
```

---

## Archivos modificados
| Archivo | Cambio | 
| :... | :... |
| `scripts.js` | Lógica de login completa |
| `login.html` | Agregado `div` para mensajes de error |
| `part3/app/__init__.py` | Agregado CORS |
| `part3/requirements.txt` | Agregado `flask-cors` |



### `part3/app/__init__.py`
```python
# Al inicio del archivo — en los imports:
from flask_cors import CORS

# Dentro de create_app(), después de crear la app:
CORS(app, resources={r"/api/*": {"origins": "*"}})
```
`resources={r"/api/*": {"origins": "*"}}`:
Permite peticiones desde cualquier origen (`*`) para todas las rutas que empiecen con `/api/`.

---

### `scripts.js`
```js
/* =============================================
   HBnB Part 4 — scripts.js
   Task 1: Login functionality
============================================= */

const API_URL = 'http://127.0.0.1:5000/api/v1';

/* ---- UTILITIES ---- */

/**
 * Store JWT token in a cookie
 */
function setCookie(name, value, days = 1) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

/**
 * Get a cookie value by name
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

/**
 * Check if user is authenticated (has token cookie)
 */
function isAuthenticated() {
    return getCookie('token') !== null;
}

/* ---- TASK 1: LOGIN ---- */

/**
 * Send login request to API
 */
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}

/* ---- EVENT LISTENERS ---- */

document.addEventListener('DOMContentLoaded', () => {

    /* --- Login Form --- */
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
                    // Store JWT token in cookie (expires in 1 day)
                    setCookie('token', data.access_token, 1);
                    // Redirect to main page
                    window.location.href = 'index.html';
                } else {
                    // Show error message
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
```
#### Estructura general del archivo
```
scripts.js
├── API_URL              → URL base de la API
├── setCookie()          → Guardar el token en el navegador
├── getCookie()          → Leer el token del navegador
├── isAuthenticated()    → Verificar si hay sesión activa
├── loginUser()          → Hacer la petición HTTP a la API
└── DOMContentLoaded     → Event listener principal del formulario
```

####   Constante de la API
```js
const API_URL = 'http://127.0.0.1:5000/api/v1';
```
Es una constante que guarda la dirección base de nuestra API Flask.
Se define una sola vez para no repetir la URL en cada función.
Cuando hagamos una petición al login, la URL completa queda:
```
http://127.0.0.1:5000/api/v1/auth/login
```

#### `setCookie()` — Guardar el token
```js
function setCookie(name, value, days = 1) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
}
```
Guarda un valor en una cookie del navegador.  
Sin esta función, el token se perdería al cambiar de página.
El token dura 1 día por defecto.  

```js
function setCookie(name, value, days = 1) {}
```
-   `name` — nombre de la cookie, en nuestro caso 'token'
-   `value` — el token JWT que devuelve la API
-   `days = 1` — parámetro con valor por defecto: si no se pasa, la cookie dura 1 día

```js
const expires = new Date();
```
-   Crea un objeto `Date` con la fecha y hora actuales.

```js
expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
```
-   Calcula la fecha de expiración sumando los días en milisegundos:
```
1 día = 24 horas × 60 minutos × 60 segundos × 1000 milisegundos
      = 86.400.000 milisegundos
```

```js
document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
```
-   Escribe la cookie en el navegador con 3 partes:
    +   `${name}=${value}` — el par clave/valor: `token=eyJhbGciOiJ...`
    +   `expires=...` — cuándo expira la cookie
    +   `path=/` — la cookie es accesible desde cualquier página de la app
    +   `SameSite=Lax`
        *   Es una mejora de seguridad, evita que la cookie se envíe en peticiones cross-site no deseadas.
        *   Como el cliente (puerto 5500) y la API (puerto 5000) son técnicamente "orígenes distintos", Chrome a veces se pone estricto. 
        *   Al poner Lax, le aseguras al navegador que la cookie es segura para ser usada en la navegación interna del proyecto.

---

####   `getCookie()` — Leer el token del navegador
```js
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}
```
Lee el valor de una cookie por su nombre.  
La usamos para recuperar el token JWT en cualquier página.  
`document.cookie` devuelve todas las cookies como un string separado por `;` — hay que dividirlo y buscar la que queremos.

```js
const cookies = document.cookie.split(';');
```
-   `document.cookie` devuelve todas las cookies como un string así:
    +   "token=eyJhbGci...; otracookie=valor; otra=valor2"
-   `.split(';')` lo convierte en un array:
    +   ["token=eyJhbGci...", " otracookie=valor", " otra=valor2"]

```js
for (let cookie of cookies) { ... }
```
-   Recorre cada cookie del array una por una.

```js
const [key, value] = cookie.trim().split('=');
```
-   `.trim()` — elimina espacios en blanco al inicio y final
-   `.split('=')` — divide por `=` en dos partes
-   `[key, value]` — desestructuración: guarda la primera parte en `key` y la segunda en `value`
-   Por ejemplo " token=eyJhbGci..." queda:
    +   key   = "token"
    +   value = "eyJhbGci..."

```js
if (key === name) return value;
```
-   Si el nombre de la cookie coincide con el que buscamos, devuelve su valor.

```js
return null;
```
-   Si no encuentra la cookie, devuelve `null`.

---

#### `isAuthenticated()` — Verificar si hay sesión activa
```js
function isAuthenticated() {
    return getCookie('token') !== null;
}
```
Verifica si el usuario está logueado.  
Devuelve `true` si existe la cookie `token`, `false` si no existe.  
Se usará en los próximos tasks para:
-   Mostrar/ocultar el botón de login en el header
-   Redirigir a login.html si el usuario no está autenticado
-   Mostrar el formulario de review solo a usuarios logueados
-   Cómo funciona:
```
getCookie('token') devuelve:
    → un string (el token)  →  !== null  →  true  ✅ autenticado
    → null                  →  === null  →  false ❌ no autenticado
```

---

#### `loginUser()` — Petición HTTP a la API
```js
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    return response;
}
```
Envía las credenciales del usuario a la API y devuelve la respuesta.  
Hace un `POST` a `/api/v1/auth/login` con el email y password en formato JSON.  

##### Línea por línea
```js
async function loginUser(email, password) {}
```
-   `async` significa que la función es asíncrona
    +   puede usar `await` para esperar respuestas sin bloquear el navegador.

```js
const response = await fetch(`${API_URL}/auth/login`, {}
```
-   `fetch()` es la **Fetch API** de JavaScript para hacer peticiones **HTTP**.  
-   `await` pausa la función hasta que la API responde.
-   La URL completa es: `http://127.0.0.1:5000/api/v1/auth/login`

```js
method: 'POST',
```
-   Define el método HTTP.  
-   Usamos `POST` porque estamos enviando datos (credenciales).

```js
headers: {'Content-Type': 'application/json'},
```
-   Le dice a la API que el **body** está en formato **`JSON`**.
-   Sin este header, **Flask** no puede leer los datos correctamente.

```js
body: JSON.stringify({ email, password })
```
-   Convierte el objeto JavaScript a un string **`JSON`** para enviarlo:
```js
{ email: "admin@hbnb.io", password: "admin1234" }
// se convierte en:
'{"email":"admin@hbnb.io","password":"admin1234"}'
```

```js
return response;
```
-   Devuelve la respuesta completa al que llamó la función.  
-   La respuesta incluye `response.ok` (true/false) y `response.json()` (el body).

---

#### Event listener del formulario
```js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();  // Evita que la página se recargue

            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorMsg = document.getElementById('login-error');

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token, 1);  // Guarda el token
                    window.location.href = 'index.html';        // Redirige
                } else {
                    errorMsg.textContent = 'Invalid email or password.';
                    errorMsg.classList.remove('d-none');         // Muestra el error
                }
            } catch (error) {
                errorMsg.textContent = 'Connection error. Make sure the API is running.';
                errorMsg.classList.remove('d-none');
            }
        });
    }
});
```
##### Línea por línea
```js
document.addEventListener('DOMContentLoaded', () => { ... })
```
-   Espera a que el HTML esté completamente cargado antes de ejecutar el código.  
-   Sin esto, `getElementById('login-form')` devolvería `null` porque el formulario aún no existe en el DOM.

```js
const loginForm = document.getElementById('login-form');
if (loginForm) { ... }
```
-   Busca el formulario por su `id`.  
-   El `if` verifica que existe — este mismo `scripts.js` se carga en todas las páginas, y no todas tienen `login-form`.

```js
loginForm.addEventListener('submit', async (event) => { ... })
```
-   Escucha el evento `submit`
    +   se activa cuando el usuario hace click en el botón **Login** o presiona **Enter**.

```js
event.preventDefault();
```
-   Evita el comportamiento por defecto del formulario HTML que sería recargar la página.  
-   Con esto manejamos el **submit** completamente con JavaScript.

```js
const email    = document.getElementById('email').value.trim();
const password = document.getElementById('password').value.trim();
```
-   Lee los valores del formulario.  
-   `.trim()` elimina espacios accidentales al inicio y final que el usuario pueda haber escrito.

```js
const errorMsg = document.getElementById('login-error');
```
-   Busca el `div` de error en el HTML.  
-   Se mostrará si el **login** falla.

```js
try { const response = await loginUser(email, password); }
```
-   `try/catch` captura errores como problemas de red.  
-   `await` espera la respuesta de la API antes de continuar.

```js
if (response.ok) { ... }
```
-   `response.ok` es true si el status HTTP es 200-299 (éxito).  
-   En nuestro caso, el login exitoso devuelve `200`.

```js
const data = await response.json();
```
-   Lee el body de la respuesta y lo convierte de **JSON** a **objeto JavaScript**:
```js
const data = await response.json();
```


```js
setCookie('token', data.access_token, 1);
```
-   Guarda el token **JWT** en una cookie que dura 1 día.

```js
window.location.href = 'index.html';
```
Redirige al usuario a la página principal.


```js
{ ... } else {
    if (errorMsg) {
        errorMsg.textContent = 'Invalid email or password. Please try again.';
        errorMsg.classList.remove('d-none'); 
    }
}
```
-   Si la API devuelve un error (401 — credenciales incorrectas):
    +   `.textContent`
        *    escribe el mensaje de error en el div
    +   `.classList.remove('d-none')`
        *   hace visible el div que estaba oculto con Bootstrap

```js
{ ... } catch (error) {
    if (errorMsg) {
        errorMsg.textContent = 'Connection error. Make sure the API is running.';
        errorMsg.classList.remove('d-none');
    }
}
```
-   Si hay un error de red (la API no está corriendo, timeout, etc.) muestra un mensaje diferente.

---

#### Flujo completo:
```
1. Usuario abre login.html
2. DOMContentLoaded → scripts.js busca #login-form
3. Usuario escribe email + password y hace click en Login
4. submit event → event.preventDefault()
5. fetch POST → http://127.0.0.1:5000/api/v1/auth/login
6. API responde:
   ✅ 200 OK  → setCookie('token', ...) → redirect index.html
   ❌ 401     → mostrar "Invalid email or password"
   ❌ Network → mostrar "Connection error"
```

---

### `login.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBnB - Login</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>

    <!-- Header -->
    <header class="hbnb-header">
        <div class="container d-flex justify-content-between align-items-center py-3">
            <img src="images/logo.png" alt="HBnB Logo" class="logo">
            <nav class="d-flex align-items-center gap-3">
                <a href="index.html" class="nav-link-custom">Home</a>
            </nav>
        </div>
    </header>

    <!-- Main -->
    <main class="container">
        <form id="login-form" class="review-card">
            <h2>Login</h2>
            <p class="text-muted mb-4">Welcome back! Please sign in to continue.</p>

            <!-- Error message -->
            <div id="login-error" class="alert alert-danger d-none"></div>

            <!-- Email -->
            <div class="mb-3">
                <label for="email" class="form-label fw-semibold">Email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    class="form-control"
                    placeholder="you@example.com"
                    required
                >
            </div>

            <!-- Password -->
            <div class="mb-4">
                <label for="password" class="form-label fw-semibold">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    class="form-control"
                    placeholder="Your password"
                    required
                >
            </div>

            <!-- Submit -->
            <div class="d-grid">
                <button type="submit" class="login-button btn-lg">Login</button>
            </div>
        </form>
    </main>

    <!-- Footer -->
    <footer class="hbnb-footer">
        <div class="container text-center py-3">
            <p class="mb-0">All rights reserved © 2026 HBnB</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="scripts.js"></script>
</body>
</html>
```
#### Cambios
Se agregó el div de error entre el título y el primer campo:
```html
<!-- Error message — oculto por defecto con d-none -->
<div id="login-error" class="alert alert-danger d-none"></div>
```

-   `d-none`
    +   es una clase de **Bootstrap** que aplica `display: none`.  
    +   Cuando el login falla, el script remueve esta clase con `classList.remove('d-none')` y el mensaje se hace visible.

---
---

# Task 2 — List of Places

1. **Verificar autenticación**
    Al cargar `index.html`, revisar si existe la cookie `token`.  
    Si existe, ocultar el botón **Login**. Si no existe, mostrarlo.
2. **Fetch de lugares**
    Hacer un `GET` a `/api/v1/places/` y mostrar los lugares dinámicamente en el HTML con JavaScript
    No hardcodeados como el **"Sample Place"** actual.
3. **Filtro por precio**
    Un dropdown con opciones **10, 50, 100, All** que filtra los lugares sin recargar la página.

## Objetivo
Mostrar la lista de lugares dinámicamente desde la API, implementar filtro por precio y controlar la visibilidad del botón Login según si el usuario está autenticado.

## Archivos modificados
| Archivo | Cambio |
|---|---|
| `index.html` | `id="login-link"` en el botón Login, opciones fijas en el dropdown, `#places-list` vacío |
| `scripts.js` | 4 funciones nuevas: `checkAuthentication`, `fetchPlaces`, `displayPlaces`, `filterPlaces` |

---

## Cambios en `index.html`
### 1. `id="login-link"` en el botón Login
```html
<a id="login-link" href="login.html" class="btn btn-login login-button">Login</a>
```
Agregamos el `id` para que JavaScript pueda encontrar este elemento y mostrarlo u ocultarlo según si hay token.

### 2. Opciones fijas en el dropdown
```html
<select id="price-filter">
    <option value="all">All</option>
    <option value="10">$10</option>
    <option value="50">$50</option>
    <option value="100">$100</option>
</select>
```
El enunciado pide exactamente estas opciones: 10, 50, 100, All.

### 3. `#places-list` vacío con clase `row`
```html
<section id="places-list" class="row">
</section>
```
Se eliminó el "Sample Place" hardcodeado — ahora los lugares se insertan dinámicamente con JavaScript.  
La clase `row` de Bootstrap organiza las cards en columnas.

---

## Funciones nuevas en `scripts.js`
### `checkAuthentication()`
```js
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    // Control login button visibility (index.html and place.html)
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }
    // place.html — show/hide add review form
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }
    // index.html — fetch all places
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }
    // place.html — fetch place details
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
    if (token && addReviewSection) {
        // Decode token payload to get current user ID
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentUserId = payload.sub;
        
        const alreadyReviewed = place.reviews && place.reviews.some(r => r.user_id === currentUserId);
        
        if (alreadyReviewed) {
            addReviewSection.style.display = 'none';
            }
    }
}
```

#### Línea por línea

```js
const token = getCookie('token');
```
Lee la cookie `token`.  
Si el usuario está logueado devuelve el **JWT**, si no devuelve `null`.

```js
const loginLink = document.getElementById('login-link');
```
Busca el botón **Login** en el HTML por su `id`.

```js
if (loginLink) { ... }
```
Verifica que el elemento existe — esta función solo corre en `index.html`.

```js
if (!token) {
    loginLink.style.display = 'block';
} else {
    loginLink.style.display = 'none';
}
```
- Sin token → muestra el botón Login (`display: block`)
- Con token → oculta el botón Login (`display: none`) porque ya está logueado

```js
fetchPlaces(token);
```
Llama a `fetchPlaces` pasando el token (puede ser `null` si no está logueado).  
`/api/v1/places/` es un endpoint público, funciona con o sin token.


```js
// Hide "Add a Review" button if user already reviewed this place
const token = getCookie('token');
const addReviewSection = document.getElementById('add-review');

if (token && addReviewSection) {
    // Decode token payload to get current user ID
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentUserId = payload.sub;

    const alreadyReviewed = place.reviews && place.reviews.some(r => r.user_id === currentUserId);

    if (alreadyReviewed) {
        addReviewSection.style.display = 'none';
    }
}
```

```javascript
const payload = JSON.parse(atob(token.split('.')[1]));
const currentUserId = payload.sub;
```
Decodifica el JWT sin librería — `split('.')[1]` toma el payload (parte del medio), `atob()` lo decodifica de base64, `JSON.parse()` lo convierte a objeto.  
`payload.sub` es el ID del usuario que guarda **Flask-JWT**.

```javascript
place.reviews.some(r => r.user_id === currentUserId)
```
`.some()` devuelve `true` si al menos una review tiene el mismo `user_id` que el usuario actual.


---

### `fetchPlaces(token)`

```js
async function fetchPlaces(token) {
    const headers = { 'Content-Type': 'application/json' };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

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
```

#### Línea por línea
```js
const headers = { 'Content-Type': 'application/json' };
```
Crea el objeto de headers base.  
`Content-Type: application/json` le dice a la API que esperamos JSON.

```js
if (token) {
    headers['Authorization'] = `Bearer ${token}`;
}
```
Si hay token, lo agrega al header de autorización.  
Formato requerido por **JWT**: `Bearer eyJhbGci...`

-   `Bearer`
    +   Bearer es el esquema de autenticación para JWT.  
    +   Cuando mandás una petición a un endpoint protegido, el servidor necesita saber que el token que enviás es un JWT y no otro tipo de credencial.  
    +   El formato es siempre:
        *   Authorization: Bearer eyJhbGci...
    +   Bearer literalmente significa "portador" en inglés — el que porta el token tiene acceso. 
    +   El servidor Flask lee este header, extrae el token después del espacio, lo verifica con la `SECRET_KEY` y si es válido permite el acceso.
    +   Sin Bearer la API no reconoce el token y devuelve 401.

```js
const response = await fetch(`${API_URL}/places/`, { headers });
```
Hace un GET a `http://127.0.0.1:5000/api/v1/places/` con los headers. `await` espera la respuesta.

```js
const places = await response.json();
```
Convierte el body de la respuesta de **JSON** a un **array JavaScript**:
```js
[
  { id: "abc123", title: "Cozy Apartment", price: 80, ... },
  { id: "def456", title: "Beach House", price: 150, ... }
]
```

```js
window.allPlaces = places;
```
Guarda los lugares en una variable global `window.allPlaces`.  
Esto permite que el filtro acceda a todos los lugares originales sin hacer otra petición a la API.

```js
displayPlaces(places);
```
Llama a la función que crea las **cards** en el HTML.

---

### `displayPlaces(places)`

```js
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p class="text-muted">No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('col-md-4');
        card.dataset.price = place.price;

        card.innerHTML = `
            <article class="place-card">
                <h2>${place.title}</h2>
                <p class="text-muted mb-1">Price per night: <strong>$${place.price}</strong></p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </article>
        `;
        placesList.appendChild(card);
    });
}
```

#### Línea por línea
```js
placesList.innerHTML = '';
```
Limpia el contenido anterior antes de insertar nuevos lugares.  
Importante para cuando el filtro vuelve a llamar esta función.

```js
if (places.length === 0) {
    placesList.innerHTML = '<p class="text-muted">No places found.</p>';
    return;
}
```
Si la API no devuelve lugares, muestra un mensaje en vez de una lista vacía.

```js
places.forEach(place => { ... })
```
Recorre cada lugar del array uno por uno.

```js
const card = document.createElement('div');
```
Crea un `<div>` nuevo en memoria — todavía no está en el HTML.

```js
card.classList.add('col-md-4');
```
Le agrega la clase Bootstrap `col-md-4` — en pantallas medianas ocupa 4 columnas de 12, mostrando 3 cards por fila.

```js
card.dataset.price = place.price;
```
Guarda el precio en el atributo `data-price` del elemento HTML:
```html
<div class="col-md-4" data-price="80">
```
El filtro lee este valor para decidir si mostrar u ocultar la card.
-   `dataset`
    +   dataset es una propiedad de los elementos HTML que permite guardar datos personalizados directamente en el elemento usando atributos `data-*`.
        *   card.dataset.price = place.price;
        *   // Genera en el HTML:
        *   // <div class="col-md-4" data-price="80">
    +   Es útil porque necesitamos que el filtro sepa el precio de cada card sin hacer otra petición a la API.  
    +   El precio viaja pegado al elemento HTML y `filterPlaces` lo lee así:
        *   const price = parseFloat(card.dataset.price);
    +   Podés guardar cualquier dato: `dataset.id`, `dataset.ciudad`, `dataset.rating`, etc.

```js
card.innerHTML = `
    <article class="place-card">
        <h2>${place.title}</h2>
        <p>Price per night: <strong>$${place.price}</strong></p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    </article>
`;
```
Inserta el HTML de la card usando template literals (backticks).  
`${place.title}`, `${place.price}` e `${place.id}` se reemplazan con los valores reales de cada lugar.

El link `place.html?id=${place.id}` pasa el ID del lugar como parámetro en la URL — el Task 3 lo usará para cargar los detalles del lugar correcto.

```js
placesList.appendChild(card);
```
Agrega la card al DOM — ahora sí se ve en el navegador.

---

### `filterPlaces(maxPrice)`

```js
function filterPlaces(maxPrice) {
    const cards = document.querySelectorAll('#places-list .col-md-4');
    const limit = maxPrice === 'all' ? Infinity : parseFloat(maxPrice);

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (price <= limit) ? 'block' : 'none';
    });
}
```

#### Línea por línea

---

1. Selección de las tarjetas
```js
const cards = document.querySelectorAll('#places-list .col-md-4');
```
Selecciona todos los divs con clase `col-md-4` dentro de `#places-list` — son todas las cards de lugares.

---

2. Definición del límite (El truco de `Infinity`)
```js
const limit = maxPrice === 'all' ? Infinity : parseFloat(maxPrice);
```
Operador terniario para comparar:
-   Si `maxPrice` es `'all'`: 
    +   El límite se establece como `Infinity` (un valor especial de JavaScript que es mayor que cualquier otro número). 
    +   Cualquier precio de casa será menor a infinito.
-   Si `maxPrice` es un número (ej. `'50'`): 
    +   Se convierte ese texto a un número real usando `parseFloat`.

---

3. El ciclo de comparación (forEach)
```js
cards.forEach(card => { ... });
```
El código empieza a revisar las tarjetas una por una.  
Por cada tarjeta (`card`), realiza las siguientes dos acciones:
-   A. Obtener el precio de la tarjeta
```js
const price = parseFloat(card.dataset.price);
```
+   Lee el precio del atributo `data-price` que guardamos en `displayPlaces`.  
+   `parseFloat` convierte el string `"80"` al número `80`.

-   B. Decidir si se muestra o se oculta
```js
card.style.display = (price <= limit) ? 'block' : 'none';
```
Usa otro operador ternario para modificar el CSS directamente:
+   **Condición**: 
    *   ¿Es el precio de esta casa menor o igual al límite seleccionado?
+   **Si es cierto (`?`)**: 
    *   Ponemos `display: 'block'` (la tarjeta se ve).
+   **Si es falso (`:`)**: 
    *   Ponemos `display: 'none'` (la tarjeta desaparece).

No se recarga la página — todo pasa en memoria en el navegador.

---

## Event listener del index
```js
const placesList = document.getElementById('places-list');
if (placesList) {
    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlaces(event.target.value);
        });
    }
}
```

```js
if (placesList) { ... }
```
Verifica que estamos en `index.html` — solo esta página tiene `#places-list`.

```js
checkAuthentication();
```
Al cargar la página verifica el **token**, muestra/oculta el **Login** y carga los lugares.

```js
priceFilter.addEventListener('change', (event) => {
    filterPlaces(event.target.value);
});
```
Cada vez que el usuario cambia el dropdown, llama a `filterPlaces` con el valor seleccionado (`"all"`, `"10"`, `"50"`, o `"100"`).


##   `placesList` en el event listener vs en `displayPlaces`
Son dos variables distintas que apuntan al mismo elemento del DOM, pero existen en contextos diferentes.
### En el event listener
```js
// En el event listener — solo para DETECTAR si estamos en index.html
const placesList = document.getElementById('places-list');
if (placesList) {
    checkAuthentication();  // si existe, arrancamos
}
```
Su único propósito es verificar que `#places-list` existe en la página.  
Si no existe, no ejecuta nada. Actúa como un guardia.

---

### En `displayPlaces`
```js
// En displayPlaces — para MANIPULAR el contenido
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';  // limpia
    // ... inserta cards
}
```
Aquí `placesList` se usa para escribir dentro del elemento — limpiar el contenido e insertar las cards.  
La razón por la que se busca dos veces con `getElementById` en vez de pasar la variable como parámetro es que `displayPlaces` es una función independiente que podría llamarse desde cualquier lado.  
Si dependiera de una variable externa sería más frágil.

---

## Flujo completo del Task 2
1. Usuario abre `index.html`
2. **DOMContentLoaded** → detecta `#places-list` → llama `checkAuthentication()`
3. `checkAuthentication()`:
   - Sin token → muestra botón **Login**
   - Con token  → oculta botón **Login**
   - En ambos casos → llama `fetchPlaces(token)`
4. `fetchPlaces()`:
   - `GET /api/v1/places/` con **Authorization header**
   - Guarda los lugares en `window.allPlaces`
   - Llama `displayPlaces(places)`
5. `displayPlaces()`:
   - Limpia `#places-list`
   - Crea una **card** por cada lugar con `data-price`
   - Appends al **DOM**
6. Usuario cambia el dropdown → `filterPlaces(maxPrice)`
   - Muestra/oculta **cards** según `data-price`


---
---

# Task 3 — Place Details
## ¿Qué pide el Task 3?

Cuatro cosas:

1. **Extraer el ID del lugar desde la URL** — cuando hacemos click en "View Details" en `index.html`, el link es `place.html?id=abc123`. Hay que leer ese `?id=abc123`.
2. **Verificar autenticación** — si hay token, mostrar el formulario de review. Si no hay token, ocultarlo.
3. **Fetch de detalles** — GET a `/api/v1/places/<id>` para obtener toda la info del lugar.
4. **Mostrar los detalles dinámicamente** — título, precio, descripción, amenities y reviews en el HTML.

---

## Archivos modificados

| Archivo | Cambio |
|---|---|
| `place.html` | `#place-details` y `#reviews` vacíos, se llenan dinámicamente |
| `scripts.js` | 3 funciones nuevas: `getPlaceIdFromURL`, `fetchPlaceDetails`, `displayPlaceDetails` + update de `checkAuthentication` |

---

## `place.html` actualizado

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBnB - Place</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="hbnb-header">
        <div class="container d-flex justify-content-between align-items-center py-3">
            <!-- logo -->
            <img src="images/logo.png" alt="HBnB Logo" class="logo">
            <!-- nav -->
            <nav class="d-flex align-items-center gap-3">
                <a href="index.html" class="nav-link-custom">Home</a>
                <!-- Task 3: id="login-link" to show/hide based on authentication -->
                <a id="login-link" href="login.html" class="btn btn-login login-button">Login</a>
            </nav>
        </div>
    </header>

    <!-- Main -->
    <main class="container my-4">

        <!-- Task 3: empty, filled dynamically by JavaScript -->
        <!-- Place info -->
        <section id="place-details" class="place-details mb-4">
            <div class="place-info"></div>
        </section>

        <!-- Task 3: empty, filled dynamically by JavaScript -->
        <!-- Reviews -->
        <section id="reviews" class="mb-4">
            <h3 class="mb-3">Reviews</h3>
        </section>
        <!-- Task 3: hidden by default, shown only if authenticated -->
         <!-- Add review -->
        <section id="add-review" class="add-review" style="display: none;">
            <h3>Add a Review</h3>
            <!-- Form -->
            <form id="review-form" class="form">
                <!-- Review text -->
                <div class="mb-3">
                    <label for="review-text" class="form-label fw-semibold">
                        Review:
                    </label>
                    <textarea id="review-text" name="review-text" class="form-control" rows="4" required></textarea>
                </div>
                <!-- Review rating -->
                <div class="mb-3">
                    <label for="review-rating" class="form-label fw-semibold">
                        Rating (1-5):
                    </label>
                    <input type="number" id="review-rating" name="review-rating" class="form-control" min="1" max="5" required>
                </div>
                <!-- Submit button -->
                <button type="submit" class="btn-primary-custom btn">
                    Submit Review
                </button>
            </form>
        </section>
    </main>

    <!-- Footer -->
    <footer class="hbnb-footer">
        <div class="container text-center py-3">
            <p class="mb-0">All rights reserved © 2026 HBnB</p>
        </div>
    </footer>
    <!-- script -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="scripts.js"></script>
</body>
</html>
```

### Cambios en `place.html`

- `id="login-link"` en el botón Login — igual que en `index.html`
- `#place-details` y `#reviews` vacíos — se llenan con JavaScript
- `#add-review` tiene `style="display: none;"` por defecto — solo se muestra si hay token
- Formulario mejorado con campo de rating (1-5)

---

## `scripts.js` — Funciones nuevas del Task 3

### `getPlaceIdFromURL()`

```javascript
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}
```

#### Línea por línea

```javascript
const params = new URLSearchParams(window.location.search);
```
**Recordatorio**: Cuando hacemos click en "View Details" en `index.html`, el link es `place.html?id=abc123`. Hay que leer ese `?id=abc123`.  

`window.location.search` devuelve la parte de la URL después del `?`:
```
URL completa:  place.html?id=abc123
.search devuelve:  "?id=abc123"
```
`URLSearchParams` convierte ese string en un objeto fácil de consultar.

```javascript
return params.get('id');
```
Lee el valor del parámetro `id`. Con la URL `place.html?id=abc123` devuelve `"abc123"`.
Si no existe el parámetro devuelve `null`.

---

### `fetchPlaceDetails(token, placeId)`

```javascript
async function fetchPlaceDetails(token, placeId) {
    const headers = { 'Content-Type': 'application/json' };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

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
```

#### Línea por línea

```javascript
const headers = { 'Content-Type': 'application/json' };
if (token) {
    headers['Authorization'] = `Bearer ${token}`;
}
```
Igual que en `fetchPlaces` — agrega el token al header si existe.

```javascript
const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
```
GET a `http://127.0.0.1:5000/api/v1/places/abc123` — la URL incluye el ID del lugar extraído de la URL.

```javascript
const place = await response.json();
displayPlaceDetails(place);
```
Convierte la respuesta a objeto JavaScript y lo pasa a `displayPlaceDetails`.

---

### `displayPlaceDetails(place)`

```javascript
function displayPlaceDetails(place) {
    const placeInfo = document.querySelector('#place-details .place-info');
    const reviewsSection = document.getElementById('reviews');

    if (!placeInfo) return;

    // Render place info
    placeInfo.innerHTML = `
        <h1>${place.title}</h1>
        <p class="price-badge">$${place.price} / night</p>
        <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
        <div class="mt-3">
            <strong>Amenities:</strong>
            <div class="mt-2">
                ${place.amenities && place.amenities.length > 0
                    ? place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
                    : '<span class="text-muted">No amenities listed.</span>'
                }
            </div>
        </div>
    `;

    // Render reviews
    if (reviewsSection) {
        const existingCards = reviewsSection.querySelectorAll('.review-card');
        existingCards.forEach(card => card.remove());

        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const card = document.createElement('div');
                card.classList.add('review-card');
                card.innerHTML = `
                    <p class="reviewer-name">${review.user_id}</p>
                    <p class="stars">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                    <p>${review.text}</p>
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
}
```

#### Sección por sección

```javascript
const placeInfo = document.querySelector('#place-details .place-info');
```
Selecciona el `div.place-info` dentro de `#place-details` — donde va la info del lugar.

##### Render place info
```javascript
placeInfo.innerHTML = `
    <h1>${place.title}</h1>
    <p class="price-badge">$${place.price} / night</p>
    <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
    ...
`;
```

Inserta el HTML del lugar con template literals.  
-   `${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}`
    +   El operador ternario `place.owner ? ... : 'N/A'` evita errores si `owner` es null.
    + Operador terniario:
        *   condición ? valor_si_es_verdadero : valor_si_es_falso

```javascript
place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
```

-   `${place.amenities && place.amenities.length > 0
                    ? place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
                    : '<span class="text-muted">No amenities listed.</span>'
    }`
1.  **Condicion**: `${place.amenities && place.amenities.length > 0 ... }`
    +   `place.amenities`: 
        *   Primero verifica que el objeto exista (que no sea null).
    +   `&&`: 
        *   Es un "y" lógico. Ambas partes deben ser ciertas.
    +   `place.amenities.length > 0`: 
        *   Verifica que la lista no esté vacía.
    + Si el lugar tiene al menos una comodidad (WiFi, TV, etc.), la condición es verdadera.
2.  **Caso Verdadero: Crear las etiquetas**: `? place.amenities.map(a => <span class="amenity-badge">${a.name}</span>).join('')`
    +   `.map()`: 
        *   Recorre la lista de comodidades una por una. 
        *   Por cada comodidad (`a`), crea un string de HTML con su nombre.
        *   Convierte cada amenity en un `<span>` con su nombre.
    +   `.join('')`: 
        *   El `.map()` devuelve un array (una lista) de strings. 
        *   El `.join('')` los pega todos en un solo texto gigante para que el navegador pueda renderizarlo sin comas entre medio.
        *   Une todos los spans en un solo string sin separadores.

3.   **Caso Falso: El mensaje de reserva**: `: '<span class="text-muted">No amenities listed.</span>'`
    +   Si la lista no existe o está vacía, simplemente muestra este mensaje grisáceo (No amenities listed.) para que el usuario no vea un espacio en blanco.

---

##### Render reviews

---

1. Limpieza del área (El "Reset")
```javascript
const existingCards = reviewsSection.querySelectorAll('.review-card');
existingCards.forEach(card => card.remove());
```
Elimina las review cards existentes antes de insertar las nuevas — evita duplicados si la función se llama dos veces.

---

2. Validación de datos
```js
if (place.reviews && place.reviews.length > 0)
```
-   Al igual que con las amenities, primero preguntamos: **"¿Existen las reseñas y la lista tiene al menos un elemento?"**.
    +   Si es `true`, empezamos a crear las tarjetas.
    +   Si es `false`, saltamos al `else` para mostrar el mensaje de "No reviews yet".

---

3. Creación dinámica de la Tarjeta
```js
const card = document.createElement('div');
card.classList.add('review-card');
```
-   Por cada reseña en la lista, JavaScript crea un nuevo elemento <div> en la memoria del navegador y le asigna la clase CSS `.review-card` que definiste en tu `styles.css`.

---

4. La lógica de las Estrellas (El toque Pro)

```javascript
'★'.repeat(review.rating) + '☆'.repeat(5 - review.rating)
```
-   Usa el método `.repeat()` para dibujar la puntuación visualmente:
    +   `'★'.repeat(review.rating)`: 
        *   Si la calificación es 4, dibuja 4 estrellas rellenas: ★★★★.
    +   `'☆'.repeat(5 - review.rating)`: 
        *   Calcula cuántas faltan para llegar a 5 (5 - 4 = 1) y dibuja estrellas vacías: ☆.
    +   Resultado: 
        *   `★★★★☆`
```
'★'.repeat(3) → '★★★'
'☆'.repeat(2) → '☆☆'
resultado: '★★★☆☆'
```

---

5. Inserción en el DOM
```js
reviewsSection.appendChild(card);
```
-   Una vez que la tarjeta tiene todo su contenido (nombre del usuario, estrellas y texto), se "pega" dentro de la sección de reseñas en tu HTML.

---

6.  **Notas**
-   `<p class="reviewer-name">${review.user_id}</p>`
    +   Actualmente estás mostrando el **UUID** (el ID largo de la base de datos) del usuario. 
    +   En una aplicación real, lo ideal sería que la **API** hiciera un `Join` para enviarte el `first_name` del usuario.
-   Tip de Julián para los C27: 
    +  "Actualmente muestro el ID del usuario, pero en una fase futura planeo optimizar el **endpoint** para obtener el nombre real mediante una relación en el **Facade**"

---

### Update de `checkAuthentication()` para `place.html`

La función ya existe en `scripts.js` para `index.html`. Hay que actualizarla para que también maneje `place.html`:

```javascript
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    // Control login button visibility (index.html and place.html)
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    // place.html — show/hide add review form
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    // index.html — fetch all places
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }

    // place.html — fetch place details
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
}
```

#### Cambios respecto a la versión anterior

```javascript
const addReviewSection = document.getElementById('add-review');
if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
}
```
Muestra u oculta el formulario de review según si hay token. Usa el operador ternario: `token ? 'block' : 'none'` — si hay token muestra, si no oculta.

```javascript
if (document.getElementById('places-list')) {
    fetchPlaces(token);
}
```
Solo llama a `fetchPlaces` si estamos en `index.html` (tiene `#places-list`).

```javascript
const placeId = getPlaceIdFromURL();
if (placeId) {
    fetchPlaceDetails(token, placeId);
}
```
Solo llama a `fetchPlaceDetails` si hay un `?id=` en la URL — es decir, si estamos en `place.html`.

---

### Event listener — agregar `place.html` al DOMContentLoaded

```javascript
/* --- Place Details Page (Task 3) --- */
const placeDetails = document.getElementById('place-details');
if (placeDetails) {
    checkAuthentication();
}
```
Detecta si estamos en `place.html` buscando `#place-details`. Si existe, llama a `checkAuthentication()` que internamente llama a `fetchPlaceDetails`.

---

## `scripts.js` completo con Tasks 1, 2 y 3

```javascript
const API_URL = 'http://127.0.0.1:5000/api/v1';

/* ---- UTILITIES ---- */

function setCookie(name, value, days = 1) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
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

/* ---- TASK 1: LOGIN ---- */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    return response;
}

/* ---- TASK 2 & 3: CHECK AUTHENTICATION ---- */

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }

    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
}

/* ---- TASK 2: LIST OF PLACES ---- */

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

    if (places.length === 0) {
        placesList.innerHTML = '<p class="text-muted">No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('col-md-4');
        card.dataset.price = place.price;
        card.innerHTML = `
            <article class="place-card">
                <h2>${place.title}</h2>
                <p>Price per night: <strong>$${place.price}</strong></p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </article>
        `;
        placesList.appendChild(card);
    });
}

function filterPlaces(maxPrice) {
    const cards = document.querySelectorAll('#places-list .col-md-4');
    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (maxPrice === 'all' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
    });
}

/* ---- TASK 3: PLACE DETAILS ---- */

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

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

    if (!placeInfo) return;

    placeInfo.innerHTML = `
        <h1>${place.title}</h1>
        <p class="price-badge">$${place.price} / night</p>
        <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
        <div class="mt-3">
            <strong>Amenities:</strong>
            <div class="mt-2">
                ${place.amenities && place.amenities.length > 0
                    ? place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
                    : '<span class="text-muted">No amenities listed.</span>'
                }
            </div>
        </div>
    `;

    if (reviewsSection) {
        reviewsSection.querySelectorAll('.review-card').forEach(card => card.remove());

        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const card = document.createElement('div');
                card.classList.add('review-card');
                card.innerHTML = `
                    <p class="reviewer-name">${review.user_id}</p>
                    <p class="stars">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                    <p>${review.text}</p>
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
}

/* ---- EVENT LISTENERS ---- */

document.addEventListener('DOMContentLoaded', () => {

    /* --- Login Form (Task 1) --- */
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

    /* --- Index Page (Task 2) --- */
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlaces(event.target.value);
            });
        }
    }

    /* --- Place Details Page (Task 3) --- */
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        checkAuthentication();
    }

});
```

---

## Flujo completo del Task 3

```
1. Usuario hace click en "View Details" en index.html
2. Navega a place.html?id=abc123
3. DOMContentLoaded → detecta #place-details → llama checkAuthentication()
4. checkAuthentication():
   - Muestra/oculta botón Login
   - Muestra/oculta #add-review según token
   - getPlaceIdFromURL() extrae "abc123" de la URL
   - fetchPlaceDetails(token, "abc123")
5. fetchPlaceDetails():
   - GET /api/v1/places/abc123
   - Llama displayPlaceDetails(place)
6. displayPlaceDetails():
   - Renderiza título, precio, host, descripción, amenities
   - Renderiza cards de reviews con estrellas
```

---
---

# Task 4 — Add Review
---

## ¿Qué pide el Task 4?

Cuatro cosas:

1. **Verificar autenticación** — si no hay token, redirigir a `index.html` inmediatamente.
2. **Extraer el ID del lugar desde la URL** — igual que en Task 3, `?id=abc123`.
3. **Enviar la review a la API** — POST a `/api/v1/reviews/` con el texto y rating.
4. **Manejar la respuesta** — mostrar mensaje de éxito o error sin recargar la página.

---

## Archivos modificados

| Archivo | Cambio |
|---|---|
| `add_review.html` | Agregar `?id=` al link "Back to Place" dinámicamente |
| `scripts.js` | 2 funciones nuevas: `submitReview`, `handleReviewResponse` + event listener para `add_review.html` |

---

## Cambios en `add_review.html`

Ajustar el link "← Back to Place", el cual debería incluir el ID del lugar para volver al lugar correcto.  
Eso lo maneja JavaScript en el event listener.

---

## Funciones nuevas en `scripts.js`

### `submitReview(token, placeId, reviewText, rating)`

```javascript
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
```

#### Línea por línea

```javascript
async function submitReview(token, placeId, reviewText, rating) {
```
Recibe 4 parámetros: el token JWT, el ID del lugar, el texto de la review y el rating (1-5).

```javascript
const response = await fetch(`${API_URL}/reviews/`, {
    method: 'POST',
});
```
POST a `http://127.0.0.1:5000/api/v1/reviews/` — crea una nueva review.

```javascript
headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
},
```
Dos headers obligatorios:
- `Content-Type` — le dice a la API que el body es JSON
- `Authorization` — el token JWT para identificar al usuario

```javascript
body: JSON.stringify({
    text: reviewText,
    rating: parseInt(rating),
    place_id: placeId
})
```
El body con los 3 campos que espera la API. 
-   `parseInt(rating)` convierte el string del radio button al número entero que espera el campo `rating` de la API.

---

### `handleReviewResponse(response, form)`

```javascript
function handleReviewResponse(response, form) {
    const successMsg = document.getElementById('success-msg');
    const errorMsg   = document.getElementById('error-msg');

    if (response.ok) {
        // Show success message
        successMsg.classList.remove('d-none');
        errorMsg.classList.add('d-none');
        // Clear the form
        form.reset();
        // Redirect to place page after 2 seconds
        const placeId = getPlaceIdFromURL();
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 2000);
    } else {
        // Show error message
        errorMsg.classList.remove('d-none');
        successMsg.classList.add('d-none');
    }
}
```

#### Línea por línea

```javascript
const successMsg = document.getElementById('success-msg');
const errorMsg   = document.getElementById('error-msg');
```
Busca los dos divs de mensajes que ya existen en `add_review.html` — ocultos por defecto con `d-none`.

```javascript
if (response.ok) {
    successMsg.classList.remove('d-none');
    errorMsg.classList.add('d-none');
```
Si la API devuelve 200-201: muestra el mensaje verde de éxito y oculta el rojo.

```javascript
form.reset();
```
Limpia todos los campos del formulario — radio buttons, textarea vuelven a su estado inicial.

```javascript
const placeId = getPlaceIdFromURL();
setTimeout(() => {
    window.location.href = `place.html?id=${placeId}`;
}, 2000);
```
`setTimeout` espera 2000 milisegundos (2 segundos) para que el usuario pueda leer el mensaje de éxito, luego redirige al lugar donde se dejó la review.

```javascript
} else {
    errorMsg.classList.remove('d-none');
    successMsg.classList.add('d-none');
}
```
Si la API devuelve error: muestra el mensaje rojo y oculta el verde.

---

### Event listener para `add_review.html`

```javascript
/* --- Add Review Page (Task 4) --- */
const reviewForm = document.getElementById('review-form');
const addReviewCard = document.querySelector('.add-review');

if (reviewForm && addReviewCard) {
    // Redirect to index if not authenticated
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }

    // Update "Back to Place" link with place ID
    const placeId = getPlaceIdFromURL();
    const backLink = document.querySelector('a[href="place.html"]');
    if (backLink && placeId) {
        backLink.href = `place.html?id=${placeId}`;
    }

    // Handle form submission
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value.trim();
        const ratingInput = document.querySelector('input[name="rating"]:checked');

        // Validate rating selection
        const ratingError = document.getElementById('rating-error');
        if (!ratingInput) {
            ratingError.classList.remove('d-none');
            return;
        }
        ratingError.classList.add('d-none');

        const rating = ratingInput.value;
        const response = await submitReview(token, placeId, reviewText, rating);
        handleReviewResponse(response, reviewForm);
    });
}
```

#### Sección por sección

```javascript
const reviewForm = document.getElementById('review-form');
const addReviewCard = document.querySelector('.add-review');
if (reviewForm && addReviewCard) {
```
Detecta que estamos en `add_review.html` buscando `#review-form` y `.add-review`. Si ambos existen, ejecuta el código del Task 4.

```javascript
const token = getCookie('token');
if (!token) {
    window.location.href = 'index.html';
}
```
Verifica autenticación inmediatamente. Si no hay token, redirige a `index.html` antes de que el usuario vea el formulario.

```javascript
const backLink = document.querySelector('a[href="place.html"]');
if (backLink && placeId) {
    backLink.href = `place.html?id=${placeId}`;
}
```
Actualiza el link "← Back to Place" para que incluya el ID del lugar. Sin esto, el botón llevaría a `place.html` sin ID y no cargaría ningún lugar.

```javascript
const ratingInput = document.querySelector('input[name="rating"]:checked');
if (!ratingInput) {
    ratingError.classList.remove('d-none');
    return;
}
```
`input[name="rating"]:checked` busca el radio button seleccionado. Si ninguno está seleccionado, muestra el mensaje de error de rating y detiene el submit con `return`.

```javascript
const response = await submitReview(token, placeId, reviewText, rating);
handleReviewResponse(response, reviewForm);
```
Envía la review y maneja la respuesta.

---

## `scripts.js` completo — Tasks 1, 2, 3 y 4

```javascript
const API_URL = 'http://127.0.0.1:5000/api/v1';

/* ---- UTILITIES ---- */

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

/* ---- TASK 1: LOGIN ---- */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    return response;
}

/* ---- TASK 2 & 3: CHECK AUTHENTICATION ---- */

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }
    const placeId = getPlaceIdFromURL();
    if (placeId && document.getElementById('place-details')) {
        fetchPlaceDetails(token, placeId);
    }
}

/* ---- TASK 2: LIST OF PLACES ---- */

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

    if (places.length === 0) {
        placesList.innerHTML = '<p class="text-muted">No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('col-md-4');
        card.dataset.price = place.price;
        card.innerHTML = `
            <article class="place-card">
                <h2>${place.title}</h2>
                <p>Price per night: <strong>$${place.price}</strong></p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </article>
        `;
        placesList.appendChild(card);
    });
}

function filterPlaces(maxPrice) {
    const cards = document.querySelectorAll('#places-list .col-md-4');
    const limit = maxPrice === 'all' ? Infinity : parseFloat(maxPrice);
    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (price <= limit) ? 'block' : 'none';
    });
}

/* ---- TASK 3: PLACE DETAILS ---- */

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

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

    if (!placeInfo) return;

    placeInfo.innerHTML = `
        <h1>${place.title}</h1>
        <p class="price-badge">$${place.price} / night</p>
        <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
        <div class="mt-3">
            <strong>Amenities:</strong>
            <div class="mt-2">
                ${place.amenities && place.amenities.length > 0
                    ? place.amenities.map(a => `<span class="amenity-badge">${a.name}</span>`).join('')
                    : '<span class="text-muted">No amenities listed.</span>'
                }
            </div>
        </div>
    `;

    if (reviewsSection) {
        reviewsSection.querySelectorAll('.review-card').forEach(card => card.remove());

        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const card = document.createElement('div');
                card.classList.add('review-card');
                card.innerHTML = `
                    <p class="reviewer-name">${review.user_id}</p>
                    <p class="stars">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                    <p>${review.text}</p>
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
}

/* ---- TASK 4: ADD REVIEW ---- */

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
        successMsg.classList.remove('d-none');
        errorMsg.classList.add('d-none');
        form.reset();
        const placeId = getPlaceIdFromURL();
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 2000);
    } else {
        errorMsg.classList.remove('d-none');
        successMsg.classList.add('d-none');
    }
}

/* ---- EVENT LISTENERS ---- */

document.addEventListener('DOMContentLoaded', () => {

    /* --- Login Form (Task 1) --- */
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

    /* --- Index Page (Task 2) --- */
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlaces(event.target.value);
            });
        }
    }

    /* --- Place Details Page (Task 3) --- */
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        checkAuthentication();
    }

    /* --- Add Review Page (Task 4) --- */
    const reviewForm = document.getElementById('review-form');
    const addReviewCard = document.querySelector('.add-review');

    if (reviewForm && addReviewCard) {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
        }

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
```

---

## Flujo completo del Task 4

```
1. Usuario hace click en "Add a Review" desde place.html
2. Navega a add_review.html?id=abc123
3. DOMContentLoaded → detecta #review-form y .add-review
4. getCookie('token'):
   - Sin token → redirect index.html ❌
   - Con token → continúa ✅
5. Actualiza "← Back to Place" con el ID correcto
6. Usuario selecciona rating y escribe review → Submit
7. event.preventDefault()
8. Valida que hay rating seleccionado
9. submitReview(token, placeId, reviewText, rating)
   → POST /api/v1/reviews/
10. handleReviewResponse():
    ✅ 201 → mensaje verde → form.reset() → redirect place.html?id=... (2s)
    ❌ error → mensaje rojo
```




---
---

# Run the app
## Iniciar env
```bash
source .venv/bin/activate
```

```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3
source .venv/bin/activate
python3 run.py
```

```bash
cd ~/holberton_projects/holbertonschool-hbnb/part4
python3 -m http.server 5500
```

# Crear admin
```bash
python3 -c "
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(first_name='Admin', last_name='User', email='admin@hbnb.io', is_admin=True)
    admin.hash_password('admin1234')
    db.session.add(admin)
    db.session.commit()
    print('Admin creado:', admin.id)
"

```

# Login
## Admin
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo $TOKEN
```

first_name: Admin
last_name: User
Email: admin@hbnb.io
Password: admin1234


---

## Test User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"password123"}'

```

first_name: Test
last_name: User
email: test@example.com
password: password123




## Julian
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name":"Julian","last_name":"Gonzalez","email":"julian@example.com","password":"password456"}'

```
first_name: Julian
last_name: Gonzalez
email: julian@example.com
Password: password456


# Places
## Paris
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JULIAN_TOKEN" \
  -d '{"title":"Apartment in Paris","description":"Charming apartment in the heart of Paris, steps from the Eiffel Tower.","price":10,"latitude":48.8566,"longitude":2.3522,"amenities":[],"image_url":"images/paris.jpg"}'

```

```bash

```

```bash

```

## Verificar
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json"
```

# IMG
```bash
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3/instance/development.db "
UPDATE places SET image_url='images/paris.jpg' WHERE id='4d40d16c-a072-4df9-86c6-aaf055a98707';
UPDATE places SET image_url='images/buenos_aires.jpg' WHERE id='35b6a8ee-eb8b-4432-86c4-d7f2d7874cc1';
UPDATE places SET image_url='images/rennes.jpg' WHERE id='1a2e2494-296f-42f5-bd19-fe7697f0c5f9';
"

```



# Amenity

## 1. Pool

```Bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name":"Pool"}'
```

## 2. Kitchen

```Bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name":"Kitchen"}'
```

## 3. WiFi

```Bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name":"WiFi"}'
```

## 4. Gym

```Bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name":"Gym"}'
```

### PUT
```
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/f05b2434-bf79-45b6-a3c9-6a75179125ea \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name": "Heating"}'
```

## 5. Pet Friendly

```Bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY" \
  -d '{"name":"Pet Friendly"}'
```

## Verificacion
```bash
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3/instance/development.db "SELECT id, name FROM amenities;"
```

## Add the amenity
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/35b6a8ee-eb8b-4432-86c4-d7f2d7874cc1/amenities/d3717728-0c6f-48e4-8a11-c5e5e654b637 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE0NDE1MywianRpIjoiODMwYmI2NDktNGFjOS00NDExLWI0YmQtOGY1NWE4NGY5MDFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImVjZDkxYzVkLWU4YzctNDE0Yi1hOTI4LTQ2ZjIzOWMyZDI0YiIsIm5iZiI6MTc3NTE0NDE1MywiY3NyZiI6IjcyZWM2M2MyLWUxNTUtNDI4MC05NjZlLTJiZGE1MWRlMTE3NSIsImV4cCI6MTc3NTIzMDU1MywiaXNfYWRtaW4iOnRydWV9.s3KNQIv1_UUwfOuk-P4f0ztlz0GjDnSV2ZYit7mL9tY"
```

