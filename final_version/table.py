from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import   datetime
import sqlite3


class Table:
    def __init__(self, root):
        self.root = root
        self.root.title('PharmAssist')
        self.root.geometry("1100x600")

        # Add some Style
        style = ttk.Style()

        # Pick a Theme
        style.theme_use('default')

        # Configure tree view colors
        style.configure("Treeview",
                        background="pink",
                        foreground="black",
                        rowheight=25,
                        fieldbackgroud="D3D3D3")

        # Change Selected Color
        style.map("Treeview",
                  background=[('selected', "#347083")])

        # Create a Treeview Frame
        tree_frame = Frame(self.root)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create the Treeview
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=self.my_tree.yview)
        # Define Columns
        self.my_tree['columns'] = ("Product Name", "Quantity", "Description", "Manufacturing Date", "Expiry Date", "Item ID")

        # Format our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Product Name", anchor=W, width=150, stretch=NO)
        self.my_tree.column("Quantity", anchor=CENTER, width=100, stretch=NO)
        self.my_tree.column("Description", anchor=CENTER, width=350, stretch=NO)
        self.my_tree.column("Manufacturing Date", anchor=CENTER, width=140, stretch=NO)
        self.my_tree.column("Expiry Date", anchor=CENTER, width=140, stretch=NO)
        self.my_tree.column("Item ID", anchor=CENTER, width=100, stretch=NO)

        # Create Headings
        self.my_tree.heading("#0", text="")
        self.my_tree.heading("Product Name", text="Product Name", anchor=W)
        self.my_tree.heading("Quantity", text="Quantity", anchor=CENTER)
        self.my_tree.heading("Description", text="Description", anchor=CENTER)
        self.my_tree.heading("Manufacturing Date", text="Manufacturing Date", anchor=CENTER)
        self.my_tree.heading("Expiry Date", text="Expiry Date", anchor=CENTER)
        self.my_tree.heading("Item ID", text="Item ID", anchor=CENTER)

        # Create Striped Row Tags
        self.my_tree.tag_configure('zero', background='pink')
        self.my_tree.tag_configure('oddrow', background='white')
        self.my_tree.tag_configure('evenrow', background='lightblue')

        # Add Search Medicine Frame
        search_frame = LabelFrame(self.root, text="Search Medicine")
        search_frame.pack(fill='x', padx=20)

        # Add Label
        search_label = Label(search_frame, text="Enter Product Name:")
        search_label.grid(row=0, column=0, padx=10, pady=10)

        # Add Entry
        self.search_entry = Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Search Button
        search_button = Button(search_frame, text="Enter", command=self.search_medicine)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        refresh_button = Button(search_frame, text="Refresh", command = self.refresh)
        refresh_button.grid(row=0, column=3, padx=10, pady=10)

        self.query_database()

    def query_database(self):
        # Create a connection
        conn = sqlite3.connect('pharmassist.db')
        c = conn.cursor()

        # Clear the tree view table
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        # Query the database
        c.execute("SELECT * FROM pharmassist")
        records = c.fetchall()

        # Insert each record into the tree view with alternating row colors
        for count, record in enumerate(records):
            # Check if the quantity is 0
            if record[1] == 0:  # Assuming the quantity is at index 1
                self.my_tree.insert(parent='', index='end', iid=f"{count}", text='',
                                    values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                    tags=('zeroquantity',))
            else:
                # Check if the medicine is expired
                expiry_date = datetime.strptime(record[4], "%Y-%m-%d")  # Assuming the expiry date is at index 4
                if expiry_date < datetime.now():
                    self.my_tree.insert(parent='', index='end', iid=f"{count}", text='',
                                        values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                        tags=('expired',))
                else:
                    if count % 2 == 0:
                        self.my_tree.insert(parent='', index='end', iid=f"{count}", text='',
                                            values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                            tags=('evenrow',))
                    else:
                        self.my_tree.insert(parent='', index='end', iid=f"{count}", text='',
                                            values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                            tags=('oddrow',))

        conn.close()

    # Configure tags
        self.my_tree.tag_configure('zeroquantity', background='pink')
        self.my_tree.tag_configure('expired', background='pink')
        self.my_tree.tag_configure('oddrow', background='white')
        self.my_tree.tag_configure('evenrow', background='lightblue')

    def search_medicine(self):
        search_name = self.search_entry.get()

        # Connect to the database file
        conn = sqlite3.connect('pharmassist.db')
        c = conn.cursor()

        # Clear the tree view
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        # Search for the medicine by name
        c.execute("SELECT * FROM pharmassist WHERE product_name like ?", (search_name,))
        records = c.fetchall()

        if records:
            # Add the search result
            global count
            count = 0

            for record in records:
                if record[1] == 0:
                    self.my_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                        tags=('zero',))
                elif count % 2 == 0:
                    self.my_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                        tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='', index='end', iid=count, text='',
                                        values=(record[0], record[1], record[2], record[3], record[4], record[5]),
                                        tags=('oddrow',))
                count += 1

        else:
            messagebox.showwarning(title="Search Medicine", message="No item found")
            self.query_database()

        conn.commit()
        conn.close()

    def refresh(self):
        self.my_tree.delete(*self.my_tree.get_children())
        self.query_database()

