from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    """
    Represents a task in the todo application.

    Attributes:
        id (int): Unique identifier of the task.
        title (str): Title of the task.
        description (str | None): Optional description.
        priority (int): Priority level from 1 to 5.
        deadline (date | None): Optional deadline.
        done (bool): Whether the task is completed.
    """
    id: int
    title: str
    description: Optional[str] = ""
    priority: int = Field(3, ge=1, le=5)
    deadline: datetime | None = None
    done: bool = False

    @field_validator("deadline", mode="before")
    @classmethod
    def parse_deadline(cls, value: object) -> datetime | None:
        """Accepte str ou datetime, stocke toujours un datetime ou None."""
        if value is None or value == "":
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            return datetime.fromisoformat(value)

        raise ValueError("Valeur de deadline invalide")

