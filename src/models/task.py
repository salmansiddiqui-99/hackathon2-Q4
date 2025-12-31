"""Task model for the todo application."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique numeric identifier (auto-generated, immutable)
        title: Short description of the task (required, non-empty)
        description: Detailed information (optional, can be empty)
        status: Current state (pending | in-progress | completed)
        priority: Importance level (high | medium | low), default: medium
        tags: List of category labels (lowercase strings), default: empty list
        created_at: Timestamp of task creation (auto-generated, immutable)
        recurrence: Recurrence pattern (none | daily | weekly | monthly), default: none
        due_date: Optional due date and time for the task, default: None
    """
    id: int
    title: str
    description: str
    status: str = "pending"
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    recurrence: str = "none"
    due_date: datetime | None = None

    VALID_STATUSES = ("pending", "in-progress", "completed")
    VALID_PRIORITIES = ("high", "medium", "low")
    VALID_RECURRENCES = ("none", "daily", "weekly", "monthly")

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(self.VALID_STATUSES)}")
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority. Must be one of: {', '.join(self.VALID_PRIORITIES)}")
        if self.recurrence not in self.VALID_RECURRENCES:
            raise ValueError(f"Invalid recurrence. Must be one of: {', '.join(self.VALID_RECURRENCES)}")
