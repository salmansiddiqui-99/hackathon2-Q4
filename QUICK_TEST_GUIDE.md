# Quick Test Guide - Phase I Todo App

## Run All Automated Tests (Recommended)

```bash
# Run core feature tests (25 tests)
python test_todo_app.py

# Run CLI simulation tests (15 tests)
python test_cli_simulation.py
```

**Expected:** All 40 tests should pass with 100% success rate.

---

## Quick Manual Verification (5 minutes)

Run the app:
```bash
python -m src.main
```

### Test Script (Follow these steps)

```
Welcome to Todo App!

=== Todo App ===
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Status
6. Exit

1️⃣ Enter choice: 1
   Enter title: Buy milk
   Enter description: Get 2% milk from store
   ✓ Expected: "Task #1 created successfully"

2️⃣ Enter choice: 1
   Enter title: Read book
   Enter description: [Press Enter]
   ✓ Expected: "Task #2 created successfully"

3️⃣ Enter choice: 1
   Enter title: [Press Enter]
   ✓ Expected: "Error: Title cannot be empty"

4️⃣ Enter choice: 2
   ✓ Expected: See both tasks listed with ID, title, description, status

5️⃣ Enter choice: 3
   Enter task ID: 1
   New title: Buy almond milk
   New description: [Press Enter]
   ✓ Expected: "Task #1 updated successfully"

6️⃣ Enter choice: 5
   Enter task ID: 1
   Enter new status: in-progress
   ✓ Expected: "Task #1 status changed to 'in-progress'"

7️⃣ Enter choice: 5
   Enter task ID: 1
   Enter new status: completed
   ✓ Expected: "Task #1 status changed to 'completed'"

8️⃣ Enter choice: 5
   Enter task ID: 1
   Enter new status: invalid
   ✓ Expected: Error showing valid options (pending, in-progress, completed)

9️⃣ Enter choice: 4
   Enter task ID: 2
   ✓ Expected: "Task #2 deleted successfully"

🔟 Enter choice: 2
   ✓ Expected: Only task #1 shown, status = completed

1️⃣1️⃣ Enter choice: 3
   Enter task ID: 999
   ✓ Expected: "Error: Task #999 not found"

1️⃣2️⃣ Enter choice: 3
   Enter task ID: abc
   ✓ Expected: "Error: Please enter a valid numeric ID"

1️⃣3️⃣ Enter choice: 6
   ✓ Expected: "Goodbye!" and app exits
```

---

## Feature Checklist

- [ ] **US1: Add Task** - Can create tasks with title and description
- [ ] **US2: List Tasks** - Can view all tasks with details
- [ ] **US3: Update Task** - Can modify task title/description
- [ ] **US4: Delete Task** - Can remove tasks by ID
- [ ] **US5: Mark Status** - Can change task status (pending/in-progress/completed)

---

## Error Handling Checklist

- [ ] Empty title rejected with error message
- [ ] Empty description accepted
- [ ] Non-existent task ID shows error
- [ ] Non-numeric ID shows error
- [ ] Invalid status shows valid options
- [ ] All operations handle edge cases gracefully

---

## Success Criteria

If all checks pass:
- ✅ All automated tests pass (40/40)
- ✅ All 5 features work correctly
- ✅ Error handling works as expected
- ✅ App exits cleanly

**Result: Application ready for demonstration**
