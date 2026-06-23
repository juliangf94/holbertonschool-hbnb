# HBnB Part 3 — Documentación paso a paso

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| **Flask** | Framework web para la API |
| **Flask-RESTX** | Extensión para crear APIs REST con documentación Swagger automática |
| **Flask-JWT-Extended** | Autenticación con tokens JWT |
| **Flask-Bcrypt** | Hasheo de contraseñas |
| **Flask-SQLAlchemy** | ORM para conectar Python con la base de datos |
| **SQLite** | Base de datos en desarrollo |
| **Flask-CORS** | Permite peticiones desde el frontend (otro origen) |
| **pytest** | Framework de testing |

---

## Estructura del proyecto

```
part3-backend/
├── run.py                      # Punto de entrada — inicia el servidor
├── config.py                   # Configuraciones (dev, test, prod)
├── app/
│   ├── __init__.py             # Application Factory — crea la app Flask
│   ├── extensions.py           # Instancias de db, bcrypt, jwt
│   ├── services/
│   │   ├── __init__.py         # Instancia única de la Facade
│   │   └── facade.py           # Capa de lógica de negocio
│   ├── models/
│   │   ├── base_model.py       # Modelo base con id, created_at, updated_at
│   │   ├── user.py             # Modelo User
│   │   ├── place.py            # Modelo Place + tabla place_amenity
│   │   ├── review.py           # Modelo Review
│   │   ├── amenity.py          # Modelo Amenity
│   │   └── place_image.py      # Modelo PlaceImage (galería)
│   ├── api/v1/
│   │   ├── auth.py             # Endpoint de login
│   │   ├── users.py            # CRUD de usuarios
│   │   ├── places.py           # CRUD de lugares + imágenes + amenities
│   │   ├── reviews.py          # CRUD de reviews
│   │   └── amenities.py        # CRUD de amenities
│   ├── persistence/
│   │   ├── repository.py       # Repository pattern (InMemory + SQLAlchemy)
│   │   └── user_repository.py  # Repositorio específico de User
│   └── tests/
│       ├── test_models.py      # Tests de modelos
│       └── test_part3.py       # Tests de integración con pytest
└── scripts/
    ├── create_tables.sql       # SQL para crear tablas manualmente
    └── initial_data.sql        # SQL con datos iniciales
```

---

## Cómo iniciar la app

```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3-backend
source .venv/bin/activate
python3 run.py
```

La API corre en `http://127.0.0.1:5000/api/v1/`  
La documentación Swagger está en `http://127.0.0.1:5000/api/v1/`

---
---

# config.py — Configuración de la app

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev_secret_key_not_for_production')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/development.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
```

## ¿Por qué hay 3 configuraciones?

| Config | Cuándo se usa | Base de datos |
|---|---|---|
| `DevelopmentConfig` | Trabajar localmente | `development.db` — archivo en disco |
| `TestingConfig` | Correr pytest | `sqlite:///:memory:` — RAM, se borra sola |
| `ProductionConfig` | Servidor real | MySQL, claves desde variables de entorno |

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```
`sqlite:///:memory:` crea la base de datos **en la memoria RAM** del servidor. Es perfecta para tests porque:
- Se crea instantáneamente
- Se borra sola cuando el test termina
- No "ensucia" el `development.db` real

```python
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
```
`os.getenv()` lee una variable de entorno del sistema. Si no existe, usa el valor por defecto. En producción la clave real se guarda en el servidor, nunca en el código.

---
---

# extensions.py — Instancias compartidas

```python
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
```

## ¿Por qué existe este archivo?

Sin `extensions.py` tendríamos un **circular import**:
```
__init__.py importa → models/user.py
models/user.py importa → from app import bcrypt
from app importa → __init__.py   ← LOOP INFINITO ❌
```

Con `extensions.py`:
```
__init__.py importa → extensions.py → bcrypt ✅
models/user.py importa → extensions.py → bcrypt ✅
```

Las instancias se crean **sin app** — están "vacías". Luego en `__init__.py` se conectan a la app con `.init_app(app)`.

---
---

# `__init__.py` — Application Factory

```python
def create_app(config_class=app_config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, 'development.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', ...)

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    with app.app_context():
        db.create_all()

    return app
```

## ¿Qué es el Application Factory Pattern?

En vez de crear la app Flask directamente al inicio del archivo:
```python
# ❌ Sin factory — no se pueden crear múltiples instancias
app = Flask(__name__)
```

Se crea dentro de una función:
```python
# ✅ Con factory — se puede llamar con distintas configuraciones
def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    ...
    return app
```

Esto permite en los tests hacer:
```python
app = create_app(TestingConfig)  # app de testing con SQLite en RAM
```

## Línea por línea

```python
app.config.from_object(config_class)
```
Carga todas las variables en MAYÚSCULAS de la clase de configuración en `app.config`. Después de esto podés acceder a `app.config['DEBUG']`, `app.config['SQLALCHEMY_DATABASE_URI']`, etc.

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```
Sin CORS, el navegador bloquea las peticiones del frontend (puerto 5500) a la API (puerto 5000) porque son "orígenes distintos". `origins: "*"` permite peticiones desde cualquier origen.

```python
bcrypt.init_app(app)
jwt.init_app(app)
db.init_app(app)
```
Conecta las extensiones "vacías" de `extensions.py` a la app Flask. Después de esto tienen acceso a `app.config`.

```python
api.add_namespace(auth_ns, path='/api/v1/auth')
```
Registra cada namespace (grupo de endpoints) en la API con su prefijo de URL.

```python
with app.app_context():
    db.create_all()
