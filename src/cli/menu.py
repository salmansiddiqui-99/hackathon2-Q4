"""CLI menu and input handlers for the todo application."""

from datetime import datetime
from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.date_parser import parse_natural_date
from src.cli.formatter import (
    get_console,
    format_menu_header,
    format_section_header,
    format_separator,
    format_task_panel,
    format_success,
    format_error,
    format_warning,
    format_info,
    format_status_badge,
    format_priority_badge
)


def display_menu() -> None:
    """Display the main menu options (T013)."""
    console = get_console()
    console.print()
    console.print(format_menu_header("Todo App"))
    console.print("[cyan]1.[/] Add Task")
    console.print("[cyan]2.[/] List Tasks")
    console.print("[cyan]3.[/] Update Task")
    console.print("[cyan]4.[/] Delete Task")
    console.print("[cyan]5.[/] Mark Status")
    console.print("[cyan]6.[/] Manage Tags")
    console.print("[cyan]7.[/] Search Tasks")
    console.print("[cyan]8.[/] Filter Tasks")
    console.print("[cyan]9.[/] Sort Tasks")
    console.print("[cyan]10.[/] Check Reminders")
    console.print("[cyan]11.[/] Exit")
    console.print()


def get_menu_choice() -> str:
    """Get user's menu choice.

    Returns:
        The user's input string
    """
    return input("Enter choice (1-11): ").strip()


def handle_add_task(service: TaskService) -> None:
    """Handle adding a new task (T014).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Add Task"))
    title = input("Enter title: ").strip()

    if not title:
        console.print(format_error("Title cannot be empty."))  # T040
        return

    description = input("Enter description (press Enter to skip): ").strip()

    # Prompt for priority
    print(f"Priority options: {', '.join(Task.VALID_PRIORITIES)}")
    priority_input = input("Enter priority (press Enter for default 'medium'): ").strip().lower()
    priority = priority_input if priority_input in Task.VALID_PRIORITIES else "medium"

    # Prompt for tags
    tags_input = input("Enter tags (comma-separated, press Enter to skip): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None

    # Prompt for recurrence
    print(f"Recurrence options: {', '.join(Task.VALID_RECURRENCES)}")
    recurrence_input = input("Enter recurrence (press Enter for default 'none'): ").strip().lower()
    recurrence = recurrence_input if recurrence_input in Task.VALID_RECURRENCES else "none"

    # Prompt for due date
    print("Enter due date (today, tomorrow, next monday, YYYY-MM-DD, YYYY-MM-DD HH:MM)")
    due_date_input = input("Due date (press Enter to skip): ").strip()
    due_date = None
    if due_date_input:
        due_date = parse_natural_date(due_date_input)
        if due_date is None:
            console.print(format_warning("Invalid date format. Task will have no due date."))  # T041

    try:
        task = service.add_task(title, description, priority, tags, recurrence, due_date)
        priority_badge = format_priority_badge(task.priority)
        # T039: Success message with formatting
        console.print(format_success(f"Task #{task.id} created successfully with priority {priority_badge}."))
        if task.tags:
            console.print(f"[dim]Tags: {', '.join(task.tags)}[/]")
        if task.recurrence != "none":
            console.print(f"[dim]Recurrence: {task.recurrence}[/]")
        if task.due_date:
            console.print(f"[dim]Due date: {task.due_date.strftime('%Y-%m-%d %H:%M')}[/]")
    except ValueError as e:
        console.print(format_error(str(e)))  # T042


def handle_list_tasks(service: TaskService) -> None:
    """Handle listing all tasks (T015, T025, T026).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("All Tasks"))

    # Check if sort preference is active
    sort_pref = service.get_sort_preference()
    if sort_pref != "none":
        tasks = service.get_sorted_tasks()
        console.print(f"[dim](Sorted by: {sort_pref})[/]")
    else:
        tasks = service.list_tasks()

    if not tasks:
        console.print(format_info("No tasks found."))
        return

    now = datetime.now()

    for task in tasks:
        # Display task in formatted panel (T025)
        console.print(format_task_panel(task, now))
        console.print()  # Add spacing between tasks (T026)


