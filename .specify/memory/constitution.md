<!--
=============================================================================
SYNC IMPACT REPORT
=============================================================================
Version Change: 1.0.0 (initial) → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Key Standards
  - Constraints
  - Phases Overview
  - Governance
Removed Sections: N/A (initial creation)
Templates Validated:
  - .specify/templates/plan-template.md ✅ (Constitution Check section present)
  - .specify/templates/spec-template.md ✅ (Requirements/Success Criteria aligned)
  - .specify/templates/tasks-template.md ✅ (User story organization compatible)
Follow-up TODOs: None
=============================================================================
-->

# Hackathon II - The Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development

All implementations MUST start with detailed specifications refined through iterations with Claude Code. No code generation may proceed without an approved specification document. Specifications serve as the single source of truth for feature requirements and acceptance criteria.

**Rationale**: Ensures alignment between intent and implementation; reduces rework; creates traceable audit trail from requirements to code.

### II. No Manual Coding

Code generation MUST be handled exclusively by Claude Code. Human developers refine specifications until Claude Code produces correct output. Direct manual code editing is prohibited except for configuration files and environment setup.

**Rationale**: Validates the Agentic Dev Stack workflow; ensures all implementations are traceable to specs and AI generations; demonstrates the hackathon's core thesis.

### III. Iterative Evolution

The application MUST progress through defined phases: console app → web application → AI chatbot → local Kubernetes → cloud deployment. Each phase builds upon the previous, maintaining backward compatibility and feature parity.

**Rationale**: Demonstrates progressive complexity mastery; ensures solid foundations before advanced features; provides clear milestones for evaluation.

### IV. Cloud-Native Focus

Architecture MUST emphasize containerization, orchestration, event-driven patterns, and AIOps. All production-bound code must be container-ready. Kubernetes manifests and Helm charts are first-class artifacts.

**Rationale**: Prepares application for scalable, resilient deployment; aligns with modern infrastructure practices; enables advanced features like auto-scaling and service mesh.

### V. Reusable Intelligence

Agent skills and subagents MUST be developed as modular, reusable components. MCP tools must be stateless and composable. AI agent behaviors must be defined declaratively and be testable independently.

**Rationale**: Promotes code reuse across phases; enables bonus features like multi-language support; supports the agentic development paradigm.

### VI. Stateless Design

Chatbots, API handlers, and MCP tools MUST be stateless. All state MUST be persisted to the database (Neon PostgreSQL). Session and conversation state must be recoverable from database alone.

**Rationale**: Enables horizontal scaling; simplifies container orchestration; ensures reliability across restarts and deployments.

### VII. Multi-User Data Isolation

All data operations MUST be scoped by user_id. API endpoints MUST validate user ownership before data access. Cross-user data leakage is a critical failure.

**Rationale**: Security requirement for multi-tenant application; enables safe shared infrastructure; meets hackathon evaluation criteria.

## Key Standards

### Technology Stack Adherence

- **Phase I**: Python 3.13+, UV package manager
- **Phase II**: Next.js 16+ (App Router), Python FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- **Phase III**: OpenAI Agents SDK, Official MCP SDK, OpenAI ChatKit
- **Phase IV**: Docker Desktop, Minikube, Helm Charts, kubectl-ai, Kagent
- **Phase V**: Kafka/Dapr, Azure AKS/Google GKE/Oracle OKE, GitHub Actions CI/CD

### Authentication and Security

- User authentication via Better Auth (signup/signin)
- API security via JWT tokens for user isolation
- Secrets managed via environment variables; never hardcoded
- OWASP Top 10 compliance mandatory

### API Contract Standards

- RESTful endpoints following pattern: `/api/{user_id}/resource`
- JSON request/response format
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- All endpoints documented with input/output schemas

### Testing Discipline

- All acceptance criteria must be independently testable
- Contract tests for API endpoints
- Integration tests for user journeys
- Tests must fail before implementation (TDD when applicable)

## Constraints

### Development Environment

- Development MUST use WSL 2 on Windows
- Python version MUST be 3.13+
- Package management via UV exclusively
- No additional tools beyond specified stacks

### Feature Progression

Features MUST be implemented progressively:

1. **Basic Level**: Add, Delete, Update, View, Mark Complete
2. **Intermediate Level**: Priorities, Tags, Search, Filter, Sort
3. **Advanced Level**: Recurring Tasks, Due Dates, Reminders

### Deployment Requirements

- **Phase IV**: Local deployment on Minikube
- **Phase V**: Cloud deployment on DigitalOcean, Azure, Google Cloud, or Oracle

### Submission Requirements

- Public GitHub repository
- Constitution file (.specify/memory/constitution.md)
- Specs history folder (specs/)
- Source code in /src
- README.md with setup instructions
- CLAUDE.md with Claude Code instructions
- Demo video under 90 seconds

## Phases Overview

| Phase | Objective | Key Deliverables |
|-------|-----------|------------------|
| I | In-Memory Console App | Python CLI with basic CRUD |
| II | Full-Stack Web App | Next.js + FastAPI + Neon DB |
| III | AI Chatbot | MCP Server + OpenAI Agents |
| IV | Local Kubernetes | Minikube + Helm Charts |
| V | Cloud Deployment | AKS/GKE/OKE + Kafka/Dapr |

## Governance

### Amendment Procedure

1. Proposed changes documented in PR description
2. Impact analysis on existing artifacts required
3. Version bump following semantic versioning
4. All dependent templates updated synchronously

### Versioning Policy

- **MAJOR**: Backward incompatible principle changes
- **MINOR**: New principles or sections added
- **PATCH**: Clarifications and wording improvements

### Compliance Review

- All PRs must verify constitution compliance
- Spec-driven development violations block merge
- Manual code introduction requires explicit justification and approval

### Runtime Guidance

For development guidance beyond this constitution, refer to:
- `CLAUDE.md` for Claude Code operational instructions
- `README.md` for project setup and execution
- Individual feature specs in `specs/` directory

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