```
`app_context()` activa el contexto de la app — SQLAlchemy necesita saber a qué app pertenece.  
`db.create_all()` lee todos los modelos registrados y crea las tablas que no existen en la base de datos. No borra las que ya existen.

---
---

# BaseModel — Modelo base

```python
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
```

## Línea por línea

```python
class BaseModel(db.Model):
```
Hereda de `db.Model` — le dice a SQLAlchemy que esta clase representa una tabla en la base de datos.

```python
__abstract__ = True
```
Le dice a SQLAlchemy que **no cree una tabla** para `BaseModel`. Solo las clases hijas (`User`, `Place`, etc.) tendrán tablas propias. `BaseModel` existe solo para compartir columnas y métodos.

```python
id = db.Column(
    db.String(36),
    primary_key=True,
    default=lambda: str(uuid.uuid4())
)
```
- `db.String(36)` — texto de hasta 36 caracteres (largo de un UUID: `"550e8400-e29b-41d4-a716-446655440000"`)
- `primary_key=True` — identifica unívocamente cada fila de la tabla
- `default=lambda: str(uuid.uuid4())` — genera un UUID automáticamente al crear cada objeto

```python
onupdate=lambda: datetime.now(timezone.utc)
```
SQLAlchemy actualiza `updated_at` automáticamente cada vez que se modifica el registro.

## Métodos

```python
def update(self, data):
    PROTECTED = {"id", "created_at"}
    for key, value in data.items():
        if hasattr(self, key) and key not in PROTECTED:
            setattr(self, key, value)
    self.updated_at = datetime.now(timezone.utc)
    db.session.commit()
```
- `PROTECTED` — evita que alguien cambie el `id` o `created_at`
- `hasattr(self, key)` — verifica que el atributo existe en el modelo antes de asignarlo
- `setattr(self, key, value)` — equivale a `self.key = value` pero usando el nombre como string

---
---

# Modelos — User, Place, Review, Amenity

## User

```python
class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False)

    places  = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
```

### ¿Qué es `db.relationship`?

```python
places = db.relationship('Place', backref='owner', lazy=True)
```
Le dice a SQLAlchemy que un `User` tiene muchos `Place`.
- `backref='owner'` — crea automáticamente `place.owner` para acceder al dueño desde el lugar
- `lazy=True` — no carga los lugares hasta que se acceda a `user.places` (optimización)

```python
def hash_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(self, password):
    return bcrypt.check_password_hash(self.password, password)
```
- `generate_password_hash()` — convierte `"admin1234"` en `"$2b$12$..."` (hash irreversible)
- `.decode('utf-8')` — el hash es bytes, lo convertimos a string para guardarlo en la DB
- `check_password_hash()` — hashea la contraseña ingresada con el mismo salt y compara

---

## Place

```python
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    owner_id    = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    image_url   = db.Column(db.String(500), nullable=True)

    reviews   = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))
    images    = db.relationship('PlaceImage', backref='place', lazy=True,
                                cascade='all, delete-orphan')
```

### ¿Por qué existe la tabla `place_amenity`?

Las relaciones **Many-to-Many** no se pueden representar directamente en SQL.  
Un lugar puede tener muchas amenities, y una amenity puede estar en muchos lugares.  
La solución es una tabla intermedia:

```
places         place_amenity       amenities
---------      ---------------     ----------
id=abc   ──→   place_id=abc        id=wifi
               amenity_id=wifi ──→
```

```python
db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True)
```
`ForeignKey('places.id')` garantiza que solo se pueden insertar IDs que existen en la tabla `places`.  
`primary_key=True` en ambas columnas crea una **clave primaria compuesta** — la combinación de `place_id + amenity_id` debe ser única.

```python
amenities = db.relationship('Amenity', secondary=place_amenity, ...)
```
`secondary=place_amenity` le dice a SQLAlchemy que use la tabla intermedia para la relación Many-to-Many.

```python
cascade='all, delete-orphan'
```
Cuando se elimina un lugar, SQLAlchemy elimina automáticamente todas sus imágenes de la tabla `place_images`.

---

## Review

```python
class Review(BaseModel):
    __tablename__ = 'reviews'

    text     = db.Column(db.String(1000), nullable=False)
    rating   = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
```

`ForeignKey('places.id')` y `ForeignKey('users.id')` aseguran que no se puede crear una review para un lugar o usuario que no existen.

---

## PlaceImage

```python
class PlaceImage(BaseModel):
    __tablename__ = 'place_images'

    place_id  = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
```

Permite que un lugar tenga múltiples imágenes en una galería. La relación `cascade='all, delete-orphan'` en `Place` asegura que si se borra el lugar, se borran también todas sus imágenes.

---

## Amenity

```python
class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name        = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def update_amenity(self, data):
        if "name" in data:
            if not data["name"] or not data["name"].strip():
                raise ValueError("Amenity name cannot be empty")
            if len(data["name"]) > 50:
                raise ValueError("Amenity name cannot exceed 50 characters")
        self.update(data)
