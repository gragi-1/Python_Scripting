# List to store tasks
tasks = []

while True:
    print("\nTo-Do List")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Mark Task as Completed")
    print("4. View Tasks")
    print("5. Check Number of Tasks")
    print("6. Clear All Tasks")
    print("7. Save Tasks to File")
    print("8. Load Tasks from File")
    print("9. Sort Tasks")
    print("10. Exit")
    
    # Ask the user for the desired option
    option = int(input("Please select an option: "))
    
    if option == 1:
        # Add task
        task = input("Please enter the task: ")
        tasks.append(task)
    elif option == 2:
        # Delete task
        task = input("Please enter the task to delete: ")
        if task in tasks:
            tasks.remove(task)
        else:
            print("Task not found.")
    elif option == 3:
        # Mark task as completed
        task = input("Please enter the task to mark as completed: ")
        if task in tasks:
            tasks.remove(task)
            tasks.append(task + " - Completed")
        else:
            print("Task not found.")
    elif option == 4:
        # View tasks
        if tasks:
            print("\nTasks:")
            for task in tasks:
                print(task)
        else:
            print("No tasks found.")
    elif option == 5:
        # Check number of tasks
        print("Number of tasks: ", len(tasks))
    elif option == 6:
        # Clear all tasks
        tasks.clear()
        print("All tasks have been cleared.")
    elif option == 7:
        # Save tasks to file
        with open('tasks.txt', 'w') as f:
            for task in tasks:
                f.write("%s\n" % task)
        print("Tasks have been saved to tasks.txt.")
    elif option == 8:
        # Load tasks from file
        try:
            with open('tasks.txt', 'r') as f:
                tasks = [line.rstrip() for line in f]
            print("Tasks have been loaded from tasks.txt.")
        except FileNotFoundError:
            print("File not found.")
    elif option == 9:
        # Sort tasks
        tasks.sort()
        print("Tasks have been sorted alphabetically.")
    elif option == 10:
        # Exit the program
        break
    else:
        print("Invalid option. Please try again.")