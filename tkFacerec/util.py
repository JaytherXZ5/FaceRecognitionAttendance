import tkinter as tk
from tkinter import messagebox

def get_button(window, text, color, command, fg ='white'):
    #object fopr tk.button
    button = tk.Button(
        window,
        text = text,
        activebackground = "black",
        activeforeground= "white",
        fg = fg,
        bg = color,
        command = command,
        height = 1,
        width=25,
        font=('Helvetica bold', 20)
    )
    return button

def get_img_label(window):
    #object for tk.label(window)
    label = tk.Label(window)

    label.grid(row = 0, column = 0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text = text)

    label.config(
        font=("sans serif", 24),
        justify = "left"
    )
    return label

def get_text_label2(window, text):
    label = tk.Label(window, text = text)

    label.config(
        font=("sans serif", 12),
        justify = "left"
    )
    return label


def get_img_label2(window):
    #object for tk.label(window)
    label = tk.Label(window)

    label.grid(row = 0, column = 0)
    return label

def get_text_label2(window, text):
    label = tk.Label(window, text = text)

    label.config(
        font=("sans serif", 10),
        justify = "left"
    )
    return label
def get_entry_text(window):
    #object for tk.Text()
    inputtxt = tk.Text(
        window, height=.5, width=28, font=("Agency FB", 24)
    )

    return inputtxt

def get_entry_text2(window):
    #object for tk.Text()
    inputtxt = tk.Entry(
        window,show="*", font=("Agency FB", 24)
    )

    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)