"""CLI menu and input handlers for the todo application."""

from datetime import datetime
from src.models.task import Task
from src.services.task_service import TaskService
from src.utils.date_parser import parse_natural_date


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo App ===")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Status")
    print("6. Manage Tags")
    print("7. Search Tasks")
    print("8. Filter Tasks")
    print("9. Sort Tasks")
    print("10. Check Reminders")
    print("11. Exit")
    print()


def get_menu_choice() -> str:
    """Get user's menu choice.

    Returns:
        The user's input string
    """
    return input("Enter choice (1-11): ").strip()


def handle_add_task(service: TaskService) -> None:
    """Handle adding a new task.

    Args:
        service: The TaskService instance
    """
    print("\n--- Add Task ---")
    title = input("Enter title: ").strip()

    if not title:
        print("Error: Title cannot be empty.")
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
            print("Warning: Invalid date format. Task will have no due date.")

    try:
        task = service.add_task(title, description, priority, tags, recurrence, due_date)
        print(f"Task #{task.id} created successfully with priority '{task.priority}'.")
        if task.tags:
            print(f"Tags: {', '.join(task.tags)}")
        if task.recurrence != "none":
            print(f"Recurrence: {task.recurrence}")
        if task.due_date:
            print(f"Due date: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_list_tasks(service: TaskService) -> None:
    """Handle listing all tasks.

    Args:
        service: The TaskService instance
    """
    print("\n--- All Tasks ---")

    # Check if sort preference is active
    sort_pref = service.get_sort_preference()
    if sort_pref != "none":
        tasks = service.get_sorted_tasks()
        print(f"(Sorted by: {sort_pref})")
    else:
        tasks = service.list_tasks()

    if not tasks:
        print("No tasks found.")
        return

    now = datetime.now()

    for task in tasks:
        # Display priority and tags in header
        tags_display = f"[{', '.join(task.tags)}]" if task.tags else "[]"
        print(f"\nID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}")
        print(f"   Tags: {tags_display}")
        if task.description:
            print(f"   Description: {task.description}")
        else:
            print("   Description: (no description)")

        # Display recurrence if not "none"
        if task.recurrence != "none":
            print(f"   Recurrence: {task.recurrence}")

        # Display due date with overdue indicator
        if task.due_date:
            due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
            if task.due_date < now and task.status != "completed":
                print(f"   Due date: {due_str} [OVERDUE]")
            else:
                print(f"   Due date: {due_str}")
        else:
            print("   Due date: No due date")


def handle_update_task(service: TaskService) -> None:
    """Handle updating a task.

    Args:
        service: The TaskService instance
    """
    print("\n--- Update Task ---")

    try:
        task_id = int(input("Enter task ID to update: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"Error: Task #{task_id} not found.")
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
            print("Warning: Invalid date format. Due date will not be changed.")
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
            print(f"Task #{task_id} updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete_task(service: TaskService) -> None:
    """Handle deleting a task.

    Args:
        service: The TaskService instance
    """
    print("\n--- Delete Task ---")

    try:
        task_id = int(input("Enter task ID to delete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if service.delete_task(task_id):
        print(f"Task #{task_id} deleted successfully.")
    else:
        print(f"Error: Task #{task_id} not found.")


def handle_mark_status(service: TaskService) -> None:
    """Handle changing task status.

    Args:
        service: The TaskService instance
    """
    print("\n--- Mark Status ---")

    try:
        task_id = int(input("Enter task ID: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"Error: Task #{task_id} not found.")
        return

    print(f"Current status: {task.status}")
    print(f"Valid statuses: {', '.join(Task.VALID_STATUSES)}")

    # Check if task is recurring before status change
    is_recurring = task.recurrence != "none"

    new_status = input("Enter new status: ").strip().lower()

    try:
        updated = service.update_status(task_id, new_status)
        if updated:
            print(f"Task #{task_id} status changed to '{new_status}'.")
            # Show auto-generation message if recurring task was completed
            if new_status == "completed" and is_recurring:
                print(f"Auto-generated next occurrence of recurring task (recurrence: {task.recurrence}).")
    except ValueError as e:
        print(f"Error: {e}")


def handle_manage_tags(service: TaskService) -> None:
    """Handle adding or removing tags from a task.

    Args:
        service: The TaskService instance
    """
    print("\n--- Manage Tags ---")

    try:
        task_id = int(input("Enter task ID: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"Error: Task #{task_id} not found.")
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
                print(f"Tags added. Current tags: {', '.join(updated.tags)}")
    elif choice == "2":
        if not task.tags:
            print("No tags to remove.")
            return
        tag_to_remove = input("Enter tag to remove: ").strip()
        updated = service.remove_tag_from_task(task_id, tag_to_remove)
        if updated:
            print(f"Tag removed. Current tags: {', '.join(updated.tags) if updated.tags else '(no tags)'}")
    elif choice == "3":
        print("Cancelled.")
    else:
        print("Invalid choice.")


def handle_search_tasks(service: TaskService) -> None:
    """Handle searching tasks by keyword.

    Args:
        service: The TaskService instance
    """
    print("\n--- Search Tasks ---")
    keyword = input("Enter search keyword: ").strip()

    results = service.search_tasks(keyword)

    if not results:
        print("No tasks found matching your search.")
        return

    print(f"\nFound {len(results)} task(s):")
    for task in results:
        tags_display = f"[{', '.join(task.tags)}]" if task.tags else "[]"
        print(f"\nID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}")
        print(f"   Tags: {tags_display}")
        if task.description:
            print(f"   Description: {task.description}")
        else:
            print("   Description: (no description)")


def handle_filter_tasks(service: TaskService) -> None:
    """Handle filtering tasks by status, priority, or tag.

    Args:
        service: The TaskService instance
    """
    print("\n--- Filter Tasks ---")
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
        print("Cancelled.")
        return
    else:
        print("Invalid choice.")
        return

    if not results:
        print(f"No tasks found matching filter: {filter_label}")
        return

    print(f"\nFound {len(results)} task(s) matching {filter_label}:")
    for task in results:
        tags_display = f"[{', '.join(task.tags)}]" if task.tags else "[]"
        print(f"\nID: {task.id} | Title: {task.title} | Status: {task.status} | Priority: {task.priority}")
        print(f"   Tags: {tags_display}")
        if task.description:
            print(f"   Description: {task.description}")
        else:
            print("   Description: (no description)")


def handle_sort_tasks(service: TaskService) -> None:
    """Handle setting sort preference for task list.

    Args:
        service: The TaskService instance
    """
    print("\n--- Sort Tasks ---")
    print("Sort by:")
    print("1. Priority (high to low)")
    print("2. Title (A-Z)")
    print("3. Creation date (oldest first)")
    print("4. Clear sort (default order)")
    print("5. Cancel")

    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":
        service.set_sort_preference("priority")
        print("Tasks will now be sorted by priority (high to low).")
    elif choice == "2":
        service.set_sort_preference("title")
        print("Tasks will now be sorted alphabetically by title.")
    elif choice == "3":
        service.set_sort_preference("created")
        print("Tasks will now be sorted by creation date (oldest first).")
    elif choice == "4":
        service.set_sort_preference("none")
        print("Sort preference cleared. Tasks will be shown in default order.")
    elif choice == "5":
        print("Cancelled.")
    else:
        print("Invalid choice.")


def handle_check_reminders(service: TaskService) -> None:
    """Display overdue and soon-due tasks.

    Args:
        service: The TaskService instance
    """
    print("\n--- Check Reminders ---")

    overdue = service.get_overdue_tasks()
    soon_due = service.get_soon_due_tasks(24)

    if not overdue and not soon_due:
        print("No overdue or upcoming tasks.")
        return

    now = datetime.now()

    if overdue:
        print("\n** Overdue Tasks **")
        for task in overdue:
            # Calculate how long overdue
            time_diff = now - task.due_date
            days = time_diff.days
            hours = time_diff.seconds // 3600

            if days > 0:
                overdue_str = f"{days} day(s) overdue"
            else:
                overdue_str = f"{hours} hour(s) overdue"

            print(f"\nID: {task.id} | Title: {task.title} | Priority: {task.priority}")
            print(f"   Due: {task.due_date.strftime('%Y-%m-%d %H:%M')} ({overdue_str})")
            print(f"   Status: {task.status}")

    if soon_due:
        print("\n** Due Soon (within 24 hours) **")
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

            print(f"\nID: {task.id} | Title: {task.title} | Priority: {task.priority}")
            print(f"   Due: {task.due_date.strftime('%Y-%m-%d %H:%M')} ({remaining_str})")
            print(f"   Status: {task.status}")
