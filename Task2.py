def run_calculator():
    print("=== Simple Python Calculator ===")

    # 1. Get the first number
    try:
        num1 = float(input("Enter the first number: "))
    except ValueError:
        print("Error: That is not a valid number.")
        return

    # 2. Get the operation choice
    print("\nAvailable Operations:")
    print(" + : Addition")
    print(" - : Subtraction")
    print(" * : Multiplication")
    print(" / : Division")
    operation = input("Choose an operation (+, -, *, /): ").strip()

    # 3. Get the second number
    try:
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Error: That is not a valid number.")
        return

    # 4. Perform the calculation and display the result
    print("\n--- Result ---")
    if operation == "+":
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif operation == "-":
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
    elif operation == "*":
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
    elif operation == "/":
        # Check for division by zero to prevent crashes
        if num2 == 0:
            print("Error: Cannot divide by zero.")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
    else:
        print("Error: Invalid operation choice.")

if __name__ == "__main__":
    run_calculator()
