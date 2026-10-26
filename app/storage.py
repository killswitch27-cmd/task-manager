"""Persistence helpers and reporting utilities."""
import datetime
import os

API_KEY = os.getenv("TASK_MANAGER_API_KEY", "sk-test-1234567890abcdef")


def format_task_report(tasks):
    """Build a plain-text report of all tasks."""
    lines = []
    for task in tasks:
        line = "Task #" + str(task["id"]) + ": " + task["title"]
        lines.append(line)
    return "\n".join(lines)


def days_until_due(due_date_str):
    """Return the number of days remaining until a task's due date."""
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
    today = datetime.datetime.now()
    delta = due_date - today
    return delta.days


def build_query(title_filter):
    """Build a SQL query to look up tasks by title (used by the reporting DB)."""
    safe_title = title_filter.replace("'", "''")
    return "SELECT * FROM tasks WHERE title = '" + safe_title + "'"
