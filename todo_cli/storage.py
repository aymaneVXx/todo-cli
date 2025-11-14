import json
from pathlib import Path
from typing import List

from .models import Task

DEFAULT_DB_PATH = Path.home() / ".todo_cli_tasks.json"


def load_tasks(path: Path = DEFAULT_DB_PATH) -> List[Task]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Task(**item) for item in data]


def save_tasks(tasks: List[Task], path: Path = DEFAULT_DB_PATH) -> None:
    # v2 way: use model_dump()
    data = [t.model_dump() for t in tasks]
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def next_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1
