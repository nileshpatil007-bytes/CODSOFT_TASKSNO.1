import tkinter as tk
from tkinter import messagebox

# --- Business Logic ---
# This holds the current mathematical expression text (e.g., "12+5")
expression = ""

def press_num(number):
    """Appends a clicked number or decimal point to the expression."""
    global expression
    expression = expression + str(number)
    equation_var.set(expression)

def press_operator(operator):
    """Appends a clicked operator to the expression with validation."""
    global expression
    
    # Don't start an expression with an operator (except minus for negative numbers)
    if expression == "" and operator != "-":
        return
        
    # Check if the last character is already an operator to avoid duplicates (e.g., "++")
    if expression and expression[-1] in ["+", "-", "*", "/"]:
        # Swap the old operator for the new one
        expression = expression[:-1] + operator
    else:
        expression = expression + operator
        
    equation_var.set(expression)

def calculate():
    """Evaluates the entire mathematical expression safely."""
    global expression
    try:
        # Check for division by zero before evaluating
        if "/0" in expression:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
            clear_screen()
            return
            
        # eval() computes the string expression directly (e.g., eval("12+3") becomes 15)
        # Using a restricted environment for eval is safer practice
        result = str(eval(expression, {"__builtins__": None}, {}))
        
        # Format floating points nicely if they end in .0
        if result.endswith(".0"):
            result = result[:-2]
            
        equation_var.set(result)
        expression = result # Keep the result so users can chain calculations
        
    except SyntaxError:
        messagebox.showerror("Input Error", "Invalid mathematical expression.")
        clear_screen()
    except Exception:
        messagebox.showerror("Error", "An unexpected error occurred.")
        clear_screen()

def clear_screen():
    """Wipes the screen completely."""
    global expression
    expression = ""
    equation_var.set("")

# --- UI Setup ---
window = tk.Tk()
window.title("Advanced Python Calculator")
window.geometry("350x450")
window.resizable(False, False)
window.configure(bg="#2c3e50") # Modern dark background theme

# String Variable to bind data dynamically to the display screen
equation_var = tk.StringVar()

# 1. The Calculator Screen (Display)
display_frame = tk.Frame(window, bg="#2c3e50")
display_frame.pack(pady=20, padx=20, fill="both")

display_screen = tk.Entry(
    display_frame, 
    textvariable=equation_var, 
    font=("Arial", 24, "bold"), 
    bd=10, 
    insertwidth=4, 
    width=14, 
    borderwidth=0,
    justify="right",
    state="readonly", # Prevents typing directly, forcing button use
    bg="#ecf0f1",
    fg="#2c3e50"
)
display_screen.pack(ipady=10, fill="both", expand=True)

# 2. The Button Grid Layout
grid_frame = tk.Frame(window, bg="#2c3e50")
grid_frame.pack(pady=10)

# Styling configurations for different button types
btn_config = {"font": ("Arial", 14, "bold"), "fg": "#ffffff", "activebackground": "#95a5a6", "borderwidth": 0, "height": 2, "width": 5}
num_bg = "#34495e"    # Dark grey for numbers
op_bg = "#e67e22"     # Orange for core operations (+, -, *, /)
clear_bg = "#e74c3c"  # Red for the Clear button
equal_bg = "#2ecc71"  # Green for the Equals button

# Row 1 Buttons
btn_clear = tk.Button(grid_frame, text="C", bg=clear_bg, command=clear_screen, **btn_config)
btn_clear.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

btn_div = tk.Button(grid_frame, text="/", bg=op_bg, command=lambda: press_operator("/"), **btn_config)
btn_div.grid(row=0, column=2, padx=3, pady=3)

btn_mult = tk.Button(grid_frame, text="*", bg=op_bg, command=lambda: press_operator("*"), **btn_config)
btn_mult.grid(row=0, column=3, padx=3, pady=3)

# Row 2 Buttons
btn_7 = tk.Button(grid_frame, text="7", bg=num_bg, command=lambda: press_num(7), **btn_config)
btn_7.grid(row=1, column=0, padx=3, pady=3)

btn_8 = tk.Button(grid_frame, text="8", bg=num_bg, command=lambda: press_num(8), **btn_config)
btn_8.grid(row=1, column=1, padx=3, pady=3)

btn_9 = tk.Button(grid_frame, text="9", bg=num_bg, command=lambda: press_num(9), **btn_config)
btn_9.grid(row=1, column=2, padx=3, pady=3)

btn_sub = tk.Button(grid_frame, text="-", bg=op_bg, command=lambda: press_operator("-"), **btn_config)
btn_sub.grid(row=1, column=3, padx=3, pady=3)

# Row 3 Buttons
btn_4 = tk.Button(grid_frame, text="4", bg=num_bg, command=lambda: press_num(4), **btn_config)
btn_4.grid(row=2, column=0, padx=3, pady=3)

btn_5 = tk.Button(grid_frame, text="5", bg=num_bg, command=lambda: press_num(5), **btn_config)
btn_5.grid(row=2, column=1, padx=3, pady=3)

btn_6 = tk.Button(grid_frame, text="6", bg=num_bg, command=lambda: press_num(6), **btn_config)
btn_6.grid(row=2, column=2, padx=3, pady=3)

btn_add = tk.Button(grid_frame, text="+", bg=op_bg, command=lambda: press_operator("+"), **btn_config)
btn_add.grid(row=2, column=3, padx=3, pady=3)

# Row 4 & 5 Layout (Consolidating 1, 2, 3, 0, dot, and Equals)
btn_1 = tk.Button(grid_frame, text="1", bg=num_bg, command=lambda: press_num(1), **btn_config)
btn_1.grid(row=3, column=0, padx=3, pady=3)

btn_2 = tk.Button(grid_frame, text="2", bg=num_bg, command=lambda: press_num(2), **btn_config)
btn_2.grid(row=3, column=1, padx=3, pady=3)

btn_3 = tk.Button(grid_frame, text="3", bg=num_bg, command=lambda: press_num(3), **btn_config)
btn_3.grid(row=3, column=2, padx=3, pady=3)

# Equals button spans vertically over two rows
btn_equal = tk.Button(grid_frame, text="=", bg=equal_bg, command=calculate, **btn_config)
btn_equal.config(height=5)
btn_equal.grid(row=3, column=3, rowspan=2, sticky="nsew", padx=3, pady=3)

btn_0 = tk.Button(grid_frame, text="0", bg=num_bg, command=lambda: press_num(0), **btn_config)
btn_0.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)

btn_dot = tk.Button(grid_frame, text=".", bg=num_bg, command=lambda: press_num("."), **btn_config)
btn_dot.grid(row=4, column=2, padx=3, pady=3)

# Run the UI main window loop
window.mainloop()
