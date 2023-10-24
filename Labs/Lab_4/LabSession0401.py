import tkinter as tk
from tkinter import messagebox, font, ttk
import sqlite3
import uuid

def init_db() :
    """Initialize the SQLite database and create table if not exists."""
    data_base = sqlite3.connect('inventory.db')
    control = data_base.cursor()
    # int: id, str: name, str: description, int: quantity 
    control.execute('''CREATE TABLE IF NOT EXISTS products
    (id TEXT PRIMARY KEY, name TEXT NOT NULL, manufacturer TEXT, 
                    description TEXT, quantity INTEGER NOT NULL, expiry TEXT);''')
    data_base.commit()
    data_base.close()

def verify_input() -> bool :
    """Confirms all user input is filled in and correct"""
    name = name_user_input.get()
    manufacturer = manufacturer_input.get()
    expiry = expiry_user_input.get()
    stock = stock_user_input.get()
    # Verify data inputs are correct...
    if not name or not manufacturer or not expiry or not stock:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return False
    # Confirm that stock count is an int > -1
    try : # make sure to catch invalid int conversions
        if int(stock) < 0 :
            messagebox.showerror("Error", "Stock count can't be negative.")
            return False
    except :
        messagebox.showerror("Error", "Stock must be an int")
        return False
    else : 
        return True

def search_product() -> None :
    """Search the database for product based on user input"""
    # Confirm user input, some options are allowed empty.
    name = name_user_input.get()
    manufacturer = manufacturer_input.get()
    expiry = expiry_user_input.get()
    stock = stock_user_input.get()
    if not name and not manufacturer and not expiry and not stock :
        messagebox.showerror("Error", "Please fill in at least one of the required fields.")
        return  
    # Confirm that stock count is an int > -1, or ignore it if left blank.
    try : # make sure to catch invalid int conversions
        if stock and int(stock) < 0 :
            messagebox.showerror("Error", "Stock count can't be negative.")
            return
    except :
        messagebox.showerror("Error", "Stock must be an int")
        return
    # Verification complete...
    # Establish connection to database
    data_base = sqlite3.connect('inventory.db')
    data_control = data_base.cursor()
    SQL_COMMAND = "SELECT * FROM products WHERE name = ? OR manufacturer = ? OR expiry = ? OR quantity = ?"
    if stock : stock = int(stock)
    data_table = data_control.execute(SQL_COMMAND, (name, manufacturer, expiry, stock))
    view_products(data_table)
    data_base.close()


def del_product() -> None : 
    """Deleting a product from the database."""
    # Confirm user input is correct.
    if not verify_input() : return
    else :
        # Collect user input:
        name = name_user_input.get()
        manufacturer = manufacturer_input.get()
        expiry = expiry_user_input.get()
        stock = stock_user_input.get()
    try :
        # ESTABLISH CONNECTION TO DATA BASE 
        data_base = sqlite3.connect('inventory.db')
        data_editor = data_base.cursor()
        SQL_COMMAND = "DELETE from products WHERE name = ? AND manufacturer = ? AND expiry = ? AND quantity = ?"
        data_editor.execute(SQL_COMMAND, (name, manufacturer, expiry, stock))
        data_base.commit()
        data_base.close()
        messagebox.showinfo("info", "Product removed from inventory")
    # Handle any unforseen runtime errors...
    except Exception as e: messagebox.showerror("Error", "Unable to find product with those fields.")

def add_product() -> None :
    """Add a new product to the database."""
    # Confirm user input is correct.
    if not verify_input() : return
    else :
        # Collect user input:
        name = name_user_input.get()
        manufacturer = manufacturer_input.get()
        expiry = expiry_user_input.get()
        stock = stock_user_input.get()
    try :
        # ESTABLISH CONNECTION TO DATA BASE 
        data_base = sqlite3.connect('inventory.db')
        data_editor = data_base.cursor()
        SQL_COMMAND = "INSERT INTO products (id, name, manufacturer, description, quantity, expiry) VALUES (?,?,?,?,?,?)"
        data_editor.execute(SQL_COMMAND, (str(uuid.uuid4()), name, 
                                          manufacturer, None, stock, expiry))
        data_base.commit()
        data_base.close()
        messagebox.showinfo("info", "Product added to inventory")
    except Exception as e: messagebox.showerror("Error", str(e))

def view_all() -> None :
    data_base = sqlite3.connect('inventory.db')
    data_control = data_base.cursor()
    SQL_COMMAND = "SELECT * FROM products"
    view_products(data_control.execute(SQL_COMMAND))
    data_base.close()

def view_products(data_table) -> None :
    """Load and display all notes from the database.
        @param data_table: a selected table of data from a database cursor
    """
    tree_view.delete(*tree_view.get_children())
    for row in data_table : # data_editor.execute("SELECT * FROM products"):
        id = row[0]
        name = row[1]
        manufacturer = row[2]
        description = row[3]
        stock = row[4]
        expiry = row[5]
        tree_view.insert("", tk.END, values=(id, name, manufacturer, expiry, stock))


# Initialize main window
root = tk.Tk()
root.title("Inventory Management System")

# Width and height of the GUI (pixels)
GUI_SIZE = "1200x700"
root.geometry(GUI_SIZE)
root.resizable = False

# Text labels
LABEL_FONT = font.Font(family="Times new roman", size=15)


# 'Item count' label :




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
INPUT_FONT = font.Font(family = "Times new roman", size = 20)
# Name input bar
name_user_input = tk.StringVar() # Gives access to the input within the associated text field.
name_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                      textvariable = name_user_input)
name_input.place(x = 450, y = 45 )
name_input['font'] = LABEL_FONT 

# Manufacturer input bar
manufacturer_user_input = tk.StringVar() # Gives access to the input within the associated text field.
manufacturer_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                              textvariable = manufacturer_user_input)
manufacturer_input.place(x = 450, y = 135 )
manufacturer_input['font'] = LABEL_FONT

# Expiry input bar
expiry_user_input = tk.StringVar() # Gives access to the input within the associated text field.
expiry_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                        textvariable = expiry_user_input)
expiry_input.place(x = 450, y = 225 )
expiry_input['font'] = LABEL_FONT
 

# Stock input bar
stock_user_input = tk.StringVar() # Gives access to the input within the associated text field.
stock_input = tk.Entry(root, width = TEXT_INPUT_WIDTH,
                       textvariable = stock_user_input)
stock_input.place(x = 450, y = 315 )
stock_input['font'] = LABEL_FONT

# Buttons :
BUTTON_FONT = font.Font(family="Times new roman", size = 20)
BUTTON_HEIGHT = 1 # (pixels)
BUTTON_WIDTH = 15 # (pixels)
# 'Add' button
add_button = tk.Button(root, text = "Add Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = add_product)
add_button.place(x = 100, y = 370)

# 'Delete' button
del_button = tk.Button(root, text = "Delete Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = del_product)
del_button.place(x = 300, y = 370)

# 'Search' button
search_button = tk.Button(root, text = "Search Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = search_product)
search_button.place(x = 800, y = 370)


# 'View' button
view_button = tk.Button(root, text = "View Products",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = view_all)
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


init_db()
root.mainloop()