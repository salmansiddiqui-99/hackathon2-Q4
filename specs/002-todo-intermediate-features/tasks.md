# Tasks: Todo Intermediate Features

**Input**: Design documents from `/specs/002-todo-intermediate-features/`
**Prerequisites**: plan.md, spec.md, existing Basic Level implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1-US5 maps to user stories

---

## Phase 1: Model Extension

- [x] T001 Add priority field (str, default "medium") to Task dataclass in src/models/task.py
- [x] T002 Add tags field (list[str], default []) to Task dataclass in src/models/task.py
- [x] T003 Add created_at field (datetime) to Task dataclass in src/models/task.py
- [x] T004 Add VALID_PRIORITIES constant and validation in src/models/task.py
- [x] T005 Update __post_init__ to validate priority in src/models/task.py

**Checkpoint**: Task model extended, existing tests still pass

---

## Phase 2: Service Extension

- [x] T006 Update add_task method signature for priority/tags in src/services/task_service.py
- [x] T007 Add search_tasks(keyword) method in src/services/task_service.py
- [x] T008 Add filter_tasks(by, value) method in src/services/task_service.py
- [x] T009 Add sort preference storage and get_sorted_tasks method in src/services/task_service.py
- [x] T010 Add add_tags_to_task(id, tags) method in src/services/task_service.py
- [x] T011 Add remove_tag_from_task(id, tag) method in src/services/task_service.py

**Checkpoint**: Service layer supports all intermediate operations

---

## Phase 3: User Story 1 - Priority Assignment (P1)

**Goal**: Users can assign/update/view priority levels
**Test**: Add task with priority → list → verify priority displayed

- [x] T012 [US1] Update handle_add_task to prompt for priority in src/cli/menu.py
- [x] T013 [US1] Update handle_update_task to allow priority change in src/cli/menu.py
- [x] T014 [US1] Update handle_list_tasks display format for priority in src/cli/menu.py

**Checkpoint**: Priority feature complete

---

## Phase 4: User Story 2 - Tags/Categories (P1)

**Goal**: Users can add/remove/view tags on tasks
**Test**: Add task with tags → manage tags → verify in list

- [x] T015 [US2] Update handle_add_task to prompt for tags in src/cli/menu.py
- [x] T016 [US2] Create handle_manage_tags function in src/cli/menu.py
- [x] T017 [US2] Update handle_list_tasks display format for tags in src/cli/menu.py

**Checkpoint**: Tags feature complete

---

## Phase 5: User Story 3 - Search Tasks (P2)

**Goal**: Users can search tasks by keyword
**Test**: Create varied tasks → search keyword → verify matches

- [x] T018 [US3] Create handle_search_tasks function in src/cli/menu.py
- [x] T019 [US3] Wire search handler to menu option in src/main.py

**Checkpoint**: Search feature complete

---

## Phase 6: User Story 4 - Filter Tasks (P2)

**Goal**: Users can filter by status/priority/tag
**Test**: Create varied tasks → apply filter → verify subset

- [x] T020 [US4] Create handle_filter_tasks function in src/cli/menu.py
- [x] T021 [US4] Wire filter handler to menu option in src/main.py

**Checkpoint**: Filter feature complete

---

## Phase 7: User Story 5 - Sort Tasks (P2)

**Goal**: Users can sort by priority/title/creation date
**Test**: Create tasks → sort → verify order

- [x] T022 [US5] Create handle_sort_tasks function in src/cli/menu.py
- [x] T023 [US5] Wire sort handler to menu option in src/main.py
- [x] T024 [US5] Update list display to show current sort order in src/cli/menu.py

**Checkpoint**: Sort feature complete

---

## Phase 8: Menu Integration & Polish

- [x] T025 Extend display_menu to show 10 options in src/cli/menu.py
- [x] T026 Update main loop for choices 6-10 in src/main.py
- [x] T027 Update module exports in src/cli/__init__.py
- [x] T028 Run backward compatibility validation (all basic features)
- [x] T029 Run full validation against all acceptance scenarios

---

## Dependencies

```
Phase 1 (Model) → Phase 2 (Service) → Phase 3-7 (User Stories) → Phase 8 (Polish)

User Stories after Phase 2:
  US1 (Priority) + US2 (Tags) → US3 (Search) / US4 (Filter) / US5 (Sort)
```

## Summary

| Phase | Tasks | Stories |
|-------|-------|---------|
| Model Extension | 5 | - |
| Service Extension | 6 | - |
| US1 Priority | 3 | P1 |
| US2 Tags | 3 | P1 |
| US3 Search | 2 | P2 |
| US4 Filter | 2 | P2 |
| US5 Sort | 3 | P2 |
| Polish | 5 | - |
| **Total** | **29** | **5** |

**MVP**: Phase 1 + 2 + US1 + US2 (17 tasks)
