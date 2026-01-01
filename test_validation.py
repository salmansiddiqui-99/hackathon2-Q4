"""Validation script for Phase 1 Intermediate Features."""

from src.services.task_service import TaskService
from src.models.task import Task


def test_backward_compatibility():
    """Test that all Basic Level features still work."""
    print("\n=== Testing Backward Compatibility (Basic Level Features) ===")
    service = TaskService()

    # Test 1: Add task with minimal params (backward compatible)
    print("\n[Test 1] Adding task with title and description only...")
    task1 = service.add_task("Buy groceries", "Milk, eggs, bread")
    assert task1.id == 1
    assert task1.title == "Buy groceries"
    assert task1.description == "Milk, eggs, bread"
    assert task1.status == "pending"
    assert task1.priority == "medium"  # Default
    assert task1.tags == []  # Default
    print(f"[OK] Task created: ID={task1.id}, Title={task1.title}, Priority={task1.priority}")

    # Test 2: List tasks
    print("\n[Test 2] Listing all tasks...")
    tasks = service.list_tasks()
    assert len(tasks) == 1
    print(f"[OK] Found {len(tasks)} task(s)")

    # Test 3: Update task (title and description)
    print("\n[Test 3] Updating task title and description...")
    updated = service.update_task(1, title="Buy groceries today", description="Milk, eggs, bread, cheese")
    assert updated is not None
    assert updated.title == "Buy groceries today"
    assert updated.description == "Milk, eggs, bread, cheese"
    print(f"[OK] Task updated: Title={updated.title}")

    # Test 4: Update status
    print("\n[Test 4] Marking task as in-progress...")
    status_updated = service.update_status(1, "in-progress")
    assert status_updated is not None
    assert status_updated.status == "in-progress"
    print(f"[OK] Status updated to: {status_updated.status}")

    # Test 5: Delete task
    print("\n[Test 5] Deleting a task...")
    service.add_task("Temporary task", "To be deleted")
    deleted = service.delete_task(2)
    assert deleted is True
    assert len(service.list_tasks()) == 1
    print("[OK] Task deleted successfully")

    print("\n[PASS] All Basic Level features working correctly!")


