# Task 1 - Basic REST API with CRUD Operations

## Objective

The objective of this task is to build a RESTful API that allows full CRUD (Create, Read, Update, Delete) operations on a "User" resource. This API will use in-memory storage (a Python dictionary) to simulate a database and implement validation using Pydantic models.

---

## What is a REST API?

A REST API (Representational State Transfer API) is a method of providing interoperability between computer systems on the internet. 

It is built on standard HTTP methods and is stateless. Each REST API exposes resources (data objects), and operations are performed on these resources via HTTP methods such as GET, POST, PUT, and DELETE.

### Key Characteristics:

* **Statelessness**: Each HTTP request from a client to server must contain all the information needed to understand and process the request.
* **Resource Identification**: Resources are identified using URIs (Uniform Resource Identifiers), such as `/users`.
* **Standard Methods**: REST uses standard HTTP verbs:

  * `GET`: Retrieve data
  * `POST`: Submit data
  * `PUT`: Update data
  * `DELETE`: Remove data
* **JSON Format**: Data is typically transferred in JSON format for ease of parsing and readability.

---

## System Architecture Overview

The basic architecture of the application can be described as follows:

```
┌─────────────────────────────────────────┐
│           Client Layer                  │
│     (Browser, Postman, Mobile App)      │
└─────────────────┬───────────────────────┘
                  │ HTTP Requests/Responses
┌─────────────────▼───────────────────────┐
│           Web Server Layer              │
│         (Uvicorn ASGI Server)           │
└─────────────────┬───────────────────────┘
                  │ ASGI Protocol
┌─────────────────▼───────────────────────┐
│        Application Layer                │
│           (FastAPI Framework)           │
└─────────────────┬───────────────────────┘
                  │ Python Function Calls
┌─────────────────▼───────────────────────┐
│         Business Logic Layer            │
│      (Route Handlers, Validation)       │
└─────────────────┬───────────────────────┘
                  │ Dictionary Operations
┌─────────────────▼───────────────────────┐
│          Data Storage Layer             │
│        (In-Memory Dictionary)           │
└─────────────────────────────────────────┘
```

---

## Technology Stack Explained

### 1. FastAPI - The Web Framework

**What is it?**
FastAPI is a modern Python framework used to create APIs quickly and efficiently. It is designed to be easy to use while also delivering high performance.

**Why use it?**

* Built-in data validation using Python type hints
* Automatic interactive documentation (Swagger UI and ReDoc)
* Fast, asynchronous I/O support

**How it works:**
FastAPI leverages type hints to create request body schemas, validates inputs using Pydantic, and routes requests using decorators like `@app.get()` or `@app.post()`.

### 2. Uvicorn - The ASGI Server

**What is it?**
Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server that serves FastAPI applications.

**WSGI vs ASGI Comparison:**

| Aspect | WSGI (e.g., Gunicorn) | ASGI (e.g., Uvicorn) |
|--------|----------------------|----------------------|
| Concurrency | Synchronous, thread-based | Asynchronous, event-loop based |
| Performance | Good for CPU-bound tasks | Excellent for I/O-bound tasks |
| WebSocket Support | No | Yes |
| HTTP/2 Support | Limited | Yes |
| Modern Features | Basic | Advanced (Server-Sent Events, etc.) |

**Why use it?**

* Enables asynchronous features of FastAPI
* Lightweight and very fast

```python
# Uvicorn manages the asyncio event loop
import asyncio
import uvicorn

# When you run: uvicorn main:app
# Uvicorn creates an event loop and runs your FastAPI app within it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# Your FastAPI app runs in this loop, handling multiple requests concurrently
```

**Command to run the app:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 4
```
- `main:app`: Module and application instance
- `--reload`: Watches for file changes (development only)
- `--host 0.0.0.0`: Accepts connections from any IP
- `--port 8000`: Server port
- `--workers 4`: Multiple worker processes (production)

### 3. Pydantic - For Data Validation

**What is it?**
Pydantic is a Python library used by FastAPI to define and validate data models.

**Why use it?**

* Automatically validates request payloads
* Ensures correct data types (e.g., `int`, `str`, `EmailStr`)
* Provides helpful error messages

**Example:**

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
```

### 4. UUID - Unique Identifier Generator

**What is it?**
UUID (Universally Unique Identifier) is a 128-bit number used to uniquely identify resources.

**Why use it?**

* Avoids ID collisions
* Safer than auto-incremented IDs

**Example:**

```python
import uuid

# UUID4 generates cryptographically random UUIDs
user_id = uuid.uuid4()
print(user_id)  # Output: f7ec0a28-6c34-11ee-8c99-0242ac120002

# Structure: 8-4-4-4-12 hexadecimal digits
# Total: 32 hexadecimal digits = 128 bits
# Probability of collision: 1 in 2^122 (virtually impossible)
```

### 5. Dictionary - In-Memory Storage

**What is it?**
Python’s built-in `dict` type is used as an in-memory storage mechanism.

**Why use it?**

* Simple and fast (constant-time lookup)
* Useful for prototyping APIs without a real database

**Example:**

```python
users = {}
users[user_id] = {"name": "Alice", "email": "alice@example.com", "age": 30}
```

---

## API Endpoints Implementation

### Create User (POST /users)

```python
@app.post("/users", status_code=201)
def create_user(user: User):
    user_id = str(uuid4())
    users[user_id] = user.dict()
    return {"id": user_id, **user.dict()}
```

### Retrieve All Users (GET /users)

```python
@app.get("/users")
def get_all_users():
    return [{"id": uid, **data} for uid, data in users.items()]
```

### Retrieve a Single User (GET /users/{user\_id})

```python
@app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **users[user_id]}
```

### Update a User (PUT /users/{user\_id})

```python
@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = user.dict()
    return {"id": user_id, **user.dict()}
```

### Delete a User (DELETE /users/{user\_id})

```python
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return
```

---

## Example Input and Validation Behavior

### Valid Request (POST /users)

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

### Invalid Request

```json
{
  "name": "",
  "email": "invalid-email",
  "age": -5
}
```

**Response:**

```json
{
  "detail": [
    {"loc": ["body", "email"], "msg": "value is not a valid email address"},
    {"loc": ["body", "age"], "msg": "ensure this value is greater than 0"}
  ]
}
```

---

## Running the Application

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn
```

### Step 2: Run the Server

```bash
uvicorn main:app --reload
```

### Step 3: Test Endpoints

Visit the interactive documentation at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
