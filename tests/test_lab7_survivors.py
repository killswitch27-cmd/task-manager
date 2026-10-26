import builtins

import app.tasks as task_module
from app.tasks import load_tasks, save_tasks


def test_load_tasks_uses_explicit_read_mode_and_utf8(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))
    real_open = builtins.open
    open_calls = []

    def recording_open(*args, **kwargs):
        open_calls.append((args, kwargs.copy()))
        return real_open(*args, **kwargs)

    monkeypatch.setattr(builtins, "open", recording_open)

    assert load_tasks() == []
    assert open_calls[0][0] == (str(tasks_file), "r")
    assert open_calls[0][1]["encoding"] == "utf-8"


def test_save_tasks_uses_explicit_write_mode_and_utf8(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(task_module, "TASKS_FILE", str(tasks_file))
    real_open = builtins.open
    open_calls = []

    def recording_open(*args, **kwargs):
        open_calls.append((args, kwargs.copy()))
        return real_open(*args, **kwargs)

    monkeypatch.setattr(builtins, "open", recording_open)

    save_tasks([{"id": 1, "title": "Study"}])

    assert open_calls[0][0] == (str(tasks_file), "w")
    assert open_calls[0][1]["encoding"] == "utf-8"
