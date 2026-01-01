"""Simulate CLI interactions to test the complete user journey."""

from io import StringIO
from unittest.mock import patch
from src.services.task_service import TaskService
from src.cli.menu import (
    handle_add_task,
    handle_list_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_status,
)


def simulate_add_task_with_description():
    """Test adding task with title and description."""
    print("\n--- Test: Add task with description ---")
    service = TaskService()

    user_inputs = ["Buy milk", "Get 2% milk from store"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_add_task(service)
            output = mock_stdout.getvalue()

    tasks = service.list_tasks()
    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
    assert tasks[0].title == "Buy milk"
    assert tasks[0].description == "Get 2% milk from store"
    assert "Task #1 created successfully" in output
    print("[PASS] Task added with description")


def simulate_add_task_empty_description():
    """Test adding task with empty description."""
    print("\n--- Test: Add task with empty description ---")
    service = TaskService()

    user_inputs = ["Read book", ""]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_add_task(service)
            output = mock_stdout.getvalue()

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == ""
    assert "Task #1 created successfully" in output
    print("[PASS] Task added with empty description")


def simulate_add_task_empty_title():
    """Test adding task with empty title."""
    print("\n--- Test: Add task with empty title (should fail) ---")
    service = TaskService()

    user_inputs = [""]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_add_task(service)
            output = mock_stdout.getvalue()

    tasks = service.list_tasks()
    assert len(tasks) == 0, "No task should be created"
    assert "Error: Title cannot be empty" in output
    print("[PASS] Empty title rejected with error message")


def simulate_list_tasks():
    """Test listing tasks."""
    print("\n--- Test: List tasks ---")
    service = TaskService()
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "")

    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        handle_list_tasks(service)
        output = mock_stdout.getvalue()

    assert "ID: 1" in output
    assert "Task 1" in output
    assert "Description 1" in output
    assert "ID: 2" in output
    assert "Task 2" in output
    assert "Status: pending" in output
    print("[PASS] All tasks listed with details")


def simulate_list_empty():
    """Test listing when no tasks exist."""
    print("\n--- Test: List empty tasks ---")
    service = TaskService()

    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        handle_list_tasks(service)
        output = mock_stdout.getvalue()

    assert "No tasks found" in output
    print("[PASS] Empty list shows appropriate message")


def simulate_update_title_only():
    """Test updating title only."""
    print("\n--- Test: Update title only ---")
    service = TaskService()
    service.add_task("Original", "Original desc")

    user_inputs = ["1", "New title", ""]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_update_task(service)
            output = mock_stdout.getvalue()

    task = service.get_task(1)
    assert task.title == "New title"
    assert task.description == "Original desc"
    assert "Task #1 updated successfully" in output
    print("[PASS] Title updated, description preserved")


