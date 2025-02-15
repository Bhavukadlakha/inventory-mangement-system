if __name__ == "__main__":
    root = Tk()
    app = BillingSystem(
        root,
        customer_db_path="customers.db",
        product_db_path="products.db",
        employee_db_path="employees.db",
        excel_path=r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/products.xlsx"
    )
    root.mainloop()               



    import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from fpdf import FPDF
import pandas as pd
from datetime import datetime


class BillingSystem:
    def __init__(self, root, customer_db_path, product_db_path, employee_db_path, excel_path):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("Billing System")

        # File paths
        self.customer_db_path = customer_db_path
        self.product_db_path = product_db_path
        self.employee_db_path = employee_db_path
        self.excel_path = excel_path

        # Variables
        self.cart = []  # Holds items in the cart
        self.total_amount = 0.0
        self.discount_rate = 0
        self.final_amount = 0.0
        self.customer_id = None
        self.selected_employee = StringVar()

        # Layout
        self.create_ui()

    def create_ui(self):
        # Frame 1 - Left Side
        frame1 = Frame(self.root, bg="lightblue", bd=5, relief=GROOVE)
        frame1.place(x=10, y=10, width=570, height=700)

        # Frame 2 - Right Side
        frame2 = Frame(self.root, bg="lightgray", bd=5, relief=GROOVE)
        frame2.place(x=590, y=10, width=570, height=700)

        # Customer Search in Frame 1
        Label(frame1, text="Search Customer by Contact", font=("Arial", 14)).pack(pady=10)
        self.var_contact = StringVar()
        Entry(frame1, textvariable=self.var_contact, font=("Arial", 14), bd=5, relief=SUNKEN).pack(pady=10)
        Button(frame1, text="Search Customer", font=("Arial", 12), bg="green", fg="white", command=self.search_customer).pack(pady=10)

        # Product Search in Frame 1
        Label(frame1, text="Search Product by ID or Barcode", font=("Arial", 14)).pack(pady=10)
        self.var_product_id = StringVar()
        Entry(frame1, textvariable=self.var_product_id, font=("Arial", 14), bd=5, relief=SUNKEN).pack(pady=10)
        Button(frame1, text="Search Product", font=("Arial", 12), bg="blue", fg="white", command=self.search_product).pack(pady=10)

        # Employee Dropdown
        Label(frame1, text="Billed By:", font=("Arial", 14)).pack(pady=10)
        self.employee_dropdown = ttk.Combobox(frame1, textvariable=self.selected_employee, font=("Arial", 12))
        self.employee_dropdown.pack(pady=10)
        self.load_employees()

        # Cart Table in Frame 2
        cart_frame = Frame(frame2)
        cart_frame.pack(fill=BOTH, expand=True)

        self.cart_tree = ttk.Treeview(cart_frame, columns=("prod_id", "name", "price", "qty", "total"), show="headings")
        self.cart_tree.heading("prod_id", text="Product ID")
        self.cart_tree.heading("name", text="Name")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Total")
        self.cart_tree.pack(fill=BOTH, expand=True)

        # Total and Discount
        self.total_label = Label(frame2, text="Total: ₹0.00", font=("Arial", 14), fg="red")
        self.total_label.pack(pady=10)
        self.discount_label = Label(frame2, text="Discount: 0% (₹0.00)", font=("Arial", 14), fg="blue")
        self.discount_label.pack(pady=10)

        # Buttons
        button_frame = Frame(frame2)
        button_frame.pack(pady=10)
        Button(button_frame, text="Apply Discount", font=("Arial", 12), bg="yellow", command=self.apply_discount).grid(row=0, column=0, padx=10)
        Button(button_frame, text="Reset Discount", font=("Arial", 12), bg="orange", command=self.reset_discount).grid(row=0, column=1, padx=10)
        Button(button_frame, text="Generate PDF", font=("Arial", 12), bg="blue", fg="white", command=self.generate_pdf).grid(row=0, column=2, padx=10)
        Button(button_frame, text="Clear Cart", font=("Arial", 12), bg="red", fg="white", command=self.clear_cart).grid(row=1, column=0, columnspan=3, pady=10)

    def load_employees(self):
        try:
            conn = sqlite3.connect(self.employee_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM employees")
            employees = cursor.fetchall()
            self.employee_dropdown['values'] = [emp[0] for emp in employees]
            if employees:
                self.selected_employee.set(employees[0][0])
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employees: {e}")

    def search_customer(self):
        contact = self.var_contact.get()
        try:
            conn = sqlite3.connect(self.customer_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE contact=?", (contact,))
            customer = cursor.fetchone()
            conn.close()
            if customer:
                self.customer_id = customer[0]
                messagebox.showinfo("Customer Found", f"Customer Name: {customer[1]}\nContact: {customer[2]}")
            else:
                messagebox.showerror("Customer Not Found", "No customer found with this contact.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search customer: {e}")

    def search_product(self):
        product_id = self.var_product_id.get()
        try:
            conn = sqlite3.connect(self.product_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id=? OR barcode=?", (product_id, product_id))
            product = cursor.fetchone()
            conn.close()

            if product:
                prod_id, name, price, quantity = product
                if quantity > 0:
                    self.cart.append((prod_id, name, price, 1))
                    self.update_cart_display()
                else:
                    messagebox.showerror("Out of Stock", "This product is out of stock!")
            else:
                messagebox.showerror("Product Not Found", "No product found with the provided ID or barcode.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search product: {e}")

    def update_cart_display(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        self.total_amount = 0.0
        for item in self.cart:
            prod_id, name, price, qty = item
            total = price * qty
            self.cart_tree.insert("", END, values=(prod_id, name, price, qty, total))
            self.total_amount += total
        self.final_amount = self.total_amount - (self.total_amount * self.discount_rate / 100)
        self.total_label.config(text=f"Total: ₹{self.total_amount:.2f}")
        self.discount_label.config(text=f"Discount: {self.discount_rate}% (₹{self.total_amount * self.discount_rate / 100:.2f})")

    def apply_discount(self):
        if self.discount_rate < 30:
            self.discount_rate += 5
        else:
            messagebox.showinfo("Max Discount", "Maximum discount of 30% already applied!")
        self.update_cart_display()

    def reset_discount(self):
        self.discount_rate = 0
        self.update_cart_display()
        messagebox.showinfo("Discount Reset", "Discount has been reset to 0%.")

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def generate_pdf(self):
        if not self.cart:
            messagebox.showerror("Error", "The cart is empty!")
            return
        if not self.customer_id:
            messagebox.showerror("Error", "Please select a customer!")
            return

        try:
            conn = sqlite3.connect(self.product_db_path)
            cursor = conn.cursor()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Invoice", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.cell(200, 10, txt=f"Billed By: {self.selected_employee.get()}", ln=True)

            pdf.cell(200, 10, txt="Products", ln=True)
            for item in self.cart:
                prod_id, name, price, qty = item
                total = price * qty
                pdf.cell(200, 10, txt=f"ID: {prod_id}, Name: {name}, Qty: {qty}, Total: ₹{total:.2f}", ln=True)

                # Update database quantity
                cursor.execute("UPDATE products SET quantity = quantity - ? WHERE product_id = ?", (qty, prod_id))

            # Update Excel
            products_df = pd.read_excel(self.excel_path)
            for item in self.cart:
                prod_id, _, _, qty = item
                idx = products_df[products_df['Product ID'] == prod_id].index[0]
                products_df.at[idx, 'Quantity'] -= qty
            products_df.to_excel(self.excel_path, index=False)

            # Totals
            pdf.cell(200, 10, txt=f"Total: ₹{self.total_amount:.2f}", ln=True)
            pdf.cell(200, 10, txt=f"Discount: {self.discount_rate}% (₹{self.total_amount * self.discount_rate / 100:.2f})", ln=True)
            pdf.cell(200, 10, txt=f"Final Amount: ₹{self.final_amount:.2f}", ln=True)

            # Save PDF
            filename = f"Invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf.output(filename)
            conn.commit()
            conn.close()

            messagebox.showinfo("Invoice Generated", f"Invoice saved as {filename}. Quantities updated.")
            self.clear_cart()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {e}")


if __name__ == "__main__":
    root = Tk()
    app = BillingSystem(
        root,
        customer_db_path="customers.db",
        product_db_path="products.db",
        employee_db_path="employees.db",
        excel_path=r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/products.xlsx"
    )
    root.mainloop()
