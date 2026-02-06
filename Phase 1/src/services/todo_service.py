"""
TodoService handles all business logic for task management
"""
from typing import List, Optional
from models.todo_task import TodoTask


class TodoService:
    """
    Core business logic for task management
    Manages tasks in-memory storage and operations
    """

    def __init__(self):
        """Initialize the service with an empty task list and ID counter"""
        self._tasks: List[TodoTask] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> TodoTask:
        """
        Add a new task to the list

        Args:
            title: The title of the task
            description: Optional description of the task

        Returns:
            The created TodoTask with assigned ID

        Raises:
            ValueError: If title is empty or invalid
        """
        # Create a new task with the next available ID
        task = TodoTask(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )

        # Validate the task before adding
        if not task.validate():
            raise ValueError("Invalid task data")

        # Add the task to the list
        self._tasks.append(task)

        # Increment the ID counter for the next task
        self._next_id += 1

        return task

    def get_all_tasks(self) -> List[TodoTask]:
        """
        Get all tasks in the list

        Returns:
            List of all TodoTask objects
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[TodoTask]:
        """
        Get a task by its ID

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The TodoTask if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[TodoTask]:
        """
        Update an existing task

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated TodoTask if found, None otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        # Update the task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        # Validate the updated task
        if not task.validate():
            raise ValueError("Invalid task data after update")

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> Optional[TodoTask]:
        """
        Toggle the completion status of a task

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated TodoTask if found, None otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        # Toggle the completion status
        task.completed = not task.completed
        return task

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task

        Returns:
            The next available ID
        """
        return self._next_id