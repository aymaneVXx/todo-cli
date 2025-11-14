from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: int = Field(3, ge=1, le=5)
    deadline: Optional[datetime] = None
    done: bool = False

    @field_validator("deadline", mode="before")
    def parse_deadline(cls, value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        # Format YYYY-MM-DD
        return datetime.strptime(value, "%Y-%m-%d")
