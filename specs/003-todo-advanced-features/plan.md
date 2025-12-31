# Implementation Plan: Todo Advanced Features

**Feature**: 003-todo-advanced-features
**Created**: 2025-12-31
**Status**: Ready for Implementation
**Input**: spec.md + user decisions

## Executive Summary

Extend the Todo Console Application with Advanced Level features: **Recurring Tasks** and **Due Dates with Reminders**. This plan preserves all Basic (001) and Intermediate (002) functionality while adding intelligent task scheduling capabilities.

## Architecture Decisions

### AD-1: Due Date Representation

**Decision**: Use `datetime` object from Python standard library

**Options Considered**:
| Option | Pros | Cons |
|--------|------|------|
| String field | Simple storage | No date arithmetic, manual parsing |
| **datetime object** | Native comparisons, sorting, arithmetic | Requires parsing on input |

**Chosen**: `datetime` object (`from datetime import datetime`)

**Rationale**: Enables accurate overdue checks (`due_date < now`), sorting by due date, and calculating next occurrence dates. Standard library provides all needed functionality.

---

### AD-2: Date Input Parsing

**Decision**: Natural language parsing using rules-based parser (no external dependencies)

**Options Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Strict format only | Simple, predictable | Poor UX, requires memorizing format |
| External library (dateutil) | Powerful parsing | Adds dependency |
| **Custom natural language parser** | Good UX, no dependencies | Limited patterns, more code |

**Chosen**: Custom rules-based parser supporting:
- "today", "tomorrow"
- "next Monday", "next Tuesday", ... "next Sunday"
- "YYYY-MM-DD" (assumes 09:00)
- "YYYY-MM-DD HH:MM"

**Rationale**: User-friendly input without adding external dependencies. Simple keyword matching handles common cases well.

---

### AD-3: Recurrence Representation

**Decision**: Template-plus-instances model with `recurrence` field on Task

**Options Considered**:
| Option | Pros | Cons |
|--------|------|------|
| String rule only | Simple | Parse on every use |
| Structured fields | Explicit | Over-engineered for basic patterns |
| **Template + auto-generate** | Clear model, preserves history | Slightly more tasks in memory |

**Chosen**: Store `recurrence` field on Task ("none", "daily", "weekly", "monthly"). When a recurring task is marked completed, auto-generate the next instance with a new due date.

**Rationale**:
- Original completed task preserved for history
- New instance gets fresh ID and calculated due date
- Simple to implement and understand

---

### AD-4: Recurrence Patterns Supported

**Decision**: Limited set (daily, weekly, monthly by date)

**Options Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Full iCal RRULE | Complete coverage | Complex parsing, overkill for Phase I |
| **Limited set** | Simple, covers 90% of use cases | No "every 2 weeks", etc. |

**Chosen**: `VALID_RECURRENCES = ("none", "daily", "weekly", "monthly")`

**Rationale**: Simple patterns that work reliably. Complex patterns deferred to future phases.

---

### AD-5: Reminder Delivery

**Decision**: On-demand "Check Reminders" command

**Options Considered**:
| Option | Pros | Cons |
|--------|------|------|
| Background thread | Proactive alerts | Not suitable for CLI app |
| **On-demand command** | User-controlled, fits CLI model | Requires user to remember to check |

**Chosen**: Menu option "Check Reminders" that displays:
- **Overdue Tasks**: due_date < now
- **Due Soon**: due_date within next 24 hours

**Rationale**: Fits the console application paradigm. Real-time notifications would require background processes unsuitable for Phase I.

---

## Implementation Phases

### Phase 1: Model Extension (Foundation)

**Goal**: Extend Task dataclass with new fields

**Changes to `src/models/task.py`**:
```python
# New fields
recurrence: str = "none"     # none | daily | weekly | monthly
due_date: datetime | None = None

# New constant
VALID_RECURRENCES = ("none", "daily", "weekly", "monthly")

# Update __post_init__ to validate recurrence
```

**Checkpoint**: Task model accepts recurrence and due_date, validates inputs

---

### Phase 2: Date Parsing Utility

**Goal**: Create natural language date parser

**New file `src/utils/date_parser.py`**:
```python
def parse_natural_date(input_str: str) -> datetime | None:
    """
    Parse natural language date input.

    Supported formats:
    - "today" → today at 09:00
    - "tomorrow" → tomorrow at 09:00
    - "next monday" through "next sunday" → next occurrence at 09:00
    - "YYYY-MM-DD" → specified date at 09:00
    - "YYYY-MM-DD HH:MM" → exact datetime

    Returns None for invalid input.
    """
```