class Pharmacist(Table):
    def __init__(self, root):
        super().__init__(root)

        record_frame = LabelFrame(self.root, text="Record")
        record_frame.pack(fill='x', padx=20)

        name_label = Label(record_frame, text="Product Name")
        name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = Entry(record_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=1)

        quantity_label = Label(record_frame, text="Quantity")
        quantity_label.grid(row=0, column=2, padx=10, pady=10)
        self.quantity_entry = Entry(record_frame)
        self.quantity_entry.grid(row=0, column=3, padx=10, pady=1)

        description_label = Label(record_frame, text="Description")
        description_label.grid(row=0, column=4, padx=10, pady=10)
        self.description_entry = Entry(record_frame)
        self.description_entry.grid(row=0, column=5, padx=10, pady=1)

        manufacturing_label = Label(record_frame, text="Manufacturing Date")
        manufacturing_label.grid(row=1, column=0, padx=10, pady=10)
        self.manufacturing_entry = Entry(record_frame)
        self.manufacturing_entry.grid(row=1, column=1, padx=10, pady=1)

        expiry_label = Label(record_frame, text="Expiry Date")
        expiry_label.grid(row=1, column=2, padx=10, pady=10)
        self.expiry_entry = Entry(record_frame)
        self.expiry_entry.grid(row=1, column=3, padx=10, pady=1)

        id_label = Label(record_frame, text="Item ID")
        id_label.grid(row=1, column=4, padx=10, pady=10)
        self.id_entry = Entry(record_frame)
        self.id_entry.grid(row=1, column=5, padx=10, pady=1)

        # Add Command Frame
        button_frame = LabelFrame(self.root, text="Commands")
        button_frame.pack(fill='x', padx=20)

        edit_button = Button(button_frame, text="Update Medicine", command=self.update_record)
        edit_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = Button(button_frame, text="Add Medicine", command=self.add_record)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_button = Button(button_frame, text="Remove Medicine", command=self.confirm_remove)
        remove_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Medicine", command=self.confirm_remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        clear_button = Button(button_frame, text="Clear Entry Boxes", command=self.clear_entries)
        clear_button.grid(row=0, column=4, padx=10, pady=10)


        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        self.query_database()

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.manufacturing_entry.delete(0, END)
        self.expiry_entry.delete(0, END)
        self.id_entry.delete(0, END)

    def select_record(self, e):
        # Clear Entry box
        self.clear_entries()

        # Grab record Number
        selected = self.my_tree.focus()
        # Grab record values
        values = self.my_tree.item(selected, 'values')

        # output to entry boxes
        if values:
            self.name_entry.insert(0, values[0])
            self.quantity_entry.insert(0, values[1])
            self.description_entry.insert(0, values[2])
            self.manufacturing_entry.insert(0, values[3])
            self.expiry_entry.insert(0, values[4])
            self.id_entry.insert(0, values[5])

    def add_record(self):
        flag = self.validate()
        if flag == True:
            # Connect to the database file
            conn = sqlite3.connect('pharmassist.db')

            # Create a cursor object to execute SQL commands
            c = conn.cursor()

            # Add new record
            c.execute("INSERT INTO pharmassist VALUES(:product_name, :quantity, :description, :manufacturing_date, :expiry_date, :item_id )",
                      {
                          'product_name': self.name_entry.get(),
                          'quantity': self.quantity_entry.get(),
                          'description': self.description_entry.get(),
                          'manufacturing_date': self.manufacturing_entry.get(),
                          'expiry_date': self.expiry_entry.get(),
                          'item_id': self.id_entry.get()
                      })

            conn.commit()
            conn.close()

            self.clear_entries()
            self.my_tree.delete(*self.my_tree.get_children())
            self.query_database()
            messagebox.showinfo("Success", "Record added successfully.")
            self.refresh()
        else:
            messagebox.showwarning(title="Error", message="Invalid Input")

    def remove(self):
        # Get the selected item
        selected = self.my_tree.selection()[0]
        # Get the Item ID of the selected item
        item_id = self.my_tree.item(selected, 'values')[5]

        # Connect to the database file
        conn = sqlite3.connect('pharmassist.db')
        c = conn.cursor()

        # Delete the record from the database
        c.execute("DELETE FROM pharmassist WHERE item_id = ?", (item_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Delete the item from the Treeview
        self.my_tree.delete(selected)
        messagebox.showinfo("Success", "Record removed successfully.")

    def confirm_remove(self):
        # Confirm before removing
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove selected record(s)?"):
            self.remove()
            self.refresh()

    def remove_all(self):
        # Get all items in the Treeview
        items = self.my_tree.get_children()

        # Connect to the database file
        conn = sqlite3.connect('pharmassist.db')
        c = conn.cursor()

        # Iterate through all items
        for item in items:
            # Get the Item ID of each item
            item_id = self.my_tree.item(item, 'values')[5]
            # Delete each item from the Treeview
            self.my_tree.delete(item)
            # Delete the record from the database
            c.execute("DELETE FROM pharmassist WHERE item_id = ?", (item_id,))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "All records removed successfully.")

    def confirm_remove_all(self):
        # Confirm before removing all records
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove all records?"):
            self.remove_all()
            self.refresh()

    def update_record(self):
        flag =self.validate()
        if flag:
        # Grab the record number
            selected = self.my_tree.focus()

        # Update record in Treeview
            self.my_tree.item(selected, text='', values=(
            self.name_entry.get(), self.quantity_entry.get(), self.description_entry.get(),
            self.manufacturing_entry.get(), self.expiry_entry.get(),
            self.id_entry.get()))

            # Connect to the database file
            conn = sqlite3.connect('pharmassist.db')

            # Create a cursor object to execute SQL commands
            c = conn.cursor()

            # Update record in the database
            c.execute("""UPDATE pharmassist SET
                      product_name = ?,
                      quantity = ?,
                      description = ?,
                      manufacturing_date = ?,
                      expiry_date = ?
                      WHERE item_id = ?""",
                      (self.name_entry.get(),
                       self.quantity_entry.get(),
                       self.description_entry.get(),
                       self.manufacturing_entry.get(),
                       self.expiry_entry.get(),
                       self.id_entry.get()))

            conn.commit()
            conn.close()
            self.refresh()
            messagebox.showinfo("Success", "Record updated successfully.")
        else:
            messagebox.showwarning(title="Error", message="Invalid Input")

    from datetime import datetime

    def validate(self):
        # Check if any entry is empty or consists only of whitespace
        entries = [
            self.name_entry.get(),
            self.quantity_entry.get(),
            self.description_entry.get(),
            self.manufacturing_entry.get(),
            self.expiry_entry.get(),
            self.id_entry.get()
        ]

        if any(entry.strip() == "" for entry in entries):
            return False

        # Validate date formats and quantity
        try:
            # Validate manufacturing and expiry dates
            val_manu_date = datetime.strptime(self.manufacturing_entry.get(), "%Y-%m-%d")
            val_expiry_date = datetime.strptime(self.expiry_entry.get(), "%Y-%m-%d")

            # Validate quantity is an integer
            val_quantity = int(self.quantity_entry.get())
        except (ValueError, TypeError):
            return False

        return True

