##   Describe the purpose of each directory and file.
##   Include instructions on how to install dependencies and run the application.

# Project Setup and Package Initialization

## Context

Before diving into the implementation of the business logic and API endpoints, it's essential to have **a well-organized project structure**. A **clear** and **modular** organization will help maintain the codebase, make it easier to integrate new features, and **ensure that your application is scalable**.

Additionally, to simplify the implementation, you are provided with the **complete in-memory repository code**.

## In this task, you will

1. Set up the structure for the Presentation, Business Logic, and Persistence layers, creating the necessary folders, packages, and files.
2. Prepare the project to use the Facade pattern for communication between layers.
3. Implement the in-memory repository to handle object storage and validation.
4. Plan for future integration of the Persistence layer, even though it won't be fully implemented in this part.

Although the Persistence layer will be fully implemented in Part 3, this task includes the implementation of the in-memory repository. This repository will later be replaced by a database-backed solution in Part 3.

## Instructions

1. **Create the Project Directory Structure**:

    Your project should be organized into the following structure:

    ```text
    hbnb/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── amenities.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── facade.py
    │   ├── persistence/
    │       ├── __init__.py
    │       ├── repository.py
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── README.md
    ```

    **Explanation:**

    - The `app/` directory contains the core application code.
    - The `api/` subdirectory houses the API endpoints, organized by version (`v1/`).
    - The `models/` subdirectory contains the business logic classes (e.g., `user.py`, `place.py`).
    - The `services/` subdirectory is where the Facade pattern is implemented, managing the interaction between layers.
    - The `persistence/` subdirectory is where the in-memory repository is implemented. This will later be replaced by a database-backed solution using SQL Alchemy.
    - `run.py` is the entry point for running the Flask application.
    - `config.py` will be used for configuring environment variables and application settings.
    - `requirements.txt` will list all the Python packages needed for the project.
    - `README.md` will contain a brief overview of the project.

