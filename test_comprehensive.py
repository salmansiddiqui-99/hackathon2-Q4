"""Comprehensive test suite for Todo Console Application.

Tests all features including new Phase 2 enhancements:
- Model validation
- Date parser
- Recurrence calculation
- Task service operations
- Backward compatibility
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Test counters
total_tests = 0
passed_tests = 0
failed_tests = 0


def test_result(name: str, condition: bool, details: str = "") -> None:
    """Record test result."""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    if condition:
        passed_tests += 1
        print(f"  PASS: {name}")
        if details:
            print(f"        {details}")
    else:
        failed_tests += 1
        print(f"  FAIL: {name}")
        if details:
            print(f"        {details}")


def print_section(title: str) -> None:
    """Print test section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)


# ========== TEST 1: MODEL TESTS ==========
print_section("TEST 1: MODEL TESTS")

try:
    from src.models.task import Task
    print("  Successfully imported Task model")

    # Test 1.1: Create Task with all fields
    try:
        task = Task(
            id=1,
            title="Test Task",
            description="Test description",
            priority="high",
            tags=["work", "urgent"],
            recurrence="daily",
            due_date=datetime.now()
        )
        test_result(
            "Create Task with all fields",
            task.title == "Test Task" and task.recurrence == "daily",
            f"Task created: {task.title}"
        )
    except Exception as e:
        test_result("Create Task with all fields", False, f"Error: {e}")

    # Test 1.2: Validate VALID_RECURRENCES constant exists
    try:
        test_result(
            "VALID_RECURRENCES constant exists",
            hasattr(Task, 'VALID_RECURRENCES'),
            f"Value: {Task.VALID_RECURRENCES if hasattr(Task, 'VALID_RECURRENCES') else 'N/A'}"
        )
    except Exception as e:
        test_result("VALID_RECURRENCES constant exists", False, f"Error: {e}")

    # Test 1.3: Validate recurrence validation works
    try:
        Task(id=2, title="Test", description="", recurrence="invalid")
        test_result("Recurrence validation", False, "Should reject invalid recurrence")
    except ValueError as e:
        test_result("Recurrence validation", True, f"Correctly rejected: {str(e)[:50]}")
    except Exception as e:
        test_result("Recurrence validation", False, f"Unexpected error: {e}")

    # Test 1.4: Validate empty title rejection
    try:
        Task(id=3, title="   ", description="")
        test_result("Empty title rejection", False, "Should reject empty title")
    except ValueError:
        test_result("Empty title rejection", True, "Correctly rejected empty title")
    except Exception as e:
        test_result("Empty title rejection", False, f"Unexpected error: {e}")

except Exception as e:
    print(f"  FAIL: Could not import Task model: {e}")


# ========== TEST 2: DATE PARSER TESTS ==========
print_section("TEST 2: DATE PARSER TESTS")

try:
    from src.utils.date_parser import parse_natural_date
    print("  Successfully imported parse_natural_date")

    # Test 2.1: Parse "today"
    try:
        result = parse_natural_date("today")
        test_result(
            "parse_natural_date('today')",
            result is not None and isinstance(result, datetime),
            f"Returns: {result}"
        )
    except Exception as e:
        test_result("parse_natural_date('today')", False, f"Error: {e}")

    # Test 2.2: Parse "tomorrow"
    try:
        result = parse_natural_date("tomorrow")
        expected_day = (datetime.now() + timedelta(days=1)).day
        test_result(
            "parse_natural_date('tomorrow')",
            result is not None and result.day == expected_day,
            f"Returns: {result}"
        )
    except Exception as e:
        test_result("parse_natural_date('tomorrow')", False, f"Error: {e}")

    # Test 2.3: Parse ISO date "2025-01-15"
    try:
        result = parse_natural_date("2025-01-15")
        test_result(
            "parse_natural_date('2025-01-15')",
            result is not None and result.year == 2025 and result.month == 1 and result.day == 15,
            f"Returns: {result}"
        )
    except Exception as e:
        test_result("parse_natural_date('2025-01-15')", False, f"Error: {e}")

    # Test 2.4: Parse ISO datetime "2025-01-15 14:30"
    try:
        result = parse_natural_date("2025-01-15 14:30")
        test_result(
            "parse_natural_date('2025-01-15 14:30')",
            result is not None and result.hour == 14 and result.minute == 30,
            f"Returns: {result}"
        )
    except Exception as e:
        test_result("parse_natural_date('2025-01-15 14:30')", False, f"Error: {e}")

    # Test 2.5: Parse invalid input
    try:
        result = parse_natural_date("invalid")
        test_result(
            "parse_natural_date('invalid')",
            result is None,
            f"Returns: {result}"
        )
    except Exception as e:
        test_result("parse_natural_date('invalid')", False, f"Error: {e}")

    # Test 2.6: Parse "next monday"
    try:
        result = parse_natural_date("next monday")
        test_result(
            "parse_natural_date('next monday')",
            result is not None and result.weekday() == 0,
            f"Returns: {result}, weekday={result.weekday() if result else 'N/A'}"
        )
    except Exception as e:
        test_result("parse_natural_date('next monday')", False, f"Error: {e}")

