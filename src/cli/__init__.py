"""Command-line interface components."""

from .menu import (
    display_menu,
    get_menu_choice,
    handle_add_task,
    handle_list_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_status,
    handle_manage_tags,
    handle_search_tasks,
    handle_filter_tasks,
    handle_sort_tasks,
    handle_check_reminders,
)

__all__ = [
    "display_menu",
    "get_menu_choice",
    "handle_add_task",
    "handle_list_tasks",
    "handle_update_task",
    "handle_delete_task",
    "handle_mark_status",
    "handle_manage_tags",
    "handle_search_tasks",
    "handle_filter_tasks",
    "handle_sort_tasks",
    "handle_check_reminders",
]
