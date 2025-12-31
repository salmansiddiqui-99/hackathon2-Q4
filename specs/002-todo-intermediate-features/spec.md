# Feature Specification: Todo Intermediate Features

**Feature Branch**: `002-todo-intermediate-features`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase I Extension: Intermediate Level Features (Organization & Usability) - Extending the in-memory Python console Todo app with priorities, tags, search/filter, and sort capabilities"

**Prerequisite**: This feature extends `001-todo-console-app`. All Basic Level features (add, list, update, delete, mark status) must remain fully functional.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Priority Assignment (Priority: P1)

As a user, I want to assign priority levels (high/medium/low) to my tasks so that I can focus on what's most important.

**Why this priority**: Priority is foundational for organization features. It affects display, sorting, and helps users identify urgent tasks at a glance.

**Independent Test**: Create tasks with different priorities, list them, verify priorities are displayed correctly.

**Acceptance Scenarios**:

1. **Given** the user is adding a new task, **When** prompted for priority, **Then** they can enter high, medium, or low (default: medium if skipped)
2. **Given** a task exists, **When** user updates the task, **Then** they can change its priority level
3. **Given** tasks exist with different priorities, **When** user lists tasks, **Then** each task displays its priority alongside other attributes
4. **Given** the user enters an invalid priority, **When** adding or updating, **Then** an error message shows valid options (high, medium, low)

---

### User Story 2 - Tags/Categories (Priority: P1)

As a user, I want to assign multiple tags to my tasks so that I can categorize and organize them by context (work, home, personal, etc.).

**Why this priority**: Tags enable flexible categorization beyond priority. Critical for search/filter functionality.

**Independent Test**: Create tasks with tags, add/remove tags from existing tasks, verify tags display in list.

**Acceptance Scenarios**:

1. **Given** the user is adding a new task, **When** prompted for tags, **Then** they can enter comma-separated tags (e.g., "work, urgent") or skip for no tags
2. **Given** a task exists, **When** user chooses to manage tags, **Then** they can add new tags or remove existing ones
3. **Given** tasks exist with tags, **When** user lists tasks, **Then** each task displays its tags (e.g., "[work, urgent]")
4. **Given** the user adds a duplicate tag to a task, **When** saving, **Then** the duplicate is ignored (no duplicate tags per task)
5. **Given** the user removes a tag from a task, **When** confirmed, **Then** that tag no longer appears on the task

---

### User Story 3 - Search Tasks (Priority: P2)

As a user, I want to search my tasks by keyword so that I can quickly find tasks containing specific text.

**Why this priority**: Search is a key usability feature but depends on having tasks with varied content (titles, descriptions, tags).

**Independent Test**: Create tasks with varied content, search by keyword, verify matching tasks are returned.

**Acceptance Scenarios**:

1. **Given** tasks exist with various titles and descriptions, **When** user searches with a keyword, **Then** tasks matching the keyword in title, description, or tags are displayed
2. **Given** a search is performed, **When** no tasks match, **Then** a message indicates no results found
3. **Given** a search is performed, **When** tasks match, **Then** they are displayed in the same format as the full list (with ID, title, description, status, priority, tags)
4. **Given** the user enters an empty search term, **When** searching, **Then** all tasks are shown (no filter applied)

---

### User Story 4 - Filter Tasks (Priority: P2)

As a user, I want to filter my task list by status, priority, or tag so that I can focus on specific subsets of tasks.

**Why this priority**: Filtering complements search and enables focused task views. Depends on priority and tags being implemented.

**Independent Test**: Create tasks with varied attributes, apply filters, verify only matching tasks appear.

**Acceptance Scenarios**:

1. **Given** tasks exist with different statuses, **When** user filters by status (pending/in-progress/completed), **Then** only tasks with that status are shown
2. **Given** tasks exist with different priorities, **When** user filters by priority (high/medium/low), **Then** only tasks with that priority are shown
3. **Given** tasks exist with different tags, **When** user filters by a specific tag, **Then** only tasks containing that tag are shown
4. **Given** a filter is applied, **When** no tasks match the criteria, **Then** a message indicates no tasks match the filter
5. **Given** the user wants to see all tasks again, **When** they clear filters, **Then** the full task list is displayed

---

### User Story 5 - Sort Tasks (Priority: P2)

As a user, I want to sort my task list by priority, title, or creation order so that I can view tasks in my preferred order.

**Why this priority**: Sorting enhances usability after basic organization features are in place.

**Independent Test**: Create multiple tasks, apply different sort options, verify order changes correctly.

**Acceptance Scenarios**:

