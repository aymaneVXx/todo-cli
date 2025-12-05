from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    priority: int = Field(3, ge=1, le=5)
    # Important : pour Mypy, deadline est datetime | None (pas str)
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
            # On laisse ValueError remonter si le format est mauvais
            return datetime.fromisoformat(value)

        raise ValueError("Valeur de deadline invalide")

