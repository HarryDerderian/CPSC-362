import tkinter as tk
from tkinter import messagebox, font, ttk
import sqlite3
import uuid

def init_db() :
    """Initialize the SQLite database and create table if not exists."""
    data_base = sqlite3.connect('inventory.db')
    control = data_base.cursor()
    # int: id, str: name, str: description, int: quantity 
    SQL_COMMAND = '''
    CREATE TABLE IF NOT EXISTS products
    (    id TEXT PRIMARY KEY, 
         name TEXT NOT NULL, 
         manufacturer TEXT, 
         description TEXT, 
         quantity INTEGER NOT NULL, 
         expiry TEXT 
    ); '''
    control.execute(SQL_COMMAND)
    data_base.commit()
    data_base.close()

def is_unique_id(id_to_check) -> bool:
    """Used to quickly check if an ID is unique or not, within the database"""
    data = sqlite3.connect('inventory.db')
    control = data.cursor()
    # SQL command to check if the ID exists in the database
    SQL_COMMAND = "SELECT 1 FROM products WHERE id = ?"
    # Execute the query with the ID to check
    control.execute(SQL_COMMAND, (id_to_check,))
    result = control.fetchone()
    # Close the database connection
    data.close()
    # Check if the result is None, which means the ID is unique
    return result is None

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


def update_product() -> None :
    """Updates a product (requires a valid id inside database)"""
    # Confirm valid inputs:
    if not verify_input() : return
    # Collect user input data
    name = name_user_input.get()
    manufacturer = manufacturer_input.get()
    expiry = expiry_user_input.get()
    stock = int(stock_user_input.get())
    # CONFIRM ID IS CORRECTLY INPUT
    id = id_user_input.get()
    if is_unique_id(id) :
        messagebox.showerror("Error", "Updating requires a valid ID")
        return
    # All inputs are correct, update values:
    SQL_COMMAND =  """
                    UPDATE products
                    SET name = ?, 
                    manufacturer = ?, 
                    description = ?, 
                    quantity = ?, 
                    expiry = ?
                    WHERE id = ?;
                  """
    data = sqlite3.connect("inventory.db")
    control = data.cursor()
    control.execute(SQL_COMMAND, (name, manufacturer, product_description.get("1.0", "end-1c"), stock, expiry, id))
    data.commit()
    data.close()
    messagebox.showinfo("info", "Product updated")

        
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

def clear_inputs() -> None :
        name_user_input.set("")
        manufacturer_user_input.set("")
        expiry_user_input.set("")
        stock_user_input.set("")
        id_user_input.set("")
        product_description.delete("1.0", "end")


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
        # refersh data display
        clear_inputs()
        view_all()

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
        sql_command = "INSERT INTO products (id, name, manufacturer, description, quantity, expiry) VALUES (?,?,?,?,?,?)"
        # Make sure to generate a random id
        id_str = str(uuid.uuid4())
        while not is_unique_id(id_str) :
            id_str = str(uuid.uuid4())
        data_editor.execute(sql_command, (id_str, name, 
                                          manufacturer, product_description.get("1.0", "end-1c"), stock, expiry))
        # Display newly added product:
        sql_command = "SELECT * from products WHERE name = ? AND manufacturer = ? AND expiry = ? AND quantity = ?"
        clear_inputs()
        view_products(data_editor.execute(sql_command, (name, manufacturer, expiry, stock)))
        # close database, alert user product was added:
        data_base.commit()
        data_base.close()
        messagebox.showinfo("info", "Product added to inventory")
    except Exception as e: messagebox.showerror("Error", str(e))

def view_in_stock() -> None :
    """Displays all products in the database that have a stock
    larger than 0, displayed on a tree view"""
    data_base = sqlite3.connect('inventory.db')
    data_control = data_base.cursor()
    SQL_COMMAND = "SELECT * FROM products WHERE quantity != 0"
    view_products(data_control.execute(SQL_COMMAND))
    data_base.close()

def view_out_of_stock() -> None :
    """Displays all products in the database with zero stock, 
    displayed on a tree view"""
    data_base = sqlite3.connect('inventory.db')
    data_control = data_base.cursor()
    SQL_COMMAND = "SELECT * FROM products WHERE quantity = 0"
    view_products(data_control.execute(SQL_COMMAND))
    data_base.close()

def view_all() -> None :
    """Displays all products in the database, displayed on a tree view"""
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

# 'Product name' label:
name_label = tk.Label(root, text = "Product Name")
name_label.place( x = 100, y = 50)
name_label['font'] = LABEL_FONT

