from datetime import datetime

import pytest
from pydantic import ValidationError

from todo_cli.models import Task


def test_task_parses_deadline_from_iso_string() -> None:
    task = Task(
        id=1,
        title="Test deadline",
        priority=3,
        deadline="2025-01-10",
    )

    assert isinstance(task.deadline, datetime)
    assert task.deadline.year == 2025
    assert task.deadline.month == 1
    assert task.deadline.day == 10


def test_task_deadline_none_when_empty_string() -> None:
    task = Task(
        id=1,
        title="No deadline",
        priority=3,
        deadline="",
    )

    assert task.deadline is None


def test_task_invalid_deadline_raises_error() -> None:
    with pytest.raises(ValidationError):
        Task(
            id=1,
            title="Bad deadline",
            priority=3,
            deadline="31-12-2025",  
        )
