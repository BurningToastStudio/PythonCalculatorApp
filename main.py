# MAX MARTIN
# Simple calculator app using tkinter

#region Imports
import tkinter as tk
#endregion

#region Window Setup
root = tk.Tk()
root.title("Calculator App Thing")
root.geometry("450x480")
root.resizable(False, False)
#endregion

#region Constants
DISPLAY_FONT = "Arial", 36
BUTTON_FONT = "Arial", 24
BUTTON_WIDTH = 4
BUTTON_HEIGHT = 2
BUTTON_PADDING = 2
#endregion

#region Globals
# display_info holds the value that is shown on the display
display_info = tk.StringVar()

# store the last result value for operation chaining
last_result_value = None

# clear the screen after pressing = or getting an error
clear_display_on_next_button_input = False

#endregion

#region Main Logic
def clear_display():
    # change the state to modify the variable but keep it read only for the user
    display.config(state="normal")
    display_info.set("")
    display.config(state="readonly")

def on_button_clicked(button_value):
    global last_result_value
    # clear the screen if it already has stuff from a previous calculation
    global clear_display_on_next_button_input
    if clear_display_on_next_button_input:
        clear_display()
        clear_display_on_next_button_input = False

    # if equals was clicked, do the math
    if button_value == "=":
        clear_display_on_next_button_input = True
        on_equals_clicked()
        return

    # clear all
    if button_value == "CA":
        last_result_value = None
        clear_display()
        return

    # list of valid operation buttons
    operation_buttons = [
        "/", "+", "-", "*"
    ]

    # Check the following to allow operation chaining:
    # nothing in the display,
    # a previous calculation was done,
    # button value is an operation button
    if display.get() == "" and last_result_value is not None and button_value in operation_buttons:
        new_value = last_result_value + str(button_value)
    else:
        # get the value in the display
        current_value = display_info.get()
        # append it to the display
        new_value = current_value + str(button_value)

    # clear entry
    if button_value == "CE":
        current_value = display_info.get()
        # string slicing [:x]
        # this removes the last character (-1) from the string and assigns it to new_value
        new_value = current_value[:-1]

    # put the new value in the display
    display.config(state="normal")
    display_info.set(new_value)
    display.config(state="readonly")

def on_equals_clicked():
    global last_result_value
    # get the current value on the display
    current_value = display_info.get()
    # try/except so it doesn’t break :)
    # basically, eval() takes a string and does the math in it
    # if it fails it will go to except
    # if successful it will show the result on the display
    try:
        # do the math and turn it into a string
        # this is the point that could fail, eval() is a built-in function
        result = str(eval(current_value))
        # save result for operation chaining
        last_result_value = result
        # show the result
        display.config(state="normal")
        display_info.set(result)
        display.config(state="readonly")

    # if there is an error with eval(), display error rather than breaking :)
    # also this works for divide-by-zero exceptions as well as general syntax errors
    except Exception:
        display.config(state="normal")
        display_info.set("Syntax Error")
        display.config(state="readonly")

#endregion

#region UI Setup

# calculator button layout
# TOP DISPLAY HERE
# 7 8 9 x CA
# 4 5 6 - CE
# 1 2 3 +
# 0 . = /

# create display
display = tk.Entry(
    font=DISPLAY_FONT,
    width=16,
    borderwidth=5,
    state="readonly",
    justify="right",
    textvariable=display_info
)
# put at top and across 4 columns
display.grid(row=0, column=0, columnspan=5)

# makes it easy to change later
# tuple stores button string and grid position
# button number, row, column
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3), ("CA", 1, 4),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3), ("CE", 2, 4),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("/", 4, 3)
]

for (name, row, column) in buttons:
    button = tk.Button(
        text=name,
        font=BUTTON_FONT,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda val=name: on_button_clicked(val)
    )
    button.grid(row=row, column=column, sticky="nsew", padx=BUTTON_PADDING, pady=BUTTON_PADDING)

#endregion

root.mainloop()