# 'ID' label:
id_label = tk.Label(root, text = "ID")
id_label.place( x = 725, y = 45)
id_label['font'] = LABEL_FONT

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

# 'Product description' label:
description_label = tk.Label(root, text = "Product description")
description_label.place( x = 845, y = 150)
description_label['font'] = LABEL_FONT


# Input text fields:
X_CORDS = 300
TEXT_INPUT_WIDTH = 30 # (pixels)
# Entry font updates the height of the Entry object
INPUT_FONT = font.Font(family = "Times new roman", size = 20)
# Name input bar
name_user_input = tk.StringVar() # Gives access to the input within the associated text field.
name_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                      textvariable = name_user_input)
name_input.place(x = X_CORDS, y = 45 )
name_input['font'] = LABEL_FONT 

# ID input bar
id_user_input = tk.StringVar() # Gives access to the input within the associated text field.
id_input = tk.Entry(root, width = 35, 
                      textvariable = id_user_input)
id_input.place(x = 780, y = 45 )
id_input['font'] = LABEL_FONT 

# Manufacturer input bar
manufacturer_user_input = tk.StringVar() # Gives access to the input within the associated text field.
manufacturer_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                              textvariable = manufacturer_user_input)
manufacturer_input.place(x = X_CORDS, y = 135 )
manufacturer_input['font'] = LABEL_FONT

# Expiry input bar
expiry_user_input = tk.StringVar() # Gives access to the input within the associated text field.
expiry_input = tk.Entry(root, width = TEXT_INPUT_WIDTH, 
                        textvariable = expiry_user_input)
expiry_input.place(x = X_CORDS, y = 225 )
expiry_input['font'] = LABEL_FONT
 

# Stock input bar
stock_user_input = tk.StringVar() # Gives access to the input within the associated text field.
stock_input = tk.Entry(root, width = TEXT_INPUT_WIDTH,
                       textvariable = stock_user_input)
stock_input.place(x = X_CORDS, y = 315 )
stock_input['font'] = LABEL_FONT

# Description input text box: 
TEXT_FIELD_WIDTH = 50
TEXT_FIELD_HEIGHT = 10
description_user_input = tk.StringVar() # Gives access to the input within the associated text field.
product_description = tk.Text(root, 
                               width= TEXT_FIELD_WIDTH,
                               height=TEXT_FIELD_HEIGHT)
product_description.place(x=725,y=180)

# Buttons :
BUTTON_FONT = font.Font(family="Times new roman", size = 20)
BUTTON_HEIGHT = 1 # (pixels)
BUTTON_WIDTH = 15 # (pixels)
# 'Add' button
add_button = tk.Button(root, text = "Add Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = add_product)
add_button.place(x = 50, y = 370)

# 'Delete' button
del_button = tk.Button(root, text = "Delete Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = del_product)
del_button.place(x = 200, y = 370)

# 'Update' button
update_button = tk.Button(root, text = "Update Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = update_product)
update_button.place(x = 350, y = 370)


# 'Out of stock' button
out_of_stock_button = tk.Button(root, text = "Out-of-Stock Items",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = view_out_of_stock)
out_of_stock_button.place(x = 900, y = 370)

# 'In stock' buttn
# 'Out of stock' button
in_stock_button = tk.Button(root, text = "In-Stock Items",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = view_in_stock)
in_stock_button.place(x = 750, y = 370)


# 'Search' button
search_button = tk.Button(root, text = "Search Product",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = search_product)
search_button.place(x = 550, y = 370)


# 'View' button
view_button = tk.Button(root, text = "View Products",
                    width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                                    command = view_all)
view_button.place(x = 1050, y = 370)

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

# building logic for clicks within the tree view :
def on_treeview_select(event) :
    """Display all fields of the product selected
    (input them into inputfields)"""
    clear_inputs()
    # product description is not stored inside treeview
    # must be retrived from database
    data_base = sqlite3.connect('inventory.db')
    control = data_base.cursor()
    SQL_COMMAND = "SELECT description FROM products WHERE id =?"
    values = tree_view.item(tree_view.selection(), 'values')
    id = values[0]
    description = control.execute(SQL_COMMAND, (id,)).fetchone()[0]
    data_base.close()
    product_description.insert("1.0", description)
    try :
        # update text fields with selected inputs
        id_user_input.set(id)
        name_user_input.set(values[1])
        manufacturer_user_input.set(values[2])
        expiry_user_input.set(values[3])
        stock_user_input.set(values[4])
    except : pass # index error that seems to happen, not sure why,
    # it doesnt change anything this just removes the error message

tree_view.bind("<<TreeviewSelect>>", on_treeview_select)

init_db()
root.mainloop()