**Implementation approach**:
1. Strip and lowercase input
2. Check for keywords: "today", "tomorrow"
3. Check for "next <weekday>" pattern
4. Try parsing ISO formats with/without time
5. Return None if no match

**Checkpoint**: Parser handles all documented formats correctly

---

### Phase 3: Recurrence Engine

**Goal**: Calculate next due dates and auto-generate instances

**New file `src/utils/recurrence.py`**:
```python
def calculate_next_due_date(
    current_due: datetime | None,
    recurrence: str
) -> datetime:
    """
    Calculate the next due date based on recurrence pattern.

    - daily: add 1 day
    - weekly: add 7 days
    - monthly: add 1 month (handle month boundaries)

    If current_due is None, use today as base.
    """
```

**Month boundary handling**:
- Jan 31 + 1 month → Feb 28/29 (last day of month)
- Use `calendar.monthrange()` to find last day

**Checkpoint**: Next dates calculated correctly for all patterns and edge cases

---

### Phase 4: Service Layer Extension

**Goal**: Update TaskService with new capabilities

**Changes to `src/services/task_service.py`**:

1. **Update `add_task()`**:
   ```python
   def add_task(
       self,
       title: str,
       description: str = "",
       priority: str = "medium",
       tags: list[str] | None = None,
       recurrence: str = "none",      # NEW
       due_date: datetime | None = None  # NEW
   ) -> Task:
   ```

2. **Update `update_task()`**:
   ```python
   def update_task(
       self,
       task_id: int,
       title: str | None = None,
       description: str | None = None,
       priority: str | None = None,
       recurrence: str | None = None,  # NEW
       due_date: datetime | None = None  # NEW (use sentinel for "clear")
   ) -> Task | None:
   ```

3. **Modify `update_status()`** for auto-generation:
   ```python
   def update_status(self, task_id: int, status: str) -> Task | None:
       # ... existing validation ...
       task.status = status

       # Auto-generate next occurrence for recurring tasks
       if status == "completed" and task.recurrence != "none":
           self._generate_next_occurrence(task)

       return task

   def _generate_next_occurrence(self, completed_task: Task) -> Task:
       """Create the next instance of a recurring task."""
       next_due = calculate_next_due_date(
           completed_task.due_date,
           completed_task.recurrence
       )
       return self.add_task(
           title=completed_task.title,
           description=completed_task.description,
           priority=completed_task.priority,
           tags=completed_task.tags.copy(),
           recurrence=completed_task.recurrence,
           due_date=next_due
       )
   ```

4. **Add reminder methods**:
   ```python
   def get_overdue_tasks(self) -> list[Task]:
       """Get tasks with due_date in the past (excludes completed)."""
       now = datetime.now()
       return [
           task for task in self._tasks
           if task.due_date and task.due_date < now and task.status != "completed"
       ]

   def get_soon_due_tasks(self, hours: int = 24) -> list[Task]:
       """Get tasks due within the next N hours (excludes completed)."""
       now = datetime.now()
       cutoff = now + timedelta(hours=hours)
       return [
           task for task in self._tasks
           if task.due_date and now <= task.due_date <= cutoff and task.status != "completed"
       ]
   ```

**Checkpoint**: Service handles recurrence, due dates, and reminder queries

---

### Phase 5: CLI Extension

**Goal**: Update menu handlers for new features

**Changes to `src/cli/menu.py`**:

1. **Update `display_menu()`** (10 → 11 options):
   ```
   10. Check Reminders  <- NEW
   11. Exit             <- Renumbered
   ```

2. **Update `get_menu_choice()`**: Accept 1-11

3. **Update `handle_add_task()`**:
   - Prompt for recurrence (show options, default "none")
   - Prompt for due date (natural language input)

4. **Update `handle_update_task()`**:
   - Show current recurrence and due date
   - Allow changing both (skip-to-keep pattern)

5. **Update `handle_list_tasks()`**:
   - Display due date (formatted or "No due date")
   - Display recurrence if not "none"
   - Show overdue indicator if applicable

6. **Add `handle_check_reminders()`**:
   ```python
   def handle_check_reminders(service: TaskService) -> None:
       """Display overdue and soon-due tasks."""
       print("\n--- Check Reminders ---")

       overdue = service.get_overdue_tasks()
       soon_due = service.get_soon_due_tasks(24)

       if not overdue and not soon_due:
           print("No overdue or upcoming tasks.")
           return

       if overdue:
           print("\n** Overdue Tasks **")
           for task in overdue:
               # Show how long overdue
               ...

       if soon_due:
           print("\n** Due Soon (within 24 hours) **")
           for task in soon_due:
               # Show time remaining
               ...
   ```

