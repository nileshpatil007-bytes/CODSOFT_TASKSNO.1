import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Local database file name
DATA_FILE = "todo_data.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My To-Do List Pro")
        self.root.geometry("450x580")
        self.root.configure(bg="#f8f9fa") # Soft clean background
        
        # Internal application data
        self.todo_list = []
        self.recently_deleted = None # Temporary home for the Undo system
        
        # --- BUILD INTERFACE ---
        self.setup_styles()
        self.create_layout()
        
        # Load any history immediately
        self.load_saved_tasks()
        
    def setup_styles(self):
        """Sets up modern looking fonts and padding styles."""
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Arial", 11), rowheight=28)
        self.style.configure("TScrollbar", gripcount=0)
        
    def create_layout(self):
        """Assembles the entire interface piece by piece."""
        # 1. Header Title
        title = tk.Label(self.root, text="✨ My Daily Tasks ✨", font=("Arial", 16, "bold"), bg="#f8f9fa", fg="#2c3e50")
        title.pack(pady=15)
        
        # 2. Input Box Area
        entry_frame = tk.Frame(self.root, bg="#f8f9fa")
        entry_frame.pack(pady=5, padx=20, fill="x")
        
        self.task_entry = tk.Entry(entry_frame, width=28, font=("Arial", 12), bd=2, relief="groove")
        self.task_entry.pack(side=tk.LEFT, padx=5, ipady=4, expand=True, fill="x")
        self.task_entry.bind("<Return>", lambda event: self.add_task()) # Press enter shortcut
        
        add_btn = tk.Button(entry_frame, text="Add Task", command=self.add_task, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=12)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # 3. Main Task Display (Treeview List)
        display_frame = tk.Frame(self.root, bg="#f8f9fa")
        display_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.tree = ttk.Treeview(display_frame, columns=("Tasks"), show="", height=12, yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Tasks", anchor="w")
        
        # Setup specific row highlights
        self.tree.tag_configure("done", foreground="#95a5a6") # Greyed out for finished tasks
        self.tree.tag_configure("pending", foreground="#2c3e50") # Strong color for active tasks
        
        # DOUBLE CLICK SHORTCUT: Triggers rapid mark complete
        self.tree.bind("<Double-1>", lambda event: self.toggle_task_shortcut())
        
        # 4. Standard Action Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=10)
        
        complete_btn = tk.Button(btn_frame, text="✔️ Mark Complete", command=self.mark_complete, bg="#3498db", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=12, pady=6)
        complete_btn.pack(side=tk.LEFT, padx=10)
        
        delete_btn = tk.Button(btn_frame, text="🗑️ Delete Task", command=self.delete_task, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=12, pady=6)
        delete_btn.pack(side=tk.LEFT, padx=10)
        
        # 5. Hidden Undo Alert Bar (Only shows up right after a deletion)
        self.undo_frame = tk.Frame(self.root, bg="#f39c12", height=40)
        self.undo_label = tk.Label(self.undo_frame, text="Task deleted.", bg="#f39c12", fg="white", font=("Arial", 10, "bold"))
        self.undo_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        undo_btn = tk.Button(self.undo_frame, text="UNDO ↩️", command=self.undo_last_deletion, bg="#d35400", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=8)
        undo_btn.pack(side=tk.RIGHT, padx=15, pady=5)

    # --- MEMORY DISK SAVE OPERATIONS ---
    def save_tasks_to_disk(self):
        """Saves current state into local JSON file automatically."""
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(self.todo_list, file, indent=4)
        except Exception as error:
            messagebox.showerror("Saving Error", f"Couldn't save your tasks: {error}")

    def load_saved_tasks(self):
        """Loads tasks from storage when the app opens up."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    self.todo_list = json.load(file)
                self.refresh_display()
            except Exception:
                self.todo_list = []

    # --- APPLICATION ENGINE LOGIC ---
    def refresh_display(self):
        """Sorts the array data and updates treeview layout visualization."""
        # Hide the undo bar on every general refresh step unless called specifically
        self.undo_frame.pack_forget()
        
        # Wipes visual drawing clean
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # SUGGESTION 1 IMPLEMENTED: Sort tasks so pending stay high, finished sink down low
        sorted_list = sorted(self.todo_list, key=lambda k: k["completed"])
        
        # Re-map our basic array pointer so tracking matches user expectations
        self.todo_list = sorted_list
        
        # Draw everything back nicely with icons
        for index, item in enumerate(self.todo_list):
            if item["completed"]:
                display_text = f" ✅  [Done]   {item['task']}"
                # Added strikethrough symbol style simulation if desired, or basic clean tag styling
                self.tree.insert("", tk.END, iid=index, values=(display_text,), tags=("done",))
            else:
                display_text = f" ❌  [Pending]   {item['task']}"
                self.tree.insert("", tk.END, iid=index, values=(display_text,), tags=("pending",))

    def add_task(self):
        """Appends new dictionary values into core map files."""
        task_name = self.task_entry.get().strip()
        if task_name:
            self.todo_list.append({"task": task_name, "completed": False})
            self.refresh_display()
            self.save_tasks_to_disk()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please type something before clicking add!")

    def get_selected_row_index(self):
        """Helper engine tool to locate index identity values accurately."""
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        # Since we force numerical mapping inside visual insert lines, conversion is direct
        return int(selected_item[0])

    def mark_complete(self):
        """Switches active values to finished for selected items."""
        index = self.get_selected_row_index()
        if index is not None:
            self.todo_list[index]["completed"] = True
            self.refresh_display()
            self.save_tasks_to_disk()
        else:
            messagebox.showwarning("Selection Missing", "Click on a task from the list first to complete it!")

    # SUGGESTION 2 IMPLEMENTED: Easy double click logic to toggle status values instantly
    def toggle_task_shortcut(self):
        """Double click toggle shortcut rule engine."""
        index = self.get_selected_row_index()
        if index is not None:
            # Flips whatever the boolean condition value currently holds
            self.todo_list[index]["completed"] = not self.todo_list[index]["completed"]
            self.refresh_display()
            self.save_tasks_to_disk()

    def delete_task(self):
        """Deletes items while safely copying values to temporary storage."""
        index = self.get_selected_row_index()
        if index is not None:
            # Store item metadata details before destroying lines completely
            removed_item = self.todo_list.pop(index)
            self.recently_deleted = {"item": removed_item, "original_index": index}
            
            self.refresh_display()
            self.save_tasks_to_disk()
            
            # SUGGESTION 3 IMPLEMENTED: Reveal toast banner block tracking options
            self.undo_label.config(text=f"Deleted: \"{removed_item['task']}\"")
            self.undo_frame.pack(fill="x", side=tk.BOTTOM)
        else:
            messagebox.showwarning("Selection Missing", "Click on a task from the list first to remove it!")

    def undo_last_deletion(self):
        """Pulls old dictionary entries from backup and returns them onto the screen."""
        if self.recently_deleted:
            data = self.recently_deleted["item"]
            # Inject records back into baseline memory
            self.todo_list.append(data)
            
            # Wipe backup registry keys
            self.recently_deleted = None
            
            self.refresh_display()
            self.save_tasks_to_disk()
            self.undo_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
