"""A small command-line task manager for operations follow-ups."""

import csv
from pathlib import Path


TODO_FILE = Path("todos.csv")
todos = []
# ``tasks`` is a convenient alias for callers that prefer that name.
tasks = todos


def add_one_task(title):
    """Append a task title to the in-memory list."""
    title = title.strip()
    if not title:
        print("Task title cannot be empty.")
        return False
    todos.append(title)
    print(f'Added: {title}')
    return True


def print_list():
    """Print pending tasks with 1-based positions for deletion."""
    if not todos:
        print("No pending tasks.")
        return

    for position, title in enumerate(todos, start=1):
        print(f"{position}. {title}")


def delete_task(number_to_delete):
    """Delete the task at a 1-based list position."""
    try:
        position = int(number_to_delete)
    except (TypeError, ValueError):
        print("Please enter a valid task number.")
        return False

    if position < 1 or position > len(todos):
        print("That task number is not in the list.")
        return False

    removed = todos.pop(position - 1)
    print(f"Deleted: {removed}")
    return True


def save_todos():
    """Save all pending tasks to todos.csv, one CSV row per task."""
    with TODO_FILE.open("w", newline="", encoding="utf-8") as todo_file:
        writer = csv.writer(todo_file)
        writer.writerows([title] for title in todos)
    print(f"Saved {len(todos)} task(s) to {TODO_FILE}.")


def load_todos():
    """Load pending tasks from todos.csv, replacing the current list."""
    try:
        with TODO_FILE.open("r", newline="", encoding="utf-8") as todo_file:
            loaded = [row[0] for row in csv.reader(todo_file) if row and row[0]]
    except FileNotFoundError:
        todos.clear()
        print(f"No saved tasks found ({TODO_FILE}).")
        return

    todos[:] = loaded
    print(f"Loaded {len(todos)} task(s) from {TODO_FILE}.")


def main():
    """Run the interactive command-line task manager."""
    actions = {
        "1": "Add a task",
        "2": "List tasks",
        "3": "Delete a task",
        "4": "Save tasks",
        "5": "Load tasks",
        "0": "Exit",
    }

    print("Daily Task Manager")
    while True:
        print("\n".join(f"{number}. {label}" for number, label in actions.items()))
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_one_task(input("Task title: "))
        elif choice == "2":
            print_list()
        elif choice == "3":
            print_list()
            if todos:
                delete_task(input("Task number to delete: "))
        elif choice == "4":
            save_todos()
        elif choice == "5":
            load_todos()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose one of the listed options.")


if __name__ == "__main__":
    main()