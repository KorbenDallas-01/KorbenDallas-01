"""
tasks.py
--------
A simple command-line task manager. Tasks are saved to a JSON file.

Usage:
    python tasks.py add "Buy groceries"
    python tasks.py add "Read a book" --priority high
    python tasks.py list
    python tasks.py list --filter done
    python tasks.py complete 2
    python tasks.py delete 1
"""

import argparse
import json
import os
from datetime import datetime


TASKS_FILE = "tasks.json"


# ── File I/O ───────────────────────────────────────────────────────────────────

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)   # BUG: missing indent= so the JSON file is one ugly line,
                               # making it hard to read or edit manually


# ── Task operations ────────────────────────────────────────────────────────────

def add_task(title: str, priority: str = "medium") -> None:
    tasks = load_tasks()

    # BUG: IDs are assigned based on list length, so if you delete task #3
    # from a 5-task list, the next new task also gets ID 3 → duplicate IDs
    new_id = len(tasks) + 1

    task = {
        "id": new_id,
        "title": title,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task #{new_id}: '{title}' [{priority}]")


def list_tasks(filter_by: str = "all") -> None:
    tasks = load_tasks()

    if len(tasks) == 0:
        print("No tasks found.")
        return

    # BUG: filter comparison is case-sensitive — "Done" won't match "done",
    # and invalid filter values silently show nothing instead of an error
    if filter_by == "done":
        tasks = [t for t in tasks if t["done"] == True]
    elif filter_by == "pending":
        tasks = [t for t in tasks if t["done"] == False]

    print(f"\n{'ID':<5} {'Status':<10} {'Priority':<10} {'Title':<35} {'Created'}")
    print("-" * 75)

    for task in tasks:
        status = "✅ done" if task["done"] else "⏳ pending"
        print(
            f"{task['id']:<5} {status:<10} {task['priority']:<10} "
            f"{task['title']:<35} {task['created_at']}"
        )
    print()


def complete_task(task_id: int) -> None:
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task #{task_id} is already marked as done.")
                return
            task["done"] = True
            save_tasks(tasks)
            print(f"✅ Task #{task_id} marked as complete.")
            return

    # BUG: no error message here — if the ID doesn't exist, the function
    # just silently returns with no output, confusing the user
    return


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    original_count = len(tasks)

    tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == original_count:
        print(f"❌ No task with ID #{task_id} found.")
        return

    save_tasks(tasks)
    print(f"🗑️  Task #{task_id} deleted.")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", type=str, help="Task description")
    add_p.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)",
    )

    # list
    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument(
        "--filter",
        dest="filter_by",
        choices=["all", "done", "pending"],
        default="all",
        help="Filter tasks (default: all)",
    )

    # complete
    complete_p = subparsers.add_parser("complete", help="Mark a task as done")
    complete_p.add_argument("id", type=int, help="Task ID to mark complete")

    # delete
    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id", type=int, help="Task ID to delete")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "add":
        add_task(args.title, args.priority)
    elif args.command == "list":
        list_tasks(args.filter_by)
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)


if __name__ == "__main__":
    main()
