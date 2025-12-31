# Tasks: Todo In-Memory Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files)
- **[Story]**: US1-US5 maps to user stories from spec

---

## Phase 1: Setup

- [x] T001 Initialize UV project with pyproject.toml at repository root
- [x] T002 Create directory structure: src/, src/models/, src/services/, src/cli/
- [x] T003 [P] Create src/__init__.py
- [x] T004 [P] Create src/models/__init__.py
- [x] T005 [P] Create src/services/__init__.py
- [x] T006 [P] Create src/cli/__init__.py

**Checkpoint**: Project structure ready

---

## Phase 2: Foundational

- [x] T007 Create Task dataclass in src/models/task.py (id, title, description, status)
- [x] T008 Create TaskService class skeleton in src/services/task_service.py (task list, id counter)
- [x] T009 Create menu display function in src/cli/menu.py (6 options + input handling)
- [x] T010 Create main.py entry point with menu loop skeleton in src/main.py

**Checkpoint**: App runs, shows menu, exits cleanly

---

## Phase 3: User Story 1 - Add Task (P1)

**Goal**: User can add tasks with title and optional description
**Test**: Run app → select add → enter title/desc → verify in list

- [x] T011 [US1] Implement add_task method in src/services/task_service.py
- [x] T012 [US1] Implement add task input handler in src/cli/menu.py (title validation, empty desc allowed)
- [x] T013 [US1] Wire add task handler to menu option 1 in src/main.py

**Checkpoint**: Can add tasks with auto-generated IDs

---

## Phase 4: User Story 2 - List Tasks (P1)

**Goal**: User can view all tasks with ID, title, description, status
**Test**: Add tasks → select list → verify formatted output

- [x] T014 [US2] Implement list_tasks method in src/services/task_service.py
- [x] T015 [US2] Implement list display formatter in src/cli/menu.py (handle empty list)
- [x] T016 [US2] Wire list handler to menu option 2 in src/main.py

**Checkpoint**: Can see all tasks formatted correctly

---

## Phase 5: User Story 3 - Update Task (P2)

**Goal**: User can update task title/description with skip-to-keep pattern
**Test**: Add task → update title only → verify change, desc unchanged

- [x] T017 [US3] Implement get_task and update_task methods in src/services/task_service.py
- [x] T018 [US3] Implement update input handler in src/cli/menu.py (show current, Enter skips)
- [x] T019 [US3] Wire update handler to menu option 3 in src/main.py

**Checkpoint**: Can update tasks partially

---

## Phase 6: User Story 4 - Delete Task (P2)

**Goal**: User can delete tasks by ID
**Test**: Add task → delete by ID → verify removed from list

- [x] T020 [US4] Implement delete_task method in src/services/task_service.py
- [x] T021 [US4] Implement delete input handler in src/cli/menu.py (ID validation)
- [x] T022 [US4] Wire delete handler to menu option 4 in src/main.py

**Checkpoint**: Can delete tasks

---

## Phase 7: User Story 5 - Mark Status (P2)

**Goal**: User can change task status (pending/in-progress/completed)
**Test**: Add task → mark in-progress → mark completed → verify changes

- [x] T023 [US5] Implement update_status method in src/services/task_service.py (validate status)
- [x] T024 [US5] Implement status input handler in src/cli/menu.py (show valid options)
- [x] T025 [US5] Wire status handler to menu option 5 in src/main.py

**Checkpoint**: Can change task status

---

## Phase 8: Polish

- [x] T026 Add error handling for non-numeric ID input in src/cli/menu.py
- [x] T027 Add type hints to all functions
- [x] T028 Run full validation against all acceptance scenarios

---

## Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3-7 (User Stories) → Phase 8 (Polish)

User Stories after Phase 2:
  US1 (Add) → US2 (List) → US3/US4/US5 can parallel
```

## Parallel Opportunities

```bash
# Phase 1 - all __init__.py files:
T003, T004, T005, T006

# After US1+US2 complete, US3/US4/US5 can run in parallel
```

## Summary

| Phase | Tasks | Stories |
|-------|-------|---------|
| Setup | 6 | - |
| Foundational | 4 | - |
| US1 Add | 3 | P1 |
| US2 List | 3 | P1 |
| US3 Update | 3 | P2 |
| US4 Delete | 3 | P2 |
| US5 Status | 3 | P2 |
| Polish | 3 | - |
| **Total** | **28** | **5** |

**MVP**: Phase 1 + 2 + US1 + US2 (16 tasks)