def handle_update_task(service: TaskService) -> None:
    """Handle updating a task (T016).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Update Task"))

    try:
        task_id = int(input("Enter task ID to update: ").strip())
    except ValueError:
        console.print(format_error("Please enter a valid numeric ID."))  # T043
        return

    task = service.get_task(task_id)
    if task is None:
        console.print(format_error(f"Task #{task_id} not found."))  # T044
        return

    print(f"Current title: {task.title}")
    print(f"Current description: {task.description or '(empty)'}")
    print(f"Current priority: {task.priority}")
    print(f"Current recurrence: {task.recurrence}")
    print(f"Current due date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}")
    print("(Press Enter to keep current value)")

    new_title = input("New title: ").strip()
    new_description = input("New description: ")

    print(f"Priority options: {', '.join(Task.VALID_PRIORITIES)}")
    new_priority = input("New priority: ").strip().lower()

    print(f"Recurrence options: {', '.join(Task.VALID_RECURRENCES)}")
    new_recurrence = input("New recurrence: ").strip().lower()

    print("Enter due date (today, tomorrow, next monday, YYYY-MM-DD, YYYY-MM-DD HH:MM)")
    new_due_date_input = input("New due date: ").strip()

    # Use None to indicate "keep current" (skip-to-keep pattern)
    title_update = new_title if new_title else None
    desc_update = new_description if new_description else None
    priority_update = new_priority if new_priority and new_priority in Task.VALID_PRIORITIES else None
    recurrence_update = new_recurrence if new_recurrence and new_recurrence in Task.VALID_RECURRENCES else None

    due_date_update = None
    if new_due_date_input:
        parsed_date = parse_natural_date(new_due_date_input)
        if parsed_date is None:
            console.print(format_warning("Invalid date format. Due date will not be changed."))  # T046
        else:
            due_date_update = parsed_date

    try:
        updated = service.update_task(
            task_id,
            title_update,
            desc_update,
            priority_update,
            recurrence_update,
            due_date_update
        )
        if updated:
            console.print(format_success(f"Task #{task_id} updated successfully."))  # T045
    except ValueError as e:
        console.print(format_error(str(e)))  # T044 (also handles ValueError)


def handle_delete_task(service: TaskService) -> None:
    """Handle deleting a task (T017).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Delete Task"))

    try:
        task_id = int(input("Enter task ID to delete: ").strip())
    except ValueError:
        console.print(format_error("Please enter a valid numeric ID."))  # T047
        return

    if service.delete_task(task_id):
        console.print(format_success(f"Task #{task_id} deleted successfully."))  # T048
    else:
        console.print(format_error(f"Task #{task_id} not found."))  # T049


def handle_mark_status(service: TaskService) -> None:
    """Handle changing task status (T018).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Mark Status"))

    try:
        task_id = int(input("Enter task ID: ").strip())
    except ValueError:
        console.print(format_error("Please enter a valid numeric ID."))  # T050
        return

    task = service.get_task(task_id)
    if task is None:
        console.print(format_error(f"Task #{task_id} not found."))  # T051
        return

    print(f"Current status: {task.status}")
    print(f"Valid statuses: {', '.join(Task.VALID_STATUSES)}")

    # Check if task is recurring before status change
    is_recurring = task.recurrence != "none"

    new_status = input("Enter new status: ").strip().lower()

    try:
        updated = service.update_status(task_id, new_status)
        if updated:
            console.print(format_success(f"Task #{task_id} status changed to '{new_status}'."))  # T052
            # Show auto-generation message if recurring task was completed
            if new_status == "completed" and is_recurring:
                console.print(format_info(f"Auto-generated next occurrence of recurring task (recurrence: {task.recurrence})."))  # T053
    except ValueError as e:
        console.print(format_error(str(e)))  # T054


def handle_manage_tags(service: TaskService) -> None:
    """Handle adding or removing tags from a task (T019).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Manage Tags"))

    try:
        task_id = int(input("Enter task ID: ").strip())
    except ValueError:
        console.print(format_error("Please enter a valid numeric ID."))  # T055
        return

    task = service.get_task(task_id)
    if task is None:
        console.print(format_error(f"Task #{task_id} not found."))  # T056
        return

    print(f"Current tags: {', '.join(task.tags) if task.tags else '(no tags)'}")
    print("\n1. Add tags")
    print("2. Remove tag")
    print("3. Cancel")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        tags_input = input("Enter tags to add (comma-separated): ").strip()
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(",")]
            updated = service.add_tags_to_task(task_id, tags)
            if updated:
                console.print(format_success(f"Tags added. Current tags: {', '.join(updated.tags)}"))  # T057
    elif choice == "2":
        if not task.tags:
            console.print(format_info("No tags to remove."))  # T059
            return
        tag_to_remove = input("Enter tag to remove: ").strip()
        updated = service.remove_tag_from_task(task_id, tag_to_remove)
        if updated:
            console.print(format_success(f"Tag removed. Current tags: {', '.join(updated.tags) if updated.tags else '(no tags)'}"))  # T058
    elif choice == "3":
        console.print(format_info("Cancelled."))  # T060
    else:
        console.print(format_error("Invalid choice."))  # T061


