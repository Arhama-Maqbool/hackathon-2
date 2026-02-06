"""
TodoTask data model representing a single task in the todo list
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TodoTask:
    """
    Represents a single task in the todo list

    Attributes:
        id: Unique identifier for the task
        title: The main description or name of the task
        description: Additional details about the task (optional)
        completed: Indicates whether the task is completed
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the TodoTask after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

    def validate(self) -> bool:
        """
        Validate the task data

        Returns:
            True if the task is valid, False otherwise
        """
        if not self.title or not self.title.strip():
            return False
        return True

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }