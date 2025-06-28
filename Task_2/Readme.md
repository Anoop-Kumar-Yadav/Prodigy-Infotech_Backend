

# TASK 2 (Persistent Storage + Database Integration in FastAPI)

---

## 1. LIBRARIES USED

Let’s start by understanding every tool/library installed.

### 1.1 FastAPI

* A modern web framework for building APIs using Python.
* Fast, easy, and supports async operations.
* Automatically generates Swagger docs.

**Why used here:**
To handle API routes like `POST /users`, `GET /users/{id}` etc.

---

### 1.2 SQLAlchemy

* SQLAlchemy is an **ORM (Object Relational Mapper)**.
* It lets you work with databases using Python classes and objects, instead of raw SQL queries.

**Why used here:**
To define the database schema (`User` table), interact with DB using Python.

---

### 1.3 Alembic

* Alembic is a **database migration tool**.
* Used with SQLAlchemy to auto-generate and apply changes to your DB structure (e.g., creating tables).

**Why used here:**
To auto-create the `users` table from your model code using Python migration scripts.

---

### 1.4 python-dotenv

* Loads environment variables (like `DATABASE_URL`) from a `.env` file.
* Helps keep secrets (like DB passwords) outside the code.

**Why used here:**
To securely load database settings and make your code environment-independent.

---

### 1.5 Uvicorn

* Uvicorn is an **ASGI web server** that runs your FastAPI app.

**Why used here:**
To serve your app locally and reload automatically during development.

---

## 2. FILES 
task_2/
├── app/
│   ├── __ init __.py
│   ├── main.py          ← Entry point of the app
│   ├── models.py        ← SQLAlchemy models (tables)
│   ├── schemas.py       ← Pydantic schemas (validation)
│   ├── crud.py          ← Business logic for CRUD operations
│   ├── database.py      ← DB engine & session creation
│   └── config.py        ← Load environment variables from .env
├── .env                 ← Secure DB credentials (e.g., DB URL)
├── requirements.txt     ← Dependencies list
└── README.md            ← Project documentation





## How `.env` + `dotenv` Works

`.env` file:

```env
DATABASE_URL=sqlite:///./users.db
```

In `database.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

* Loads `.env` values into memory
* Use `os.getenv("DATABASE_URL")` to fetch it
