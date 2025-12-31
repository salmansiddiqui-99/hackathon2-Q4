# Feature Specification: Todo Advanced Features

**Feature Branch**: `003-todo-advanced-features`
**Created**: 2025-12-31
**Status**: Draft
**Input**: Phase I Extension: Advanced Level Features (Intelligent Features)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Recurring Task (Priority: P1)

Users can create tasks with recurrence patterns (daily, weekly, monthly) so that repetitive tasks are automatically scheduled without manual re-entry.

**Why this priority**: Recurring tasks are the core differentiating feature of this level. Without this, users must manually recreate repetitive tasks.

**Independent Test**: Can be fully tested by creating a task with "weekly" recurrence and verifying the recurrence field is stored and displayed correctly.

**Acceptance Scenarios**:

1. **Given** I am adding a new task, **When** I select "daily" as recurrence, **Then** the task is created with recurrence="daily" and this is displayed in task list
2. **Given** I am adding a new task, **When** I press Enter to skip recurrence, **Then** the task is created with recurrence="none" (default)
3. **Given** I am adding a new task, **When** I enter an invalid recurrence like "yearly", **Then** the system shows an error and defaults to "none"

---

### User Story 2 - Auto-Generate Next Occurrence (Priority: P1)

When a recurring task is marked as completed, the system automatically creates the next occurrence so users don't have to manually recreate recurring tasks.

**Why this priority**: This is the payoff of the recurring task feature - without auto-generation, recurrence is just a label.

**Independent Test**: Can be tested by creating a recurring task, marking it complete, and verifying a new pending task is auto-created with the next due date.

**Acceptance Scenarios**:

1. **Given** a task with recurrence="daily" and due_date=today, **When** I mark it "completed", **Then** a new task is created with status="pending" and due_date=tomorrow
2. **Given** a task with recurrence="weekly" and due_date=2025-01-01, **When** I mark it "completed", **Then** a new task is created with due_date=2025-01-08
3. **Given** a task with recurrence="none", **When** I mark it "completed", **Then** no new task is created
4. **Given** a recurring task without a due_date, **When** I mark it "completed", **Then** a new task is created using today as the base for calculating next due date

---

### User Story 3 - Set Due Date on Task (Priority: P1)

Tasks can have an optional due date and time so users can track deadlines.

**Why this priority**: Due dates are essential for the reminder feature and recurring task date calculations.

**Independent Test**: Can be tested by creating a task with a due date and verifying it displays in the task list.

**Acceptance Scenarios**:

1. **Given** I am adding a new task, **When** I enter "2025-01-15 14:30" as due date, **Then** the task is created with that exact datetime
2. **Given** I am adding a new task, **When** I press Enter to skip due date, **Then** the task is created with due_date=None
3. **Given** I am updating a task, **When** I enter a new due date, **Then** the due date is updated

---

### User Story 4 - Natural Date Input (Priority: P2)

Users can enter dates in natural language like "tomorrow" or "next Friday" for convenient date entry.

**Why this priority**: Enhances usability but the core feature works with ISO format dates. This is a convenience layer.

**Independent Test**: Can be tested by entering "tomorrow" when prompted for due date and verifying the correct date is set.

**Acceptance Scenarios**:

1. **Given** I am prompted for due date, **When** I enter "tomorrow", **Then** the due date is set to tomorrow at 09:00
2. **Given** I am prompted for due date, **When** I enter "today", **Then** the due date is set to today at 09:00
3. **Given** I am prompted for due date, **When** I enter "next Monday", **Then** the due date is set to the next Monday at 09:00
4. **Given** I am prompted for due date, **When** I enter "2025-01-15", **Then** the due date is set to 2025-01-15 at 09:00
5. **Given** I am prompted for due date, **When** I enter "invalid-date", **Then** an error is shown and I can retry

---

### User Story 5 - Check Reminders (Priority: P2)

Users can view overdue and soon-due tasks (within 24 hours) via a "Check Reminders" menu option so they don't miss deadlines.