```

### Columnas

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `name` | `String(50)` | `NOT NULL`, `UNIQUE` | Nombre de la amenity (WiFi, Pool, etc.) |
| `description` | `String(255)` | nullable | Descripción opcional |

```python
unique=True
```
Garantiza que no pueden existir dos amenities con el mismo nombre — no tiene sentido tener dos "WiFi" en la base de datos.

### `update_amenity()`

```python
def update_amenity(self, data):
    if "name" in data:
        if not data["name"] or not data["name"].strip():
            raise ValueError("Amenity name cannot be empty")
        if len(data["name"]) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
    self.update(data)
```

Método propio de validación antes de delegar al `update()` del `BaseModel`.
- `.strip()` elimina espacios — no se puede crear una amenity llamada `"   "` (solo espacios)
- Valida que el nombre no exceda 50 caracteres antes de intentar guardarlo

### Relación Many-to-Many con Place

Las amenities se conectan a los lugares a través de la tabla intermedia `place_amenity` definida en `place.py`. Una amenity puede estar en muchos lugares y un lugar puede tener muchas amenities.

```
amenities        place_amenity       places
----------       -------------       -------
id=wifi    ←──  amenity_id=wifi     id=abc
               place_id=abc    ──→
```

---
---

# Repository Pattern — Capa de persistencia

El **Repository Pattern** es una capa de abstracción entre la lógica de negocio (Facade) y la base de datos.

```
API (endpoints)
    ↓
Facade (lógica de negocio)
    ↓
Repository (acceso a datos)
    ↓
Base de datos (SQLite)
```

La Facade no sabe si los datos están en SQLite, en memoria o en MySQL — solo llama métodos del repositorio.

## Repository abstracto

```python
class Repository(ABC):
    @abstractmethod
    def add(self, obj): pass

    @abstractmethod
    def get(self, obj_id): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def update(self, obj_id, data): pass

    @abstractmethod
    def delete(self, obj_id): pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value): pass
```

`ABC` (Abstract Base Class) — define un "contrato". Cualquier clase que herede de `Repository` **debe** implementar todos estos métodos. Si no lo hace, Python lanza un error.

## SQLAlchemyRepository

```python
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model  # Ej: User, Place, Review

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)
        # Equivale a: SELECT * FROM users WHERE id = 'obj_id'

    def get_all(self):
        return self.model.query.all()
        # Equivale a: SELECT * FROM users

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
        # Equivale a: SELECT * FROM users WHERE email = 'email' LIMIT 1
```

### ¿Qué es `db.session`?

`db.session` es una transacción en memoria. Los cambios que hacés con `db.session.add()` no se guardan en la base de datos hasta que llamás `db.session.commit()`.

```
db.session.add(user)    ← objeto en memoria, aún no en DB
db.session.commit()     ← AHORA sí se escribe en la DB
```

Si algo falla antes del `commit()`, `db.session.rollback()` deshace todos los cambios.

## UserRepository

```python
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
```

`UserRepository` hereda todo el CRUD genérico de `SQLAlchemyRepository` y agrega el método específico `get_user_by_email()` que solo tiene sentido para usuarios.

---
---

# Facade — Lógica de negocio

La **Facade** es el puente entre la API y la base de datos. Concentra toda la lógica de negocio: validaciones, reglas de negocio, coordinación entre repositorios.

```python
class HBnBFacade:
    def __init__(self):
        self.user_repo    = UserRepository()
        self.place_repo   = SQLAlchemyRepository(Place)
        self.review_repo  = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
```

Cada repositorio maneja una entidad. La Facade los coordina.

## Ejemplo — crear un lugar

```python
def create_place(self, place_data):
    # 1. Validar campos requeridos
    required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
    for field in required_fields:
        if field not in place_data:
            raise ValueError(f"Missing required field: {field}")

    # 2. Validar rangos
    if place_data['price'] < 0:
        raise ValueError("Price must be greater than or equal to 0")
    if not (-90 <= place_data['latitude'] <= 90):
        raise ValueError("Latitude must be between -90 and 90")

    # 3. Verificar que el owner existe
    owner = self.user_repo.get(place_data['owner_id'])
    if owner is None:
        raise ValueError("Owner not found")

    # 4. Crear y guardar
    place = Place(
        title=place_data['title'],
        price=place_data['price'],
        latitude=place_data['latitude'],
        longitude=place_data['longitude'],
        owner_id=place_data['owner_id']
    )
    self.place_repo.add(place)
    return place
```

La API solo llama `facade.create_place(data)` — no sabe nada de validaciones ni base de datos.

---
---

# auth.py — Endpoint de Login

```python
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Paso 1: buscar el usuario por email
        user = facade.get_user_by_email(credentials['email'])

        # Paso 2: verificar que existe y que la contraseña es correcta
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Paso 3: generar el token JWT
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin},
            expires_delta=timedelta(days=1)
        )

        # Paso 4: devolver el token
        return {'access_token': access_token}, 200