def simulate_update_description_only():
    """Test updating description only."""
    print("\n--- Test: Update description only ---")
    service = TaskService()
    service.add_task("Title", "Original desc")

    user_inputs = ["1", "", "New description"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_update_task(service)
            output = mock_stdout.getvalue()

    task = service.get_task(1)
    assert task.title == "Title"
    assert task.description == "New description"
    assert "Task #1 updated successfully" in output
    print("[PASS] Description updated, title preserved")


def simulate_update_nonexistent():
    """Test updating non-existent task."""
    print("\n--- Test: Update non-existent task ---")
    service = TaskService()

    user_inputs = ["999"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_update_task(service)
            output = mock_stdout.getvalue()

    assert "Error: Task #999 not found" in output
    print("[PASS] Non-existent task error shown")


def simulate_update_invalid_id():
    """Test updating with non-numeric ID."""
    print("\n--- Test: Update with non-numeric ID ---")
    service = TaskService()

    user_inputs = ["abc"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_update_task(service)
            output = mock_stdout.getvalue()

    assert "Error: Please enter a valid numeric ID" in output
    print("[PASS] Non-numeric ID rejected")


def simulate_delete_task():
    """Test deleting task."""
    print("\n--- Test: Delete task ---")
    service = TaskService()
    service.add_task("Task 1", "")
    service.add_task("Task 2", "")

    user_inputs = ["1"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_delete_task(service)
            output = mock_stdout.getvalue()

    assert len(service.list_tasks()) == 1
    assert service.get_task(1) is None
    assert service.get_task(2) is not None
    assert "Task #1 deleted successfully" in output
    print("[PASS] Task deleted successfully")


def simulate_delete_nonexistent():
    """Test deleting non-existent task."""
    print("\n--- Test: Delete non-existent task ---")
    service = TaskService()

    user_inputs = ["999"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_delete_task(service)
            output = mock_stdout.getvalue()

    assert "Error: Task #999 not found" in output
    print("[PASS] Non-existent delete error shown")


def simulate_mark_status_in_progress():
    """Test marking task as in-progress."""
    print("\n--- Test: Mark as in-progress ---")
    service = TaskService()
    service.add_task("Task", "")

    user_inputs = ["1", "in-progress"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_mark_status(service)
            output = mock_stdout.getvalue()

    task = service.get_task(1)
    assert task.status == "in-progress"
    assert "status changed to 'in-progress'" in output
    print("[PASS] Status changed to in-progress")


def simulate_mark_status_completed():
    """Test marking task as completed."""
    print("\n--- Test: Mark as completed ---")
    service = TaskService()
    service.add_task("Task", "")

    user_inputs = ["1", "completed"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_mark_status(service)
            output = mock_stdout.getvalue()

    task = service.get_task(1)
    assert task.status == "completed"
    assert "status changed to 'completed'" in output
    print("[PASS] Status changed to completed")


def simulate_mark_invalid_status():
    """Test marking with invalid status."""
    print("\n--- Test: Mark with invalid status ---")
    service = TaskService()
    service.add_task("Task", "")

    user_inputs = ["1", "invalid"]
    with patch('builtins.input', side_effect=user_inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_mark_status(service)
            output = mock_stdout.getvalue()

    assert "Error: Invalid status" in output
    assert "pending" in output and "in-progress" in output and "completed" in output
    print("[PASS] Invalid status rejected with valid options shown")


def simulate_complete_user_journey():
    """Test a complete user journey."""
    print("\n--- Test: Complete user journey ---")
    service = TaskService()

    # Add tasks
    print("  1. Adding 3 tasks...")
    service.add_task("Morning workout", "30 min cardio")
    service.add_task("Review pull requests", "")
    service.add_task("Team meeting", "Discuss Q1 roadmap")
    assert len(service.list_tasks()) == 3

    # Mark task 1 as in-progress then completed
    print("  2. Marking task #1 in-progress then completed...")
    service.update_status(1, "in-progress")
    service.update_status(1, "completed")
    assert service.get_task(1).status == "completed"

    # Update task 2 title
    print("  3. Updating task #2 title...")
    service.update_task(2, title="Review and merge PRs")
    assert service.get_task(2).title == "Review and merge PRs"

    # Delete task 3
    print("  4. Deleting task #3...")
    service.delete_task(3)
    assert len(service.list_tasks()) == 2
    assert service.get_task(3) is None

    # Verify final state
    print("  5. Verifying final state...")
    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1 and tasks[0].status == "completed"
    assert tasks[1].id == 2 and tasks[1].status == "pending"

    print("[PASS] Complete user journey succeeded")


def main():
    """Run all CLI simulation tests."""
    print("="*70)
    print("CLI INTERACTION SIMULATION TESTS")
    print("="*70)

    tests = [
        simulate_add_task_with_description,
        simulate_add_task_empty_description,
        simulate_add_task_empty_title,
        simulate_list_tasks,
        simulate_list_empty,
        simulate_update_title_only,
        simulate_update_description_only,
        simulate_update_nonexistent,
        simulate_update_invalid_id,
        simulate_delete_task,
        simulate_delete_nonexistent,
        simulate_mark_status_in_progress,
        simulate_mark_status_completed,
        simulate_mark_invalid_status,
        simulate_complete_user_journey,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test.__name__}: {e}")

    print("\n" + "="*70)
    print(f"CLI SIMULATION SUMMARY: {passed}/{len(tests)} passed, {failed}/{len(tests)} failed")
    print("="*70)

    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
