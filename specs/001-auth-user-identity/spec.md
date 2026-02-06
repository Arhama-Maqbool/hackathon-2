# Feature Specification: Authentication & User Identity

**Feature Branch**: `001-auth-user-identity`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "Authentication & User Identity (Spec 1) for Phase II Todo Full-Stack Web Application (Hackathon): implement user authentication with Better Auth, issue JWT tokens, and enforce stateless JWT verification + user isolation in the backend API."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sign up and sign in (Priority: P1)

A user can create an account and sign in, and receives an authentication token they can use to access
protected app features.

**Why this priority**: Without sign up/sign in, no other multi-user or isolation requirements can be
validated.

**Independent Test**: A reviewer can sign up, sign in, and observe that the user receives a JWT token
(or equivalent auth token) suitable for API requests.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they sign up with valid credentials, **Then** the user account is
   created and the user is authenticated.
2. **Given** an existing user, **When** they sign in with valid credentials, **Then** the user is
   authenticated and receives a JWT.
3. **Given** an existing user, **When** they sign in with invalid credentials, **Then** authentication
   fails and no JWT is issued.

---

### User Story 2 - Use JWT to access protected API (Priority: P2)

An authenticated user can call protected API endpoints by attaching their JWT token to requests.

**Why this priority**: This is the end-to-end contract between frontend and backend for authenticated
actions.

**Independent Test**: A reviewer can take a valid JWT token and call a protected endpoint successfully
by attaching it to the request as a bearer token.

**Acceptance Scenarios**:

1. **Given** a valid JWT, **When** the user calls a protected API endpoint while presenting the token
   as a bearer token, **Then** the request is accepted and processed.
2. **Given** a valid JWT, **When** the backend extracts user identity from the token, **Then** the
   backend treats the request as belonging to that user.

---

### User Story 3 - Reject unauthenticated / unauthorized requests (Priority: P3)

Requests without a valid JWT are rejected, and requests cannot operate on another user’s resources.

**Why this priority**: Prevents cross-user data exposure and enforces strict user isolation.

**Independent Test**: A reviewer can call the same protected endpoint with (a) no token, (b) an invalid
or expired token, and (c) a valid token for a different user, and verify correct rejection behavior.

**Acceptance Scenarios**:

1. **Given** no Authorization header, **When** a user calls a protected endpoint, **Then** the backend
   returns HTTP 401.
2. **Given** a malformed/invalid/expired JWT, **When** a user calls a protected endpoint, **Then** the
   backend returns HTTP 401.
3. **Given** a valid JWT for user A, **When** a request attempts to access resources owned by user B
   (e.g., the request path contains user B’s user id), **Then** the backend denies the request and
   does not return any of user B’s data.

### Edge Cases

- Missing bearer-token prefix (e.g., token presented without the expected scheme)
- Multiple Authorization headers
- JWT is structurally valid but expired
- JWT signature fails validation (wrong secret)
- JWT missing required identity fields (e.g., missing user id claim)
- User id in request path is malformed
- Authenticated request attempts to enumerate other user ids (must not leak whether other users exist)

## Assumptions & Dependencies

- A shared secret is available to backend services via the `BETTER_AUTH_SECRET` environment variable.
- Authentication is evaluated in the context of a multi-user Todo application; authenticated identity
  will be used by other specs (API + data persistence, frontend integration).
- The client can securely store and present the issued JWT token when calling protected APIs.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support user signup and sign in via Better Auth.
- **FR-002**: Upon successful authentication, system MUST issue a JWT token that represents the
  authenticated user identity.
- **FR-003**: Client MUST attach the JWT to protected API requests using the standard bearer-token
  scheme.
- **FR-004**: Backend MUST treat JWT verification as the source of truth for API authentication, and
  MUST NOT rely on any frontend session validation.
- **FR-005**: Backend MUST validate the JWT signature using a shared secret provided via the
  `BETTER_AUTH_SECRET` environment variable.
- **FR-006**: Backend MUST extract authenticated user identity from the JWT and use it for request
  authorization.
- **FR-007**: API requests without a valid JWT MUST return HTTP 401 Unauthorized.
- **FR-008**: When a request is scoped to a specific user id (e.g., the user id appears in the request
  path), the backend MUST enforce that the authenticated user identity matches that user id; otherwise
  the request MUST be rejected and MUST NOT return data for another user.
- **FR-009**: Backend MUST never return data belonging to a different user than the authenticated user.
- **FR-010**: Authentication/authorization checks MUST be reusable across endpoints via a shared
  backend mechanism (to prevent missed checks on individual endpoints).

### Key Entities *(include if feature involves data)*

- **User**: A person who can sign up/sign in and own todo data.
- **JWT Token**: A signed token that encodes the authenticated user identity and is presented on API
  requests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can complete sign up and sign in in a single flow without external assistance.
- **SC-002**: For a protected API endpoint, requests without a valid JWT are consistently rejected with
  HTTP 401.
- **SC-003**: When running multi-user test scenarios, the backend never returns another user’s data.
- **SC-004**: Reviewers can verify, via repeatable steps, that user identity used by the backend is
  derived solely from JWT verification (not from client-side session state).
