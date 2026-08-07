import os
import psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import Response

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

@app.on_event("startup")
def startup():
    with get_db() as conn:
        with conn.cursor() as cur:
            # Create table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE
                )
            """)
            # Seed three example tasks only if empty
            cur.execute("SELECT COUNT(*) AS count FROM tasks")
            if cur.fetchone()['count'] == 0:
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Learn Docker", True))
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Connect Postgres", False))
                cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Write Compose File", False))
        conn.commit()

@app.get("/tasks")
def get_tasks():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks")
            return cur.fetchall()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cur.fetchone()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task

class TaskCreate(BaseModel):
    title: str
    done: bool = False

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
                (task.title, task.done)
            )
            new_task = cur.fetchone()
        conn.commit()
        return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
                (task.title, task.done, task_id)
            )
            updated_task = cur.fetchone()
            if not updated_task:
                raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
        return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
            deleted = cur.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Task not found")
        conn.commit()
        return Response(status_code=204)