# Quickstart Guide: Todo Application

**Feature**: Todo Application (001-todo-app)
**Date**: 2026-01-02

## Prerequisites

- Python 3.13 or higher
- Basic command-line knowledge

## Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or if no requirements.txt exists yet:
   ```bash
   # No external dependencies required - only uses Python standard library
   ```

3. **Run the application**:
   ```bash
   python src/cli/todo_cli.py
   ```

## Basic Usage

### Running the Application
The application starts with a menu-driven interface. Simply run the command above and follow the on-screen prompts.

### Available Operations

1. **Add Task**: Create a new task with a title and optional description
2. **View Tasks**: Display all tasks with their ID, title, description, and completion status
3. **Update Task**: Modify the title or description of an existing task
4. **Delete Task**: Remove a task by its ID
5. **Mark Complete/Incomplete**: Toggle the completion status of a task

### Example Workflow

1. Start the application
2. Select "Add Task" and enter a title like "Buy groceries"
3. Optionally add a description like "Milk, bread, eggs"
4. Select "View Tasks" to see your task list
5. Select "Mark Complete/Incomplete" to update the status of your task
6. Continue using the application as needed

## Development

### Project Structure
```
src/
├── models/
│   └── todo_task.py     # TodoTask data model
├── services/
│   └── todo_service.py  # Core business logic
├── cli/
│   └── todo_cli.py      # Console interface
└── lib/
    └── utils.py         # Utility functions
```

### Running Tests
```bash
pytest tests/
```

### Adding New Features
1. Update the specification in `specs/001-todo-app/spec.md`
2. Update this plan in `specs/001-todo-app/plan.md`
3. Add tasks to `specs/001-todo-app/tasks.md`
4. Implement the feature following the architecture
5. Add appropriate tests