```

## ¿Qué es JWT?

**JSON Web Token** — tiene 3 partes separadas por `.`:

```
eyJhbGciOiJIUzI1NiJ9   ← Header (algoritmo)
.
eyJzdWIiOiJ1c2VyMTIzIn0  ← Payload (datos: user_id, is_admin, expiración)
.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← Signature (firma)
```

El servidor firma el token con `JWT_SECRET_KEY`. Si alguien modifica el payload, la firma ya no coincide y el servidor rechaza el token.

```python
identity=str(user.id)
```
`identity` es el dato principal del token — el ID del usuario. Se recupera con `get_jwt_identity()` en los endpoints protegidos.

```python
additional_claims={"is_admin": user.is_admin}
```
Datos extras que viajan en el token. Se recuperan con `get_jwt()`. Así sabemos si el usuario es admin sin consultar la base de datos en cada petición.

```python
expires_delta=timedelta(days=1)
```
El token expira en 1 día. Después de eso el usuario debe hacer login de nuevo.

---
---

# Endpoints — Control de acceso (RBAC)

RBAC (Role-Based Access Control) — diferentes permisos según el rol del usuario.

## Crear un lugar — `POST /api/v1/places/`

```python
@jwt_required()
def post(self):
    current_user = get_jwt_identity()
    place_data = request.json
    # Se fuerza el owner_id desde el token — el usuario no puede falsificarlo
    place_data['owner_id'] = current_user
    place = facade.create_place(place_data)
    return {...}, 201
```

`place_data['owner_id'] = current_user` — aunque el usuario mande un `owner_id` diferente en el body, siempre se sobreescribe con el ID del token. Evita que alguien cree lugares "en nombre de otro".

## Actualizar un lugar — `PUT /api/v1/places/<id>`

```python
@jwt_required()
def put(self, place_id):
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    current_user = get_jwt_identity()

    place = facade.get_place(place_id)
    if place is None:
        return {'error': 'Place not found'}, 404

    # Solo el dueño o admin puede modificar
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    ...
```

```python
if not is_admin and place.owner_id != current_user:
```
Lógica del ownership check:
- Si es admin → siempre puede
- Si no es admin Y el lugar no es suyo → 403 Forbidden

## Crear una review — `POST /api/v1/reviews/`

```python
@jwt_required()
def post(self):
    current_user = get_jwt_identity()
    review_data = request.json
    review_data['user_id'] = current_user  # ID siempre viene del token

    # No se puede reviewar el propio lugar
    place = facade.get_place(review_data['place_id'])
    if place.owner_id == current_user:
        return {'error': 'You cannot review your own place'}, 400

    # No se puede reviewar el mismo lugar dos veces
    existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
    for review in existing_reviews:
        if review.user_id == current_user:
            return {'error': 'You have already reviewed this place'}, 400
```

## Resumen de permisos

| Endpoint | Público | Usuario autenticado | Solo admin |
|---|---|---|---|
| `GET /places/` | ✅ | ✅ | ✅ |
| `POST /places/` | ❌ | ✅ (owner) | ✅ |
| `PUT /places/<id>` | ❌ | ✅ (solo su lugar) | ✅ |
| `GET /users/` | ✅ | ✅ | ✅ |
| `POST /users/` | ❌ | ❌ | ✅ |
| `PUT /users/<id>` | ❌ | ✅ (solo su perfil) | ✅ |
| `POST /amenities/` | ❌ | ❌ | ✅ |
| `POST /reviews/` | ❌ | ✅ | ✅ |
| `DELETE /reviews/<id>` | ❌ | ✅ (solo su review) | ✅ |

---
---

# Endpoints — CRUD completo

Cada archivo en `app/api/v1/` define un `Namespace` de Flask-RESTX con sus rutas. Todos los endpoints devuelven JSON.

---

## users.py

### `POST /api/v1/users/` — Crear usuario (solo admin)

```python
@jwt_required()
def post(self):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403
    user_data = api.payload
    new_user = facade.create_user(user_data)
    return {'id': ..., 'first_name': ..., 'last_name': ..., 'email': ...}, 201
```

| Campo | Detalle |
|---|---|
| Auth requerida | Sí — JWT de admin |
| Body | `first_name`, `last_name`, `email`, `password` |
| Éxito | `201` |
| Errores | `400` email duplicado · `403` no es admin |

```python
if not claims.get('is_admin'):
    return {'error': 'Admin privileges required'}, 403
```
`get_jwt()` lee los `additional_claims` del token — `is_admin` se guardó ahí en el login. Solo los admins pueden crear usuarios; los usuarios normales no pueden auto-registrarse.

---

### `GET /api/v1/users/` — Listar todos los usuarios (público)

```python
def get(self):
    users = facade.get_all_users()
    return [{'id': ..., 'first_name': ..., 'last_name': ..., 'email': ...} for user in users], 200
