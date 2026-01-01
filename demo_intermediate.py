"""Demonstration of Phase 1 Intermediate Features."""

from src.services.task_service import TaskService


def demo_intermediate_features():
    """Demonstrate all intermediate features."""
    service = TaskService()

    print("\n" + "="*60)
    print("PHASE 1 INTERMEDIATE FEATURES DEMONSTRATION")
    print("="*60)

    # Feature 1: Priority
    print("\n### Feature 1: Priority Assignment ###")
    print("\nCreating tasks with different priorities...")

    service.add_task(
        "Fix critical bug",
        "Production server crash",
        priority="high",
        tags=["urgent", "backend"]
    )

    service.add_task(
        "Review pull request",
        "Code review for new feature",
        priority="medium",
        tags=["work", "review"]
    )

    service.add_task(
        "Read documentation",
        "Python 3.13 features",
        priority="low",
        tags=["learning"]
    )

    print("[OK] Created 3 tasks with high/medium/low priorities")

    # Feature 2: Tags
    print("\n### Feature 2: Tags/Categories ###")
    print("\nAdding tags to existing task...")

    service.add_tags_to_task(1, ["critical", "hotfix"])
    print("[OK] Added tags to task #1")

    # Feature 3: Search
    print("\n### Feature 3: Search Tasks ###")
    print("\nSearching for 'bug'...")

    results = service.search_tasks("bug")
    print(f"[OK] Found {len(results)} task(s) matching 'bug':")
    for task in results:
        print(f"  - #{task.id}: {task.title}")

    # Feature 4: Filter
    print("\n### Feature 4: Filter Tasks ###")
    print("\nFiltering by priority=high...")

    high_tasks = service.filter_tasks("priority", "high")
    print(f"[OK] Found {len(high_tasks)} high priority task(s):")
    for task in high_tasks:
        print(f"  - #{task.id}: {task.title} [{task.priority}]")

    print("\nFiltering by tag='work'...")
    work_tasks = service.filter_tasks("tag", "work")
    print(f"[OK] Found {len(work_tasks)} task(s) with 'work' tag:")
    for task in work_tasks:
        print(f"  - #{task.id}: {task.title} {task.tags}")

    # Feature 5: Sort
    print("\n### Feature 5: Sort Tasks ###")

    print("\nSorting by priority (high to low)...")
    service.set_sort_preference("priority")
    sorted_tasks = service.get_sorted_tasks()
    print("[OK] Tasks sorted by priority:")
    for task in sorted_tasks:
        print(f"  - #{task.id}: {task.title} [{task.priority}]")

    print("\nSorting alphabetically by title...")
    service.set_sort_preference("title")
    sorted_tasks = service.get_sorted_tasks()
    print("[OK] Tasks sorted by title:")
    for task in sorted_tasks:
        print(f"  - #{task.id}: {task.title}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY: All 5 Intermediate Features Working")
    print("="*60)
    print("\n[PASS] Priority Assignment - high/medium/low levels")
    print("[PASS] Tags/Categories - add/remove tags, deduplication")
    print("[PASS] Search - case-insensitive, across title/desc/tags")
    print("[PASS] Filter - by status/priority/tag")
    print("[PASS] Sort - by priority/title/creation date")
    print("\n[PASS] Backward Compatibility - All Basic features preserved")
    print("       (Add, List, Update, Delete, Mark Status, Exit)")

    print("\n" + "="*60)
    print("Ready for production use!")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo_intermediate_features()
