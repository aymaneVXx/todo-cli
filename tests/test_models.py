from datetime import datetime

from todo_cli.models import Task


def test_deadline_parsing():
    t = Task(id=1, title="Test", deadline="2025-01-01")
    assert isinstance(t.deadline, datetime)
    assert t.deadline.year == 2025
