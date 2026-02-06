# Implementation Plan: Authentication & User Identity

**Branch**: `001-auth-user-identity` | **Date**: 2026-01-14 | **Spec**: [spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-auth-user-identity/spec.md`

## Summary

This plan covers implementing secure user authentication for the Phase II Todo Full-Stack Web Application using Better Auth (frontend) and JWT-based verification (backend). The implementation enables users to sign up and sign in, receive JWT tokens, and access protected API endpoints with enforced user isolation. The architecture follows a clean separation: Better Auth handles credential management and JWT issuance on the Next.js frontend, while the FastAPI backend independently verifies JWT signatures using a shared secret and enforces that authenticated users can only access their own data.

## Technical Context

**Language/Version**: TypeScript (Next.js 16+ App Router), Python 3.11+ (FastAPI)
**Primary Dependencies**: Better Auth (Next.js), PyJWT (FastAPI), jose (for JWT verification in Node.js if needed)
**Storage**: Neon Serverless PostgreSQL for user persistence (handled by Better Auth adapter)
**Testing**: Jest/Vitest (frontend), pytest (backend), integration tests for end-to-end auth flow
**Target Platform**: Web browser (frontend), Linux server (backend API)
**Project Type**: Web application with separate frontend and backend
**Performance Goals**: Token verification <50ms p95, support concurrent authenticated users
**Constraints**: MUST use Better Auth for frontend authentication; MUST use shared JWT secret via BETTER_AUTH_SECRET; MUST NOT rely on frontend session state for backend authorization
**Scale/Scope**: Single-instance deployment for hackathon; supports multiple users with isolated task data

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-driven development**: Feature follows spec → plan → tasks → code path (this plan is evidence)
- [x] **Agentic workflow**: All implementation will be performed via Claude Code (no manual coding)
- [x] **Incremental evolution**: Authentication builds on Phase I foundations (user model concepts) without breaking them
- [x] **Clean architecture**: Clear separation between frontend auth (Better Auth) and backend verification (FastAPI dependency)
- [x] **Phase II tech stack alignment**: Next.js, FastAPI, SQLModel, Neon DB as required by constitution
- [x] **Multi-user task isolation**: User ID from JWT enforced on all backend data access
- [x] **JWT authentication**: BETTER_AUTH_SECRET environment variable used for signature verification

## Project Structure

### Documentation (this feature)

```text
specs/001-auth-user-identity/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── auth/            # Better Auth configuration
│   ├── components/      # Auth UI components (sign in/up forms)
│   └── lib/             # Auth utilities, API client with JWT attachment
└── tests/
    └── auth/            # Auth integration tests

backend/
├── src/
│   ├── auth/            # JWT verification dependency
│   ├── api/             # Protected endpoints that require auth
│   └── models/          # User entity (SQLModel)
└── tests/
    └── auth/            # Auth verification tests
```

**Structure Decision**: Web application structure with separate frontend and backend directories. Frontend handles credential management via Better Auth; backend contains reusable JWT verification logic in `auth/` module for injection into protected endpoints via FastAPI dependencies.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations. The architecture follows standard patterns for split-frontend JWT auth without introducing additional projects, patterns, or dependencies beyond the specified stack.

---

## Phase 0: Research

### Open Questions from Technical Context

1. **Better Auth JWT plugin configuration**: Need to confirm exact Better Auth plugins required for JWT token generation and how to expose the token to the frontend client.
2. **JWT claim structure**: Need to determine which claims (sub, exp, iat) must be included and how user identity is encoded.
3. **FastAPI dependency pattern**: Need to decide between middleware vs. dependency injection for JWT verification on protected routes.

### Research Tasks

- Task: "Research Better Auth JWT plugin configuration for Next.js and token exposure patterns"
- Task: "Research FastAPI JWT verification patterns with PyJWT or python-jose"
- Task: "Research user isolation patterns in FastAPI using dependency injection"

---

## Phase 1: Design & Contracts

### Data Model

The User entity represents authenticated users. Better Auth handles credential storage; the backend needs only the user ID for authorization decisions.

```typescript
// frontend (Better Auth schema - handled by adapter)
interface User {
  id: string           // Primary identifier, used in JWT sub claim
  email: string        // For display/contact purposes
  createdAt: Date      // Account creation timestamp
}

// backend (SQLModel - for potential future use)
interface User {
  id: string           // Primary identifier, matches JWT sub claim
  email: string        // Denormalized for query optimization
}
```

### API Contracts

#### Authentication Flow

```
Client (Next.js + Better Auth)
  │
  ├─► POST /api/auth/signup  → Creates user account, returns session + JWT
  ├─► POST /api/auth/signin  → Validates credentials, returns session + JWT
  │
  └─► Protected API calls with Authorization: Bearer <JWT>
        │
        ▼
Backend (FastAPI)
  │
  ├─► JWT Verification Dependency
  │     │
  │     └─► Validates signature using BETTER_AUTH_SECRET
  │           Extracts userId from JWT claims
  │           Returns authenticated user context
  │
  └─► Protected Endpoints (require auth)
        │
        ├─► GET /api/todos           → Returns todos for authenticated user
        ├─► POST /api/todos          → Creates todo owned by authenticated user
        ├─► GET /api/todos/{id}      → Returns todo only if owned by authenticated user
        └─► ... (other CRUD operations)
```

#### JWT Token Structure

```json
{
  "sub": "user-uuid-here",
  "iat": 1736894400,
  "exp": 1736898000,
  "iss": "todo-app"
}
```

#### Error Responses

```json
// 401 Unauthorized
{
  "error": "unauthorized",
  "message": "Missing or invalid authentication token"
}
```

```json
// 403 Forbidden (user id mismatch)
{
  "error": "forbidden",
  "message": "Cannot access resources for another user"
}
```

---

## Phase 2: Next Steps

After this plan is approved:

1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Execute tasks in order: frontend auth setup → backend JWT verification → integration tests
3. Each task produces code via Claude Code prompts (no manual coding)
4. Verify success criteria from spec after implementation

---

## Quickstart

**Prerequisites**:
- Next.js frontend project initialized
- FastAPI backend project initialized
- BETTER_AUTH_SECRET environment variable set (shared secret)
- Neon PostgreSQL connection string available

**Setup order**:
1. Install Better Auth and configure JWT plugin in frontend
2. Create JWT verification dependency in backend
3. Add auth dependency to protected endpoints
4. Test end-to-end: signup → signin → call protected endpoint with JWT
