import os
import psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import HTTPException

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