def test_intermediate_features():
    """Test all Intermediate Level features."""
    print("\n=== Testing Intermediate Level Features ===")
    service = TaskService()

    # US1: Priority Assignment
    print("\n[US1] Testing Priority Assignment...")
    high_task = service.add_task("Urgent report", "Due today", priority="high")
    assert high_task.priority == "high"
    print(f"[OK] High priority task: {high_task.title}")

    low_task = service.add_task("Read book", "Chapter 5", priority="low")
    assert low_task.priority == "low"
    print(f"[OK] Low priority task: {low_task.title}")

    # Test priority validation
    try:
        service.add_task("Invalid", "Test", priority="critical")
        assert False, "Should have raised ValueError for invalid priority"
    except ValueError as e:
        print(f"[OK] Priority validation works: {e}")

    # US2: Tags/Categories
    print("\n[US2] Testing Tags/Categories...")
    tagged_task = service.add_task(
        "Fix bug",
        "Authentication issue",
        priority="high",
        tags=["work", "urgent", "backend"]
    )
    assert len(tagged_task.tags) == 3
    assert "work" in tagged_task.tags
    assert "urgent" in tagged_task.tags
    assert "backend" in tagged_task.tags
    print(f"[OK] Task with tags: {tagged_task.tags}")

    # Test tag deduplication
    dup_task = service.add_task("Test", "Dup", tags=["work", "Work", "WORK"])
    assert len(dup_task.tags) == 1
    assert dup_task.tags[0] == "work"
    print(f"[OK] Tag deduplication works: {dup_task.tags}")

    # Test add tags to existing task
    service.add_tags_to_task(1, ["personal", "home"])
    task = service.get_task(1)
    assert "personal" in task.tags
    assert "home" in task.tags
    print(f"[OK] Added tags to existing task: {task.tags}")

    # Test remove tag
    service.remove_tag_from_task(1, "personal")
    task = service.get_task(1)
    assert "personal" not in task.tags
    assert "home" in task.tags
    print(f"[OK] Removed tag from task: {task.tags}")

    # US3: Search Tasks
    print("\n[US3] Testing Search...")
    results = service.search_tasks("report")
    assert len(results) == 1
    assert results[0].title == "Urgent report"
    print(f"[OK] Search by title: found {len(results)} task(s)")

    results = service.search_tasks("authentication")
    assert len(results) == 1
    assert results[0].title == "Fix bug"
    print(f"[OK] Search by description: found {len(results)} task(s)")

    results = service.search_tasks("work")
    assert len(results) >= 1  # At least one task with 'work' tag
    print(f"[OK] Search by tag: found {len(results)} task(s)")

    # US4: Filter Tasks
    print("\n[US4] Testing Filter...")
    high_priority_tasks = service.filter_tasks("priority", "high")
    assert len(high_priority_tasks) == 2  # Urgent report + Fix bug
    print(f"[OK] Filter by priority=high: found {len(high_priority_tasks)} task(s)")

    work_tasks = service.filter_tasks("tag", "work")
    assert len(work_tasks) >= 1
    print(f"[OK] Filter by tag=work: found {len(work_tasks)} task(s)")

    pending_tasks = service.filter_tasks("status", "pending")
    print(f"[OK] Filter by status=pending: found {len(pending_tasks)} task(s)")

    # US5: Sort Tasks
    print("\n[US5] Testing Sort...")
    service.set_sort_preference("priority")
    sorted_tasks = service.get_sorted_tasks()
    # First task should be high priority
    assert sorted_tasks[0].priority == "high"
    print(f"[OK] Sort by priority: first task has priority={sorted_tasks[0].priority}")

    service.set_sort_preference("title")
    sorted_tasks = service.get_sorted_tasks()
    # Should be alphabetically sorted
    titles = [t.title for t in sorted_tasks]
    assert titles == sorted(titles, key=str.lower)
    print(f"[OK] Sort by title: tasks in alphabetical order")

    service.set_sort_preference("created")
    sorted_tasks = service.get_sorted_tasks()
    # Should be in creation order (oldest first)
    print(f"[OK] Sort by creation date: {len(sorted_tasks)} tasks ordered")

    service.set_sort_preference("none")
    assert service.get_sort_preference() == "none"
    print("[OK] Sort preference cleared")

    print("\n[PASS] All Intermediate Level features working correctly!")


def test_acceptance_scenarios():
    """Test specific acceptance scenarios from spec."""
    print("\n=== Testing Acceptance Scenarios ===")
    service = TaskService()

    # AS1: Priority display
    print("\n[AS1] Priority must be displayed in list...")
    task = service.add_task("Test", "Priority display", priority="high")
    tasks = service.list_tasks()
    assert tasks[0].priority == "high"
    print("[OK] Priority field accessible in task list")

    # AS2: Tags display
    print("\n[AS2] Tags must be displayed in list...")
    task = service.add_task("Test2", "Tag display", tags=["work", "urgent"])
    tasks = service.list_tasks()
    assert len(tasks[1].tags) == 2
    print("[OK] Tags field accessible in task list")

    # AS3: Search case-insensitive
    print("\n[AS3] Search must be case-insensitive...")
    service.add_task("Important Task", "Very important")
    results = service.search_tasks("IMPORTANT")
    assert len(results) >= 1
    print("[OK] Case-insensitive search works")

    # AS4: Filter returns subset
    print("\n[AS4] Filter must return only matching tasks...")
    all_tasks = service.list_tasks()
    filtered = service.filter_tasks("priority", "high")
    assert len(filtered) <= len(all_tasks)
    assert all(t.priority == "high" for t in filtered)
    print(f"[OK] Filter returned {len(filtered)}/{len(all_tasks)} tasks")

    # AS5: Created timestamp exists
    print("\n[AS5] Tasks must have creation timestamp...")
    task = service.add_task("Time test", "Check timestamp")
    assert task.created_at is not None
    print(f"[OK] Task has creation timestamp: {task.created_at}")

    print("\n[PASS] All acceptance scenarios passed!")


if __name__ == "__main__":
    try:
        test_backward_compatibility()
        test_intermediate_features()
        test_acceptance_scenarios()
        print("\n" + "="*60)
        print("*** ALL VALIDATION TESTS PASSED!")
        print("="*60)
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
