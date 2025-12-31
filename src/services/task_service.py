"""Task service for managing todo tasks in memory."""

from datetime import datetime, timedelta
from src.models.task import Task
from src.utils.recurrence import calculate_next_due_date


class TaskService:
    """Service for CRUD operations on tasks.

    Maintains an in-memory list of tasks with auto-incrementing IDs.
    """

    def __init__(self) -> None:
        """Initialize the task service with empty task list."""
        self._tasks: list[Task] = []
        self._next_id: int = 1
        self._sort_preference: str = "none"  # none | priority | title | created

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: list[str] | None = None,
        recurrence: str = "none",
        due_date: datetime | None = None
    ) -> Task:
        """Add a new task with auto-generated ID.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)
            priority: Task priority (high | medium | low), default: medium
            tags: List of tags (optional), will be normalized to lowercase
            recurrence: Recurrence pattern (none | daily | weekly | monthly), default: none
            due_date: Optional due date and time for the task

        Returns:
            The created Task object

        Raises:
            ValueError: If title is empty or priority/recurrence is invalid
        """
        # Normalize tags to lowercase and deduplicate
        normalized_tags = []
        if tags:
            normalized_tags = list(set(tag.strip().lower() for tag in tags if tag.strip()))

        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=normalized_tags,
            recurrence=recurrence,
            due_date=due_date
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks.

        Returns:
            List of all Task objects
        """
        return self._tasks.copy()

    def get_task(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: The task ID to find

        Returns:
            Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        recurrence: str | None = None,
        due_date: datetime | None | object = None
    ) -> Task | None:
        """Update a task's title, description, priority, recurrence, and/or due_date.

        Args:
            task_id: The task ID to update
            title: New title (None to keep current)
            description: New description (None to keep current)
            priority: New priority (None to keep current)
            recurrence: New recurrence pattern (None to keep current)
            due_date: New due date (None to keep current, use sentinel object to clear)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If new title is empty or priority/recurrence is invalid
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        if priority is not None:
            if priority not in Task.VALID_PRIORITIES:
                raise ValueError(f"Invalid priority. Must be one of: {', '.join(Task.VALID_PRIORITIES)}")
            task.priority = priority

        if recurrence is not None:
            if recurrence not in Task.VALID_RECURRENCES:
                raise ValueError(f"Invalid recurrence. Must be one of: {', '.join(Task.VALID_RECURRENCES)}")
            task.recurrence = recurrence

        # Handle due_date update (support explicit None to clear)
        if due_date is not None and not isinstance(due_date, type(None)):
            task.due_date = due_date

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if deleted, False if not found
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def update_status(self, task_id: int, status: str) -> Task | None:
        """Update a task's status.

        Auto-generates next occurrence for recurring tasks when marked completed.

        Args:
            task_id: The task ID to update
            status: New status (pending | in-progress | completed)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If status is invalid
        """
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(Task.VALID_STATUSES)}")

        task = self.get_task(task_id)
        if task is None:
            return None

        task.status = status

        # Auto-generate next occurrence for recurring tasks when completed
        if status == "completed" and task.recurrence != "none":
            self._generate_next_occurrence(task)

        return task

    def _generate_next_occurrence(self, completed_task: Task) -> Task:
        """Create the next instance of a recurring task.

        Args:
            completed_task: The task that was just completed

        Returns:
            The newly created next occurrence task
        """
        next_due = calculate_next_due_date(
            completed_task.due_date,
            completed_task.recurrence
        )

        return self.add_task(
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            tags=completed_task.tags.copy() if completed_task.tags else None,
            recurrence=completed_task.recurrence,
            due_date=next_due
        )

    def search_tasks(self, keyword: str) -> list[Task]:
        """Search tasks by keyword in title, description, or tags.

        Args:
            keyword: Search term (case-insensitive)

        Returns:
            List of tasks matching the keyword
        """
        if not keyword.strip():
            return self._tasks.copy()

        keyword_lower = keyword.lower()
        results = []

        for task in self._tasks:
            # Search in title
            if keyword_lower in task.title.lower():
                results.append(task)
                continue

            # Search in description
            if keyword_lower in task.description.lower():
                results.append(task)
                continue

            # Search in tags
            if any(keyword_lower in tag for tag in task.tags):
                results.append(task)

        return results

    def filter_tasks(self, by: str, value: str) -> list[Task]:
        """Filter tasks by status, priority, or tag.

        Args:
            by: Filter dimension (status | priority | tag)
            value: Value to filter by

        Returns:
            List of tasks matching the filter criteria
        """
        value_lower = value.lower()

        if by == "status":
            return [task for task in self._tasks if task.status == value_lower]
        elif by == "priority":
            return [task for task in self._tasks if task.priority == value_lower]
        elif by == "tag":
            return [task for task in self._tasks if value_lower in task.tags]
        else:
            return self._tasks.copy()

    def get_sorted_tasks(self) -> list[Task]:
        """Get tasks sorted by current preference.

        Returns:
            List of tasks sorted according to preference (none | priority | title | created)
        """
        if self._sort_preference == "priority":
            # Sort by priority: high -> medium -> low
            priority_order = {"high": 0, "medium": 1, "low": 2}
            return sorted(self._tasks, key=lambda t: priority_order[t.priority])
        elif self._sort_preference == "title":
            # Sort alphabetically by title (A-Z)
            return sorted(self._tasks, key=lambda t: t.title.lower())
        elif self._sort_preference == "created":
            # Sort by creation date (oldest first)
            return sorted(self._tasks, key=lambda t: t.created_at)
        else:
            # No sort preference, return as-is
            return self._tasks.copy()

    def set_sort_preference(self, preference: str) -> None:
        """Set the sort preference.

        Args:
            preference: Sort preference (none | priority | title | created)
        """
        self._sort_preference = preference

    def get_sort_preference(self) -> str:
        """Get the current sort preference.

        Returns:
            Current sort preference string
        """
        return self._sort_preference

    def add_tags_to_task(self, task_id: int, tags: list[str]) -> Task | None:
        """Add tags to an existing task.

        Args:
            task_id: The task ID to update
            tags: List of tags to add (will be normalized and deduplicated)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        # Normalize new tags and add to existing (avoiding duplicates)
        normalized_tags = [tag.strip().lower() for tag in tags if tag.strip()]
        current_tags_set = set(task.tags)
        current_tags_set.update(normalized_tags)
        task.tags = list(current_tags_set)

        return task

    def remove_tag_from_task(self, task_id: int, tag: str) -> Task | None:
        """Remove a tag from an existing task.

        Args:
            task_id: The task ID to update
            tag: Tag to remove (case-insensitive)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        tag_lower = tag.strip().lower()
        if tag_lower in task.tags:
            task.tags.remove(tag_lower)

        return task

    def get_overdue_tasks(self) -> list[Task]:
        """Get tasks with due_date in the past (excludes completed tasks).

        Returns:
            List of overdue tasks
        """
        now = datetime.now()
        return [
            task for task in self._tasks
            if task.due_date and task.due_date < now and task.status != "completed"
        ]

    def get_soon_due_tasks(self, hours: int = 24) -> list[Task]:
        """Get tasks due within the next N hours (excludes completed tasks).

        Args:
            hours: Number of hours to look ahead (default: 24)

        Returns:
            List of tasks due soon
        """
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        return [
            task for task in self._tasks
            if task.due_date and now <= task.due_date <= cutoff and task.status != "completed"
        ]
