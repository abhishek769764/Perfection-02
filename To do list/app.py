from flask import Flask, render_template, request, redirect, url_for
import random
import os
from datetime import date

app = Flask(__name__)

TASKS_FILE = "tasks.txt"
DATE_FILE = "date.txt"

def load_tasks():
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("||")
                if len(parts) == 2:
                    task_text, completed = parts
                    tasks.append({"text": task_text, "completed": completed == "1"})
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            completed_flag = "1" if task["completed"] else "0"
            f.write(f"{task['text']}||{completed_flag}\n")

def load_last_date():
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_today_date():
    today_str = str(date.today())
    with open(DATE_FILE, "w") as f:
        f.write(today_str)

def reset_if_new_day():
    last_date = load_last_date()
    today_str = str(date.today())
    if last_date != today_str:
        save_tasks([])
        save_today_date()

@app.route("/", methods=["GET", "POST"])
def home():
    reset_if_new_day()
    tasks = load_tasks()

    messages = [
        "Let's get things done today! 💪",
        "Rise and grind! What’s on your list?",
        "Conquer your tasks one by one!",
        "Time to crush your goals! 🚀"
    ]
    greeting = random.choice(messages)

    if request.method == "POST":
        if "tasks" in request.form:
            new_tasks = request.form.getlist("tasks")
            for task in new_tasks:
                if task.strip():
                    tasks.append({"text": task.strip(), "completed": False})
        if "completed" in request.form:
            completed_indexes = list(map(int, request.form.getlist("completed")))
            for i, task in enumerate(tasks):
                task["completed"] = i in completed_indexes
        save_tasks(tasks)
        return redirect(url_for("home"))

    completed_count = sum(1 for t in tasks if t["completed"])
    total_tasks = len(tasks)

    return render_template("index.html", greeting=greeting, tasks=tasks,
                           completed_count=completed_count, total_tasks=total_tasks)

@app.route("/delete/<int:index>")
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
  
