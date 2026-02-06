import sys
from io import StringIO
from unittest.mock import patch
import main

def test_todo_app():
    """Test the updated todo application"""

    # Test adding, viewing, updating, and deleting tasks
    inputs = [
        "1",           # Add task
        "Buy groceries",
        "1",           # Add another task
        "Complete project",
        "2",           # View tasks
        "3",           # Update task
        "1",           # Select first task
        "Buy fruits and vegetables",  # New task content
        "2",           # View tasks again
        "4",           # Delete task
        "1",           # Select first task to delete
        "2",           # View tasks again
        "5"            # Exit
    ]

    input_iter = iter(inputs)

    def mock_input(prompt=""):
        print(prompt, end="")
        return next(input_iter)

    # Patch the input function to simulate user input
    with patch('builtins.input', side_effect=inputs):
        # Capture printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            main.main()
        except StopIteration:
            # Expected when we've exhausted our mock inputs
            pass
        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

        output = captured_output.getvalue()
        print("Application ran successfully! Here's what would be displayed:")
        print(output)

if __name__ == "__main__":
    test_todo_app()