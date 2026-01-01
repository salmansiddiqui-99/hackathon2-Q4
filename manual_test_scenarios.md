# Manual Test Scenarios - Phase I Todo App

## Test Execution Log

### US1 - Add Task

#### Test 1.1: Add task with title and description
**Steps:**
1. Run: `python -m src.main`
2. Select option 1 (Add Task)
3. Enter title: "Buy milk"
4. Enter description: "Get 2% milk from store"

**Expected:** Task created with unique ID, confirmation message shown

#### Test 1.2: Add task with empty description
**Steps:**
1. Select option 1
2. Enter title: "Read book"
3. Press Enter (skip description)

**Expected:** Task created successfully with empty description

#### Test 1.3: Add task with empty title
**Steps:**
1. Select option 1
2. Press Enter (empty title)

**Expected:** Error message "Title cannot be empty"

---

### US2 - List Tasks

#### Test 2.1: List when tasks exist
**Steps:**
1. Add 2-3 tasks
2. Select option 2 (List Tasks)

**Expected:** All tasks shown with ID, title, description, status

#### Test 2.2: List when empty
**Steps:**
1. Start fresh app (no tasks)
2. Select option 2

**Expected:** Message "No tasks found."

---

### US3 - Update Task

#### Test 3.1: Update title only
**Steps:**
1. Create a task
2. Select option 3 (Update Task)
3. Enter task ID
4. Enter new title
5. Press Enter (skip description)

**Expected:** Only title updated, description unchanged

#### Test 3.2: Update description only
**Steps:**
1. Select option 3
2. Enter task ID
3. Press Enter (skip title)
4. Enter new description

**Expected:** Only description updated, title unchanged

#### Test 3.3: Update non-existent ID
**Steps:**
1. Select option 3
2. Enter ID: 999

**Expected:** Error message "Task #999 not found"

---

### US4 - Delete Task

#### Test 4.1: Delete existing task
**Steps:**
1. Create 2 tasks
2. Select option 4 (Delete Task)
3. Enter ID of first task
4. List tasks to verify

**Expected:** Task removed, only second task remains

#### Test 4.2: Delete non-existent ID
**Steps:**
1. Select option 4
2. Enter ID: 999

**Expected:** Error message "Task #999 not found"

---

### US5 - Mark Status

#### Test 5.1: Mark as in-progress
**Steps:**
1. Create a task (default: pending)
2. Select option 5 (Mark Status)
3. Enter task ID
4. Enter status: "in-progress"

**Expected:** Status changed to in-progress

#### Test 5.2: Mark as completed
**Steps:**
1. Select option 5
2. Enter task ID
3. Enter status: "completed"

**Expected:** Status changed to completed

#### Test 5.3: Invalid status
**Steps:**
1. Select option 5
2. Enter task ID
3. Enter status: "invalid"

**Expected:** Error showing valid options (pending, in-progress, completed)

---

### Edge Cases

#### Edge 1: Non-numeric ID input
**Steps:**
1. Select option 3, 4, or 5
2. Enter "abc" as ID

**Expected:** Error "Please enter a valid numeric ID"

#### Edge 2: Exit option
**Steps:**
1. Select option 6 (Exit)

**Expected:** "Goodbye!" message, app terminates cleanly

#### Edge 3: Invalid menu choice
**Steps:**
1. Enter "9" at menu

**Expected:** Error "Invalid choice. Please enter a number between 1 and 6"

---

## Complete User Journey Test

**Scenario:** User manages daily tasks from start to finish

```
1. Start app
2. Add task: "Morning workout" / "30 min cardio"
3. Add task: "Review pull requests" / ""
4. Add task: "Team meeting" / "Discuss Q1 roadmap"
5. List tasks → verify 3 tasks shown
6. Mark task #1 as in-progress
7. Mark task #1 as completed
8. Update task #2 title to "Review and merge PRs"
9. Delete task #3
10. List tasks → verify 2 tasks, #1 completed, #2 pending
11. Exit
```

**Expected:** All operations succeed, data remains consistent throughout session
