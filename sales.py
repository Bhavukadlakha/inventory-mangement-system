import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd

# Database paths
SALES_DB_PATH = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\bill_products.db"
EMPLOYEES_DB_PATH = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\employees.db"

class SalesTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Tracking")

        # UI Elements
        self.create_ui()

    def create_ui(self):
        """Create UI elements like buttons, dropdowns, and table"""
        frame_filters = tk.Frame(self.root)
        frame_filters.pack(pady=10)

        # Buttons for Today, Week, Month
        self.filter_option = tk.StringVar(value="Today")
        btn_today = tk.Button(frame_filters, text="Today", command=lambda: self.update_table("Today"))
        btn_week = tk.Button(frame_filters, text="Week", command=lambda: self.update_table("Week"))
        btn_month = tk.Button(frame_filters, text="Month", command=lambda: self.update_table("Month"))
        btn_today.grid(row=0, column=0, padx=5)
        btn_week.grid(row=0, column=1, padx=5)
        btn_month.grid(row=0, column=2, padx=5)

        # Employee Filter Dropdown
        tk.Label(frame_filters, text="Employee:").grid(row=0, column=3, padx=5)
        self.employee_var = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(frame_filters, textvariable=self.employee_var)
        self.employee_dropdown.grid(row=0, column=4, padx=5)

        # Payment Type Dropdown
        tk.Label(frame_filters, text="Payment Type:").grid(row=0, column=5, padx=5)
        self.payment_var = tk.StringVar()
        self.payment_dropdown = ttk.Combobox(frame_filters, textvariable=self.payment_var, values=["All", "Cash", "Paytm"])
        self.payment_dropdown.grid(row=0, column=6, padx=5)

        # Fetch employees for dropdown
        self.load_employee_names()

        # Table
        self.tree = ttk.Treeview(self.root, columns=("Date", "Employee", "Amount", "Discount", "Payment"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Employee", text="Employee")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Discount", text="Discount %")
        self.tree.heading("Payment", text="Payment Type")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Total Sales Label
        self.total_label = tk.Label(self.root, text="Total Sales: ₹0", font=("Arial", 14, "bold"), fg="green")
        self.total_label.pack(pady=10)

        # Load initial data
        self.update_table("Today")

    def load_employee_names(self):
        """Load employee names from database into dropdown"""
        conn = sqlite3.connect(EMPLOYEES_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name FROM employees")
        employees = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.employee_dropdown["values"] = ["All"] + employees

    def get_sales_data(self, filter_type, employee=None, payment_type=None):
        """Fetch and filter sales data from database"""
        conn = sqlite3.connect(SALES_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT bill_id, employee_name, price, discount, date, payment_type FROM bill_products")
        sales = cursor.fetchall()
        conn.close()

        # Convert to DataFrame
        df = pd.DataFrame(sales, columns=["bill_id", "employee_name", "price", "discount", "date", "payment_type"])

        # Convert date to datetime object
        df["date"] = pd.to_datetime(df["date"], format="%I:%M:%S %p, %d-%m-%Y")

        # Handle NULL payment_type (treat as Cash)
        df["payment_type"].fillna("Cash", inplace=True)

        # Filter by Date
        today = datetime.now().date()
        if filter_type == "Today":
            df = df[df["date"].dt.date == today]
        elif filter_type == "Week":
            start_of_week = today - timedelta(days=today.weekday())
            df = df[df["date"].dt.date >= start_of_week]
        elif filter_type == "Month":
            df = df[df["date"].dt.month == today.month]

        # Filter by Employee
        if employee and employee != "All":
            df = df[df["employee_name"] == employee]

        # Filter by Payment Type
        if payment_type and payment_type != "All":
            df = df[df["payment_type"] == payment_type]

        return df

    def update_table(self, filter_type):
        """Update table and total sales based on filters"""
        employee = self.employee_var.get()
        payment_type = self.payment_var.get()

        # Fetch filtered sales data
        df = self.get_sales_data(filter_type, employee, payment_type)

        # Clear existing table data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row["date"], row["employee_name"], row["price"], row["discount"], row["payment_type"]))

        # Update total sales
        total_sales = df["price"].sum()
        self.total_label.config(text=f"Total Sales: ₹{total_sales}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesTrackingApp(root)
    root.mainloop()