```

No requiere token. Devuelve la lista completa de usuarios sin la contraseña.

---

### `GET /api/v1/users/<user_id>` — Obtener un usuario (público)

```python
def get(self, user_id):
    user = facade.get_user(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    return {'id': ..., 'first_name': ..., 'last_name': ..., 'email': ...}, 200
```

| Éxito | `200` con datos del usuario |
|---|---|
| Error | `404` si no existe |

---

### `PUT /api/v1/users/<user_id>` — Actualizar usuario

```python
@jwt_required()
def put(self, user_id):
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    current_user = get_jwt_identity()

    if not is_admin and user_id != current_user:
        return {'error': 'Unauthorized action'}, 403

    if not is_admin and ('email' in user_data or 'password' in user_data):
        return {'error': 'You cannot modify email or password'}, 400
```

Reglas de negocio:
- Usuario normal → solo puede modificar **su propio perfil**, y **no puede cambiar email ni password**
- Admin → puede modificar cualquier usuario y cualquier campo
- Si el admin cambia el email, se verifica que no esté en uso por otro usuario

| Éxito | `200` |
|---|---|
| Errores | `403` no autorizado · `400` email duplicado · `404` no existe |

---

## amenities.py

### `POST /api/v1/amenities/` — Crear amenity (solo admin)

```python
@jwt_required()
def post(self):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403
    amenity = facade.create_amenity(api.payload)
    return {'id': amenity.id, 'name': amenity.name}, 201
```

| Body | `name` (requerido) |
|---|---|
| Auth | JWT de admin |
| Éxito | `201` |
| Errores | `400` nombre vacío o > 50 chars · `403` no es admin |

---

### `GET /api/v1/amenities/` — Listar amenities (público)

```python
def get(self):
    amenities = facade.get_all_amenities()
    return [{'id': a.id, 'name': a.name} for a in amenities], 200
```

---

### `GET /api/v1/amenities/<amenity_id>` — Obtener amenity (público)

Devuelve `{'id': ..., 'name': ...}` o `404` si no existe.

---

### `PUT /api/v1/amenities/<amenity_id>` — Actualizar amenity (solo admin)

```python
@jwt_required()
def put(self, amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403
    updated = facade.update_amenity(amenity_id, api.payload)
    return {'message': 'Amenity updated successfully', 'amenity': {'id': ..., 'name': ...}}, 200
```

La validación del nombre (no vacío, máximo 50 caracteres) la hace `Amenity.update_amenity()` antes de persistir.

---

## places.py

### `POST /api/v1/places/` — Crear lugar (usuario autenticado)

```python
@jwt_required()
def post(self):
    current_user = get_jwt_identity()
    place_data = request.json
    place_data['owner_id'] = current_user  # se fuerza desde el token
    place = facade.create_place(place_data)
    return {'id': ..., 'title': ..., 'price': ..., 'owner_id': ...}, 201
```

| Body | `title`, `price`, `latitude`, `longitude` (requeridos) · `description`, `image_url` (opcionales) |
|---|---|
| Auth | JWT de cualquier usuario |
| owner_id | Siempre se toma del token, ignorando lo que mande el body |
| Éxito | `201` |
| Errores | `400` validación fallida · `401` sin token |

---

### `GET /api/v1/places/` — Listar lugares (público)

```python
def get(self):
    places = facade.get_all_places()
    return [{
        'id': ..., 'title': ..., 'price': ...,
        'owner': {'id': ..., 'first_name': ..., 'last_name': ...},
        'amenities': [{'id': ..., 'name': ...}],
        'image_url': ...
    } for p in places], 200
```

Devuelve una lista con info básica de cada lugar, incluyendo el owner y las amenities ya resueltos (no solo IDs).

---

### `GET /api/v1/places/<place_id>` — Detalle de un lugar (público)

```python
def get(self, place_id):
    place = facade.get_place(place_id)
    reviews = facade.get_reviews_by_place(place_id)
    return {
        'id': ..., 'title': ..., 'description': ..., 'price': ...,
        'owner': {'id': ..., 'first_name': ..., 'last_name': ..., 'email': ...},
        'amenities': [...],
        'reviews': [{'id': ..., 'text': ..., 'rating': ..., 'user_id': ..., 'created_at': ...}],
        'image_url': ...,
        'images': [{'id': ..., 'image_url': ...}]   # galería completa
    }, 200
```

Es el endpoint más completo — devuelve toda la información del lugar incluyendo owner, amenities, reviews con fecha, e imágenes de galería.

---

### `PUT /api/v1/places/<place_id>` — Actualizar lugar (owner o admin)

```python
@jwt_required()
def put(self, place_id):
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    updated_place = facade.update_place(place_id, request.json)
    return {'id': ..., 'title': ..., ...}, 200
```

Solo el dueño del lugar o un admin pueden modificarlo.

---

### `POST /api/v1/places/<place_id>/amenities/<amenity_id>` — Agregar amenity a lugar

```python
@jwt_required()
def post(self, place_id, amenity_id):
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    facade.add_amenity_to_place(place_id, amenity_id)
    return {'message': 'Amenity added successfully'}, 200
```

Conecta una amenity existente a un lugar existente en la tabla `place_amenity`. Solo el owner o admin pueden hacer esto.

---

### `GET /api/v1/places/<place_id>/reviews` — Reviews de un lugar (público)

```python
def get(self, place_id):
    reviews = facade.get_reviews_by_place(place_id)
    return [{'id': ..., 'text': ..., 'rating': ..., 'user_id': ...} for r in reviews], 200
```

---

## reviews.py

### `POST /api/v1/reviews/` — Crear review (usuario autenticado)

```python
@jwt_required()
def post(self):
    current_user = get_jwt_identity()
    review_data['user_id'] = current_user  # se fuerza desde el token

    place = facade.get_place(review_data['place_id'])
    if place.owner_id == current_user:
        return {'error': 'You cannot review your own place'}, 400

    for review in existing_reviews:
        if review.user_id == current_user:
            return {'error': 'You have already reviewed this place'}, 400

    r = facade.create_review(review_data)
    return {'id': ..., 'text': ..., 'rating': ..., 'user_id': ..., 'place_id': ...}, 201
```

| Body | `text`, `rating` (1-5), `place_id` |
|---|---|
| Auth | JWT de cualquier usuario |
| Reglas | No reviewar propio lugar · No reviewar el mismo lugar dos veces |
| Éxito | `201` |
| Errores | `400` reglas violadas · `404` lugar no existe |

---

### `GET /api/v1/reviews/` — Listar todas las reviews (público)

Devuelve todas las reviews con `id`, `text`, `rating`, `user_id`, `place_id`.

---

### `GET /api/v1/reviews/<review_id>` — Obtener una review (público)

Devuelve los datos de la review o `404` si no existe.

---

### `PUT /api/v1/reviews/<review_id>` — Actualizar review (author o admin)

```python
@jwt_required()
def put(self, review_id):
    if not is_admin and r.user_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    updated = facade.update_review(review_id, request.json)
    return {'id': ..., 'text': ..., 'rating': ..., 'user_id': ..., 'place_id': ...}, 200
```

Solo el autor de la review o un admin pueden modificarla.

---

### `DELETE /api/v1/reviews/<review_id>` — Eliminar review (author o admin)

```python
@jwt_required()
def delete(self, review_id):
    if not is_admin and success.user_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    facade.delete_review(review_id)
    return {'message': 'Review deleted successfully'}, 200
```

---
---

# Endpoints — Galería de imágenes (PlaceImage)

Los endpoints de galería viven dentro de `places.py` porque una imagen pertenece a un lugar.

### `GET /api/v1/places/<place_id>/images` — Obtener imágenes (público)

```python
def get(self, place_id):
    images = facade.get_place_images(place_id)
    return [{'id': img.id, 'image_url': img.image_url} for img in images], 200
```

Devuelve todas las imágenes de galería de un lugar. No requiere token.

---

### `POST /api/v1/places/<place_id>/images` — Agregar imagen (owner o admin)

```python
@jwt_required()
def post(self, place_id):
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    if not data.get('image_url'):
        return {'error': 'image_url is required'}, 400
    img = facade.add_place_image(place_id, data['image_url'])
    return {'id': img.id, 'image_url': img.image_url}, 201
```

| Body | `image_url` (requerido) |
|---|---|
| Auth | JWT — owner del lugar o admin |
| Éxito | `201` con `id` e `image_url` de la imagen creada |
| Errores | `400` sin image_url · `403` no autorizado · `404` lugar no existe |

La imagen se guarda en la tabla `place_images` vinculada al lugar por `place_id`.  
El frontend usa la **última imagen** de la lista como imagen hero (cabecera) en `place.html`.

---

### `DELETE /api/v1/places/<place_id>/images/<image_id>` — Eliminar imagen (owner o admin)

```python
@jwt_required()
def delete(self, place_id, image_id):
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403
    deleted = facade.delete_place_image(image_id)
    if not deleted:
        return {'error': 'Image not found'}, 404
    return {'message': 'Image deleted successfully'}, 200
```

`facade.delete_place_image()` busca la imagen por su `image_id`, la borra de la DB y devuelve `True`. Si no existe devuelve `False` y el endpoint responde `404`.

---
---

# Diagrama de relaciones (ERD)

```
users               places              reviews
------              -------             --------
id (PK)    ←──┐    id (PK)    ←──┐    id (PK)
first_name     │    title          │    text
last_name      │    description    │    rating
email          │    price          │    place_id (FK) ──→ places.id
password       │    latitude       │    user_id (FK)  ──→ users.id
is_admin       └─── owner_id (FK)  └────
               └─── (backref: owner)

place_amenity       amenities           place_images
--------------      ----------          ------------
place_id (FK)       id (PK)            id (PK)
amenity_id (FK)     name               place_id (FK)
                    description        image_url
```

### Relaciones

| Tipo | Ejemplo |
|---|---|
| One-to-Many | Un User tiene muchos Places |
| One-to-Many | Un Place tiene muchas Reviews |
| One-to-Many | Un Place tiene muchas PlaceImages |
| Many-to-Many | Un Place tiene muchas Amenities (y viceversa) |

---
---

# Swagger — Documentación automática

Flask-RESTX genera la documentación Swagger automáticamente.

```python
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    ...
})

