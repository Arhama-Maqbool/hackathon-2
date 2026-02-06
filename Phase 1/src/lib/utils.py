"""
Utility functions for the Todo application
"""


def validate_task_title(title: str) -> bool:
    """
    Validate that a task title is not empty or whitespace-only

    Args:
        title: The title to validate

    Returns:
        True if the title is valid, False otherwise
    """
    if not title:
        return False
    if not title.strip():
        return False
    return True


def format_task_display(task) -> str:
    """
    Format a task for display in the console

    Args:
        task: The task object to format (with id, title, description, completed attributes)

    Returns:
        Formatted string representation of the task
    """
    status = "X" if task.completed else "O"
    title = task.title
    description = f" - {task.description}" if task.description else ""
    return f"[{status}] {task.id}. {title}{description}"


def get_user_input(prompt: str) -> str:
    """
    Get input from the user with a prompt

    Args:
        prompt: The prompt to display to the user

    Returns:
        The user's input as a string
    """
    return input(prompt).strip()


def confirm_action(prompt: str) -> bool:
    """
    Ask the user to confirm an action

    Args:
        prompt: The confirmation prompt to display

    Returns:
        True if the user confirms, False otherwise
    """
    response = input(f"{prompt} (y/N): ").strip().lower()
    return response in ['y', 'yes', '1', 'true']