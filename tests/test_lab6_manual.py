
import json

import app.tasks as task_module
from app.tasks import load_tasks, save_tasks, find_task_by_title


def test_load_tasks_existing_file(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    expected = [{"id": 1, "title": "Study", "priority": 1,
                 "tags": [], "done": False}]
    file_path.write_text(json.dumps(expected), encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(file_path))

    assert load_tasks() == expected


def test_load_tasks_missing_file(tmp_path, monkeypatch):
    file_path = tmp_path / "missing.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(file_path))

    assert load_tasks() == []


def test_save_tasks_persists_data(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(file_path))
    tasks = [{"id": 1, "title": "Study", "priority": 2,
              "tags": ["school"], "done": False}]

    save_tasks(tasks)

    saved = json.loads(file_path.read_text(encoding="utf-8"))
    assert saved == tasks


def test_find_task_by_title_returns_correct_task():
    first = {"id": 1, "title": "Study"}
    second = {"id": 2, "title": "Exercise"}

    assert find_task_by_title([first, second], "Exercise") == second


def test_find_task_by_title_missing_title_returns_none():
    tasks = [{"id": 1, "title": "Study"}]

    assert find_task_by_title(tasks, "Unknown") is None


def test_find_task_by_title_duplicate_returns_first_match():
    first = {"id": 1, "title": "Study"}
    second = {"id": 2, "title": "Study"}

    assert find_task_by_title([first, second], "Study") is first