@api.expect(place_model)
@api.response(201, 'Place successfully created')
@api.response(400, 'Invalid input data')
def post(self):
    """Create a new place (authenticated users only)"""
```

- `api.model()` — define el esquema del body esperado
- `@api.expect()` — indica qué modelo espera el endpoint
- `@api.response()` — documenta los posibles códigos de respuesta
- El docstring `"""..."""` aparece como descripción en Swagger

Accedé a la documentación en: `http://127.0.0.1:5000/api/v1/`

---
---

# Flujos completos

## Flujo de Login
```
1. Frontend envía POST /api/v1/auth/login con email y password
2. auth.py recibe la petición
3. facade.get_user_by_email(email) → busca el usuario en la DB
4. user.verify_password(password) → bcrypt compara hashes
5. create_access_token(identity=user.id, is_admin=user.is_admin)
6. Devuelve {"access_token": "eyJ..."}
7. Frontend guarda el token en una cookie
```

## Flujo de crear un lugar
```
1. Frontend envía POST /api/v1/places/ con Authorization: Bearer <token>
2. @jwt_required() verifica el token
3. get_jwt_identity() extrae el user_id del token
4. place_data['owner_id'] = current_user (se fuerza el owner)
5. facade.create_place(place_data):
   - Valida campos requeridos
   - Valida rangos (precio > 0, latitud entre -90 y 90)
   - Verifica que el owner existe
   - Crea el objeto Place
   - place_repo.add(place) → db.session.add() + db.session.commit()
6. Devuelve los datos del lugar creado con status 201
```

