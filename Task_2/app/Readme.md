# Task 2 – Persistent Storage with Database Integration (FastAPI + SQLAlchemy)

## Objective

The objective of this task is to upgrade the in-memory REST API built in Task 1 to use a **relational database** for permanent, reliable, and scalable data storage. We will use **FastAPI** for building the API, **SQLAlchemy** as an ORM (Object Relational Mapper) to interact with the database, and **python-dotenv** for environment variable management. Optional support for **Alembic** (a migration tool) and **UUIDs** (for unique identifiers) will also be introduced.

This ensures that user data is stored persistently and can be managed safely across application restarts and deployments.

---

## Why Move From In-Memory to Persistent Storage?

The dictionary approach used in Task 1 (`users = {}`) was temporary. Once the server restarts, **all user data is lost**. It also has no way to efficiently search, sort, or scale.

### Limitations of In-Memory Storage:

* No persistence (data is lost when server restarts)
* Not scalable
* Cannot be shared across multiple processes or servers

### Benefits of Using a Database:

* **Permanent storage**: Data remains after server restart
* **Efficient queries**: Search, sort, filter efficiently
* **Structured schema**: Enforce rules on data
* **Scalability**: Use with millions of users

---

## Tools, Libraries, and Concepts Explained

### 1. FastAPI – Web Framework

**FastAPI** is a modern, Python-based web framework to build REST APIs easily. It uses **type hints** to automatically validate inputs and generate documentation.

#### Key Benefits:

* Automatic generation of Swagger UI documentation (`/docs`)
* Easy request handling using decorators like `@app.post()`
* Built-in validation using `pydantic`
* Supports both synchronous and asynchronous routes

### 2. Uvicorn – ASGI Server

**Uvicorn** is a fast, lightweight web server that runs FastAPI apps.

#### Key Concepts:

* **ASGI** (Asynchronous Server Gateway Interface): Enables modern Python web frameworks to handle async requests.

#### Usage:

```bash
uvicorn main:app --reload
```

* `main`: Python file name
* `app`: FastAPI instance
* `--reload`: Automatically reloads the app on file changes (for development)

---

### 3. SQLAlchemy – ORM (Object Relational Mapper)

**SQLAlchemy** is a Python library that connects Python code to relational databases (like SQLite, MySQL, PostgreSQL).

#### What is an ORM?

ORM stands for **Object Relational Mapper**. It maps Python classes to database tables, allowing you to:

* Define database structure using Python classes
* Write database queries using Python instead of SQL

#### Key Features:

* Models (tables) defined as Python classes
* Querying tables using methods instead of raw SQL
* Portable across multiple SQL databases (SQLite, PostgreSQL, etc.)

---

### 4. Alembic – Database Migration Tool

**Alembic** is a tool for managing database schema changes over time (i.e., creating/modifying tables). It works with SQLAlchemy.

#### Why Alembic?

* Auto-generates migration scripts from model changes
* Lets you version control your schema
* Applies updates incrementally with `alembic upgrade`

#### Example Commands:

```bash
alembic init alembic                    # Initialize Alembic
alembic revision --autogenerate -m "init"   # Generate migration
alembic upgrade head                    # Apply migration
```

---

### 5. python-dotenv – Load Environment Variables

`.env` files are used to store sensitive or environment-specific values, like your database URL.

**python-dotenv** loads `.env` values into your Python environment using `os.getenv()`.

#### Why use `.env`?

* Keeps credentials (e.g., DB passwords) out of source code
* Lets you easily switch between dev, test, and prod databases

#### Example:

`.env` file:

```env
DATABASE_URL=sqlite:///./users.db
```

`database.py`:

```python
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

### 6. Declarative Base (Base)

Used in SQLAlchemy to declare table models. All tables must inherit from `Base`:

```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

Then used like:

```python
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
```

---

### 7. Session and SessionLocal

Each request needs a separate connection (called a "session") to the database. SQLAlchemy uses sessions to interact with the DB.

```python
SessionLocal = sessionmaker(bind=engine, autoflush=False)
```

And later:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This gives each route handler its own temporary DB connection.

---

### 8. Pydantic – Input Validation

**Pydantic** is used to create request and response schemas. It validates the types of incoming data (e.g., ensures `age` is an integer, `email` is valid).

Example:

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
```

This ensures incoming data is structured correctly. Invalid data (like `age="abc"`) is automatically rejected.

---

### 9. UUID – Unique Identifiers

Instead of using numbers (1, 2, 3...) for user IDs, we use **UUIDs** which are random, globally unique values.

#### Example:

```python
from uuid import uuid4
user_id = str(uuid4())  # 'a4b88e91-0bb0-4a70-96fa-1b322b2f9a4e'
```

#### Why use UUIDs?

* Prevents conflicts in distributed systems
* Harder to guess user IDs
* Always unique across devices and environments

---

### 10. HTTPException

FastAPI allows you to return error messages using HTTPException:

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="User not found")
```

This will return a structured error message to the client with status 404.

---

### 11. Depends (Dependency Injection)

`Depends()` is used to inject dependencies like the database connection.

Instead of manually calling `get_db()`, FastAPI automatically calls it for you:

```python
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(...)
```

---

## Summary

| Term/Tool            | Role                                                       |
| -------------------- | ---------------------------------------------------------- |
| **FastAPI**          | Framework to build the API                                 |
| **Uvicorn**          | ASGI web server to run FastAPI app                         |
| **SQLAlchemy**       | ORM for Python to interact with databases                  |
| **Alembic**          | Manages schema changes in the DB (migrations)              |
| **Pydantic**         | Validates input data and structures responses              |
| **python-dotenv**    | Loads sensitive variables from `.env` into the code        |
| **Declarative Base** | Declares all table models                                  |
| **SessionLocal**     | Manages connections between API routes and the DB          |
| **UUID**             | Generates safe, unique IDs for users                       |
| **HTTPException**    | Used to return structured errors like 404                  |
| **Depends**          | Automatically provides database sessions to route handlers |

---
