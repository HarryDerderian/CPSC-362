import tkinter as tk
from tkinter import messagebox, font, ttk
import sqlite3

def init_db():
    """Initialize the SQLite database and create table if not exists."""
    data_base = sqlite3.connect('inventory.db')
    control = data_base.cursor()
    # int: id, str: name, str: description, int: quantity 
    control.execute('''CREATE TABLE IF NOT EXISTS products
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL, description TEXT, quantity INTEGER NOT NULL);''')
    data_base.commit()
    data_base.close()

def add_product():
    """Add a new product to the database."""
    note = note_var.get()
    if note:
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (note_text) VALUES (?)", (note,))
        conn.commit()
        conn.close()
        note_var.set('') # Clear the input
        load_notes()
    else:
        messagebox.showerror("Error", "Note cannot be empty!")

def load_notes():
    """Load and display all notes from the database."""
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM notes"):
        listbox.insert(tk.END, row[1])
    conn.close()
def delete_note():
    """Delete the selected note from the database."""
    selected_note = listbox.get(tk.ACTIVE)
    if selected_note:
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("DELETE FROM notes WHERE note_text=?", (selected_note,))
        conn.commit()
        conn.close()
        load_notes()
# Initialize main window
root = tk.Tk()
root.title("Inventory Management System")
# Width and height of the GUI (pixels)
GUI_SIZE = "1200x700"
root.geometry(GUI_SIZE)
root.resizable = False
# Center the GUI on the screen


# Text labels
LABEL_FONT = font.Font(family="Times new roman", size=15)
# 'Product name' label :
name_label = tk.Label(root, text = "Product Name")
name_label.place( x = 100, y = 50)
name_label['font'] = LABEL_FONT

# 'Manufacturer' label:
manufacturer_label = tk.Label(root, text = "Manufacturer")
manufacturer_label.place( x = 100, y = 140)
manufacturer_label['font'] = LABEL_FONT

# 'Expiry Date' label:
expiry_label= tk.Label(root, text = "Expiry Date")
expiry_label.place( x = 105, y = 230)
expiry_label['font'] = LABEL_FONT

# 'Stock' label:
stock_label = tk.Label(root, text = "Stock")
stock_label.place( x = 125, y = 320)
stock_label['font'] = LABEL_FONT


# Input text fields:
TEXT_INPUT_WIDTH = 30 # (pixels)
# Entry font updates the height of the Entry object
INPUT_FONT = font.Font(family="Times new roman", size = 20)
# Name input bar
name_input = tk.Entry(root, width = TEXT_INPUT_WIDTH)
name_input.place(x = 450, y = 45 )
name_input['font'] = LABEL_FONT 

# Manufacturer input bar
manufacturer_input = tk.Entry(root, width = TEXT_INPUT_WIDTH)
manufacturer_input.place(x = 450, y = 135 )
manufacturer_input['font'] = LABEL_FONT 

# Expiry input bar
expiry_input = tk.Entry(root, width = TEXT_INPUT_WIDTH)
expiry_input.place(x = 450, y = 225 )
expiry_input['font'] = LABEL_FONT 

# Stock input bar
stock_input = tk.Entry(root, width = TEXT_INPUT_WIDTH)
stock_input.place(x = 450, y = 315 )
stock_input['font'] = LABEL_FONT 

# Buttons :
BUTTON_FONT = font.Font(family="Times new roman", size = 20)
BUTTON_HEIGHT = 1 # (pixels)
BUTTON_WIDTH = 15 # (pixels)
# 'Add' button
add_button = tk.Button(root, text = "Add Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = None)
add_button.place(x = 100, y = 370)

# 'Delete' button
del_button = tk.Button(root, text = "Delete Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = None)
del_button.place(x = 545, y = 370)

# 'View' button
view_button = tk.Button(root, text = "View Products",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = None)
view_button.place(x = 1000, y = 370)

# Tree view (main data display) 
tree_view = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5"), 
                         show = 'headings', height= 11)
# column 1 header
tree_view.column("#1", anchor = tk.CENTER)
tree_view.heading("#1", text = "Product ID")
tree_view.column("#1", width=240)
# column 2 header
tree_view.column("#2", anchor = tk.CENTER)
tree_view.heading("#2", text = "Product Name")
tree_view.column("#2", width=240)
# column 3 header
tree_view.column("#3", anchor = tk.CENTER)
tree_view.heading("#3", text = "manufacturer")
tree_view.column("#3", width=240)
# column 4 header
tree_view.column("#4", anchor = tk.CENTER)
tree_view.heading("#4", text = "Expiry Date")
tree_view.column("#4", width=240)
# column 5 header
tree_view.column("#5", anchor = tk.CENTER)
tree_view.heading("#5", text = "Stock")
tree_view.column("#5", width=240)
# set cords
tree_view.place( x= 0, y = 410)

# Define StringVar for storing notes
note_var = tk.StringVar()
# Create entry widget and buttons
#tk.Entry(root, textvariable=note_var, width=50).pack(padx=10, pady=10)
#tk.Button(root, text="Add Note", command=add_note).pack(padx=10, pady=5)
#tk.Button(root, text="Delete Note", command=delete_note).pack(padx=10, pady=5)
# Create a listbox to display notes
#listbox = tk.Listbox(root, width=50)
#listbox.pack(padx=10, pady=10)
#init_db() # Initialize the database and create table if not exists
#load_notes() # Load notes on startup
init_db()
root.mainloop()