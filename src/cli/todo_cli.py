"""
Console interface for the Todo application
"""
from typing import Optional
from services.todo_service import TodoService
from lib.utils import format_task_display, get_user_input, confirm_action


class TodoCLI:
    """
    Console interface and user interaction layer
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance"""
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*40)
        print("TODO APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("-"*40)

    def add_task(self):
        """Handle adding a new task"""
        print("\n--- Add New Task ---")
        title = get_user_input("Enter task title: ")

        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = get_user_input("Enter task description (optional, press Enter to skip): ")
        if not description:  # If user just pressed Enter, set to None
            description = None

        try:
            task = self.service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def view_tasks(self):
        """Handle viewing all tasks"""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print(format_task_display(task))

    def update_task(self):
        """Handle updating an existing task"""
        print("\n--- Update Task ---")
        try:
            task_id = int(get_user_input("Enter task ID to update: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {format_task_display(task)}")

        # Get new values or keep existing ones
        new_title = get_user_input(f"Enter new title (current: '{task.title}', press Enter to keep): ")
        if not new_title:  # If user just pressed Enter, keep current title
            new_title = task.title

        new_description = get_user_input(f"Enter new description (current: '{task.description}', press Enter to keep): ")
        if new_description == "":  # If user just pressed Enter, check if they want to keep current or set to None
            new_description = task.description

        try:
            updated_task = self.service.update_task(task_id, new_title, new_description)
            if updated_task:
                print("Task updated successfully!")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def delete_task(self):
        """Handle deleting a task"""
        print("\n--- Delete Task ---")
        try:
            task_id = int(get_user_input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Task to delete: {format_task_display(task)}")

        if confirm_action("Are you sure you want to delete this task?"):
            if self.service.delete_task(task_id):
                print("Task deleted successfully!")
            else:
                print(f"Error: Task with ID {task_id} could not be deleted.")
        else:
            print("Delete operation cancelled.")

    def toggle_task_status(self):
        """Handle toggling task completion status"""
        print("\n--- Toggle Task Status ---")
        try:
            task_id = int(get_user_input("Enter task ID to toggle status: "))
        except ValueError:
            print("Error: Please enter a valid task ID (number).")
            return

        # Check if task exists
        task = self.service.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {format_task_display(task)}")

        # Toggle the status
        updated_task = self.service.toggle_task_status(task_id)
        if updated_task:
            new_status = "completed" if updated_task.completed else "incomplete"
            print(f"Task status updated to {new_status}!")
        else:
            print(f"Error: Could not toggle status for task with ID {task_id}.")

    def run(self):
        """Main application loop"""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()
            choice = get_user_input("Select an option (1-6): ")

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.toggle_task_status()
            elif choice == '6':
                print("Thank you for using the Todo Application. Goodbye!")
                break
            else:
                print("Invalid option. Please select 1-6.")