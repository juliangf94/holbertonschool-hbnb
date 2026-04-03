# HBnB Part 3 — Guía de Preguntas para la Presentación

---

## ARQUITECTURA Y CONFIGURACIÓN

**¿Qué es el Application Factory Pattern y por qué lo usamos?**
Es un patrón donde la app Flask se crea dentro de una función `create_app()` en vez de directamente al inicio del archivo. Lo usamos para poder crear múltiples instancias con distintas configuraciones — desarrollo, testing, producción — sin cambiar el código.

**¿Qué hace `app.config.from_object(config_class)`?**
Flask lee todas las variables en MAYÚSCULAS de la clase de configuración (`DevelopmentConfig`, `TestingConfig`, etc.) y las carga en `app.config`. Centraliza toda la configuración en un solo lugar.

**¿Para qué sirve `extensions.py`?**
Crea las instancias de `db`, `bcrypt` y `jwt` fuera de `create_app()`. Esto evita el circular import — cualquier archivo puede importar estas extensiones sin causar conflictos de importación.

**¿Qué es un circular import y cómo lo resolviste?**
Es cuando dos archivos se importan mutuamente y Python entra en un loop infinito. Lo resolvimos creando `extensions.py` como archivo neutral — `__init__.py` y los modelos importan desde ahí en vez de importarse entre sí.

**¿Para qué sirven los tres configs: DevelopmentConfig, TestingConfig, ProductionConfig?**
- `DevelopmentConfig` — para desarrollar localmente, `DEBUG=True`, SQLite local
- `TestingConfig` — para pytest, base de datos en RAM (`sqlite:///:memory:`), se borra sola
- `ProductionConfig` — para servidor real, `DEBUG=False`, MySQL, claves desde variables de entorno

---

## AUTENTICACIÓN Y JWT

**¿Cómo funciona el sistema de login?**
El usuario manda email y password al endpoint `POST /api/v1/auth/login`. La facade busca el usuario por email, verifica el password con bcrypt, y si es correcto genera un token JWT con el ID del usuario y su rol `is_admin`. El token dura 1 hora.

**¿Qué es JWT y por qué es seguro?**
JSON Web Token — tiene 3 partes: header, payload y signature. El servidor firma el token con `SECRET_KEY`. Si alguien modifica el payload, la firma ya no coincide y el servidor rechaza el token. No se guardan sesiones en el servidor.

**¿Cómo sabés quién está logueado en un endpoint protegido?**
Con `get_jwt_identity()` que extrae el ID del usuario del token, y `get_jwt()` que devuelve todos los claims incluyendo `is_admin`.

**¿Qué es `@jwt_required()`?**
Es un decorator que bloquea el endpoint si no hay token válido en el header `Authorization: Bearer <token>`. Devuelve 401 automáticamente.

**¿Por qué el token expira en 1 hora?**
Por seguridad — si alguien roba el token, solo lo puede usar durante 1 hora. Con `timedelta(hours=1)` en `create_access_token()`.

---

## BCRYPT Y PASSWORDS

**¿Por qué nunca guardás la contraseña en texto plano?**
Si alguien accede a la base de datos vería todas las contraseñas. Con bcrypt guardamos un hash irreversible — nadie puede recuperar la contraseña original.

**¿Cómo funciona bcrypt para verificar una contraseña?**
Bcrypt incluye un "salt" (semilla aleatoria) dentro del hash. Al verificar, extrae el salt del hash guardado, hashea la contraseña ingresada con ese mismo salt y compara los resultados.

**¿Por qué `hash_password()` usa `bcrypt` de `extensions.py`?**
Antes causaba circular import porque `user.py` importaba `from app import bcrypt`. Con `extensions.py` el import está en un archivo neutral que no causa conflictos.

---

## RBAC (CONTROL DE ACCESO)

**¿Qué es RBAC?**
Role-Based Access Control — control de acceso basado en roles. En HBnB hay dos roles: usuario normal y admin (`is_admin=True`).

**¿Cómo funciona el ownership check en places?**
En el PUT de places verificamos que `place.owner_id == current_user` (ID del token). Si no coinciden devolvemos 403. El admin bypasea esta verificación con `if not is_admin and place.owner_id != current_user`.

**¿Por qué el owner_id se fuerza desde el token y no desde el body?**
Sin esto cualquier usuario podría enviar un `owner_id` de otra persona y crear un lugar en su nombre. Al sobreescribirlo con el token garantizamos que el owner siempre es el usuario autenticado.

**¿Cuáles endpoints son solo para admins?**
- `POST /api/v1/users/` — crear usuarios
- `POST /api/v1/amenities/` — crear amenities
- `PUT /api/v1/amenities/<id>` — modificar amenities

**¿Cómo se creó el primer admin para testear?**
Con `flask shell` insertamos el admin directamente en la base de datos. En producción se usa el script SQL `initial_data.sql`.

---

## SQLALCHEMY Y REPOSITORIO

**¿Qué es SQLAlchemy y por qué lo usamos?**
Es un ORM (Object-Relational Mapper) — permite trabajar con la base de datos usando Python en vez de SQL puro. En vez de `INSERT INTO users...` hacés `db.session.add(user)`.

