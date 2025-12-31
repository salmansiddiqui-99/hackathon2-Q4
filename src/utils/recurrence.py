"""Recurrence calculation utilities for the todo application."""

import calendar
from datetime import datetime, timedelta


def calculate_next_due_date(
    current_due: datetime | None,
    recurrence: str
) -> datetime:
    """Calculate the next due date based on recurrence pattern.

    Args:
        current_due: Current due date (or None to use today)
        recurrence: Recurrence pattern (daily | weekly | monthly)

    Returns:
        The next due date

    Raises:
        ValueError: If recurrence pattern is invalid
    """
    # Use today at 09:00 if no current due date
    if current_due is None:
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        base_date = current_due

    if recurrence == "daily":
        # Add 1 day
        return base_date + timedelta(days=1)

    elif recurrence == "weekly":
        # Add 7 days
        return base_date + timedelta(days=7)

    elif recurrence == "monthly":
        # Add 1 month with month boundary handling
        year = base_date.year
        month = base_date.month
        day = base_date.day

        # Calculate next month
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        # Handle day overflow (e.g., Jan 31 → Feb 28/29)
        max_day_in_next_month = calendar.monthrange(next_year, next_month)[1]
        next_day = min(day, max_day_in_next_month)

        return base_date.replace(year=next_year, month=next_month, day=next_day)

    else:
        raise ValueError(f"Invalid recurrence pattern: {recurrence}")
