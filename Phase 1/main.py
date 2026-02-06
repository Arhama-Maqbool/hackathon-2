def main():
    todos = []
    while True:
        print("\n--- Welcome Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            task = input("Enter new task: ")
            todos.append(task)
            print(f"Task '{task}' added successfully!")

        elif choice == "2":
            if not todos:
                print("No tasks available.")
            else:
                print("\n--- Current Tasks ---")
                for i, task in enumerate(todos, 1):
                    print(f"{i}. {task}")

        elif choice == "3":
            if not todos:
                print("No tasks available to update.")
            else:
                print("\n--- Current Tasks ---")
                for i, task in enumerate(todos, 1):
                    print(f"{i}. {task}")

                try:
                    index = int(input("Enter task number to update: ")) - 1
                    if 0 <= index < len(todos):
                        old_task = todos[index]
                        new_task = input(f"Enter new task (current: '{old_task}'): ")
                        todos[index] = new_task
                        print(f"Task updated from '{old_task}' to '{new_task}'")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "4":
            if not todos:
                print("No tasks available to delete.")
            else:
                print("\n--- Current Tasks ---")
                for i, task in enumerate(todos, 1):
                    print(f"{i}. {task}")

                try:
                    index = int(input("Enter task number to delete: ")) - 1
                    if 0 <= index < len(todos):
                        deleted_task = todos.pop(index)
                        print(f"Task '{deleted_task}' deleted successfully!")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "5":
            print("Thank you for using the Todo Application!")
            break

        else:
            print("Invalid choice. Please select a number between 1-5.")

if __name__ == "__main__":
    main()
