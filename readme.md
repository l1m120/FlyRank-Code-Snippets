# FlyRank AI Internship - Weekly Submissions

## Week 2: FastAPI CRUD API

### 📖 What This Is
This repository contains a fully functional RESTful CRUD (Create, Read, Update, Delete) API built with **FastAPI** and Python 3.10+. It serves as the Stage 6 final submission for the FlyRank AI backend engineering assignment. The API utilizes an in-memory data store to track and manage a collection of tasks. It strictly enforces standard HTTP methods and proper status code handling (200 OK, 201 Created, 204 No Content, 400 Bad Request, and 404 Not Found).

### 🚀 How to Install & Run
Ensure you have Python 3.10+ installed. Open your terminal (or PowerShell) in the project directory and run the following combined command to install the required dependencies and launch the local server:

```bash
pip install fastapi uvicorn && python -m uvicorn CRUD_API:app --reload
```
*Note: The server will be hosted locally. You can access the API at `http://localhost:8000` and the interactive documentation at `http://localhost:8000/docs`.*

### 🚏 API Endpoints Table

| Method | Endpoint | Description | Expected Status Codes |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Root welcome message | `200 OK` |
| **GET** | `/health` | API system health check | `200 OK` |
| **GET** | `/tasks` | Retrieve a list of all current tasks | `200 OK` |
| **GET** | `/tasks/{task_id}` | Retrieve a specific task by its unique ID | `200 OK`, `404 Not Found` |
| **POST** | `/tasks` | Create and store a new task | `201 Created`, `400 Bad Request` |
| **PUT** | `/tasks/{task_id}` | Fully update an existing task by ID | `200 OK`, `404 Not Found` |
| **DELETE** | `/tasks/{task_id}` | Remove a task from the data store | `204 No Content`, `404 Not Found` |

## How to Install & Run

Ensure you have FastAPI and Uvicorn installed (`pip install fastapi uvicorn`), then start the server with this command:

```bash
python -m uvicorn CRUD_API:app --reload

### 💻 Sample `curl` Output
Here is a verified response from testing the `/health` endpoint directly from the Windows PowerShell terminal:

```bash
curl.exe -i http://localhost:8000/health
```

```http
HTTP/1.1 200 OK
date: Fri, 31 Jul 2026 05:18:49 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}
```

### 📸 Interactive Documentation (Swagger UI)
FastAPI automatically generates interactive OpenAPI documentation based on the Python type hints. Below is the Swagger UI capturing all 7 active endpoints running successfully:

![Swagger UI Screenshot](week-2/FastAPI_output.png)

## Week 3: SQLite Database Integration

### 🗄️ Why SQLite?
For Week 3, the in-memory data store was replaced with a real database. SQLite was chosen because it requires absolutely zero manual setup, operates entirely out of a single local file, and provides immediate data persistence so that records survive server restarts.

### 💾 Storage Details & Auto-Creation
The database lives in a local file named `tasks.db` in the root directory.

* **Zero-Setup Cloning:** The codebase is designed to automatically create the `tasks.db` file, generate the `tasks` table, and seed it with three example tasks the very first time the application runs. There is no manual database configuration required.
* **Git-Ignored:** The `tasks.db` file is added to `.gitignore` so that anyone cloning this repository starts with a completely fresh, empty database.

### 🚀 Running the Project
You can start the project using a single command. Running this on a fresh clone will automatically initialize the database and seed the data within seconds:

```bash
python -m uvicorn CRUD_API:app --reload
```

After running the project, execute the GET /tasks request to return the available tasks 

![Get Tasks Screenshot](week-3-1/get_task_output.png)

### 🔍 Example SQL Query
During Stage 4 testing, direct queries were executed against the database using DB Browser for SQLite. Here is an example query used to count the total number of tasks currently stored to ensure seeding was successful:

``` bash
SELECT COUNT(*) FROM tasks;
```

### 📸 Database Verification (DB Browser)
Below is a screenshot of the tasks.db file opened directly in DB Browser for SQLite, proving the data persists correctly outside of the API:

![Get Tasks Screenshot](week-3-1/SQL_output.png)

## Week 3: Containerized Task API

### 📌 What This Is

This is a RESTful CRUD API built with **Python** and **FastAPI**, backed by a real **PostgreSQL** database. Both the application and the database run entirely inside **Docker containers** and are orchestrated using **Docker Compose**.

By utilizing **Docker volumes**, the PostgreSQL database persists its data even if the containers are stopped, removed, or recreated.

---

### 🚀 Features

- RESTful CRUD API built with FastAPI
- PostgreSQL database running in Docker
- Docker Compose for multi-container orchestration
- Persistent database storage using Docker volumes
- Automatic database initialization and sample data seeding
- Interactive Swagger API documentation

---

### 🛠️ Tech Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- SQLAlchemy
- Pydantic

---

### ⚡ Quickstart

#### 1. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

#### 2. Start the application

Run both the API and PostgreSQL containers:

```bash
docker compose up
```

> **Note**
>
> During the first startup, the API will automatically:
>
> - Connect to PostgreSQL
> - Create the `tasks` table
> - Seed the database with three example tasks

---

### 🌐 Access the Application

API Base URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

### API Endpoints

| Method | Endpoint | Description | Status Codes |
|---------|----------|-------------|--------------|
| **GET** | `/tasks` | Retrieve all tasks | `200` |
| **GET** | `/tasks/{id}` | Retrieve a task by ID | `200`, `404` |
| **POST** | `/tasks` | Create a new task | `201`, `400` |
| **PUT** | `/tasks/{id}` | Update a task's title or `done` status | `200`, `400`, `404` |
| **DELETE** | `/tasks/{id}` | Delete a task | `204`, `404` |

---

### Example Request

Retrieve all tasks using `curl`:

```bash
curl.exe -i http://localhost:8000/tasks
```

### Example Output

```text
HTTP/1.1 200 OK
date: Fri, 07 Aug 2026 05:58:17 GMT
server: uvicorn
content-length: 145
content-type: application/json

