# Tasks: Console UI Enhancement

**Input**: Design documents from `/specs/004-console-ui-enhancement/`
**Prerequisites**: plan.md (completed), spec.md (completed)

**Tests**: No automated tests required - manual validation against acceptance criteria

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths relative to: `C:\Users\haroon traders\Desktop\projects\backup\hackathon_2\`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and create foundational formatting module

- [ ] T001 Add rich library dependency (uv add "rich>=13.7.0")
- [ ] T002 Create src/cli/formatter.py with module docstring and imports

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core formatting infrastructure that MUST be complete before ANY user story can be implemented

**Critical**: No user story work can begin until this phase is complete

- [ ] T003 [P] Define color scheme constants (COLORS dict) in src/cli/formatter.py
- [ ] T004 [P] Define symbol constants (SYMBOLS dict) in src/cli/formatter.py
- [ ] T005 Create get_console() function returning configured Console instance in src/cli/formatter.py
- [ ] T006 [P] Implement format_success(message: str) function in src/cli/formatter.py
- [ ] T007 [P] Implement format_error(message: str) function in src/cli/formatter.py
- [ ] T008 [P] Implement format_warning(message: str) function in src/cli/formatter.py
- [ ] T009 [P] Implement format_info(message: str) function in src/cli/formatter.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Enhanced Visual Hierarchy and Readability (Priority: P1) - MVP

**Goal**: Implement clear visual organization with headers, separators, and spacing throughout the application

**Independent Test**: Run application and verify all menus and sections have clear bordered headers, proper spacing, and visual separation

### Implementation for User Story 1

- [ ] T010 [US1] Implement format_menu_header(title: str) returning Panel in src/cli/formatter.py
- [ ] T011 [US1] Implement format_section_header(title: str) returning styled string in src/cli/formatter.py
- [ ] T012 [US1] Implement format_separator() returning visual separator line in src/cli/formatter.py
- [ ] T013 [US1] Update display_menu() in src/cli/menu.py to use format_menu_header() for main menu
- [ ] T014 [US1] Update handle_add_task() in src/cli/menu.py to use format_section_header() for "Add Task" header
- [ ] T015 [US1] Update handle_list_tasks() in src/cli/menu.py to use format_section_header() for "All Tasks" header
- [ ] T016 [US1] Update handle_update_task() in src/cli/menu.py to use format_section_header() for "Update Task" header
- [ ] T017 [US1] Update handle_delete_task() in src/cli/menu.py to use format_section_header() for "Delete Task" header
- [ ] T018 [US1] Update handle_mark_status() in src/cli/menu.py to use format_section_header() for "Mark Status" header
- [ ] T019 [US1] Update handle_manage_tags() in src/cli/menu.py to use format_section_header() for "Manage Tags" header
- [ ] T020 [US1] Update handle_search_tasks() in src/cli/menu.py to use format_section_header() for "Search Tasks" header
- [ ] T021 [US1] Update handle_filter_tasks() in src/cli/menu.py to use format_section_header() for "Filter Tasks" header
- [ ] T022 [US1] Update handle_sort_tasks() in src/cli/menu.py to use format_section_header() for "Sort Tasks" header
- [ ] T023 [US1] Update handle_check_reminders() in src/cli/menu.py to use format_section_header() for "Check Reminders" header
- [ ] T024 [US1] Implement format_task_panel(task: Task, now: datetime) returning Panel in src/cli/formatter.py
- [ ] T025 [US1] Update handle_list_tasks() in src/cli/menu.py to use format_task_panel() for each task display
- [ ] T026 [US1] Add spacing between tasks in handle_list_tasks() using console.print()
- [ ] T027 [US1] Update main() in src/main.py to use get_console() and format welcome message with Panel

**Checkpoint**: At this point, User Story 1 should be fully functional - all menus have clear visual hierarchy

---

## Phase 4: User Story 2 - Color-Coded Status and Priority Indicators (Priority: P2)

**Goal**: Implement color-coded status and priority indicators for instant visual recognition

**Independent Test**: Create tasks with different statuses and priorities, verify each displays with correct colors and symbols

### Implementation for User Story 2

- [ ] T028 [P] [US2] Implement format_status_badge(status: str) returning styled string in src/cli/formatter.py
- [ ] T029 [P] [US2] Implement format_priority_badge(priority: str) returning styled string in src/cli/formatter.py
- [ ] T030 [US2] Implement format_overdue_indicator() returning styled warning in src/cli/formatter.py
- [ ] T031 [US2] Update format_task_panel() in src/cli/formatter.py to include format_status_badge() for status display
- [ ] T032 [US2] Update format_task_panel() in src/cli/formatter.py to include format_priority_badge() for priority display
- [ ] T033 [US2] Update format_task_panel() in src/cli/formatter.py to include format_overdue_indicator() when due_date < now
- [ ] T034 [US2] Update handle_search_tasks() in src/cli/menu.py to use format_task_panel() with colored badges
- [ ] T035 [US2] Update handle_filter_tasks() in src/cli/menu.py to use format_task_panel() with colored badges
- [ ] T036 [US2] Update handle_check_reminders() in src/cli/menu.py to display overdue tasks with red highlighting
- [ ] T037 [US2] Update handle_check_reminders() in src/cli/menu.py to display soon-due tasks with yellow highlighting
- [ ] T038 [US2] Add colored priority display in handle_add_task() success message in src/cli/menu.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - visual hierarchy plus color coding

---

## Phase 5: User Story 3 - Improved User Feedback Messages (Priority: P2)

**Goal**: Implement clear, visually distinct feedback for success, errors, and warnings

**Independent Test**: Perform various operations and verify success=green, errors=red, warnings=yellow with appropriate symbols

### Implementation for User Story 3

- [ ] T039 [US3] Update handle_add_task() in src/cli/menu.py to use format_success() for task created message
- [ ] T040 [US3] Update handle_add_task() in src/cli/menu.py to use format_error() for empty title error
- [ ] T041 [US3] Update handle_add_task() in src/cli/menu.py to use format_warning() for invalid date warning
- [ ] T042 [US3] Update handle_add_task() in src/cli/menu.py to use format_error() for ValueError exceptions
- [ ] T043 [US3] Update handle_update_task() in src/cli/menu.py to use format_error() for invalid ID error
- [ ] T044 [US3] Update handle_update_task() in src/cli/menu.py to use format_error() for task not found error
- [ ] T045 [US3] Update handle_update_task() in src/cli/menu.py to use format_success() for update success message
- [ ] T046 [US3] Update handle_update_task() in src/cli/menu.py to use format_warning() for invalid date warning
- [ ] T047 [US3] Update handle_delete_task() in src/cli/menu.py to use format_error() for invalid ID error
- [ ] T048 [US3] Update handle_delete_task() in src/cli/menu.py to use format_success() for delete success message
- [ ] T049 [US3] Update handle_delete_task() in src/cli/menu.py to use format_error() for task not found error
- [ ] T050 [US3] Update handle_mark_status() in src/cli/menu.py to use format_error() for invalid ID error
- [ ] T051 [US3] Update handle_mark_status() in src/cli/menu.py to use format_error() for task not found error
- [ ] T052 [US3] Update handle_mark_status() in src/cli/menu.py to use format_success() for status change success
- [ ] T053 [US3] Update handle_mark_status() in src/cli/menu.py to use format_info() for auto-generated recurring task message
- [ ] T054 [US3] Update handle_mark_status() in src/cli/menu.py to use format_error() for ValueError exceptions
- [ ] T055 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_error() for invalid ID error
- [ ] T056 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_error() for task not found error
- [ ] T057 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_success() for tags added message
- [ ] T058 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_success() for tag removed message
- [ ] T059 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_info() for no tags to remove message
- [ ] T060 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_info() for cancelled message
- [ ] T061 [US3] Update handle_manage_tags() in src/cli/menu.py to use format_error() for invalid choice
- [ ] T062 [US3] Update handle_search_tasks() in src/cli/menu.py to use format_info() for no results message
- [ ] T063 [US3] Update handle_filter_tasks() in src/cli/menu.py to use format_info() for no results message
- [ ] T064 [US3] Update handle_filter_tasks() in src/cli/menu.py to use format_info() for cancelled message
- [ ] T065 [US3] Update handle_filter_tasks() in src/cli/menu.py to use format_error() for invalid choice
- [ ] T066 [US3] Update handle_sort_tasks() in src/cli/menu.py to use format_success() for all sort preference messages
- [ ] T067 [US3] Update handle_sort_tasks() in src/cli/menu.py to use format_info() for cancelled message
- [ ] T068 [US3] Update handle_sort_tasks() in src/cli/menu.py to use format_error() for invalid choice
- [ ] T069 [US3] Update handle_check_reminders() in src/cli/menu.py to use format_info() for no reminders message
- [ ] T070 [US3] Update get_menu_choice() error in src/main.py to use format_error() for invalid choice
- [ ] T071 [US3] Update main() exit message in src/main.py to use format_success() for "Goodbye!"

**Checkpoint**: At this point, all user stories 1, 2, and 3 work - complete visual feedback system

---

## Phase 6: User Story 4 - Enhanced Input Prompts and Help Text (Priority: P3)

**Goal**: Implement input prompts with examples, format hints, and available options

**Independent Test**: Enter input scenarios and verify all prompts show format examples and valid options inline

### Implementation for User Story 4

- [ ] T072 [US4] Implement format_input_prompt(prompt: str, hint: str, current: str) in src/cli/formatter.py
- [ ] T073 [US4] Update priority prompt in handle_add_task() to show format_input_prompt with options and default
- [ ] T074 [US4] Update tags prompt in handle_add_task() to show format_input_prompt with format hint
- [ ] T075 [US4] Update recurrence prompt in handle_add_task() to show format_input_prompt with options and default
- [ ] T076 [US4] Update due date prompt in handle_add_task() to show format_input_prompt with examples
- [ ] T077 [US4] Update title prompt in handle_update_task() to show format_input_prompt with current value
- [ ] T078 [US4] Update description prompt in handle_update_task() to show format_input_prompt with current value
- [ ] T079 [US4] Update priority prompt in handle_update_task() to show format_input_prompt with options and current
- [ ] T080 [US4] Update recurrence prompt in handle_update_task() to show format_input_prompt with options and current
- [ ] T081 [US4] Update due date prompt in handle_update_task() to show format_input_prompt with examples and current
- [ ] T082 [US4] Update status prompt in handle_mark_status() to show format_input_prompt with valid statuses
- [ ] T083 [US4] Update menu choice prompt in get_menu_choice() to show format_input_prompt with hint
- [ ] T084 [US4] Add hint to main menu display showing quick quit option or help text
- [ ] T085 [US4] Update filter menu in handle_filter_tasks() to show clearer option descriptions
- [ ] T086 [US4] Update sort menu in handle_sort_tasks() to show clearer option descriptions
- [ ] T087 [US4] Update tags management menu in handle_manage_tags() to show clearer option descriptions

**Checkpoint**: All input prompts now provide helpful guidance and reduce user errors

---

## Phase 7: User Story 5 - Progress and Loading Indicators (Priority: P3)

**Goal**: Implement visual indicators for multi-step operations and confirmations

**Independent Test**: Perform multi-step operations and verify step indicators and confirmation prompts appear

### Implementation for User Story 5

- [ ] T088 [US5] Implement format_confirmation_prompt(message: str, default: bool) in src/cli/formatter.py
- [ ] T089 [US5] Implement format_step_indicator(current: int, total: int, step_name: str) in src/cli/formatter.py
- [ ] T090 [US5] Add confirmation prompt to handle_delete_task() before deleting task
- [ ] T091 [US5] Add step indicators to handle_add_task() showing current field being entered
- [ ] T092 [US5] Add step indicators to handle_update_task() showing current field being updated
- [ ] T093 [US5] Add step indicators to handle_manage_tags() showing current step in tag management
- [ ] T094 [US5] Add summary message after handle_update_task() showing what fields were changed
- [ ] T095 [US5] Add summary message after handle_manage_tags() showing tag operation result

**Checkpoint**: All complex operations now have clear progress indication and confirmations

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and edge case handling

- [ ] T096 [P] Test NO_COLOR environment variable fallback (set NO_COLOR=1 and verify symbols work)
- [ ] T097 [P] Test with very long task titles (>100 chars) and verify text wrapping in panels
- [ ] T098 [P] Test with multi-line descriptions and verify proper formatting in panels
- [ ] T099 [P] Test with many tags (>10) and verify display doesn't break formatting
- [ ] T100 [P] Test with special characters in task titles and verify proper escaping
- [ ] T101 Test on Windows Command Prompt and verify color display works correctly
- [ ] T102 Test on Windows PowerShell and verify color display works correctly
- [ ] T103 Verify terminal width <80 chars doesn't break formatting (graceful degradation)
- [ ] T104 Run through all acceptance criteria from spec.md and verify each passes
- [ ] T105 Add docstrings to all functions in src/cli/formatter.py with type hints
- [ ] T106 Update imports in src/cli/menu.py to include all formatter functions
- [ ] T107 Verify console output maintains consistent spacing throughout application

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - Can proceed sequentially in priority order (US1 → US2 → US3 → US4 → US5)
  - US2 depends on US1 (uses format_task_panel from US1)
  - US3-US5 can build incrementally on US1-US2
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 (extends format_task_panel created in US1)
- **User Story 3 (P2)**: Can start after Foundational - Uses format functions from Foundational
- **User Story 4 (P3)**: Can start after Foundational - Independent of other stories
- **User Story 5 (P3)**: Can start after Foundational - Independent of other stories

### Within Each User Story

- US1: T010-T012 can run in parallel (different functions)
- US1: T013-T023 must run sequentially (same file: menu.py)
- US1: T024 must complete before T025-T026
- US2: T028-T030 can run in parallel (different functions)
- US2: T031-T033 must run sequentially (modify same function)
- US3: All tasks modify menu.py sequentially
- US4: All tasks modify menu.py sequentially
- US5: T088-T089 can run in parallel (different functions)

### Parallel Opportunities

- Phase 1: T001 and T002 can run together
- Phase 2: T003-T004 can run together, T006-T009 can run together
- Phase 8: T096-T105 (most test tasks) can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T009) - CRITICAL
3. Complete Phase 3: User Story 1 (T010-T027)
4. **STOP and VALIDATE**: Test all menus have visual hierarchy
5. Demo if ready - basic visual improvements working

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP - visual hierarchy!)
3. Add User Story 2 → Test independently → Demo (colors added!)
4. Add User Story 3 → Test independently → Demo (feedback messages!)
5. Add User Story 4 → Test independently → Demo (better prompts!)
6. Add User Story 5 → Test independently → Demo (progress indicators!)
7. Complete Polish → Final validation → Full feature complete

Each story adds value without breaking previous stories.

---

## Notes

- [P] tasks = different files or functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each logical group of tasks
- Stop at any checkpoint to validate story independently
- src/cli/menu.py modifications should be done carefully to avoid breaking existing logic
- All existing functionality must remain intact - only display changes
- Use console = get_console() consistently across all menu functions