## Flujo de crear una review
```
1. Frontend envía POST /api/v1/reviews/ con Authorization: Bearer <token>
2. @jwt_required() verifica el token
3. review_data['user_id'] = current_user (se fuerza el author)
4. Verifica que el lugar existe
5. Verifica que el usuario no es el dueño del lugar
6. Verifica que el usuario no ya revisó el lugar
7. facade.create_review(review_data):
   - Valida rating (1-5)
   - Verifica que el user existe
   - Verifica que el place existe
   - Crea el objeto Review
   - review_repo.add(review) → DB
8. Devuelve los datos de la review con status 201
```

---
---

# Tests con pytest

## Cómo correr los tests

```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3-backend
source .venv/bin/activate
python3 -m pytest app/tests/ -v
```

## ¿Qué son los fixtures?

Son funciones que preparan el estado antes de los tests:

```python
@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)  # app con SQLite en RAM
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()  # cliente HTTP para hacer peticiones

@pytest.fixture(scope='session')
def admin_token(client):
    # Hace login y devuelve el token del admin
    response = client.post('/api/v1/auth/login', json={
        'email': 'admin@hbnb.io', 'password': 'admin1234'
    })
    return response.json['access_token']
```

`scope='session'` — el fixture se crea una vez y se reutiliza en todos los tests de la sesión.

## Tipos de tests

```python
def test_create_place(client, admin_token, user_token):
    """El usuario puede crear un lugar"""
    response = client.post('/api/v1/places/', json={...},
        headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 201

def test_owner_id_forced_from_token(client, user_token):
    """El owner_id siempre viene del token, no del body"""
    response = client.post('/api/v1/places/', json={
        ..., 'owner_id': 'fake-owner-id'  # intentamos mandar un ID falso
    }, headers={'Authorization': f'Bearer {user_token}'})
    data = response.get_json()
    assert data['owner_id'] != 'fake-owner-id'  # debe ser el del token

def test_cannot_review_own_place(client, user_token, place_id):
    """Un usuario no puede reviewar su propio lugar"""
    response = client.post('/api/v1/reviews/', json={
        'text': 'great', 'rating': 5, 'place_id': place_id
    }, headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 400
```

---
---

# Comandos útiles

## Iniciar el servidor
```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3-backend
source .venv/bin/activate
python3 run.py
```

## Crear admin
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

## Obtener token de admin
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo $TOKEN
```

## Verificar base de datos
```bash
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3-backend/instance/development.db "SELECT id, email, is_admin FROM users;"
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3-backend/instance/development.db "SELECT id, title, price FROM places;"
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3-backend/instance/development.db "SELECT id, name FROM amenities;"
```

---

## Credenciales de prueba

| Usuario | Email | Password | Rol |
|---|---|---|---|
| Admin | admin@hbnb.io | admin1234 | Admin |
| Test User | test@example.com | password123 | Usuario |
| Julian | julian@example.com | password456 | Usuario |

---
---

# Preguntas de práctica

## ¿Para qué se usa `db`?

`db` es la instancia de SQLAlchemy definida en `extensions.py`. Tiene tres roles:

**1. Definir tablas** — a través de los modelos
```python
class Review(db.Model):
    text = db.Column(db.String(1000), nullable=False)
```

**2. Leer datos**
```python
db.session.get(Review, review_id)     # SELECT * FROM reviews WHERE id = ?
Review.query.all()                     # SELECT * FROM reviews
Review.query.filter_by(place_id=x)    # SELECT * FROM reviews WHERE place_id = ?
```

**3. Escribir datos**
```python
db.session.add(review)    # prepara el INSERT en memoria
db.session.commit()       # ejecuta el SQL y guarda en disco
db.session.delete(review) # prepara el DELETE
```

Sin el `commit()`, el objeto existe en Python pero nunca llega a la base de datos.

---

## ¿Para qué creamos `UserRepository`?

`SQLAlchemyRepository` es genérico — sirve para cualquier modelo (`Place`, `Review`, `Amenity`). Tiene `get`, `get_all`, `add`, `delete`... pero no sabe buscar por email porque email es un concepto específico de `User`.

`UserRepository` hereda todo el CRUD genérico y agrega solo lo que `User` necesita:

```python
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)  # le dice al padre "trabajá con la tabla users"

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
```

Se usa en dos lugares críticos:
- **Login** — verificar que el email existe antes de comparar la contraseña
- **Crear usuario** — verificar que el email no esté ya registrado

---

## ¿Para qué usamos `get_jwt()` y `get_jwt_identity()`?

Son dos funciones distintas que leen partes distintas del token JWT:

```python
current_user = get_jwt_identity()   # devuelve el identity → el ID del usuario
claims       = get_jwt()            # devuelve TODOS los claims → incluye is_admin
```

`get_jwt_identity()` responde **¿quién es?** — devuelve el `str(user.id)` que se guardó al hacer login:
```python
# En auth.py al crear el token:
create_access_token(identity=str(user.id), ...)

# En places.py al usarlo:
current_user = get_jwt_identity()        # "abc-123-uuid"
place_data['owner_id'] = current_user    # fuerza el owner desde el token
```

`get_jwt()` responde **¿qué rol tiene?** — devuelve todos los additional_claims:
```python
# En auth.py al crear el token:
create_access_token(additional_claims={"is_admin": user.is_admin}, ...)