[{"id":1,"title":"Learn Docker","done":true},{"id":2,"title":"Connect Postgres","done":false},{"id":3,"title":"Write Compose File","done":false}]
```

---

### Database Persistence Proof

Below is proof that the PostgreSQL database is running inside Docker and that data is successfully persisted using Docker volumes.


![DB Screenshot](week-3-2/db_output.png)

---

## Week 4: Secured Task API — Authentication & Authorization

### 📌 What This Is

This is a **secure RESTful API** built with **Python and FastAPI**, featuring a complete authentication and authorization system backed by **Supabase**.

The project demonstrates modern backend security practices by delegating identity management and cryptographic operations, such as password hashing and JWT signing, to a trusted **Identity Provider (Supabase)**.

The application allows users to:

* Create an account
* Log in and receive a JSON Web Token (JWT)
* Use the JWT as a Bearer token to access protected routes
* Log out of their active session
* Access protected user-specific data
* Reuse a centralized authentication dependency across multiple protected endpoints

The project also includes a reusable authentication guard that verifies the user's JWT through Supabase before allowing access to restricted resources.

---

### 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **Supabase**
* **Pydantic**
* **Uvicorn**
* **python-dotenv**
* **JWT Authentication**
* **Swagger / OpenAPI**

---

### 🚀 Setup & Quickstart

#### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

#### 2. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

> ⚠️ **Important:** Never commit your real `.env` file to GitHub.

Open `.env` and fill in your Supabase project credentials:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

Make sure your environment variable names match those used in your application.

---

#### 3. Install Dependencies

Install the required Python packages:

```bash
pip install fastapi uvicorn supabase python-dotenv pydantic
```

Alternatively, if the project includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

#### 4. Start the FastAPI Server

Run the development server:

```bash
python -m uvicorn main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

---

### 📚 API Documentation

FastAPI automatically generates interactive API documentation.

#### Swagger UI

Open:

```text
http://localhost:8000/docs
```

#### ReDoc

Open:

```text
http://localhost:8000/redoc
```

Swagger UI allows you to directly test the API endpoints from your browser.

---

### 🔐 Authentication Flow

The authentication process follows this general flow:

```text
┌──────────────┐
│    Client    │
└──────┬───────┘
       │
       │ 1. Sign Up / Login
       ▼
┌──────────────┐
│   FastAPI    │
└──────┬───────┘
       │
       │ 2. Authentication Request
       ▼
┌──────────────┐
│   Supabase   │
│     Auth     │
└──────┬───────┘
       │
       │ 3. JWT Access Token
       ▼
┌──────────────┐
│    Client    │
└──────┬───────┘
       │
       │ 4. Bearer Token
       ▼
┌──────────────┐
│   Protected  │
│    Route     │
└──────┬───────┘
       │
       │ 5. Verify JWT
       ▼
┌──────────────┐
│   Supabase   │
│ Token Verify │
└──────┬───────┘
       │
       │ 6. Authorized
       ▼
┌──────────────┐
│ Protected    │
│    Data      │
└──────────────┘
```

### How It Works

1. The user registers through `/auth/signup`.
2. The user logs in through `/auth/login`.
3. Supabase authenticates the user and returns a JWT access token.
4. The client stores the access token.
5. The client sends the token with protected requests:

```http
Authorization: Bearer <access_token>
```

6. FastAPI extracts the Bearer token.
7. The authentication dependency verifies the token through Supabase.
8. If the token is valid, access to the protected endpoint is granted.
9. If the token is invalid or missing, the request is rejected.

---

### 🔗 API Endpoints

| Method | Endpoint               | Description                                            | Requires Auth? |
| ------ | ---------------------- | ------------------------------------------------------ | -------------- |
| `POST` | `/auth/signup`         | Register a new user account with email and password    | ❌ No           |
| `POST` | `/auth/login`          | Authenticate a user and receive a JWT (`access_token`) | ❌ No           |
| `POST` | `/auth/logout`         | End the user's active session                          | ✅ Yes          |
| `GET`  | `/public/info`         | Retrieve generic public information                    | ❌ No           |
| `GET`  | `/protected/profile`   | Retrieve secure profile data                           | ✅ Yes          |
| `GET`  | `/protected/dashboard` | Access an additional protected route                   | ✅ Yes          |

> 🔒 Protected routes require the JWT to be included in the request header:
>
> ```http
> Authorization: Bearer <token>
> ```

---

### 🧪 Example Authentication Request

### Sign Up

```http
POST /auth/signup
Content-Type: application/json
```

Example request body:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

---

### Login

```http
POST /auth/login
Content-Type: application/json
```

Example request body:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

A successful login returns an access token similar to:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Accessing a Protected Endpoint

Include the returned JWT in the `Authorization` header:

```http
GET /protected/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

### 🔑 Swagger UI & Bearer Authentication

FastAPI's built-in Swagger UI has been configured with an `HTTPBearer` security scheme.

This adds an **Authorize 🔒** button to the Swagger documentation.

Instead of manually adding the JWT to every request, you can:

1. Log in through `/auth/login`.
2. Copy the returned `access_token`.
3. Click **Authorize** in Swagger UI.
4. Enter the token.
5. Click **Authorize**.
6. Test protected endpoints directly from the browser.

This makes it much easier to demonstrate and test the authentication system.

### Swagger UI Preview

![Swagger UI](week-4/swagger_output.png)`

