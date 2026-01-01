"""UI formatting utilities for console output.

This module provides cross-platform terminal formatting using the rich library.
Includes color-coded status/priority indicators, formatted messages, bordered
panels, and styled input prompts. Supports graceful fallback for terminals
without color capability.

All formatting functions follow consistent conventions:
- Status colors: pending=cyan, in-progress=yellow, completed=green
- Priority colors: high=red, medium=yellow, low=cyan
- Message colors: success=green, error=red, warning=yellow, info=blue
"""

from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from src.models.task import Task


# Shared console instance for consistent output
_console: Console | None = None


# Color scheme constants (T003)
COLORS = {
    "status": {
        "pending": "cyan",
        "in-progress": "yellow",
        "completed": "green"
    },
    "priority": {
        "high": "red",
        "medium": "yellow",
        "low": "cyan"
    },
    "message": {
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "blue"
    }
}

# Symbol constants (T004)
# Using simpler ASCII-compatible symbols for Windows compatibility
SYMBOLS = {
    "success": "[OK]",
    "error": "[X]",
    "warning": "[!]",
    "info": "[i]",
    "completed": "[OK]",
    "in_progress": "[>]",
    "pending": "[ ]",
    "high_priority": "!!!",
    "medium_priority": "!!",
    "low_priority": "!",
    "overdue": "[!]"
}


def get_console() -> Console:
    """Get the shared Rich Console instance (T005).

    Returns:
        Configured Console object with auto color detection
    """
    global _console
    if _console is None:
        # Configure console with safe_box=True for better Windows compatibility
        # and legacy_windows=False to avoid encoding issues
        _console = Console(
            force_terminal=True,
            color_system="auto",
            legacy_windows=False,
            safe_box=True
        )
    return _console


def format_success(message: str) -> str:
    """Format a success message with color and symbol (T006).

    Args:
        message: Success message text

    Returns:
        Formatted string with rich markup
    """
    return f"[{COLORS['message']['success']}]{SYMBOLS['success']} {message}[/]"


def format_error(message: str) -> str:
    """Format an error message with color and symbol (T007).

    Args:
        message: Error message text

    Returns:
        Formatted string with rich markup
    """
    return f"[{COLORS['message']['error']}]{SYMBOLS['error']} {message}[/]"


def format_warning(message: str) -> str:
    """Format a warning message with color and symbol (T008).

    Args:
        message: Warning message text

    Returns:
        Formatted string with rich markup
    """
    return f"[{COLORS['message']['warning']}]{SYMBOLS['warning']} {message}[/]"


def format_info(message: str) -> str:
    """Format an info message with color and symbol (T009).

    Args:
        message: Info message text

    Returns:
        Formatted string with rich markup
    """
    return f"[{COLORS['message']['info']}]{SYMBOLS['info']} {message}[/]"


def format_menu_header(title: str) -> Panel:
    """Create a formatted menu header with border (T010).

    Args:
        title: Menu title text

    Returns:
        Rich Panel object for display
    """
    return Panel(
        Text(title, style="bold cyan", justify="center"),
        border_style="cyan",
        padding=(0, 2)
    )


def format_section_header(title: str) -> str:
    """Format a section header with styling (T011).

    Args:
        title: Section header text

    Returns:
        Formatted header string with rich markup
    """
    # Using plain ASCII dashes for Windows compatibility
    return f"\n[bold yellow]{'-' * 60}[/]\n[bold yellow]{title}[/]\n[bold yellow]{'-' * 60}[/]"


def format_separator() -> str:
    """Create a visual separator line (T012).

    Returns:
        Formatted separator string
    """
    return f"[dim]{'-' * 60}[/]"


def format_status_badge(status: str) -> str:
    """Create a colored status badge with symbol (T028).

    Args:
        status: Task status (pending/in-progress/completed)

    Returns:
        Formatted status string with color and symbol
    """
    color = COLORS["status"].get(status, "white")
    symbol = SYMBOLS.get(status.replace("-", "_"), "•")
    return f"[{color}]{symbol} {status.upper()}[/]"


def format_priority_badge(priority: str) -> str:
    """Create a colored priority badge with symbol (T029).

    Args:
        priority: Task priority (high/medium/low)

    Returns:
        Formatted priority string with color and symbol
    """
    color = COLORS["priority"].get(priority, "white")
    if priority == "high":
        symbol = SYMBOLS["high_priority"]
    elif priority == "medium":
        symbol = SYMBOLS["medium_priority"]
    else:
        symbol = SYMBOLS["low_priority"]
    return f"[{color}]{symbol} {priority.upper()}[/]"


def format_overdue_indicator() -> str:
    """Create a formatted overdue warning indicator (T030).

    Returns:
        Formatted overdue warning string
    """
    return f"[red bold]{SYMBOLS['overdue']} OVERDUE[/]"


def format_task_panel(task: Task, now: datetime) -> Panel:
    """Format a task for display in a bordered panel (T024, T031-T033).

    Args:
        task: Task object to display
        now: Current datetime for overdue calculation

    Returns:
        Rich Panel with formatted task information
    """
    # Build task content
    content_lines = []

    # First line: ID, Title
    content_lines.append(f"[bold]ID:[/] {task.id} | [bold]Title:[/] {task.title}")

    # Second line: Status and Priority with colored badges (T031, T032)
    status_badge = format_status_badge(task.status)
    priority_badge = format_priority_badge(task.priority)
    content_lines.append(f"[bold]Status:[/] {status_badge} | [bold]Priority:[/] {priority_badge}")

    # Tags
    tags_display = f"[{', '.join(task.tags)}]" if task.tags else "[]"
    content_lines.append(f"[bold]Tags:[/] {tags_display}")

    # Description
    if task.description:
        content_lines.append(f"[bold]Description:[/] {task.description}")
    else:
        content_lines.append("[bold]Description:[/] [dim](no description)[/]")

    # Recurrence
    if task.recurrence != "none":
        content_lines.append(f"[bold]Recurrence:[/] {task.recurrence}")

    # Due date with overdue check (T033)
    if task.due_date:
        due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
        if task.due_date < now and task.status != "completed":
            overdue = format_overdue_indicator()
            content_lines.append(f"[bold]Due date:[/] {due_str} {overdue}")
        else:
            content_lines.append(f"[bold]Due date:[/] {due_str}")
    else:
        content_lines.append("[bold]Due date:[/] [dim]No due date[/]")

    content = "\n".join(content_lines)

    return Panel(
        content,
        border_style="blue",
        padding=(0, 1),
        expand=False
    )
