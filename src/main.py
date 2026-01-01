"""Main entry point for the Todo Console Application."""

from src.services.task_service import TaskService
from src.cli.menu import (
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
from src.cli.formatter import get_console, format_menu_header, format_success, format_error


def main() -> None:
    """Run the todo application main loop (T027, T070-T071)."""
    service = TaskService()
    console = get_console()

    console.print(format_menu_header("Welcome to Todo App!"))

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            handle_add_task(service)
        elif choice == "2":
            handle_list_tasks(service)
        elif choice == "3":
            handle_update_task(service)
        elif choice == "4":
            handle_delete_task(service)
        elif choice == "5":
            handle_mark_status(service)
        elif choice == "6":
            handle_manage_tags(service)
        elif choice == "7":
            handle_search_tasks(service)
        elif choice == "8":
            handle_filter_tasks(service)
        elif choice == "9":
            handle_sort_tasks(service)
        elif choice == "10":
            handle_check_reminders(service)
        elif choice == "11":
            console.print(format_success("Goodbye!"))  # T071
            break
        else:
            console.print(format_error("Invalid choice. Please enter a number between 1 and 11."))  # T070


if __name__ == "__main__":
    main()
