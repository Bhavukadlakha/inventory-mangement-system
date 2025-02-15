import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import random

class CustomerClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+300+100")
        self.root.title("Products and Supplier Management")

        # Database setup
        self.conn = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/customers.db')  # Correct database path
        self.cursor = self.conn.cursor()
        self.create_customer_table()

        # Variables
        self.var_cust_id = StringVar()
        self.var_cust_name = StringVar()
        self.var_cust_address = StringVar()
        self.var_cust_contact = StringVar()

        # Title
        title = Label(self.root, text="Customer Management System", font=("goudy old style", 20, "bold"),
                      bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Customer Form
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=80)
        txt_name = Entry(self.root, textvariable=self.var_cust_name, font=("times new roman", 15), bg="lightyellow").place(x=200, y=80, width=200)

        lbl_address = Label(self.root, text="Address", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=130)
        txt_address = Entry(self.root, textvariable=self.var_cust_address, font=("times new roman", 15), bg="lightyellow").place(x=200, y=130, width=200)

        lbl_contact = Label(self.root, text="Contact", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=180)
        txt_contact = Entry(self.root, textvariable=self.var_cust_contact, font=("times new roman", 15), bg="lightyellow").place(x=200, y=180, width=200)

        # Buttons
        btn_add = Button(self.root, text="Save", font=("times new roman", 15, "bold"), bg="green", fg="white",
                         command=self.add_customer).place(x=50, y=250, width=100)
        btn_delete = Button(self.root, text="Delete", font=("times new roman", 15, "bold"), bg="red", fg="white",
                            command=self.delete_customer).place(x=160, y=250, width=100)
        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15, "bold"), bg="orange", fg="white",
                           command=self.clear_form).place(x=270, y=250, width=100)

        # Search Bar
        lbl_search = Label(self.root, text="Search by Contact", font=("times new roman", 15, "bold"), bg="white").place(x=500, y=80)
        self.var_search = StringVar()
        txt_search = Entry(self.root, textvariable=self.var_search, font=("times new roman", 15), bg="lightyellow").place(x=680, y=80, width=150)
        btn_search = Button(self.root, text="Search", font=("times new roman", 15, "bold"), bg="blue", fg="white",
                            command=self.search_customer).place(x=840, y=80, width=100)

        # Customer List (Treeview)
        self.customer_table = ttk.Treeview(self.root, columns=("cust_id", "name", "address", "contact"), show="headings")
        self.customer_table.place(x=50, y=350, width=800, height=200)

        self.customer_table.heading("cust_id", text="Customer ID")
        self.customer_table.heading("name", text="Name")
        self.customer_table.heading("address", text="Address")
        self.customer_table.heading("contact", text="Contact")

        self.customer_table.column("cust_id", width=150)
        self.customer_table.column("name", width=150)
        self.customer_table.column("address", width=200)
        self.customer_table.column("contact", width=150)

        self.customer_table.bind("<ButtonRelease-1>", self.get_selected_row)
        self.fetch_customers()

    def create_customer_table(self):
        """Create the customer table if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                contact TEXT UNIQUE NOT NULL
            )
        """)
        self.conn.commit()

    def add_customer(self):
        """Add a new customer to the database."""
        name = self.var_cust_name.get()
        address = self.var_cust_address.get()
        contact = self.var_cust_contact.get()

        if not name or not contact:
            messagebox.showerror("Error", "Name and Contact are required!", parent=self.root)
            return

        if len(contact) != 10 or not contact.isdigit():
            messagebox.showerror("Error", "Contact must be a 10-digit number!", parent=self.root)
            return

        try:
            self.cursor.execute("INSERT INTO customers (name, address, contact) VALUES (?, ?, ?)", (name, address, contact))
            self.conn.commit()
            messagebox.showinfo("Success", "Customer added successfully!", parent=self.root)
            self.fetch_customers()
            self.clear_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Contact number already exists!", parent=self.root)

    def delete_customer(self):
        """Delete the selected customer from the database."""
        contact = self.var_cust_contact.get()

        if not contact:
            messagebox.showerror("Error", "Please select a customer to delete!", parent=self.root)
            return

        self.cursor.execute("DELETE FROM customers WHERE contact=?", (contact,))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer deleted successfully!", parent=self.root)
        self.fetch_customers()
        self.clear_form()

    def search_customer(self):
        """Search for a customer by contact number."""
        contact = self.var_search.get()

        if not contact:
            messagebox.showerror("Error", "Please enter a contact number to search!", parent=self.root)
            return

        self.cursor.execute("SELECT * FROM customers WHERE contact=?", (contact,))
        row = self.cursor.fetchone()

        if row:
            self.customer_table.delete(*self.customer_table.get_children())
            self.customer_table.insert("", END, values=row)
        else:
            messagebox.showinfo("Not Found", "No customer found with this contact number!", parent=self.root)

    def fetch_customers(self):
        """Fetch all customers from the database and display in the Treeview."""
        self.customer_table.delete(*self.customer_table.get_children())
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            self.customer_table.insert("", END, values=row)

    def get_selected_row(self, event):
        """Populate the form with the selected row data."""
        selected_row = self.customer_table.focus()
        data = self.customer_table.item(selected_row, "values")
        if data:
            self.var_cust_id.set(data[0])
            self.var_cust_name.set(data[1])
            self.var_cust_address.set(data[2])
            self.var_cust_contact.set(data[3])

    def clear_form(self):
        """Clear the form fields."""
        self.var_cust_id.set("")
        self.var_cust_name.set("")
        self.var_cust_address.set("")
        self.var_cust_contact.set("")


if __name__ == "__main__":
    root = Tk()
    app = CustomerClass(root)
    root.mainloop()
