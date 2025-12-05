from todo_cli.models import Task
from todo_cli.storage import load_tasks, next_id, save_tasks


def test_save_and_load(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [Task(id=1, title="Hello")]
    save_tasks(tasks, path)
    loaded = load_tasks(path)
    assert len(loaded) == 1
    assert loaded[0].title == "Hello"


def test_next_id():
    tasks = [Task(id=1, title="A"), Task(id=2, title="B")]
    assert next_id(tasks) == 3