# En places.py al usarlo:
claims   = get_jwt()
is_admin = claims.get('is_admin', False)   # True o False

if not is_admin and place.owner_id != current_user:
    return {'error': 'Unauthorized action'}, 403
```

Resumen:

| Función | ¿Qué devuelve? | ¿Para qué se usa? |
|---|---|---|
| `get_jwt_identity()` | ID del usuario | Saber quién hace la petición |
| `get_jwt()` | Todos los claims | Verificar roles (`is_admin`) |

---

## ¿Para qué se usa `payload`?

El payload es la **parte del medio** del token JWT (entre los dos puntos `.`), codificada en base64. Contiene los datos que se guardaron al crear el token:

```
eyJhbGciOiJIUzI1NiJ9  .  eyJzdWIiOiJ1c2VyMTIzIiwiaXNfYWRtaW4iOmZhbHNlfQ  .  SflKxwRJSMeKK...
      header                              payload                                  signature
```

El payload decodificado contiene:
```json
{
  "sub": "abc-123-uuid",
  "is_admin": false,
  "exp": 1234567890,
  "iat": 1234567890
}
```

En el **backend**, Flask-JWT lo decodifica automáticamente con `get_jwt_identity()` y `get_jwt()`.

En el **frontend** (`common.js`), lo decodificamos manualmente para obtener el ID del usuario sin hacer una petición extra a la API:
```js
const payload = JSON.parse(atob(token.split('.')[1]));
const currentUserId = payload.sub;   // "abc-123-uuid"
```

- `token.split('.')[1]` — toma la parte del medio
- `atob()` — decodifica base64 a string
- `JSON.parse()` — convierte el string a objeto JavaScript
- `payload.sub` — el `sub` (subject) es donde JWT guarda el `identity` (el user.id)

---
---

# Descripción concisa de cada archivo

| Archivo | En una línea |
|---|---|
| `run.py` | Punto de entrada — crea la app con `create_app()` y arranca el servidor |
| `config.py` | Define 3 configs: dev (SQLite en disco), test (SQLite en RAM), prod (MySQL + env vars) |
| `extensions.py` | Crea `db`, `bcrypt` y `jwt` sin app — soluciona el problema de circular imports |
| `app/__init__.py` | Application Factory — crea Flask, conecta extensiones, registra namespaces, crea tablas |
| `models/base_model.py` | Padre de todos los modelos — UUID automático, `created_at`, `updated_at`, `update()` |
| `models/user.py` | Tabla `users` — hasheo de contraseñas con bcrypt, relaciones a places y reviews |
| `models/place.py` | Tabla `places` + tabla intermedia `place_amenity` para la relación Many-to-Many con amenities |
| `models/review.py` | Tabla `reviews` — FK a `places.id` y `users.id` |
| `models/amenity.py` | Tabla `amenities` — nombre único, validación de longitud |
| `models/place_image.py` | Tabla `place_images` — galería de imágenes por lugar, se borra en cascada con el lugar |
| `persistence/repository.py` | Repository Pattern — `SQLAlchemyRepository` con CRUD genérico para cualquier modelo |
| `persistence/user_repository.py` | Extiende el repositorio genérico agregando `get_user_by_email()` |
| `services/facade.py` | Capa de lógica de negocio — valida datos, coordina repositorios, aplica reglas |
| `api/v1/auth.py` | Único endpoint de login — verifica credenciales y devuelve el token JWT |
| `api/v1/users.py` | CRUD de usuarios — admin crea, cualquiera lee, usuario actualiza solo el suyo |
| `api/v1/places.py` | CRUD de lugares + endpoints de galería de imágenes + agregar amenities |
| `api/v1/reviews.py` | CRUD de reviews — con control de duplicados y ownership |
| `api/v1/amenities.py` | CRUD de amenities — solo admin puede crear y actualizar |

---
---

# Puntos clave para la presentación

Estos son los conceptos que más preguntan — si los entendés bien, podés responder casi cualquier pregunta:

**1. Application Factory** — `create_app()` existe para poder crear la app con distintas configs (dev, test). Sin esto, los tests no pueden usar una base de datos separada.

**2. `extensions.py`** — `db`, `bcrypt` y `jwt` se crean sin app para evitar circular imports. Se "conectan" a la app después con `init_app(app)`.

**3. JWT** — tiene 3 partes: header, payload (user_id + is_admin + expiración), signature. El servidor firma con `JWT_SECRET_KEY`. Si alguien modifica el payload, la firma no coincide y el token es rechazado.

**4. `get_jwt_identity()`** responde quién es el usuario. **`get_jwt()`** responde qué rol tiene.

**5. Repository Pattern** — la Facade no habla directamente con SQLAlchemy. Habla con el repositorio. Si mañana cambiamos de SQLite a PostgreSQL, solo cambia el repositorio, no la Facade ni los endpoints.

**6. Ownership check** — el patrón que se repite en todos los endpoints protegidos:
```python
if not is_admin and resource.owner_id != current_user:
    return {'error': 'Unauthorized action'}, 403
```

**7. `owner_id` siempre viene del token** — en `POST /places/` y `POST /reviews/`, aunque el usuario mande un `owner_id` en el body, siempre se sobreescribe con el ID del token. Evita suplantación de identidad.

**8. bcrypt** — las contraseñas nunca se guardan en texto plano. Se hashean con `generate_password_hash()` y se verifican con `check_password_hash()`. El hash es irreversible.
