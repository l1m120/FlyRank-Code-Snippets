from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

# --- STAGE 0: CREATE YOUR DATABASE ---
app = FastAPI()
DB_FILE = "tasks.db"

# helper function to establish db conection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        
        # 2. Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        
        # 3. Seed 3 tasks ONLY if count is 0
        if count == 0:
            example_tasks = [
                ("Buy groceries", 0),
                ("Finish FlyRank assignment", 0),
                ("Walk the dog", 1)
            ]
            # Use placeholders (?) for security!
            cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", example_tasks)
            conn.commit()

# Run this function right away when the script starts
init_db()

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def read_health():
    return {"status": "ok"}

# --- STAGE 1: READ FROM DATABASE ---

@app.get("/tasks")
def get_tasks():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        # Fetch all rows and convert them to standard Python dictionaries
        return [dict(row) for row in cursor.fetchall()]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Pass the task_id as a tuple: (task_id,)
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return dict(task)

# --- STAGE 2: CREATE NEW TASKS ---
class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Basic validation
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Insert the new task using placeholders (?)
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, 0))
        conn.commit()
        
        # SQLite automatically generated the ID, let's grab it
        new_id = cursor.lastrowid
        
        # Return the newly created task
        return {"id": new_id, "title": task.title, "done": False}

# --- STAGE 3: UPDATE AND DELETE ---
class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Run the UPDATE query
        cursor.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?", 
            (task.title, task.done, task_id)
        )
        conn.commit()
        
        # cursor.rowcount tells us how many rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
            
        return {"id": task_id, "title": task.title, "done": task.done}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
            
        return None # 204 No Content expects an empty body