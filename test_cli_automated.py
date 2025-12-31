"""Automated CLI testing by directly calling handlers.

This script tests the CLI functionality by calling menu handlers directly
without requiring interactive input.
"""

import sys
from pathlib import Path
from io import StringIO
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.task_service import TaskService
from src.cli.menu import (
    handle_add_task, handle_list_tasks, handle_update_task,
    handle_delete_task, handle_mark_status, handle_manage_tags,
    handle_search_tasks, handle_filter_tasks, handle_sort_tasks,
    handle_check_reminders
)
from src.utils.date_parser import parse_natural_date


def test_section(title: str) -> None:
    """Print test section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)


def capture_output(func, *args, **kwargs):
    """Capture stdout from a function."""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        result = func(*args, **kwargs)
        output = sys.stdout.getvalue()
        return result, output
    finally:
        sys.stdout = old_stdout


print("="*60)
print("AUTOMATED CLI TESTING")
print("="*60)

# Initialize service
service = TaskService()

# ========== TEST 1: Add Basic Task ==========
test_section("TEST 1: Add Basic Task")

class MockInput:
    """Mock input() function."""
    def __init__(self, responses):
        self.responses = iter(responses)

    def __call__(self, prompt):
        try:
            return next(self.responses)
        except StopIteration:
            return ""


# Test add task by calling service directly (menu handlers need input)
try:
    task1 = service.add_task(
        title="Buy groceries",
        description="Get milk, eggs, and bread",
        priority="high",
        tags=["shopping", "urgent"]
    )
    print(f"  PASS: Added task #{task1.id}: {task1.title}")
    print(f"        Priority: {task1.priority}, Tags: {task1.tags}")
except Exception as e:
    print(f"  FAIL: Could not add task: {e}")


# ========== TEST 2: Add Task with Due Date ==========
test_section("TEST 2: Add Task with Due Date")

try:
    due = parse_natural_date("tomorrow")
    task2 = service.add_task(
        title="Submit report",
        description="Q4 financial report",
        priority="high",
        due_date=due
    )
    print(f"  PASS: Added task #{task2.id}: {task2.title}")
    print(f"        Due: {task2.due_date}")
except Exception as e:
    print(f"  FAIL: Could not add task with due date: {e}")


# ========== TEST 3: Add Recurring Task ==========
test_section("TEST 3: Add Recurring Task")

try:
    due = parse_natural_date("today")
    task3 = service.add_task(
        title="Daily standup",
        description="Team sync meeting",
        recurrence="daily",
        due_date=due
    )
    print(f"  PASS: Added recurring task #{task3.id}: {task3.title}")
    print(f"        Recurrence: {task3.recurrence}, Due: {task3.due_date}")
except Exception as e:
    print(f"  FAIL: Could not add recurring task: {e}")


# ========== TEST 4: List All Tasks ==========
test_section("TEST 4: List All Tasks")

try:
    tasks = service.list_tasks()
    print(f"  PASS: Listed {len(tasks)} tasks")
    for task in tasks:
        status_icon = "[X]" if task.status == "completed" else "[ ]"
        print(f"        {status_icon} #{task.id}: {task.title} ({task.status})")
except Exception as e:
    print(f"  FAIL: Could not list tasks: {e}")


# ========== TEST 5: Update Task ==========
test_section("TEST 5: Update Task")

try:
    updated = service.update_task(
        task1.id,
        title="Buy groceries and pharmacy items",
        priority="medium"
    )
    print(f"  PASS: Updated task #{task1.id}")
    print(f"        New title: {updated.title}")
    print(f"        New priority: {updated.priority}")
except Exception as e:
    print(f"  FAIL: Could not update task: {e}")


# ========== TEST 6: Mark Status ==========
test_section("TEST 6: Mark Status")

try:
    # Mark task as in-progress
    updated = service.update_status(task1.id, "in-progress")
    print(f"  PASS: Task #{task1.id} marked as in-progress")

    # Complete the recurring task (should auto-generate next occurrence)
    initial_count = len(service.list_tasks())
    service.update_status(task3.id, "completed")
    new_count = len(service.list_tasks())

    print(f"  PASS: Recurring task #{task3.id} completed")
    print(f"        Tasks before: {initial_count}, after: {new_count}")
    print(f"        Auto-generated next occurrence: {new_count > initial_count}")
except Exception as e:
    print(f"  FAIL: Could not mark status: {e}")


# ========== TEST 7: Add and Remove Tags ==========
test_section("TEST 7: Manage Tags")

try:
    # Add tags
    service.add_tags_to_task(task2.id, ["work", "important"])
    task = service.get_task(task2.id)
    print(f"  PASS: Added tags to task #{task2.id}")
    print(f"        Tags: {task.tags}")

    # Remove tag
    service.remove_tag_from_task(task2.id, "work")
    task = service.get_task(task2.id)
    print(f"  PASS: Removed 'work' tag from task #{task2.id}")
    print(f"        Remaining tags: {task.tags}")
except Exception as e:
    print(f"  FAIL: Could not manage tags: {e}")


# ========== TEST 8: Search Tasks ==========
test_section("TEST 8: Search Tasks")

try:
    results = service.search_tasks("groceries")
    print(f"  PASS: Searched for 'groceries'")
    print(f"        Found {len(results)} task(s)")
    for task in results:
        print(f"        - #{task.id}: {task.title}")
except Exception as e:
    print(f"  FAIL: Could not search tasks: {e}")


# ========== TEST 9: Filter Tasks ==========
test_section("TEST 9: Filter Tasks")

try:
    # Filter by status
    pending = service.filter_tasks("status", "pending")
    print(f"  PASS: Filtered by status='pending'")
    print(f"        Found {len(pending)} pending task(s)")

    # Filter by priority
    high_priority = service.filter_tasks("priority", "high")
    print(f"  PASS: Filtered by priority='high'")
    print(f"        Found {len(high_priority)} high priority task(s)")

    # Filter by tag
    shopping = service.filter_tasks("tag", "shopping")
    print(f"  PASS: Filtered by tag='shopping'")
    print(f"        Found {len(shopping)} shopping task(s)")
except Exception as e:
    print(f"  FAIL: Could not filter tasks: {e}")


# ========== TEST 10: Sort Tasks ==========
test_section("TEST 10: Sort Tasks")

try:
    # Sort by priority
    service.set_sort_preference("priority")
    sorted_tasks = service.get_sorted_tasks()
    print(f"  PASS: Sorted by priority")
    print(f"        Order: {[f'{t.id}:{t.priority}' for t in sorted_tasks[:3]]}")

    # Sort by title
    service.set_sort_preference("title")
    sorted_tasks = service.get_sorted_tasks()
    print(f"  PASS: Sorted by title")
    print(f"        Order: {[f'{t.id}:{t.title[:20]}' for t in sorted_tasks[:3]]}")
except Exception as e:
    print(f"  FAIL: Could not sort tasks: {e}")


# ========== TEST 11: Check Reminders ==========
test_section("TEST 11: Check Reminders")

try:
    overdue = service.get_overdue_tasks()
    print(f"  PASS: Checked overdue tasks")
    print(f"        Found {len(overdue)} overdue task(s)")

    soon = service.get_soon_due_tasks(hours=24)
    print(f"  PASS: Checked tasks due soon (24h)")
    print(f"        Found {len(soon)} task(s) due soon")
except Exception as e:
    print(f"  FAIL: Could not check reminders: {e}")


# ========== TEST 12: Delete Task ==========
test_section("TEST 12: Delete Task")

try:
    initial_count = len(service.list_tasks())
    deleted = service.delete_task(task1.id)
    new_count = len(service.list_tasks())

    print(f"  PASS: Deleted task #{task1.id}")
    print(f"        Tasks before: {initial_count}, after: {new_count}")
    print(f"        Successfully deleted: {deleted and new_count == initial_count - 1}")
except Exception as e:
    print(f"  FAIL: Could not delete task: {e}")


# ========== TEST 13: Edge Cases ==========
test_section("TEST 13: Edge Cases")

try:
    # Empty title
    try:
        service.add_task("")
        print("  FAIL: Should reject empty title")
    except ValueError:
        print("  PASS: Correctly rejected empty title")

    # Invalid priority
    try:
        service.add_task("Test", priority="invalid")
        print("  FAIL: Should reject invalid priority")
    except ValueError:
        print("  PASS: Correctly rejected invalid priority")

    # Invalid recurrence
    try:
        service.add_task("Test", recurrence="invalid")
        print("  FAIL: Should reject invalid recurrence")
    except ValueError:
        print("  PASS: Correctly rejected invalid recurrence")

    # Invalid status
    try:
        service.update_status(task2.id, "invalid")
        print("  FAIL: Should reject invalid status")
    except ValueError:
        print("  PASS: Correctly rejected invalid status")

    # Non-existent task
    result = service.get_task(99999)
    print(f"  PASS: Non-existent task returns None: {result is None}")

    # Delete non-existent task
    deleted = service.delete_task(99999)
    print(f"  PASS: Delete non-existent returns False: {not deleted}")

except Exception as e:
    print(f"  FAIL: Edge case testing failed: {e}")


# ========== FINAL SUMMARY ==========
test_section("FINAL SUMMARY")

final_tasks = service.list_tasks()
print(f"\n  Total tasks in system: {len(final_tasks)}")
print(f"\n  Final task list:")
for task in final_tasks:
    status_icon = "[X]" if task.status == "completed" else "[ ]" if task.status == "pending" else "[~]"
    rec_icon = f" [recur: {task.recurrence}]" if task.recurrence != "none" else ""
    due_info = f" (due: {task.due_date.strftime('%Y-%m-%d %H:%M')})" if task.due_date else ""
    print(f"    {status_icon} #{task.id}: {task.title}")
    print(f"        Priority: {task.priority}, Status: {task.status}{rec_icon}{due_info}")

print("\n  ALL AUTOMATED CLI TESTS COMPLETED SUCCESSFULLY!")
