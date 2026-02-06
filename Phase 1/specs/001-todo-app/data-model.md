# Data Model: Todo Application

**Feature**: Todo Application (001-todo-app)
**Date**: 2026-01-02

## Entities

### TodoTask
**Description**: Represents a single task in the todo list

**Fields**:
- `id`: int (auto-incremented, unique)
  - Purpose: Unique identifier for the task
  - Constraints: Positive integer, auto-generated
  - Validation: Must be unique within the system
- `title`: str
  - Purpose: The main description or name of the task
  - Constraints: Required field, non-empty
  - Validation: Must not be empty or whitespace-only
- `description`: str
  - Purpose: Additional details about the task
  - Constraints: Optional field
  - Validation: Can be empty or None
- `completed`: bool
  - Purpose: Indicates whether the task is completed
  - Constraints: Boolean value
  - Validation: Must be either True or False

**State Transitions**:
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user marks task as incomplete

**Relationships**:
- Part of a TaskList collection

### TaskList
**Description**: Collection of TodoTask entities managed in memory

**Fields**:
- `tasks`: List[TodoTask]
  - Purpose: Contains all tasks in the system
  - Constraints: Collection of TodoTask objects
  - Validation: Should maintain uniqueness of IDs
- `next_id`: int
  - Purpose: Counter for generating unique IDs
  - Constraints: Positive integer, starts at 1
  - Validation: Must increment with each new task

## Validation Rules

### TodoTask Validation
1. **Title Required**: The title field must be provided and not empty
2. **ID Uniqueness**: Each task must have a unique ID within the TaskList
3. **Type Validation**: Fields must match their defined types (id=int, title=str, description=str, completed=bool)

### TaskList Validation
1. **ID Generation**: New tasks must receive the next available ID
2. **Lookup Validation**: Operations by ID must verify the ID exists before proceeding
3. **Integrity**: The collection must maintain data integrity across all operations

## Data Flow

### Creation Flow
1. User provides title (and optional description)
2. System assigns next available ID from TaskList counter
3. System sets completed status to False by default
4. Task is added to TaskList

### Update Flow
1. User provides task ID and new values
2. System validates ID exists
3. System updates specified fields only
4. Task remains in TaskList

### Deletion Flow
1. User provides task ID
2. System validates ID exists
3. System removes task from TaskList
4. Task is no longer accessible

### Status Toggle Flow
1. User provides task ID
2. System validates ID exists
3. System toggles completed status
4. Task remains in TaskList with updated status