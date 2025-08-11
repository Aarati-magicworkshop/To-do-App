import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
''')
conn.commit()

def add_task():
    
    task = input("Enter task: ")
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    print("Task added successfully!")

def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    if rows:
        print("\n")
        print("-"*19, "To-Do List" , "-"*19)
        print(f"{'ID':<5} {'Task':<30} {'Status':<10}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<30} {row[2]:<10}")
    else:
        print("No tasks found!")


def mark_completed():

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    if total_tasks == 0:
        print("No tasks available to mark as completed!")
        return
    
    view_tasks()
    task_id = input("Enter task ID to mark as completed: ")

    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cursor.fetchone() is None:
        print(f"Task ID {task_id} not found!")
        return

    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    print(f"Task ID {task_id} marked as completed!")


def update_task():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    if total_tasks == 0:
        print("No tasks available to update the task!")
        return
    
    view_tasks()
    task_id = input("Enter task ID to update: ")

    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cursor.fetchone() is None:
        print(f"Task ID {task_id} not found!")
        return

    new_task = input("Enter new task description: ")
    cursor.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, task_id))
    conn.commit()
    print(f"Task ID {task_id} updated!")

def delete_task():

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    if total_tasks == 0:
        print("No tasks available to delete the task!")
        return
    view_tasks()
    task_id = input("Enter task ID to delete: ")

    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if cursor.fetchone() is None:
        print(f"Task ID {task_id} not found!")
        return

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    print(f"Task ID {task_id} deleted!")

def table_del():

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    if total_tasks > 0:
        # print("No tasks available to delete the task!")
        # return
        cursor.execute("DROP TABLE IF EXISTS tasks")
        # conn.commit()

        print("To-do List tasks deleted successfully.")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        conn.commit()

    else:
        print("No tasks available to clear all the task!")
        return

# conn.close()


def main():
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. Update Task Details")
        print("5. Delete Task")
        print("6. Clear the to-do List")
        print("7. Exit")
        

        choice = input("Enter choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            update_task()
        elif choice == "5":
            delete_task()
        
        elif choice == "6":
            table_del()

        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print(" Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()




