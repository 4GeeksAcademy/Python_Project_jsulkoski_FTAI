"""Unit tests for the daily task manager (run with ``python3 test.py``)."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        app.todos.clear()
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.todo_file_patch = patch.object(app, "TODO_FILE", Path(self.temp_dir.name) / "todos.csv")
        self.todo_file_patch.start()

    def tearDown(self):
        self.todo_file_patch.stop()
        self.temp_dir.cleanup()
        self.redirect.__exit__(None, None, None)

    def test_add_and_print_tasks(self):
        app.add_one_task("Call the warehouse")
        app.add_one_task("Confirm delivery")
        app.print_list()
        self.assertEqual(app.todos, ["Call the warehouse", "Confirm delivery"])
        self.assertIn("1. Call the warehouse", self.output.getvalue())
        self.assertIn("2. Confirm delivery", self.output.getvalue())

    def test_delete_uses_one_based_position(self):
        app.todos.extend(["First", "Second", "Third"])
        self.assertTrue(app.delete_task("2"))
        self.assertEqual(app.todos, ["First", "Third"])
        self.assertFalse(app.delete_task("5"))

    def test_save_and_load_csv_tasks(self):
        app.todos.extend(["Task with, comma", 'Task with "quotes"', "Task on another shift"])
        app.save_todos()
        app.todos.clear()
        app.load_todos()
        self.assertEqual(app.todos, ["Task with, comma", 'Task with "quotes"', "Task on another shift"])

    def test_load_missing_file_clears_tasks(self):
        app.todos.append("Unsaved task")
        app.load_todos()
        self.assertEqual(app.todos, [])


if __name__ == "__main__":
    unittest.main()