1. **Given** tasks exist with different priorities, **When** user sorts by priority, **Then** tasks are ordered high → medium → low
2. **Given** tasks exist with different titles, **When** user sorts alphabetically, **Then** tasks are ordered A-Z by title
3. **Given** multiple tasks exist, **When** user sorts by creation order, **Then** tasks are shown in the order they were added (oldest first) or newest first (user choice)
4. **Given** the user applies a sort, **When** the list is displayed, **Then** the current sort order is indicated
5. **Given** sorting is combined with filtering, **When** both are active, **Then** only filtered tasks are shown in the sorted order

---

### Edge Cases

- What happens when searching with special characters? The system performs literal string matching; special characters are treated as regular text.
- How does filter by tag handle case sensitivity? Tag matching is case-insensitive (e.g., "Work" matches "work").
- What happens when sorting tasks with the same priority? Tasks with equal priority maintain their relative order (stable sort).
- Can filters be combined (e.g., priority AND status)? For Phase I, only single-dimension filtering is supported (one filter at a time).
- How are tags normalized? Tags are stored in lowercase and trimmed of whitespace.

## Requirements *(mandatory)*

### Functional Requirements

**Priority Feature:**
- **FR-101**: System MUST allow users to assign priority (high/medium/low) when adding a task
- **FR-102**: System MUST default to "medium" priority if user skips priority input
- **FR-103**: System MUST allow users to change task priority during update
- **FR-104**: System MUST display task priority in the list view

**Tags Feature:**
- **FR-201**: System MUST allow users to assign zero or more tags when adding a task
- **FR-202**: System MUST accept comma-separated tag input (e.g., "work, urgent, home")
- **FR-203**: System MUST provide a menu option to add tags to an existing task
- **FR-204**: System MUST provide a menu option to remove tags from an existing task
- **FR-205**: System MUST prevent duplicate tags on the same task
- **FR-206**: System MUST normalize tags to lowercase and trim whitespace
- **FR-207**: System MUST display task tags in the list view (e.g., "[work, urgent]")

**Search Feature:**
- **FR-301**: System MUST provide a search option in the menu
- **FR-302**: System MUST search across title, description, and tags
- **FR-303**: System MUST perform case-insensitive keyword matching
- **FR-304**: System MUST display matching tasks in standard list format
- **FR-305**: System MUST show "no results" message when search finds no matches

**Filter Feature:**
- **FR-401**: System MUST provide a filter option in the menu
- **FR-402**: System MUST support filtering by status (pending/in-progress/completed)
- **FR-403**: System MUST support filtering by priority (high/medium/low)
- **FR-404**: System MUST support filtering by tag
- **FR-405**: System MUST display filtered tasks in standard list format
- **FR-406**: System MUST provide option to clear active filter

**Sort Feature:**
- **FR-501**: System MUST provide a sort option in the menu
- **FR-502**: System MUST support sorting by priority (high → medium → low)
- **FR-503**: System MUST support sorting alphabetically by title (A-Z)
- **FR-504**: System MUST support sorting by creation order (oldest first or newest first)
- **FR-505**: System MUST indicate current sort order when listing tasks
- **FR-506**: System MUST apply sort to both full list and filtered results

**Backward Compatibility:**
- **FR-601**: System MUST preserve all Basic Level features (add, list, update, delete, mark status, exit)
- **FR-602**: System MUST maintain existing Task attributes (id, title, description, status)

### Key Entities

- **Task** (extended): Represents a todo item with the following attributes:
  - ID: Unique numeric identifier (auto-generated, immutable)
  - Title: Short description of the task (required, non-empty, mutable)
  - Description: Detailed information about the task (optional, can be empty, mutable)
  - Status: Current state (pending | in-progress | completed)
  - Priority: Importance level (high | medium | low), default: medium
  - Tags: List of category labels (list of lowercase strings), default: empty list
  - Created_at: Timestamp of task creation (auto-generated, immutable) - for sort by creation order

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-101**: Users can assign and view priorities on 100% of tasks
- **SC-102**: Users can add/remove tags with immediate visual feedback in list view
- **SC-103**: Search returns results in under 1 second for up to 100 tasks
- **SC-104**: Filter reduces displayed tasks to only matching criteria
- **SC-105**: Sort reorders task display according to selected criteria
- **SC-106**: All 5 Basic Level features continue to work correctly after extension
- **SC-107**: All new features accessible through clear, numbered menu options
- **SC-108**: 100% of code generated via Claude Code iterations with no manual edits

## Clarifications

### Session 2025-12-31

(To be filled during /sp.clarify if needed)

## Assumptions

- Menu will be extended with new options for search, filter, sort, and tag management
- Priority and tags can be optionally set during task creation (not mandatory)
- Single filter dimension at a time (no combined filters like "high priority AND work tag")
- Search is substring matching, not exact match or regex
- Creation timestamp is added to Task model for sort-by-creation functionality
- Existing tasks from Basic Level (if any in session) will have default priority (medium) and empty tags
