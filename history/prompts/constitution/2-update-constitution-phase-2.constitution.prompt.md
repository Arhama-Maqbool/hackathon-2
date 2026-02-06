---
id: 2
title: Update Constitution Phase 2
stage: constitution
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: sp.constitution
labels: [constitution, governance, phase-2, hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: Phase II – Todo Full-Stack Web Application (Hackathon)

Scope division:
This project is divided into three specifications:
1. Authentication & User Identity (Better Auth + JWT)
2. Backend API & Data Persistence (FastAPI + SQLModel + Neon PostgreSQL)
3. Frontend Integration & User Experience (Next.js App Router)

Core principles:
- Spec-driven development: All work follows the Spec → Plan → Tasks → Implementation flow
- No manual coding: All implementation must be generated via Claude Code using approved prompts
- Security-first design: Authentication, authorization, and user isolation are mandatory
- Correctness: API behavior must strictly match defined specifications
- Reproducibility: Prompts, plans, and outputs must be traceable and reviewable
- Separation of concerns: Frontend, backend, authentication, and database logic are clearly separated

Key standards:
- All REST API endpoints follow RESTful conventions
- JWT-based authentication enforced on all protected endpoints
- Task ownership enforced on every database query and mutation
- Unauthorized requests must return HTTP 401
- Frontend must attach JWT tokens to all API requests
- Backend must verify JWT signature using shared secret
- Database access handled exclusively via SQLModel ORM
- Neon Serverless PostgreSQL used for persistent storage
- Each spec must produce its own specification and plan artifacts

Constraints:
- Technology stack is fixed:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (JWT-based)
- Shared JWT secret configured via environment variable BETTER_AUTH_SECRET
- No cross-service session sharing between frontend and backend
- No deviation from Agentic Dev Stack workflow
- Phase evaluated on process, prompts, and iterations, not only final output

Success criteria:
- All 5 basic Todo features implemented as a web application
- Multi-user support with strict user data isolation
- JWT authentication correctly enforced end-to-end
- Backend APIs return correct data filtered by authenticated user
- Frontend correctly reflects authenticated user state
- All three specs completed with corresponding plans and prompts
- Project passes functional, security, and workflow review

## Response snapshot

Initial analysis shows existing constitution at .specify/memory/constitution.md already contains:
- Core principles (spec-driven development, agentic workflow, incremental evolution, traceability, clean architecture, reproducibility)
- Phase-specific standards for Phase II (Full-Stack Web Application) matching the tech stack
- Development workflow standards and governance

The existing constitution v1.0.0 (ratified 2026-01-02) is aligned with the Phase II requirements. Key findings:
- Technology stack matches (Next.js, FastAPI, SQLModel, Neon DB, Authentication)
- Multi-user task isolation is already in Phase II standards
- Spec → Plan → Tasks → Implementation workflow is covered by "spec-driven development" principle
- No [NEEDS CLARIFICATION] markers or placeholders remain in the existing constitution

Decision: Constitution is already suitable for Phase II; no updates needed at this time. The existing
constitution provides adequate guidance for the Authentication & User Identity specification.

## Outcome

- ✅ Impact: Constitution reviewed for Phase II alignment - existing v1.0.0 is suitable
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md (no changes made)
- 🔁 Next prompts: Proceed to /sp.specify for Authentication & User Identity
- 🧠 Reflection: Existing constitution covers Phase II requirements; no amendment needed

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): constitution review - no updates required
- Prompt variant (if applicable): constitutional review for Phase II alignment
- Next experiment (smallest change to try): none needed - constitution already suitable