**¿Qué es el Repository Pattern?**
Es una capa de abstracción entre la lógica de negocio y la base de datos. La Facade no sabe si los datos están en memoria o en SQLite — solo llama `user_repo.add()` o `user_repo.get()`.

**¿Por qué existe `InMemoryRepository` si ahora usamos SQLAlchemy?**
Se mantiene para backward compatibility y testing rápido. Los tests de la Part 2 lo usaban.

**¿Por qué `UserRepository` hereda de `SQLAlchemyRepository`?**
Para tener el CRUD genérico (add, get, delete) más métodos específicos de User como `get_user_by_email()`. Es más explícito y fácil de mantener que el genérico.

**¿Qué hace `db.session.commit()`?**
Escribe todos los cambios pendientes en la base de datos. Si falla, `db.session.rollback()` deshace todos los cambios para no dejar la base en estado inconsistente.

---

## MODELOS Y RELACIONES

**¿Qué es `__abstract__ = True` en BaseModel?**
Le dice a SQLAlchemy que no cree una tabla para `BaseModel`. Solo las clases hijas (`User`, `Place`, etc.) tendrán tablas propias.

**¿Qué es `PROTECTED = {"id", "created_at"}` en el método `update()`?**
Evita que alguien modifique el ID o la fecha de creación de un objeto — son campos que nunca deberían cambiar después de crearse.

**¿Cómo funciona la relación One-to-Many entre User y Place?**
En `User` definimos `places = db.relationship('Place', backref='owner', lazy=True)`. El `backref` crea automáticamente `place.owner` para acceder al dueño desde el lugar.

**¿Qué es una tabla de asociación y para qué sirve `place_amenity`?**
Las relaciones Many-to-Many no se pueden representar directamente en SQL. `place_amenity` es una tabla intermedia con dos columnas: `place_id` y `amenity_id`. Cada fila representa que un lugar tiene una amenity.

**¿Por qué `owner_id` tiene `ForeignKey('users.id')`?**
Garantiza integridad referencial — no se puede crear un lugar con un `owner_id` que no existe en la tabla `users`. La base de datos lo rechaza automáticamente.

---

## SQL SCRIPTS

**¿Para qué sirven los scripts SQL si ya tenemos SQLAlchemy?**
SQLAlchemy genera las tablas con Python, pero es importante entender cómo se ve el esquema en SQL puro. En producción real los DBAs trabajan con SQL, no con ORMs.

**¿Qué hace `create_tables.sql`?**
Crea las 5 tablas (`users`, `places`, `reviews`, `amenities`, `place_amenity`) con sus columnas, tipos de datos, primary keys, foreign keys y constraints. El orden importa — `users` antes que `places` porque `places` referencia `users`.

**¿Por qué el password del admin en `initial_data.sql` está hasheado?**
Nunca se guarda una contraseña en texto plano en la base de datos, ni siquiera en scripts SQL. El hash fue generado con `bcrypt.generate_password_hash("admin1234")`.

**¿Qué es `UNIQUE (user_id, place_id)` en la tabla reviews?**
Un constraint compuesto que garantiza que un usuario solo puede reviewar un lugar una vez. La combinación de ambos campos debe ser única.

---

## TESTS

**¿Qué es pytest y cómo funciona?**
Es un framework de testing para Python. Lee archivos que empiezan con `test_`, ejecuta funciones que empiezan con `test_` y verifica que las condiciones con `assert` sean verdaderas.

**¿Qué son los fixtures en pytest?**
Son funciones que preparan el estado antes de los tests. En nuestro caso `app`, `client`, `admin_token` y `user_token` son fixtures — se crean una vez y se comparten entre todos los tests de la sesión.

**¿Por qué usamos `TestingConfig` en los tests?**
Usa `sqlite:///:memory:` — base de datos en RAM que se crea al iniciar los tests y se borra sola al terminar. No toca el archivo `development.db` real.

**¿Qué es GitHub Actions y para qué lo configuramos?**
Es un sistema de CI/CD (Continuous Integration) de GitHub. Cada vez que hacemos push, GitHub ejecuta automáticamente todos los tests en un servidor limpio. Si fallan, nos avisa antes de que el código llegue a producción.

**¿Qué verifica `test_owner_id_forced_from_token`?**
Que aunque el usuario mande un `owner_id` falso en el body, el endpoint siempre use el ID del token JWT. Verifica que `data['owner_id'] != 'fake-owner-id'`.

**¿Qué verifica `test_cannot_review_own_place`?**
Que un usuario no pueda reviewar su propio lugar. Crea un lugar con el token del usuario y luego intenta crear una review para ese mismo lugar — debe devolver 400.

---

## DIAGRAMA ER

**¿Qué es un diagrama ER?**
Entity-Relationship Diagram — representa visualmente la estructura de la base de datos: qué tablas existen, qué columnas tienen y cómo se relacionan.

**¿Qué significa `||--o{` en Mermaid.js?**
- `||` — exactamente uno (lado izquierdo)
- `o{` — cero o muchos (lado derecho)
- Es la notación para one-to-many: un User tiene muchos Places

**¿Por qué `Place_Amenity` aparece en el diagrama?**
Porque las relaciones Many-to-Many necesitan una tabla intermedia en SQL. No se puede tener directamente "un Place tiene muchos Amenities" sin esta tabla de asociación.
