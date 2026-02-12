# holbertonschool-hbnb

## Package Diagram

```mermaid

classDiagram
    direction TB

    class API_Endpoints {
        <<Presentation Layer>>
        +POST /users
        +POST /places
        +POST /reviews
        +GET /places
    }

    class HBnBFacade {
        <<Facade>>
        +createUser(data)
        +createPlace(data)
        +addReview(data)
        +getPlace(id)
    }

    class User {
        +String email
    }
    class Place {
        +String title
    }
    class Review {
        +int rating
    }
    class Amenity {
        +String name
    }
    
    class BaseModel {
        +UUID id
        +save()
        +update()
    }

    class IRepository {
        <<Interface>>
        +save(obj)
        +get(id)
        +update(obj)
        +delete(id)
    }

    class SQLAlchemyRepository {
        +session
    }

    %% Relations
    API_Endpoints --> HBnBFacade : "1. Request"
    
    HBnBFacade --> User : "2. Business Logic"
    HBnBFacade --> Place
    HBnBFacade --> Review
    HBnBFacade --> Amenity

    HBnBFacade --> IRepository : "3. Persist"

    %% Héritage
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% Implémentation
    IRepository <|.. SQLAlchemyRepository

```
# Architecture Overview

This project follows a layered architecture combined with the Facade pattern and the Repository pattern.

## Presentation Layer – API Endpoints

The `API_Endpoints` class represents the presentation layer of the application.  
It exposes HTTP routes such as:

- `POST /users`
- `POST /places`
- `POST /reviews`
- `GET /places`

This layer is responsible for handling incoming HTTP requests and forwarding them to the business layer.

---

## Business Layer – HBnBFacade

The `HBnBFacade` acts as a Facade.

It provides simplified methods such as:

- `createUser(data)`
- `createPlace(data)`
- `addReview(data)`
- `getPlace(id)`

The facade centralizes the business logic and coordinates interactions between models and repositories.

This design:
- Reduces coupling
- Simplifies the API layer
- Improves maintainability

---
## Domain Models

The main entities of the system are:

- `User`
- `Place`
- `Review`
- `Amenity`

All of them inherit from `BaseModel`, which provides:

- A unique identifier (`UUID id`)
- Common methods (`save()`, `update()`)

This promotes code reuse and consistency.

---

# Persistence Layer – Repository Pattern

The project uses the Repository pattern to abstract database operations.


## `IRepository` (Interface)
Defines generic methods:
- `save(obj)`
- `get(id)`
- `update(obj)`
- `delete(id)`


## `SQLAlchemyRepository`
Implements `IRepository` using SQLAlchemy and manages database sessions.

The facade interacts only with the `IRepository` interface, not directly with SQLAlchemy.  
This makes the system more flexible and easier to test.

## Flow of a Request
1. The client sends a request to an API endpoint.
2. The API layer forwards the request to `HBnBFacade`.
3. The facade applies business logic.
4. The facade calls the repository to persist or retrieve data.
5. The repository interacts with the database.

---