def handle_search_tasks(service: TaskService) -> None:
    """Handle searching tasks by keyword (T020, T034).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Search Tasks"))
    keyword = input("Enter search keyword: ").strip()

    results = service.search_tasks(keyword)

    if not results:
        console.print(format_info("No tasks found matching your search."))
        return

    console.print(f"\n[bold]Found {len(results)} task(s):[/]")
    now = datetime.now()
    for task in results:
        console.print(format_task_panel(task, now))
        console.print()


def handle_filter_tasks(service: TaskService) -> None:
    """Handle filtering tasks by status, priority, or tag (T021).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Filter Tasks"))
    print("Filter by:")
    print("1. Status")
    print("2. Priority")
    print("3. Tag")
    print("4. Cancel")

    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        print(f"Status options: {', '.join(Task.VALID_STATUSES)}")
        status = input("Enter status to filter by: ").strip().lower()
        results = service.filter_tasks("status", status)
        filter_label = f"status={status}"
    elif choice == "2":
        print(f"Priority options: {', '.join(Task.VALID_PRIORITIES)}")
        priority = input("Enter priority to filter by: ").strip().lower()
        results = service.filter_tasks("priority", priority)
        filter_label = f"priority={priority}"
    elif choice == "3":
        tag = input("Enter tag to filter by: ").strip()
        results = service.filter_tasks("tag", tag)
        filter_label = f"tag={tag}"
    elif choice == "4":
        console.print(format_info("Cancelled."))  # T064
        return
    else:
        console.print(format_error("Invalid choice."))  # T065
        return

    if not results:
        console.print(format_info(f"No tasks found matching filter: {filter_label}"))
        return

    console.print(f"\n[bold]Found {len(results)} task(s) matching {filter_label}:[/]")
    now = datetime.now()
    for task in results:
        console.print(format_task_panel(task, now))
        console.print()


def handle_sort_tasks(service: TaskService) -> None:
    """Handle setting sort preference for task list (T022).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Sort Tasks"))
    print("Sort by:")
    print("1. Priority (high to low)")
    print("2. Title (A-Z)")
    print("3. Creation date (oldest first)")
    print("4. Clear sort (default order)")
    print("5. Cancel")

    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":
        service.set_sort_preference("priority")
        console.print(format_success("Tasks will now be sorted by priority (high to low)."))  # T066
    elif choice == "2":
        service.set_sort_preference("title")
        console.print(format_success("Tasks will now be sorted alphabetically by title."))  # T066
    elif choice == "3":
        service.set_sort_preference("created")
        console.print(format_success("Tasks will now be sorted by creation date (oldest first)."))  # T066
    elif choice == "4":
        service.set_sort_preference("none")
        console.print(format_success("Sort preference cleared. Tasks will be shown in default order."))  # T066
    elif choice == "5":
        console.print(format_info("Cancelled."))  # T067
    else:
        console.print(format_error("Invalid choice."))  # T068


def handle_check_reminders(service: TaskService) -> None:
    """Display overdue and soon-due tasks (T023, T036-T037).

    Args:
        service: The TaskService instance
    """
    console = get_console()
    console.print(format_section_header("Check Reminders"))

    overdue = service.get_overdue_tasks()
    soon_due = service.get_soon_due_tasks(24)

    if not overdue and not soon_due:
        console.print(format_info("No overdue or upcoming tasks."))
        return

    now = datetime.now()

    if overdue:
        console.print("\n[red bold]** Overdue Tasks **[/]")  # T036: Red highlighting
        for task in overdue:
            # Calculate how long overdue
            time_diff = now - task.due_date
            days = time_diff.days
            hours = time_diff.seconds // 3600

            if days > 0:
                overdue_str = f"{days} day(s) overdue"
            else:
                overdue_str = f"{hours} hour(s) overdue"

            priority_badge = format_priority_badge(task.priority)
            console.print(f"\n[bold]ID:[/] {task.id} | [bold]Title:[/] {task.title} | [bold]Priority:[/] {priority_badge}")
            console.print(f"   [bold]Due:[/] {task.due_date.strftime('%Y-%m-%d %H:%M')} [red]({overdue_str})[/]")
            console.print(f"   [bold]Status:[/] {format_status_badge(task.status)}")

    if soon_due:
        console.print("\n[yellow bold]** Due Soon (within 24 hours) **[/]")  # T037: Yellow highlighting
        for task in soon_due:
            # Calculate time remaining
            time_diff = task.due_date - now
            hours = time_diff.seconds // 3600
            minutes = (time_diff.seconds % 3600) // 60

            if time_diff.days > 0:
                remaining_str = f"in {time_diff.days} day(s)"
            elif hours > 0:
                remaining_str = f"in {hours} hour(s)"
            else:
                remaining_str = f"in {minutes} minute(s)"

            priority_badge = format_priority_badge(task.priority)
            console.print(f"\n[bold]ID:[/] {task.id} | [bold]Title:[/] {task.title} | [bold]Priority:[/] {priority_badge}")
            console.print(f"   [bold]Due:[/] {task.due_date.strftime('%Y-%m-%d %H:%M')} [yellow]({remaining_str})[/]")
            console.print(f"   [bold]Status:[/] {format_status_badge(task.status)}")
