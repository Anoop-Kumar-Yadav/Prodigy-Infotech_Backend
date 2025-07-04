
# JWT Authentication API – FastAPI

This is Task 3 of my internship at **Prodigy InfoTech**. It implements **JWT-based Authentication** and **Role-Based Authorization** using FastAPI, with secure password handling and protected API routes.

---

## What I Learned (Theoretical Concepts)

### Authentication vs Authorization

* **Authentication**: Confirms the user’s identity (e.g., login with email and password).
* **Authorization**: Determines what actions a user can perform based on their role (e.g., only admin can access `/admin`).

### What is JWT (JSON Web Token)?

* A compact, URL-safe way of representing claims.
* Contains 3 parts:

  1. **Header** (algorithm info)
  2. **Payload** (data like user ID, role, expiry)
  3. **Signature** (proves token hasn't been tampered)
* Sent via HTTP header: `Authorization: Bearer <token>`
* Stateless: no session storage required

### How JWT Works:

1. User logs in with credentials.
2. Server verifies credentials.
3. Server generates a token and sends it back.
4. Token is used to access protected routes.

### Role-Based Access Control (RBAC)

* Assigns roles to users: `user`, `admin`
* Protects routes like `/admin` using conditional logic.

### Bcrypt for Password Security

* One-way hash algorithm for storing passwords.
* Adds a **salt** to make every hash unique.
* Verifies user passwords by comparing the hashed version.

### FastAPI + Python-Jose + Bcrypt

* **FastAPI**: Framework used to build APIs.
* **python-jose**: Used to encode and decode JWT.
* **passlib\[bcrypt]**: Used to hash passwords securely.
* **dotenv**: Used to load secret config from `.env` file.
* **SQLAlchemy**: ORM for interacting with SQLite database.

---

## Features Implemented

* User Registration (`/register`)
* User Login with JWT (`/login`)
* Password hashing with `bcrypt`
* Protected routes using Bearer token
* Role-based access control (`user`, `admin`)
* SQLite database via SQLAlchemy
* Environment-specific configurations with `.env`

---

## Tech Stack

* **FastAPI** – API framework
* **SQLAlchemy** – ORM for database access
* **python-jose** – JWT creation and validation
* **passlib\[bcrypt]** – Password hashing
* **dotenv** – Load environment variables
* **SQLite** – Lightweight relational DB

---


## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/task3_auth_api.git
cd task3_auth_api
```


### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` File

```env
DATABASE_URL=sqlite:///./users.db
SECRET_KEY=your_very_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the App

```bash
uvicorn app.main:app --reload
```

---

## API Testing

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

### Auth Flow

1. **Register:** `POST /register`
2. **Login:** `POST /login` → receive JWT
3. **Use JWT:** Add header `Authorization: Bearer <token>` to access:

   * `GET /me` (any authenticated user)
   * `GET /admin` (admin-only)

---

## Role-Based Access Demo

| User  | Can Access `/me` | Can Access `/admin` |
| ----- | ---------------- | ------------------- |
| user  | Yes              | No (Forbidden)      |
| admin | Yes              | Yes                 |

---

## Sample User JSON

```json
{
  "name": "Anoop",
  "email": "anoop@example.com",
  "password": "securepass123",
  "age": 22,
  "role": "admin"
}
```
