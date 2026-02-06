# Research: Authentication & User Identity

**Feature**: Authentication & User Identity (Spec 1)
**Date**: 2026-01-14

## Research Questions

### Q1: Better Auth JWT Plugin Configuration

**Question**: How to configure Better Auth's JWT plugin in Next.js and expose tokens to the client?

**Findings**:

Better Auth provides a dedicated JWT plugin (`better-auth`) with the `jwtClient()` plugin for client-side token access.

**Configuration**:
```typescript
import { createAuth } from "better-auth";
import { jwtClient } from "better-auth/plugins";

export const auth = createAuth({
  // ... other config
  plugins: [
    jwtClient()
  ]
});
```

**Token Access on Client**:
```typescript
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL
});

// Get current JWT token
const token = await authClient.token();
```

**Key Configuration Options** (from `jwt()` plugin on server):
- `issuer`, `audience`, `expirationTime` (default: 15 minutes)
- `definePayload()`: customize claims included in token
- `getSubject()`: customize the subject claim (default: user id)
- `rotationInterval`: automatic key rotation
- `algorithm`: EdDSA (default), ES256, RSA256, PS256, etc.

**Sources**:
- [Better Auth Plugins Documentation](https://better-auth.com/docs/plugins)
- [Better Auth JWT Plugin Documentation](https://better-auth.com/docs/plugins/jwt)

---

### Q2: FastAPI JWT Verification Patterns

**Question**: How to implement JWT verification in FastAPI using PyJWT or python-jose?

**Findings**:

FastAPI's official documentation recommends **PyJWT** for JWT handling with dependency injection.

**Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, exceptions as jwt_exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(
            token,
            key=os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"],  # or EdDSA, RS256, etc.
            options={"verify_exp": True}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id}
    except jwt_exceptions.InvalidTokenError:
        raise credentials_exception
```

**Key Points**:
- Use `OAuth2PasswordBearer` for the authorization header scheme
- Catch `jwt_exceptions.InvalidTokenError` for all validation failures
- Extract user identity from `payload.get("sub")`
- Return 401 with `WWW-Authenticate: Bearer` header on failure

**Alternative with python-jose**:
python-jose provides additional features like JWKS support for RSA/ECDSA keys:
```python
from jose import jwt, JWTError

try:
    payload = jwt.decode(
        token,
        key=os.getenv("BETTER_AUTH_SECRET"),
        algorithms=["HS256"],
        options={"verify_exp": True}
    )
except JWTError:
    raise HTTPException(...)
```

**Decision**: Use **PyJWT** for simplicity (sufficient for symmetric HS256 or EdDSA keys matching Better Auth defaults).

**Sources**:
- [FastAPI Security Tutorial - OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

---

### Q3: User Isolation Patterns in FastAPI

**Question**: How to enforce user isolation using FastAPI dependency injection?

**Findings**:

**Pattern 1: User Context Dependency**:
```python
from typing import Annotated

async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> str:
    # Verify JWT and extract user_id
    payload = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")

# Use in endpoints
@app.get("/todos")
async def get_todos(
    user_id: Annotated[str, Depends(get_current_user_id)]
) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).all()
```

**Pattern 2: User ID Path Validation**:
```python
async def validate_user_access(
    user_id: str,
    current_user_id: Annotated[str, Depends(get_current_user_id)]
) -> str:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's resources"
        )
    return user_id

@app.get("/users/{user_id}/todos")
async def get_user_todos(
    validated_user_id: Annotated[str, Depends(validate_user_access)]
):
    # Now safe to query for this user
    return db.query(Todo).filter(Todo.user_id == validated_user_id).all()
```

**Key Principles**:
1. Always derive user identity from JWT claims (never from request parameters)
2. Reject requests where path user_id doesn't match JWT user_id
3. Filter all queries by authenticated user_id
4. Return consistent 401/403 errors without leaking user existence

---

## Architecture Decision Summary

| Decision | Chosen Approach | Rationale |
|----------|-----------------|-----------|
| Frontend Auth Library | Better Auth + jwtClient | Official, well-documented, JWT-native |
| Frontend Token Access | `authClient.token()` | Clean API, async, handles token refresh |
| Backend JWT Library | PyJWT | Official FastAPI recommendation, simpler than jose |
| Backend Auth Pattern | Dependency Injection | Reusable, testable, matches FastAPI idioms |
| User Isolation | Query + Path validation | Dual enforcement: query filters by user, path validates ownership |
| JWT Algorithm | EdDSA (Better Auth default) + HS256 (FastAPI) | Better Auth defaults to EdDSA; use matching algorithm on backend |
| Token Expiration | 15 minutes (default) | Balanced security/usability for hackathon |

---

## Next Steps

1. Use `authClient.token()` for JWT access on Next.js frontend
2. Implement PyJWT verification dependency in FastAPI
3. Enforce user isolation via dependency injection on all protected routes
4. Configure matching JWT algorithm (EdDSA or HS256) on both sides
