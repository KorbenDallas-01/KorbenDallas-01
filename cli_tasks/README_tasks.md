# ✅ CLI Task Manager

A simple command-line task manager that stores tasks locally in a JSON file.

---

## Features

- Add tasks with a title and priority level (low / medium / high)
- List all tasks, or filter by done / pending
- Mark tasks as complete
- Delete tasks
- Persistent storage via a local `tasks.json` file

---

## Usage

```bash
# Add a task
python tasks.py add "Buy groceries"
python tasks.py add "Finish report" --priority high

# List all tasks
python tasks.py list

# List only pending tasks
python tasks.py list --filter pending

# Mark task #2 as done
python tasks.py complete 2

# Delete task #1
python tasks.py delete 1
```

---

## Example output

```
ID    Status     Priority   Title                               Created
---------------------------------------------------------------------------
1     ⏳ pending  high       Finish report                       2024-11-01 09:15
2     ✅ done     medium     Buy groceries                       2024-11-01 09:16
```

---

## Known issues / future improvements

- Task IDs can collide after deletions (to be fixed)
- No support for editing a task title after creation
- No due dates yet

---

## Requirements

No external dependencies. Requires Python 3.8+.