**Why this priority**: Valuable feature but requires due dates to be set first. Provides the reminder functionality promised in the feature description.

**Independent Test**: Can be tested by creating tasks with various due dates and using "Check Reminders" to verify correct categorization.

**Acceptance Scenarios**:

1. **Given** a task with due_date in the past, **When** I select "Check Reminders", **Then** the task appears under "Overdue Tasks"
2. **Given** a task with due_date within the next 24 hours, **When** I select "Check Reminders", **Then** the task appears under "Due Soon"
3. **Given** no tasks are overdue or due soon, **When** I select "Check Reminders", **Then** I see "No overdue or upcoming tasks"
4. **Given** a completed task with a past due date, **When** I select "Check Reminders", **Then** the completed task does NOT appear in reminders

---

### Edge Cases

- **EC-001**: Monthly recurrence on Jan 31 → next occurrence is Feb 28 (or 29 in leap year)
- **EC-002**: Recurring task without due_date uses today as base for next occurrence
- **EC-003**: Setting due date in the past is allowed (task shows as overdue)
- **EC-004**: Tasks without due_date are excluded from reminders
- **EC-005**: Completed tasks are excluded from reminders
- **EC-006**: Task exactly at 24-hour boundary is included in "due soon"

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST add `recurrence` field to Task with values: "none", "daily", "weekly", "monthly"
- **FR-002**: System MUST add `due_date` field to Task as optional datetime (default: None)
- **FR-003**: System MUST validate recurrence values and reject invalid patterns
- **FR-004**: System MUST auto-generate next occurrence when recurring task marked completed
- **FR-005**: System MUST calculate next due date based on recurrence pattern
- **FR-006**: System MUST parse natural date inputs: "today", "tomorrow", "next <weekday>"
- **FR-007**: System MUST parse ISO date formats: "YYYY-MM-DD" and "YYYY-MM-DD HH:MM"
- **FR-008**: System MUST provide "Check Reminders" command showing overdue and soon-due tasks
- **FR-009**: System MUST categorize reminders as "Overdue" (past) or "Due Soon" (within 24 hours)
- **FR-010**: System MUST exclude completed tasks from reminders
- **FR-011**: System MUST display due date and recurrence in task list view
- **FR-012**: System MUST allow updating due date and recurrence on existing tasks
- **FR-013**: System MUST handle month boundary edge cases for monthly recurrence
- **FR-014**: System MUST preserve original completed recurring task in history

### Key Entities

- **Task (extended)**: Now includes `recurrence` (str: none/daily/weekly/monthly) and `due_date` (datetime or None)
- **Natural Date Parser**: Utility to convert user input strings to datetime objects
- **Recurrence Calculator**: Utility to compute next due date based on current date and pattern

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 user stories implemented with acceptance scenarios passing
- **SC-002**: Natural date parsing handles all 5 input formats correctly
- **SC-003**: Auto-generation creates correct next occurrences for all recurrence patterns
- **SC-004**: All Basic Level (001) and Intermediate Level (002) features remain functional
- **SC-005**: Menu expanded to 11 options with "Check Reminders" working correctly
- **SC-006**: Edge cases (month boundaries, missing due dates) handled gracefully

## Out of Scope

- Persistent storage (remains in-memory only)
- Push/email notifications
- Timezone handling (uses local system time)
- Complex recurrence patterns (e.g., "every 2 weeks", "weekdays only")
- Snooze functionality for reminders
- Calendar integration

## Data Model Changes

```python
VALID_RECURRENCES = ("none", "daily", "weekly", "monthly")
recurrence: str = "none"  # NEW field
due_date: datetime | None = None  # NEW field
```

## Menu Structure (Extended from 10 to 11 options)

```
=== Todo App ===
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Status
6. Manage Tags
7. Search Tasks
8. Filter Tasks
9. Sort Tasks
10. Check Reminders  <- NEW
11. Exit             <- Renumbered
```
