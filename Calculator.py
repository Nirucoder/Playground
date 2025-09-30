import tkinter as tk

# Function to update expression in the text entry box
def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)

# Function to evaluate the final expression
def equalpress():
    try:
        global expression
        total = str(eval(expression))  # eval evaluates string as math expression
        equation.set(total)
        expression = total
    except:
        equation.set(" error ")
        expression = ""

# Function to clear the text entry box
def clear():
    global expression
    expression = ""
    equation.set("")

# Main driver code
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple Calculator")
    root.geometry("320x400")

    expression = ""

    # StringVar() updates automatically in Entry widget
    equation = tk.StringVar()

    # Entry widget (display screen)
    entry_field = tk.Entry(root, textvariable=equation, font=('Arial', 20),
                           bd=10, relief="sunken", justify="right")
    entry_field.grid(columnspan=4, ipadx=8, ipady=8, pady=10)

    # Buttons layout (numbers + operators)
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ]

    # Loop to create buttons
    for (text, row, col) in buttons:
        if text == "=":
            b = tk.Button(root, text=text, fg="white", bg="green",
                          command=equalpress, height=2, width=7, font=('Arial', 14))
        else:
            b = tk.Button(root, text=text, fg="black", bg="lightgray",
                          command=lambda t=text: press(t), height=2, width=7, font=('Arial', 14))
        b.grid(row=row, column=col, padx=5, pady=5)

    # Clear button
    clear_btn = tk.Button(root, text='C', fg="white", bg="red",
                          command=clear, height=2, width=32, font=('Arial', 14))
    clear_btn.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    root.mainloop()