**Checkpoint**: All menu options functional, reminders display correctly

---

### Phase 6: Main Loop Update

**Goal**: Wire new handler to main loop

**Changes to `src/main.py`**:
```python
elif choice == "10":
    handle_check_reminders(service)
elif choice == "11":
    print("Goodbye!")
    break
else:
    print("Invalid choice. Please enter a number between 1 and 11.")
```

**Update imports** to include `handle_check_reminders`

**Checkpoint**: Full menu operational with 11 options

---

### Phase 7: Module Exports

**Goal**: Update package exports

**Changes to `src/cli/__init__.py`**:
- Add `handle_check_reminders` to imports and `__all__`

**Changes to `src/utils/__init__.py`** (new file):
- Export `parse_natural_date`, `calculate_next_due_date`

**Checkpoint**: Clean imports, no circular dependencies

---

### Phase 8: Quality Validation

**Goal**: Comprehensive testing and backward compatibility

**Validation Checklist**:

1. **Basic Level (001) Operations**:
   - [ ] Add task (title, description only)
   - [ ] List tasks
   - [ ] Update task (title, description)
   - [ ] Delete task
   - [ ] Mark status (pending → in-progress → completed)

2. **Intermediate Level (002) Features**:
   - [ ] Priority assignment (high/medium/low)
   - [ ] Tags (add, remove, display)
   - [ ] Search tasks by keyword
   - [ ] Filter by status/priority/tag
   - [ ] Sort by priority/title/created

3. **Advanced Level (003) Features**:
   - [ ] Create task with due date (natural language)
   - [ ] Create task with recurrence pattern
   - [ ] Update due date and recurrence
   - [ ] View due date/recurrence in list
   - [ ] Check reminders (overdue display)
   - [ ] Check reminders (due soon display)
   - [ ] Auto-generate next occurrence on completion
   - [ ] Monthly recurrence month-boundary handling

4. **Edge Cases**:
   - [ ] Task without due date (reminders excluded)
   - [ ] Completed task (reminders excluded)
   - [ ] Invalid date input (error handling)
   - [ ] Invalid recurrence (defaults to "none")
   - [ ] Empty task list reminders

**Checkpoint**: All validation items pass

---

## File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `src/models/task.py` | Modify | Add recurrence, due_date fields |
| `src/utils/__init__.py` | Create | Package init |
| `src/utils/date_parser.py` | Create | Natural date parsing |
| `src/utils/recurrence.py` | Create | Next date calculation |
| `src/services/task_service.py` | Modify | Add reminder methods, auto-generation |
| `src/cli/menu.py` | Modify | Update handlers, add reminders |
| `src/cli/__init__.py` | Modify | Export new handler |
| `src/main.py` | Modify | Wire option 10, renumber exit |

**Total**: 8 files (3 new, 5 modified)

---

## Dependencies

- `datetime` (stdlib) - Date/time handling
- `calendar` (stdlib) - Month boundary calculations
- `timedelta` (from datetime) - Duration calculations

**No external dependencies required.**

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Month boundary bugs | Use `calendar.monthrange()` for accurate last-day calculation |
| Date parsing ambiguity | Clear error messages, allow retry on invalid input |
| Breaking existing features | Comprehensive backward compatibility validation |
| Recurrence infinite loops | Only generate on explicit "completed" status change |

---

## Testing Strategy

**Method**: Manual console interaction with systematic validation

**Test Data for Current Date (2025-12-31)**:
- Overdue task: due_date = 2025-12-30 → appears in overdue
- Due soon task: due_date = 2026-01-01 08:00 → appears in due soon
- Future task: due_date = 2026-01-15 → not in reminders
- No due date task: excluded from reminders
- Completed task with past due date: excluded from reminders

**Recurrence Testing**:
- Daily: Complete task → verify new task due tomorrow
- Weekly: Complete task → verify new task due +7 days
- Monthly (Jan 31): Complete → verify Feb 28/29

---

## Success Criteria (from spec)

- [x] All 5 user stories mapped to implementation phases
- [x] Natural date parsing (5 formats) in Phase 2
- [x] Auto-generation logic in Phase 4
- [x] Backward compatibility validation in Phase 8
- [x] Menu expansion (10→11) in Phase 5-6
- [x] Edge cases addressed in Phase 3 and 8
