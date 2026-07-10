import sys

def show_menu():
    print("\n" + "="*30)
    print("      TO-DO LIST MANAGER      ")
    print("="*30)
    print("1. View To-Do List")
    print("2. Add a Task")
    print("3. Mark Task as Complete")
    print("4. Delete a Task")
    print("5. Exit")
    print("="*30)

def view_tasks(tasks):
    # Check if the list is empty
    if not tasks:
        print("\nℹ️ Your to-do list is currently empty!")
        return
    
    print("\n--- YOUR TASKS ---")
    # Loop through and print every task
    for index, item in enumerate(tasks, start=1):
        status = "✅ [Done]" if item["completed"] else "❌ [Pending]"
        print(f"{index}. {status} {item['task']}")

def add_task(tasks):
    task_name = input("\nEnter the task: ").strip()
    if task_name:
        tasks.append({"task": task_name, "completed": False})
        print(f"👍 Added: '{task_name}'")
    else:
        print("⚠️ Task cannot be empty!")

def mark_complete(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("\nEnter the number of the task to mark complete: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["completed"] = True
            print(f"🎉 Task {task_num} marked as complete!")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("\nEnter the number of the task to delete: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            print(f"🗑️ Deleted: '{removed['task']}'")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def main():
    # Defining the list safely inside main
    todo_list = []
    
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            view_tasks(todo_list)
        elif choice == '2':
            add_task(todo_list)
        elif choice == '3':
            mark_complete(todo_list)
        elif choice == '4':
            delete_task(todo_list)
        elif choice == '5':
            print("\nGoodbye! Stay productive! 👋")
            sys.exit()
        else:
            print("⚠️ Invalid choice. Please select between 1 and 5.")

if __name__ == "__main__":
    main()