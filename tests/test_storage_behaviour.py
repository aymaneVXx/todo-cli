
from todo_cli.models import Task
from todo_cli.storage import load_tasks, next_id, save_tasks


def test_load_tasks_returns_empty_list_if_file_missing(tmp_path) -> None:
    db_path = tmp_path / "tasks.json"

    tasks = load_tasks(path=db_path)

    assert tasks == []


def test_save_and_load_tasks_roundtrip(tmp_path) -> None:
    db_path = tmp_path / "tasks.json"

    original_tasks = [
        Task(id=1, title="Task 1", priority=3),
        Task(id=2, title="Task 2", priority=5, done=True),
    ]

    save_tasks(original_tasks, path=db_path)
    loaded_tasks = load_tasks(path=db_path)

    assert len(loaded_tasks) == len(original_tasks)
    assert [t.model_dump() for t in loaded_tasks] == [
        t.model_dump() for t in original_tasks
    ]


def test_load_tasks_invalid_json_returns_empty_list(tmp_path) -> None:
    db_path = tmp_path / "tasks.json"
    db_path.write_text("{not valid json", encoding="utf-8")

    tasks = load_tasks(path=db_path)

    assert tasks == []


def test_next_id_empty_list_returns_1() -> None:
    tasks: list[Task] = []
    assert next_id(tasks) == 1


def test_next_id_returns_max_plus_one() -> None:
    tasks = [
        Task(id=1, title="A", priority=3),
        Task(id=5, title="B", priority=2),
        Task(id=3, title="C", priority=4),
    ]

    assert next_id(tasks) == 6
