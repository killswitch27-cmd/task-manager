"""Executable Lab 4 regression tests for the reconstructed task requirements."""
import json

import app.tasks as task_module
from app.tasks import (
    add_task,
    average_priority,
    complete_task,
    find_task_by_title,
    get_pending_tasks,
    load_tasks,
    remove_task,
    save_tasks,
)


def test_tc_01_load_missing_file(tmp_path, monkeypatch):
    task_file = tmp_path / "missing.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(task_file))

    assert load_tasks() == []


def test_tc_02_load_existing_file(tmp_path, monkeypatch):
    task_file = tmp_path / "tasks.json"
    expected = [{"id": 1, "title": "Study", "priority": 2,
                 "tags": ["school"], "done": False}]
    task_file.write_text(json.dumps(expected), encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(task_file))

    assert load_tasks() == expected


def test_tc_03_save_and_reload(tmp_path, monkeypatch):
    task_file = tmp_path / "tasks.json"
    tasks = [
        {"id": 1, "title": "Study", "priority": 1, "tags": [], "done": False},
        {"id": 2, "title": "Exercise", "priority": 3,
         "tags": ["health"], "done": True},
    ]
    monkeypatch.setattr(task_module, "TASKS_FILE", str(task_file))

    save_tasks(tasks)

    assert load_tasks() == tasks


def test_tc_04_add_task_defaults():
    tasks = [{"id": 1, "title": "Existing", "priority": 2,
              "tags": [], "done": False}]

    task = add_task(tasks, "New")

    assert task == {
        "id": 2,
        "title": "New",
        "priority": 1,
        "tags": [],
        "done": False,
    }
    assert tasks[-1] is task


def test_tc_05_add_task_custom_fields():
    tags = ["work"]
    tasks = []

    task = add_task(tasks, "Report", priority=3, tags=tags)

    assert task["priority"] == 3
    assert task["tags"] == ["work"]
    assert task["tags"] is not tags


def test_tc_06_complete_known_task():
    tasks = [
        {"id": 1, "title": "A", "done": False},
        {"id": 2, "title": "B", "done": False},
    ]

    assert complete_task(tasks, 2) is True
    assert tasks == [
        {"id": 1, "title": "A", "done": False},
        {"id": 2, "title": "B", "done": True},
    ]


def test_tc_07_complete_unknown_task():
    tasks = [{"id": 1, "title": "A", "done": False}]
    original = [task.copy() for task in tasks]

    assert complete_task(tasks, 99) is False
    assert tasks == original


def test_tc_08_pending_tasks_include_first_and_exclude_done():
    first = {"id": 1, "title": "First", "done": False}
    completed = {"id": 2, "title": "Done", "done": True}
    missing_done = {"id": 3, "title": "Legacy"}

    assert get_pending_tasks([first, completed, missing_done]) == [
        first,
        missing_done,
    ]


def test_tc_09_average_priority_nonempty():
    tasks = [
        {"id": 1, "priority": 1},
        {"id": 2, "priority": 2},
        {"id": 3, "priority": 3},
    ]

    assert average_priority(tasks) == 2


def test_tc_10_average_priority_empty():
    assert average_priority([]) == 0


def test_tc_11_find_matching_title():
    match = {"id": 2, "title": "Exercise"}

    assert find_task_by_title(
        [{"id": 1, "title": "Study"}, match],
        "Exercise",
    ) is match


def test_tc_12_find_missing_title():
    assert find_task_by_title([{"id": 1, "title": "Study"}], "Unknown") is None


def test_tc_13_find_first_duplicate_title():
    first = {"id": 1, "title": "Study"}
    second = {"id": 2, "title": "Study"}

    assert find_task_by_title([first, second], "Study") is first


def test_tc_14_remove_known_task():
    tasks = [
        {"id": 1, "title": "A"},
        {"id": 2, "title": "B"},
        {"id": 3, "title": "C"},
    ]

    remove_task(tasks, 2)

    assert tasks == [{"id": 1, "title": "A"}, {"id": 3, "title": "C"}]


def test_tc_15_remove_unknown_task():
    tasks = [{"id": 1, "title": "A"}]
    original = [task.copy() for task in tasks]

    remove_task(tasks, 99)

    assert tasks == original
