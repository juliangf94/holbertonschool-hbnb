# HBnB Evolution: Technical Documentation
## 3. User Registration - Sequence Diagram

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call, POST /users
API->>BusinessLogic: createUser()
BusinessLogic->>Database: INSERT user

alt email/username exists
Database-->>BusinessLogic: constraint error
BusinessLogic-->>API: UserAlreadyExists
API-->>User: 409 Conflict
else user created
Database-->>BusinessLogic: userId
BusinessLogic-->>API: success
API-->>User: 201 Created
end
```

#   Explanatory Notes
##   Brief Description :
-   This API call allows a new user to register in the system by submitting required information such as email, username, and password.
-   The purpose of the sequence diagram is to illustrate how the system validates the input, processes the registration request, and either creates the user or returns an appropriate error response.

##  Flow of Interactions :
-   The User sends a POST /users request to the API layer with the user's registration data.
-   The API recieves the request and forwards it to the Business Logic layer.
-   The Business Logic validates the input and Attempts to create the user in the Database.
-   The Database enforces constraints, such as unique username or email
-   If constraint is violated, the error is propagated:
    -   Business Logic translate it into a meaningful error.
    -   API returns Code 409 (Conflict).
-   If the registration is successful:
    -   The database returns the new user ID.
    -   API respond with code 201 (Created).

-   Each layer contributes as follows:
    -   API: Handles HTTP Communication
    -   Business Logic: Applies rules and orchetrates operations
    -   Database: Ensure Data integrity and persistence

## 4. Place Creation - Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: API Call, POST /places
    API->>BusinessLogic: createPlace()
    BusinessLogic->>Database: INSERT place

    alt place exists / invalid data
        Database-->>BusinessLogic: consraint error
        BusinessLogic-->>API: PlaceAlreadyExists
        API-->>User: 400 Bad Request
    else place created
        Database-->>BusinessLogic: placeId
        BusinessLogic-->>API: success
        API-->>User: 201 Created
end
```

#   Explanatory Notes
##   Brief Description :
-   This API call allows an authenticated user to create a new place listing (similar to Airbnb).
-   The sequence diagram shows how the system validates the submitted data and stores the new place in the database.

##  Flow of Interactions :
-   The User sends a POST /places request containing place details.
-   The API recieves the request and forwards it to the Business Logic layer.
-   The Business Logic validates the input and sends an insert request to the Database.
-   The Database stores the new place and returns the unique Place ID
-   If constraint is violated, the error is propagated:
    -   API returns code 400 (Bad Request)
-   If the registration is successful:
    -   API respond with code 201 (Created).

-   Each layer contributes as follows:
    -   API: Handles HTTP Communication
    -   Business Logic: Applies rules and validation
    -   Database: Enforces constraints and persistance

## 5. Review Submission - Sequence Diagram

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call, POST /users
API->>BusinessLogic: createUser()
BusinessLogic->>Database: INSERT user

alt email/username exists
Database-->>BusinessLogic: constraint error
BusinessLogic-->>API: UserAlreadyExists
API-->>User: 409 Conflict
else user created
Database-->>BusinessLogic: userId
BusinessLogic-->>API: success
API-->>User: 201 Created
end
```

#   Explanatory Notes
##   Brief Description :
-   This API call allows a new user to register in the system by submitting required information such as email, username, and password.
-   The purpose of the sequence diagram is to illustrate how the system validates the input, processes the registration request, and either creates the user or returns an appropriate error response.

##  Flow of Interactions :
-   The User sends a POST /users request to the API layer with the user's registration data.
-   The API recieves the request and forwards it to the Business Logic layer.
-   The Business Logic validates the input and Attempts to create the user in the Database.
-   The Database enforces constraints, such as unique username or email
-   If constraint is violated, the error is propagated:
    -   Business Logic translate it into a meaningful error.
    -   API returns error 409 (Conflict).
-   If the registration is successful:
    -   The database returns the new user ID.
    -   API respond with code 201 (Created).

-
## 6. Fetching a Listof Places - Sequence Diagram

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call, POST /users
API->>BusinessLogic: createUser()
BusinessLogic->>Database: INSERT user

alt email/username exists
Database-->>BusinessLogic: constraint error
BusinessLogic-->>API: UserAlreadyExists
API-->>User: 409 Conflict
else user created
Database-->>BusinessLogic: userId
BusinessLogic-->>API: success
API-->>User: 201 Created
end
```

#   Explanatory Notes
##   Brief Description :
-   This API call allows a new user to register in the system by submitting required information such as email, username, and password.
-   The purpose of the sequence diagram is to illustrate how the system validates the input, processes the registration request, and either creates the user or returns an appropriate error response.

##  Flow of Interactions :
-   The User sends a POST /users request to the API layer with the user's registration data.
-   The API recieves the request and forwards it to the Business Logic layer.
-   The Business Logic validates the input and Attempts to create the user in the Database.
-   The Database enforces constraints, such as unique username or email
-   If constraint is violated, the error is propagated:
    -   Business Logic translate it into a meaningful error.
    -   API returns error 409 (Conflict).
-   If the registration is successful:
    -   The database returns the new user ID.
    -   API respond with code 201 (Created).
