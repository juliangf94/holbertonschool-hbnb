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
part3/
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
│   └── persistence/
│       ├── repository.py       # Repository pattern (InMemory + SQLAlchemy)
│       └── user_repository.py  # Repositorio específico de User
└── tests/
    └── test_endpoints.py       # Tests de integración con pytest
```

---

## Cómo iniciar la app

```bash
cd ~/holberton_projects/holbertonschool-hbnb/part3
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

# \_\_init\_\_.py — Application Factory

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
id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
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
cd ~/holberton_projects/holbertonschool-hbnb/part3
source .venv/bin/activate
python3 -m pytest tests/ -v
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
cd ~/holberton_projects/holbertonschool-hbnb/part3
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
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3/instance/development.db "SELECT id, email, is_admin FROM users;"
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3/instance/development.db "SELECT id, title, price FROM places;"
sqlite3 ~/holberton_projects/holbertonschool-hbnb/part3/instance/development.db "SELECT id, name FROM amenities;"
```

---

## Credenciales de prueba

| Usuario | Email | Password | Rol |
|---|---|---|---|
| Admin | admin@hbnb.io | admin1234 | Admin |
| Test User | test@example.com | password123 | Usuario |
| Julian | julian@example.com | password456 | Usuario |