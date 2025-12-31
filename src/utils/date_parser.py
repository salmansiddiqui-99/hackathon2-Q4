"""Natural language date parser for the todo application."""

from datetime import datetime, timedelta


def parse_natural_date(input_str: str) -> datetime | None:
    """Parse natural language date input.

    Supported formats:
    - "today" → today at 09:00
    - "tomorrow" → tomorrow at 09:00
    - "next monday" through "next sunday" → next occurrence at 09:00
    - "YYYY-MM-DD" → specified date at 09:00
    - "YYYY-MM-DD HH:MM" → exact datetime

    Args:
        input_str: The date string to parse

    Returns:
        Parsed datetime object, or None if invalid input
    """
    if not input_str or not input_str.strip():
        return None

    input_lower = input_str.strip().lower()
    now = datetime.now()

    # Handle "today"
    if input_lower == "today":
        return now.replace(hour=9, minute=0, second=0, microsecond=0)

    # Handle "tomorrow"
    if input_lower == "tomorrow":
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

    # Handle "next <weekday>"
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    if input_lower.startswith("next "):
        weekday_name = input_lower[5:]  # Remove "next "
        if weekday_name in weekdays:
            target_weekday = weekdays[weekday_name]
            current_weekday = now.weekday()

            # Calculate days until next occurrence
            days_ahead = target_weekday - current_weekday
            if days_ahead <= 0:  # Target day already passed this week
                days_ahead += 7

            next_date = now + timedelta(days=days_ahead)
            return next_date.replace(hour=9, minute=0, second=0, microsecond=0)

    # Handle ISO formats: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"
    try:
        # Try full datetime format first
        if " " in input_str:
            return datetime.strptime(input_str.strip(), "%Y-%m-%d %H:%M")
        else:
            # Date only, set time to 09:00
            parsed_date = datetime.strptime(input_str.strip(), "%Y-%m-%d")
            return parsed_date.replace(hour=9, minute=0, second=0, microsecond=0)
    except ValueError:
        pass

    # Invalid input
    return None
