"""Comprehensive test suite for Phase I Todo App."""

from src.models.task import Task
from src.services.task_service import TaskService


class TestResults:
    """Track test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def record(self, test_name: str, passed: bool, message: str = ""):
        """Record a test result."""
        self.tests.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
            print(f"[PASS] {test_name}")
        else:
            self.failed += 1
            print(f"[FAIL] {test_name}")
            if message:
                print(f"  -> {message}")

    def summary(self):
        """Print summary of test results."""
        total = self.passed + self.failed
        print("\n" + "="*70)
        print(f"TEST SUMMARY: {self.passed}/{total} passed, {self.failed}/{total} failed")
        print("="*70)

        if self.failed > 0:
            print("\nFailed tests:")
            for test in self.tests:
                if not test["passed"]:
                    print(f"  - {test['name']}")
                    if test["message"]:
                        print(f"    {test['message']}")


def test_us1_add_task():
    """US1 - Add Task acceptance scenarios."""
    print("\n" + "="*70)
    print("US1 - ADD TASK")
    print("="*70)

    results = TestResults()

    # Scenario 1: Add task with title and description
    service = TaskService()
    try:
        task = service.add_task("Buy milk", "Get 2% milk from store")
        results.record(
            "US1.1: Add task with title and description",
            task.id == 1 and task.title == "Buy milk" and task.description == "Get 2% milk from store",
            f"Expected ID=1, got {task.id}"
        )
    except Exception as e:
        results.record("US1.1: Add task with title and description", False, str(e))

    # Scenario 2: Add task with empty description
    try:
        task2 = service.add_task("Read book", "")
        results.record(
            "US1.2: Add task with empty description",
            task2.id == 2 and task2.description == "",
            f"Expected ID=2 with empty desc, got ID={task2.id}, desc='{task2.description}'"
        )
    except Exception as e:
        results.record("US1.2: Add task with empty description", False, str(e))

    # Scenario 3: Add task with empty title (should fail)
    try:
        task3 = service.add_task("", "Some description")
        results.record(
            "US1.3: Add task with empty title (should error)",
            False,
            "Expected ValueError but task was created"
        )
    except ValueError as e:
        results.record(
            "US1.3: Add task with empty title (should error)",
            "empty" in str(e).lower(),
            f"Got error: {e}"
        )

    # Verify unique IDs
    try:
        task4 = service.add_task("Third task", "")
        results.record(
            "US1.4: Verify unique auto-incrementing IDs",
            task4.id == 3,
            f"Expected ID=3, got {task4.id}"
        )
    except Exception as e:
        results.record("US1.4: Verify unique auto-incrementing IDs", False, str(e))

    return results


def test_us2_list_tasks():
    """US2 - List Tasks acceptance scenarios."""
    print("\n" + "="*70)
    print("US2 - LIST TASKS")
    print("="*70)

    results = TestResults()

    # Scenario 1: List when tasks exist
    service = TaskService()
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "")

    tasks = service.list_tasks()
    results.record(
        "US2.1: List when tasks exist",
        len(tasks) == 2 and tasks[0].id == 1 and tasks[1].id == 2,
        f"Expected 2 tasks, got {len(tasks)}"
    )

    # Verify all fields shown
    task = tasks[0]
    results.record(
        "US2.2: Verify all fields present (ID, title, description, status)",
        hasattr(task, 'id') and hasattr(task, 'title') and
        hasattr(task, 'description') and hasattr(task, 'status'),
        "Missing required fields"
    )

    # Scenario 2: List when empty
    empty_service = TaskService()
    empty_tasks = empty_service.list_tasks()
    results.record(
        "US2.3: List when empty",
        len(empty_tasks) == 0,
        f"Expected 0 tasks, got {len(empty_tasks)}"
    )

    return results


def test_us3_update_task():
    """US3 - Update Task acceptance scenarios."""
    print("\n" + "="*70)
    print("US3 - UPDATE TASK")
    print("="*70)

    results = TestResults()

    service = TaskService()
    task = service.add_task("Original title", "Original description")

    # Scenario 1: Update title only
    updated = service.update_task(1, title="New title", description=None)
    results.record(
        "US3.1: Update title only (skip description)",
        updated and updated.title == "New title" and updated.description == "Original description",
        f"Title: {updated.title if updated else 'None'}, Desc: {updated.description if updated else 'None'}"
    )

    # Scenario 2: Update description only
    updated = service.update_task(1, title=None, description="New description")
    results.record(
        "US3.2: Update description only (skip title)",
        updated and updated.title == "New title" and updated.description == "New description",
        f"Title: {updated.title if updated else 'None'}, Desc: {updated.description if updated else 'None'}"
    )

    # Scenario 3: Update non-existent ID
    updated = service.update_task(999, title="Test")
    results.record(
        "US3.3: Update non-existent ID (should return None)",
        updated is None,
        f"Expected None, got {updated}"
    )

    # Edge case: Update with empty title (should fail)
    try:
        service.update_task(1, title="", description=None)
        results.record(
            "US3.4: Update with empty title (should error)",
            False,
            "Expected ValueError but update succeeded"
        )
    except ValueError as e:
        results.record(
            "US3.4: Update with empty title (should error)",
            "empty" in str(e).lower(),
            f"Got error: {e}"
        )

    return results


def test_us4_delete_task():
    """US4 - Delete Task acceptance scenarios."""
    print("\n" + "="*70)
    print("US4 - DELETE TASK")
    print("="*70)

    results = TestResults()

    service = TaskService()
    service.add_task("Task 1", "")
    service.add_task("Task 2", "")

    # Scenario 1: Delete existing task
    deleted = service.delete_task(1)
    remaining = service.list_tasks()
    results.record(
        "US4.1: Delete existing task",
        deleted and len(remaining) == 1 and remaining[0].id == 2,
        f"Deleted={deleted}, Remaining tasks: {len(remaining)}"
    )

    # Scenario 2: Delete non-existent ID
    deleted = service.delete_task(999)
    results.record(
        "US4.2: Delete non-existent ID (should return False)",
        not deleted,
        f"Expected False, got {deleted}"
    )

    return results


def test_us5_mark_status():
    """US5 - Mark Status acceptance scenarios."""
    print("\n" + "="*70)
    print("US5 - MARK STATUS")
    print("="*70)

    results = TestResults()

    service = TaskService()
    task = service.add_task("Test task", "")

    # Verify initial status
    results.record(
        "US5.0: Initial status is 'pending'",
        task.status == "pending",
        f"Expected 'pending', got '{task.status}'"
    )

    # Scenario 1: Mark as in-progress
    updated = service.update_status(1, "in-progress")
    results.record(
        "US5.1: Mark as in-progress",
        updated and updated.status == "in-progress",
        f"Expected 'in-progress', got '{updated.status if updated else 'None'}'"
    )

    # Scenario 2: Mark as completed
    updated = service.update_status(1, "completed")
    results.record(
        "US5.2: Mark as completed",
        updated and updated.status == "completed",
        f"Expected 'completed', got '{updated.status if updated else 'None'}'"
    )

    # Scenario 3: Invalid status
    try:
        service.update_status(1, "invalid-status")
        results.record(
            "US5.3: Invalid status (should error)",
            False,
            "Expected ValueError but update succeeded"
        )
    except ValueError as e:
        error_msg = str(e).lower()
        has_error_info = "invalid" in error_msg or "must be one of" in error_msg
        results.record(
            "US5.3: Invalid status (should error with valid options)",
            has_error_info,
            f"Got error: {e}"
        )

    # Scenario 4: Update status of non-existent task
    updated = service.update_status(999, "completed")
    results.record(
        "US5.4: Update status of non-existent task (should return None)",
        updated is None,
        f"Expected None, got {updated}"
    )

    return results


def test_edge_cases():
    """Additional edge cases."""
    print("\n" + "="*70)
    print("EDGE CASES")
    print("="*70)

    results = TestResults()

    service = TaskService()

    # Whitespace handling in title
    try:
        task = service.add_task("   ", "desc")
        results.record(
            "EDGE.1: Title with only whitespace (should error)",
            False,
            "Expected ValueError but task was created"
        )
    except ValueError as e:
        results.record(
            "EDGE.1: Title with only whitespace (should error)",
            "empty" in str(e).lower(),
            f"Got error: {e}"
        )

    # Valid statuses check
    results.record(
        "EDGE.2: Valid statuses defined",
        Task.VALID_STATUSES == ("pending", "in-progress", "completed"),
        f"Got: {Task.VALID_STATUSES}"
    )

    # Task immutability of ID
    task = service.add_task("Test", "")
    original_id = task.id
    task.title = "Changed"
    results.record(
        "EDGE.3: Task ID remains unchanged after modification",
        task.id == original_id,
        f"ID changed from {original_id} to {task.id}"
    )

    # List returns copy (non-mutating)
    service2 = TaskService()
    service2.add_task("Task 1", "")
    tasks1 = service2.list_tasks()
    tasks2 = service2.list_tasks()
    results.record(
        "EDGE.4: list_tasks returns independent copy",
        tasks1 is not tasks2,
        "Same list object returned (should be copy)"
    )

    return results


def test_data_model():
    """Test data model compliance."""
    print("\n" + "="*70)
    print("DATA MODEL COMPLIANCE")
    print("="*70)

    results = TestResults()

    # Test Task model attributes
    task = Task(id=1, title="Test", description="Desc", status="pending")
    results.record(
        "MODEL.1: Task has required attributes",
        hasattr(task, 'id') and hasattr(task, 'title') and
        hasattr(task, 'description') and hasattr(task, 'status'),
        "Missing required attributes"
    )

    # Test default status
    task2 = Task(id=2, title="Test2", description="")
    results.record(
        "MODEL.2: Default status is 'pending'",
        task2.status == "pending",
        f"Expected 'pending', got '{task2.status}'"
    )

    # Test invalid status validation
    try:
        task3 = Task(id=3, title="Test3", description="", status="bad-status")
        results.record(
            "MODEL.3: Invalid status rejected",
            False,
            "Expected ValueError but task was created"
        )
    except ValueError as e:
        results.record(
            "MODEL.3: Invalid status rejected",
            "invalid" in str(e).lower(),
            f"Got error: {e}"
        )

    return results


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("PHASE I TODO APP - COMPREHENSIVE TEST SUITE")
    print("="*70)

    all_results = []

    # Run all test suites
    all_results.append(test_us1_add_task())
    all_results.append(test_us2_list_tasks())
    all_results.append(test_us3_update_task())
    all_results.append(test_us4_delete_task())
    all_results.append(test_us5_mark_status())
    all_results.append(test_edge_cases())
    all_results.append(test_data_model())

    # Aggregate results
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed

    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%")
    print("="*70)

    if total_failed > 0:
        print("\nFailed tests:")
        for result_set in all_results:
            for test in result_set.tests:
                if not test["passed"]:
                    print(f"  - {test['name']}")
                    if test["message"]:
                        print(f"    {test['message']}")
    else:
        print("\nALL TESTS PASSED!")

    return total_failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
