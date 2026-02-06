"""
Main entry point for the Todo Application
"""
from cli.todo_cli import TodoCLI


def main():
    """Main function to run the Todo application"""
    try:
        cli = TodoCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again or contact support if the problem persists.")


if __name__ == "__main__":
    main()