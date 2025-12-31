# Tasks: Todo Advanced Features

**Input**: Design documents from `/specs/003-todo-advanced-features/`
**Prerequisites**: plan.md, spec.md, Basic Level (001), Intermediate Level (002)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1-US5 maps to user stories

---

## Phase 1: Model Extension

- [x] T001 Add VALID_RECURRENCES constant ("none", "daily", "weekly", "monthly") to src/models/task.py
- [x] T002 Add recurrence field (str, default "none") to Task dataclass in src/models/task.py
- [x] T003 Add due_date field (datetime | None, default None) to Task dataclass in src/models/task.py
- [x] T004 Update __post_init__ to validate recurrence in Task.VALID_RECURRENCES in src/models/task.py

**Checkpoint**: Task model extended with recurrence and due_date fields

---

## Phase 2: Date Parsing Utility

- [x] T005 [P] Create src/utils/__init__.py with package exports
- [x] T006 Create parse_natural_date function handling "today"/"tomorrow" in src/utils/date_parser.py
- [x] T007 Add "next <weekday>" parsing to parse_natural_date in src/utils/date_parser.py
- [x] T008 Add ISO format parsing (YYYY-MM-DD, YYYY-MM-DD HH:MM) to parse_natural_date in src/utils/date_parser.py

**Checkpoint**: Natural date parser handles all 5 formats

---

## Phase 3: Recurrence Engine

- [x] T009 Create calculate_next_due_date for daily (+1 day) in src/utils/recurrence.py
- [x] T010 Add weekly recurrence (+7 days) to calculate_next_due_date in src/utils/recurrence.py
- [x] T011 Add monthly recurrence with month boundary handling in src/utils/recurrence.py
- [x] T012 Handle None due_date (use today as base) in calculate_next_due_date in src/utils/recurrence.py

**Checkpoint**: Recurrence calculations work for all patterns

---

## Phase 4: User Story 1 - Create Recurring Task (P1)

**Goal**: Users can create tasks with recurrence patterns
**Test**: Add task → select recurrence → verify stored and displayed

- [x] T013 [US1] Update add_task signature for recurrence parameter in src/services/task_service.py
- [x] T014 [US1] Update handle_add_task to prompt for recurrence in src/cli/menu.py
- [x] T015 [US1] Update handle_list_tasks to display recurrence in src/cli/menu.py

**Checkpoint**: Recurring task creation complete

---

## Phase 5: User Story 3 - Set Due Date on Task (P1)

**Goal**: Tasks can have optional due date and time
**Test**: Add task → enter due date → verify in list

- [x] T016 [US3] Update add_task signature for due_date parameter in src/services/task_service.py
- [x] T017 [US3] Update handle_add_task to prompt for due date in src/cli/menu.py
- [x] T018 [US3] Update handle_list_tasks to display due date in src/cli/menu.py
- [x] T019 [US3] Update update_task to accept recurrence and due_date in src/services/task_service.py
- [x] T020 [US3] Update handle_update_task to allow changing recurrence/due_date in src/cli/menu.py

**Checkpoint**: Due date creation and update complete

---

## Phase 6: User Story 4 - Natural Date Input (P2)

**Goal**: Users can enter dates in natural language
**Test**: Enter "tomorrow" → verify correct date set

- [x] T021 [US4] Integrate parse_natural_date into handle_add_task in src/cli/menu.py
- [x] T022 [US4] Add error handling and retry for invalid date input in src/cli/menu.py
- [x] T023 [US4] Integrate parse_natural_date into handle_update_task in src/cli/menu.py

**Checkpoint**: Natural date input working in add and update

---

## Phase 7: User Story 2 - Auto-Generate Next Occurrence (P1)

**Goal**: System auto-creates next instance when recurring task completed
**Test**: Complete recurring task → verify new task created with next due date

- [x] T024 [US2] Add _generate_next_occurrence method in src/services/task_service.py
- [x] T025 [US2] Modify update_status to call _generate_next_occurrence for recurring tasks in src/services/task_service.py
- [x] T026 [US2] Update handle_mark_status to show auto-generation message in src/cli/menu.py

**Checkpoint**: Auto-generation on completion working

---

## Phase 8: User Story 5 - Check Reminders (P2)

**Goal**: Users can view overdue and soon-due tasks
**Test**: Create tasks with various due dates → Check Reminders → verify categorization

- [x] T027 [US5] Add get_overdue_tasks method in src/services/task_service.py
- [x] T028 [US5] Add get_soon_due_tasks method (24 hours) in src/services/task_service.py
- [x] T029 [US5] Create handle_check_reminders function in src/cli/menu.py
- [x] T030 [US5] Display overdue tasks with time elapsed in handle_check_reminders in src/cli/menu.py
- [x] T031 [US5] Display soon-due tasks with time remaining in handle_check_reminders in src/cli/menu.py

**Checkpoint**: Reminders feature complete

---

## Phase 9: Menu Integration & Polish

- [x] T032 Update display_menu to show 11 options (add Check Reminders) in src/cli/menu.py
- [x] T033 Update get_menu_choice to accept 1-11 in src/cli/menu.py
- [x] T034 Wire choice "10" to handle_check_reminders in src/main.py
- [x] T035 Renumber Exit to "11" in src/main.py
- [x] T036 Update imports in src/main.py to include handle_check_reminders
- [x] T037 Update exports in src/cli/__init__.py to include handle_check_reminders
- [x] T038 Update src/utils/__init__.py exports for parse_natural_date and calculate_next_due_date

**Checkpoint**: Full 11-option menu operational

---

## Phase 10: Quality Validation

- [x] T039 Validate Basic Level features (add/list/update/delete/mark status)
- [x] T040 Validate Intermediate features (priority/tags/search/filter/sort)
- [x] T041 Validate recurring task creation and display
- [x] T042 Validate due date creation with natural language
- [x] T043 Validate auto-generation on recurring task completion
- [x] T044 Validate Check Reminders shows overdue and soon-due
- [x] T045 Validate edge cases (no due date, completed tasks excluded, invalid input)

**Checkpoint**: All acceptance scenarios pass

---

## Dependencies

```
Phase 1 (Model) → Phase 2 (Date Parser) → Phase 3 (Recurrence)
                          ↓                       ↓
                    Phase 4 (US1) ←→ Phase 5 (US3)
                          ↓                ↓
                    Phase 6 (US4) ← ─ ─ ─ ─┘
                          ↓
                    Phase 7 (US2) → Phase 8 (US5)
                          ↓
                    Phase 9 (Menu) → Phase 10 (Validation)
```

## Parallel Opportunities

| Phase | Parallel Tasks |
|-------|----------------|
| Phase 2 | T005 (utils init) can run parallel |
| Phase 4-5 | US1 and US3 can develop in parallel after Phase 3 |

## Summary

| Phase | Tasks | Stories |
|-------|-------|---------|
| Model Extension | 4 | - |
| Date Parsing | 4 | - |
| Recurrence Engine | 4 | - |
| US1 Recurring Task | 3 | P1 |
| US3 Due Date | 5 | P1 |
| US4 Natural Input | 3 | P2 |
| US2 Auto-Generate | 3 | P1 |
| US5 Reminders | 5 | P2 |
| Menu Integration | 7 | - |
| Validation | 7 | - |
| **Total** | **45** | **5** |

**MVP**: Phase 1-5 (US1 + US3) = 20 tasks
**Full Feature**: All 45 tasks
