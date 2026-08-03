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

# --- STAGE 2: In-Memory Data and Read Endpoints ---
# FlyRank wants an id (number), title (text), and done (boolean).
class TaskCreate(BaseModel):
    title: str
    done: bool = False

class Task(TaskCreate):
    id: int

# Initialize with 3 sample tasks
tasks: List[Task] = [
    Task(id=1, title="Watch the W2 lecture", done=True),
    Task(id=2, title="Read MDN: How the web works", done=False),
    Task(id=3, title="Buy milk", done=False)
]

# Provide the next available ID
def get_next_id():
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    # Stage 2: Return 404 with JSON error if unknown
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# --- STAGE 3: Create ---
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    # Stage 3: Empty string validation (FastAPI/Pydantic automatically handles missing fields)
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required")
        
    new_task = Task(id=get_next_id(), title=task.title, done=task.done)
    tasks.append(new_task)
    return new_task

# --- STAGE 4: Update & Delete ---
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskCreate):
    if not task_update.title.strip():
        raise HTTPException(status_code=400, detail="title is required")
        
    for task in tasks:
        if task.id == task_id:
            task.title = task_update.title
            task.done = task_update.done
            return task
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# --- STAGE 5: Swagger UI is automatically available at /docs ---