except Exception as e:
    print(f"  FAIL: Could not import date_parser: {e}")


# ========== TEST 3: RECURRENCE TESTS ==========
print_section("TEST 3: RECURRENCE TESTS")

try:
    from src.utils.recurrence import calculate_next_due_date
    print("  Successfully imported calculate_next_due_date")

    # Test 3.1: Daily recurrence
    try:
        base = datetime(2025, 1, 15, 9, 0)
        result = calculate_next_due_date(base, "daily")
        expected = datetime(2025, 1, 16, 9, 0)
        test_result(
            "calculate_next_due_date with daily",
            result == expected,
            f"Base: {base} -> Next: {result}"
        )
    except Exception as e:
        test_result("calculate_next_due_date with daily", False, f"Error: {e}")

    # Test 3.2: Weekly recurrence
    try:
        base = datetime(2025, 1, 15, 9, 0)
        result = calculate_next_due_date(base, "weekly")
        expected = datetime(2025, 1, 22, 9, 0)
        test_result(
            "calculate_next_due_date with weekly",
            result == expected,
            f"Base: {base} -> Next: {result}"
        )
    except Exception as e:
        test_result("calculate_next_due_date with weekly", False, f"Error: {e}")

    # Test 3.3: Monthly recurrence
    try:
        base = datetime(2025, 1, 15, 9, 0)
        result = calculate_next_due_date(base, "monthly")
        expected = datetime(2025, 2, 15, 9, 0)
        test_result(
            "calculate_next_due_date with monthly",
            result == expected,
            f"Base: {base} -> Next: {result}"
        )
    except Exception as e:
        test_result("calculate_next_due_date with monthly", False, f"Error: {e}")

    # Test 3.4: None base date (uses today)
    try:
        result = calculate_next_due_date(None, "daily")
        test_result(
            "calculate_next_due_date with None base",
            result is not None and isinstance(result, datetime),
            f"Result: {result}"
        )
    except Exception as e:
        test_result("calculate_next_due_date with None base", False, f"Error: {e}")

    # Test 3.5: Month boundary handling (Jan 31 -> Feb 28/29)
    try:
        base = datetime(2025, 1, 31, 9, 0)
        result = calculate_next_due_date(base, "monthly")
        # Feb 2025 has 28 days
        expected = datetime(2025, 2, 28, 9, 0)
        test_result(
            "calculate_next_due_date month boundary",
            result == expected,
            f"Jan 31 -> {result}"
        )
    except Exception as e:
        test_result("calculate_next_due_date month boundary", False, f"Error: {e}")

except Exception as e:
    print(f"  FAIL: Could not import recurrence module: {e}")


# ========== TEST 4: SERVICE TESTS ==========
print_section("TEST 4: SERVICE TESTS")

try:
    from src.services.task_service import TaskService
    print("  Successfully imported TaskService")

    service = TaskService()

    # Test 4.1: Add task with recurrence and due_date
    try:
        due = datetime(2025, 1, 20, 14, 0)
        task = service.add_task(
            title="Recurring Task",
            description="Test recurring",
            recurrence="daily",
            due_date=due
        )
        test_result(
            "add_task with recurrence and due_date",
            task.recurrence == "daily" and task.due_date == due,
            f"Task #{task.id}: {task.title}, recurrence={task.recurrence}"
        )
    except Exception as e:
        test_result("add_task with recurrence and due_date", False, f"Error: {e}")

    # Test 4.2: Update task with recurrence and due_date
    try:
        new_due = datetime(2025, 1, 25, 10, 0)
        updated = service.update_task(1, recurrence="weekly", due_date=new_due)
        test_result(
            "update_task with recurrence and due_date",
            updated is not None and updated.recurrence == "weekly" and updated.due_date == new_due,
            f"Updated: recurrence={updated.recurrence if updated else 'N/A'}"
        )
    except Exception as e:
        test_result("update_task with recurrence and due_date", False, f"Error: {e}")

    # Test 4.3: Auto-generation for recurring tasks
    try:
        # Add a daily recurring task
        task = service.add_task(
            title="Daily Exercise",
            recurrence="daily",
            due_date=datetime(2025, 1, 15, 9, 0)
        )
        task_id = task.id
        initial_count = len(service.list_tasks())

        # Mark as completed - should trigger auto-generation
        service.update_status(task_id, "completed")
        new_count = len(service.list_tasks())

        test_result(
            "update_status triggers auto-generation",
            new_count == initial_count + 1,
            f"Tasks before: {initial_count}, after: {new_count}"
        )
    except Exception as e:
        test_result("update_status triggers auto-generation", False, f"Error: {e}")

    # Test 4.4: Get overdue tasks
    try:
        # Add overdue task
        past_due = datetime.now() - timedelta(days=1)
        overdue_task = service.add_task(
            title="Overdue Task",
            due_date=past_due
        )

        overdue = service.get_overdue_tasks()
        test_result(
            "get_overdue_tasks",
            len(overdue) > 0 and any(t.id == overdue_task.id for t in overdue),
            f"Found {len(overdue)} overdue task(s)"
        )
    except Exception as e:
        test_result("get_overdue_tasks", False, f"Error: {e}")

    # Test 4.5: Get soon due tasks
    try:
        # Add task due in 12 hours
        soon_due = datetime.now() + timedelta(hours=12)
        soon_task = service.add_task(
            title="Soon Task",
            due_date=soon_due
        )

        soon = service.get_soon_due_tasks(hours=24)
        test_result(
            "get_soon_due_tasks",
            len(soon) > 0 and any(t.id == soon_task.id for t in soon),
            f"Found {len(soon)} task(s) due soon"
        )
    except Exception as e:
        test_result("get_soon_due_tasks", False, f"Error: {e}")

