from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

#instance 
app = FastAPI(title="To-Do Application")

# databse conection
def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    ''')
    conn.commit()

# plydantic models for validation
class TaskCreate(BaseModel):
    task: str

class TaskUpdate(BaseModel):
    task: str


@app.post("/tasks")
def add_task(task: TaskCreate):
# def add_task(task:str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task) VALUES (?)", (task.task,))
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return {"message": "Task added successfully!", "task_id": task_id}

@app.get("/tasks")
def view_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return [dict(row) for row in tasks]


@app.put("/tasks/{task_id}/complete")
def mark_completed(task_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    tot_task=cur.execute("SELECT COUNT(*) FROM tasks").fetchall()
    if tot_task[0][0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="No tasks available to mark as completed")
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cur.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": f"Task ID {task_id} marked as completed"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_task: TaskUpdate):
    conn = get_db_connection()
    cur = conn.cursor()
    tot_task = cur.execute("SELECT COUNT(*) FROM tasks").fetchall()
    if tot_task[0][0] == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="No tasks available to update")
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cur.execute("UPDATE tasks SET task=? WHERE id=?", (new_task.task, task_id))
    conn.commit()
    # cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    # updated_task = cur.fetchone()
    conn.close()
    return {"message": f"Task ID {task_id} updated"}
    # return {
    #     "id": updated_task[0],
    #     "task": updated_task[1],
    #     "status": updated_task[2]
    # }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    tot_task = cur.execute("SELECT COUNT(*) FROM tasks").fetchall()
    if tot_task[0][0] == 0:     
        conn.close()
        raise HTTPException(status_code=404, detail="No tasks available to delete")
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cur.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": f"Task ID {task_id} deleted"}

@app.delete("/tasks")
def clear_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    tot_task = cur.execute("SELECT COUNT(*) FROM tasks").fetchall()
    if tot_task[0][0] == 0: 
        conn.close()
        raise HTTPException(status_code=404, detail="No tasks available to delete")
    cur.execute("DELETE FROM tasks")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
    conn.commit()
    conn.close()
    return {"message": "All tasks deleted and ID counter reset"}
