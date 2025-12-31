---
id: 002
title: Create Implementation Plan
stage: plan
date: 2025-12-31
surface: agent
model: claude-opus-4-5-20251101
feature: 003-todo-advanced-features
branch: 003-todo-advanced-features
user: haroon traders
command: /sp.plan
labels: ["planning", "architecture", "recurring-tasks", "due-dates", "reminders"]
links:
  spec: specs/003-todo-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-todo-advanced-features/plan.md
tests:
  - Plan covers all 5 user stories
  - All architecture decisions documented
---

## Prompt

/sp.plan

create:
  - task_model_extension: Extend Task class with due_date (datetime), recurrence_rule, and parent_recurring_id
  - recurrence_engine: Logic to generate next instance when recurring task is marked complete
  - date_parsing_system: Natural language date input parsing for due dates
  - reminder_system: "Check reminders" command to simulate notifications for overdue/soon-due tasks
  - menu_and_display_updates: Add new commands and enhance list view for due dates and recurrence info
  - quality_validation: Comprehensive checks to preserve all prior functionality

decisions_needing_documentation:
  - due_date_representation: datetime_object (from datetime import datetime)
  - date_input_parsing: natural_language_parsing using simple keyword/rules-based parser
  - recurrence_representation: template_plus_instances model
  - recurrence_patterns_supported: limited_set (daily, weekly, monthly by date)
  - reminder_delivery: on_demand_command

testing_strategy:
  - Manual console interaction
  - Preserve all Basic and Intermediate features
  - Test with current date (December 31, 2025)

## Response snapshot

Created comprehensive implementation plan with:

**Architecture Decisions**: 5 documented
- AD-1: Due date as datetime object
- AD-2: Natural language parsing (custom rules-based)
- AD-3: Template-plus-instances for recurrence
- AD-4: Limited recurrence patterns (daily/weekly/monthly)
- AD-5: On-demand reminder command

**Implementation Phases**: 8 phases
1. Model Extension - Add recurrence, due_date fields
2. Date Parsing Utility - Natural language parser
3. Recurrence Engine - Next date calculation
4. Service Layer Extension - Auto-generation, reminder queries
5. CLI Extension - Menu handlers, display updates
6. Main Loop Update - Wire option 10, renumber exit
7. Module Exports - Clean package structure
8. Quality Validation - Backward compatibility checks

**File Changes**: 8 files (3 new, 5 modified)
- New: date_parser.py, recurrence.py, utils/__init__.py
- Modified: task.py, task_service.py, menu.py, main.py, cli/__init__.py

**Dependencies**: None (stdlib only)

## Outcome

- Impact: Complete implementation roadmap for Advanced Level features
- Tests: Plan validated against all 5 user stories
- Files: 1 file created (plan.md)
- Next prompts: `/sp.tasks` to generate task breakdown
- Reflection: Plan follows user decisions exactly, no external dependencies

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Plan structure PASS
- Prompt variant (if applicable): User-provided decisions integrated
- Next experiment (smallest change to try): N/A - proceed to task generation