except Exception as e:
    print(f"  FAIL: Could not import TaskService: {e}")


# ========== TEST 5: BACKWARD COMPATIBILITY ==========
print_section("TEST 5: BACKWARD COMPATIBILITY")

try:
    service2 = TaskService()

    # Test 5.1: Basic add/list/update/delete
    try:
        task = service2.add_task("Basic Task", "Description")
        task_id = task.id
        tasks = service2.list_tasks()
        service2.update_task(task_id, title="Updated Task")
        deleted = service2.delete_task(task_id)

        test_result(
            "Basic add/list/update/delete",
            len(tasks) == 1 and deleted,
            "All basic operations work"
        )
    except Exception as e:
        test_result("Basic add/list/update/delete", False, f"Error: {e}")

    # Test 5.2: Priority/tags
    try:
        task = service2.add_task(
            "Tagged Task",
            priority="high",
            tags=["work", "urgent"]
        )
        test_result(
            "Priority/tags",
            task.priority == "high" and "work" in task.tags,
            f"Priority: {task.priority}, Tags: {task.tags}"
        )
    except Exception as e:
        test_result("Priority/tags", False, f"Error: {e}")

    # Test 5.3: Search/filter/sort
    try:
        service2.add_task("Search Test 1", "Find me", tags=["test"])
        service2.add_task("Search Test 2", "Find me too", priority="low")

        search_results = service2.search_tasks("Find")
        filter_results = service2.filter_tasks("tag", "test")
        service2.set_sort_preference("priority")
        sorted_tasks = service2.get_sorted_tasks()

        test_result(
            "Search/filter/sort",
            len(search_results) >= 2 and len(filter_results) >= 1 and len(sorted_tasks) >= 2,
            f"Search: {len(search_results)}, Filter: {len(filter_results)}, Sorted: {len(sorted_tasks)}"
        )
    except Exception as e:
        test_result("Search/filter/sort", False, f"Error: {e}")

    # Test 5.4: Status updates
    try:
        task = service2.add_task("Status Test")
        service2.update_status(task.id, "in-progress")
        updated = service2.get_task(task.id)

        test_result(
            "Status updates",
            updated is not None and updated.status == "in-progress",
            f"Status: {updated.status if updated else 'N/A'}"
        )
    except Exception as e:
        test_result("Status updates", False, f"Error: {e}")

    # Test 5.5: Tag operations
    try:
        task = service2.add_task("Tag Operations")
        service2.add_tags_to_task(task.id, ["new", "tag"])
        task_with_tags = service2.get_task(task.id)
        has_new_tag = task_with_tags and "new" in task_with_tags.tags

        service2.remove_tag_from_task(task.id, "new")
        task_after_removal = service2.get_task(task.id)
        removed_new_tag = task_after_removal and "new" not in task_after_removal.tags
        still_has_tag = task_after_removal and "tag" in task_after_removal.tags

        test_result(
            "Tag operations (add/remove)",
            has_new_tag and removed_new_tag and still_has_tag,
            f"Tags after add: {task_with_tags.tags if task_with_tags else 'N/A'}, after remove: {task_after_removal.tags if task_after_removal else 'N/A'}"
        )
    except Exception as e:
        test_result("Tag operations (add/remove)", False, f"Error: {e}")

except Exception as e:
    print(f"  FAIL: Could not test backward compatibility: {e}")


# ========== TEST 6: MAIN ENTRY POINT ==========
print_section("TEST 6: MAIN ENTRY POINT")

try:
    from src import main
    test_result(
        "Import src.main module",
        True,
        "Main module loads successfully"
    )
except Exception as e:
    test_result("Import src.main module", False, f"Error: {e}")


# ========== SUMMARY ==========
print_section("TEST SUMMARY")
print(f"\n  Total Tests:  {total_tests}")
print(f"  Passed:       {passed_tests} ({100*passed_tests//total_tests if total_tests > 0 else 0}%)")
print(f"  Failed:       {failed_tests} ({100*failed_tests//total_tests if total_tests > 0 else 0}%)")

if failed_tests == 0:
    print("\n  ALL TESTS PASSED!")
    sys.exit(0)
else:
    print(f"\n  {failed_tests} TEST(S) FAILED")
    sys.exit(1)
