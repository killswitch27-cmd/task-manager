
import json

import pytest

import app.tasks as task_module
from app.tasks import load_tasks, save_tasks, find_task_by_title


def test_load_tasks_reads_existing_file(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    expected_tasks = [
        {"id": 1, "title": "Task A", "priority": 1, "tags": [], "done": False}
    ]
    tasks_file.write_text(json.dumps(expected_tasks), encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = load_tasks()

    assert result == expected_tasks


def test_load_tasks_returns_empty_list_when_file_missing(tmp_path, monkeypatch):
    tasks_file = tmp_path / "missing_tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))

    result = load_tasks()

    assert result == []


def test_save_tasks_writes_data_to_file(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))
    tasks = [
        {"id": 1, "title": "Task A", "priority": 2, "tags": ["work"], "done": False}
    ]

    save_tasks(tasks)

    assert tasks_file.exists()
    assert json.loads(tasks_file.read_text(encoding="utf-8")) == tasks


def test_save_tasks_can_be_loaded_again(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))
    tasks = [
        {"id": 1, "title": "Task A", "priority": 1, "tags": [], "done": False},
        {"id": 2, "title": "Task B", "priority": 3, "tags": ["urgent"], "done": True},
    ]

    save_tasks(tasks)
    result = load_tasks()

    assert result == tasks


def test_find_task_by_title_returns_matching_task():
    tasks = [
        {"id": 1, "title": "Task A"},
        {"id": 2, "title": "Task B"},
    ]

    result = find_task_by_title(tasks, "Task B")

    assert result == tasks[1]


def test_find_task_by_title_returns_none_when_title_missing():
    tasks = [{"id": 1, "title": "Task A"}]

    result = find_task_by_title(tasks, "Task C")

    assert result is None


def test_find_task_by_title_returns_first_duplicate():
    first_task = {"id": 1, "title": "Task A"}
    second_task = {"id": 2, "title": "Task A"}
    tasks = [first_task, second_task]

    result = find_task_by_title(tasks, "Task A")

    assert result is first_task
