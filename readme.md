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

![Swagger UI Screenshot](./FastAPI_output.png)