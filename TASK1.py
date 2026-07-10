import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Imported ttk to use the modern Treeview widget
import json
import os

# The name of the file where your tasks will be stored on your computer
DATA_FILE = "todo_data.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("420x500") # Made slightly wider to fit the text perfectly
        
        # Internal task list storage
        self.todo_list = []
        
        # --- UI ELEMENTS ---
        # Title Label
        self.title_label = tk.Label(root, text="TO-DO LIST MANAGER", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # Task Input Field
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=5)
        
        self.task_entry = tk.Entry(self.entry_frame, width=28, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_task, bg="green", fg="white")
        self.add_button.pack(side=tk.LEFT)
        
        # --- UPGRADED TASK DISPLAY (Treeview instead of Listbox) ---
        # This widget allows individual text styles and row coloring.
        self.tree = ttk.Treeview(root, columns=("Tasks"), show="", height=15)
        self.tree.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        # Configure the column width and text size
        self.tree.column("#0", width=0, stretch=tk.NO) # Hide the default tree column
        self.tree.column("Tasks", width=360, anchor="w")
        
        # Set up custom font for the Treeview rows
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11))
        
        # CREATE COLOR TAGS: This maps names like 'done' and 'pending' to specific text colors
        self.tree.tag_configure("done", foreground="#27ae60")     # Nice dark green
        self.tree.tag_configure("pending", foreground="#c0392b")  # Nice dark red
        
        # Action Buttons Frame
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)
        
        self.complete_button = tk.Button(self.btn_frame, text="Mark Complete", command=self.mark_complete, bg="blue", fg="white")
        self.complete_button.pack(side=tk.LEFT, padx=10)
        
        self.delete_button = tk.Button(self.btn_frame, text="Delete Task", command=self.delete_task, bg="red", fg="white")
        self.delete_button.pack(side=tk.LEFT, padx=10)
        
        # Load any existing tasks immediately upon starting the app
        self.load_data()
        
    # --- STORAGE OPERATIONS ---
    def save_data(self):
        """Saves the current todo_list array into a text file using JSON format."""
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(self.todo_list, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save your tasks: {e}")

    def load_data(self):
        """Looks for a saved file and populates the tree view if found."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    self.todo_list = json.load(file)
                self.update_listbox()
            except Exception:
                self.todo_list = []

    # --- FUNCTIONALITY ---
    def update_listbox(self):
        """Refreshes the visible display using the data in self.todo_list and applies colors."""
        # Clear current view
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Re-populate with color tags applied
        for item in self.todo_list:
            if item["completed"]:
                status_text = f"✅ [Done]  {item['task']}"
                # The tags="done" argument applies the green text color we configured earlier
                self.tree.insert("", tk.END, values=(status_text,), tags=("done",))
            else:
                status_text = f"❌ [Pending]  {item['task']}"
                # The tags="pending" argument applies the red text color
                self.tree.insert("", tk.END, values=(status_text,), tags=("pending",))

    def add_task(self):
        """Grabs text from entry field and saves it."""
        task_name = self.task_entry.get().strip()
        if task_name:
            self.todo_list.append({"task": task_name, "completed": False})
            self.update_listbox()
            self.save_data()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def get_selected_index(self):
        """Helper function to find which row number is currently clicked."""
        selected_item = self.tree.selection()
        if not selected_item:
            raise IndexError
        # Find the position index of the clicked row item
        return self.tree.index(selected_item[0])

    def mark_complete(self):
        """Marks the selected item as finished."""
        try:
            selected_index = self.get_selected_index()
            self.todo_list[selected_index]["completed"] = True
            self.update_listbox()
            self.save_data()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task from the list first!")

    def delete_task(self):
        """Removes the selected item from the array and display."""
        try:
            selected_index = self.get_selected_index()
            self.todo_list.pop(selected_index)
            self.update_listbox()
            self.save_data()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
