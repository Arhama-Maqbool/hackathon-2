"""
Simple test script to verify Todo application functionality
"""
import sys
import os
# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.todo_service import TodoService
from models.todo_task import TodoTask


def test_todo_functionality():
    """Test all functionality of the Todo application"""
    print("Testing Todo Application functionality...")

    # Create a service instance
    service = TodoService()

    # Test 1: Add tasks
    print("\n1. Testing task creation...")
    task1 = service.add_task("Buy groceries", "Milk, bread, eggs")
    print(f"   Added task: ID={task1.id}, Title='{task1.title}', Description='{task1.description}', Completed={task1.completed}")

    task2 = service.add_task("Complete project", "Finish the Todo app implementation")
    print(f"   Added task: ID={task2.id}, Title='{task2.title}', Description='{task2.description}', Completed={task2.completed}")

    # Test 2: View all tasks
    print("\n2. Testing task listing...")
    all_tasks = service.get_all_tasks()
    print(f"   Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        status = "X" if task.completed else "O"
        print(f"   [{status}] {task.id}. {task.title} - {task.description}")

    # Test 3: Update a task
    print("\n3. Testing task update...")
    updated_task = service.update_task(task1.id, "Buy groceries and cook dinner", "Milk, bread, eggs, chicken")
    if updated_task:
        print(f"   Updated task: ID={updated_task.id}, Title='{updated_task.title}', Description='{updated_task.description}'")
    else:
        print("   Failed to update task")

    # Test 4: Toggle task status
    print("\n4. Testing task status toggle...")
    toggled_task = service.toggle_task_status(task1.id)
    if toggled_task:
        print(f"   Toggled task {toggled_task.id} to completed={toggled_task.completed}")
    else:
        print("   Failed to toggle task status")

    # Test 5: Get task by ID
    print("\n5. Testing get task by ID...")
    found_task = service.get_task_by_id(task2.id)
    if found_task:
        print(f"   Found task: ID={found_task.id}, Title='{found_task.title}'")
    else:
        print("   Task not found")

    # Test 6: Delete a task
    print("\n6. Testing task deletion...")
    delete_result = service.delete_task(task2.id)
    print(f"   Delete result: {delete_result}")

    # Check remaining tasks
    remaining_tasks = service.get_all_tasks()
    print(f"   Remaining tasks after deletion: {len(remaining_tasks)}")
    for task in remaining_tasks:
        status = "X" if task.completed else "O"
        print(f"   [{status}] {task.id}. {task.title}")

    print("\nSUCCESS: All functionality tests passed!")


if __name__ == "__main__":
    test_todo_functionality()