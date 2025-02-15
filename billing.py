from fpdf import FPDF
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import os
import random
import pywhatkit  # For sending messages on WhatsApp
import win32print  # For printing the PDF
from pdf2image import convert_from_path  # For converting PDF to image

class BillingSystem:
    def __init__(self, root, customer_db_path, product_db_path, employee_db_path, excel_path):
        self.root = root
        self.root.geometry("1450x750")
        self.root.title("Billing System")

        # File paths
        self.customer_db_path = customer_db_path
        self.product_db_path = product_db_path
        self.employee_db_path = employee_db_path
        self.excel_path = excel_path
        self.bill_products_db_path = r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/bill_products.db"

        # Variables
        self.cart = []  # Holds items in the cart
        self.total_amount = 0.0
        self.discount_rate = 0
        self.final_amount = 0.0
        self.customer_id = None
        self.selected_employee = StringVar() 
        self.payment_type = StringVar() 
        self.current_time = StringVar() 

        # Layout
        self.create_ui()

    def create_ui(self):
        # Frame 1 - Left Side
        frame1 = Frame(self.root, bg="lightblue", bd=5, relief=GROOVE)
        frame1.place(x=10, y=10, width=500, height=700)

        # Frame 2 - Right Side
        frame2 = Frame(self.root, bg="lightgray", bd=5, relief=GROOVE)
        frame2.place(x=520, y=10, width=570, height=700) 

        # Frame 3 - Customer Details
        self.frame3 = Frame(self.root, bg="white", bd=5, relief=GROOVE)
        self.frame3.place(x=1100, y=10, width=300, height=700)

        Label(self.frame3, text="Customer Details", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        self.customer_name_label = Label(self.frame3, text="Name: N/A", font=("Arial", 12), bg="white")
        self.customer_name_label.pack(pady=5)
        self.customer_address_label = Label(self.frame3, text="Address: N/A", font=("Arial", 12), bg="white")
        self.customer_address_label.pack(pady=5)
        self.customer_contact_label = Label(self.frame3, text="Contact: N/A", font=("Arial", 12), bg="white")
        self.customer_contact_label.pack(pady=5)

        # Add Send PDF Button
        send_pdf_button = Button(self.frame3, text="Send PDF", font=("Arial", 12), bg="blue", fg="black", command=self.send_pdf)
        send_pdf_button.pack(pady=10)

        # Add Print PDF Button
        print_pdf_button = Button(self.frame3, text="Print PDF", font=("Arial", 12), bg="red", fg="black", command=self.print_pdf)
        print_pdf_button.pack(pady=10)

        # Customer Search in Frame 1
        Label(frame1, text="Search Customer by Contact", font=("Arial", 14)).pack(pady=10)
        self.var_contact = StringVar()
        self.contact_entry = Entry(frame1, textvariable=self.var_contact, font=("Arial", 14), bd=5, relief=SUNKEN)
        self.contact_entry.pack(pady=10)
        self.contact_entry.bind("<Return>", lambda event: self.search_customer())
        Button(frame1, text="Search Customer", font=("Arial", 12), bg="green", fg="white", command=self.search_customer).pack(pady=10)

        # Product Search in Frame 1
        Label(frame1, text="Search Product by ID or Barcode", font=("Arial", 14)).pack(pady=10)
        self.var_PRODUCTID = StringVar()
        self.product_entry = Entry(frame1, textvariable=self.var_PRODUCTID, font=("Courier", 18), bd=5, relief=SUNKEN)
        self.product_entry.pack(pady=10)
        self.product_entry.bind("<Return>", lambda event: self.search_product())
        Button(frame1, text="Search Product", font=("Arial", 12), bg="blue", fg="white", command=self.search_product).pack(pady=10)

        # Employee Dropdown
        Label(frame1, text="Billed By:", font=("Arial", 14)).pack(pady=10)
        self.employee_dropdown = ttk.Combobox(frame1, textvariable=self.selected_employee, font=("Arial", 12))
        self.employee_dropdown.pack(pady=10)
        self.load_employees()
        # Payment Type Dropdown
        Label(frame1, text="Payment Type:", font=("Arial", 14)).pack(pady=10)
        self.payment_dropdown = ttk.Combobox(frame1, textvariable=self.payment_type, font=("Arial", 12), values=["Cash", "Paytm"])
        self.payment_dropdown.pack(pady=10) 

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
        self.total_label = Label(frame2, text="Total: 0.00", font=("Arial", 14), fg="red")
        self.total_label.pack(pady=10)
        self.discount_label = Label(frame2, text="Discount: 0% (0.00)", font=("Arial", 14), fg="blue")
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
        contact = self.var_contact.get().strip()  # Strip to avoid extra spaces
        try:
            conn = sqlite3.connect(self.customer_db_path)
            cursor = conn.cursor()

            # Query customer by contact
            cursor.execute("SELECT * FROM customers WHERE contact=?", (contact,))
            customer_full = cursor.fetchone()  # Used for frame1's messagebox

            cursor.execute("SELECT name, address, contact FROM customers WHERE contact=?", (contact,))
            customer_details = cursor.fetchone()  # Used for frame3 details

            conn.close()

            # Update frame1 (message box)
            if customer_full:
                self.customer_id = customer_full[0]
                messagebox.showinfo(
                    "Customer Found",
                    f"Customer Name: {customer_full[1]}\nContact: {customer_full[2]}"
                )
                self.product_entry.focus_set()
            else:
                messagebox.showerror("Customer Not Found", "No customer found with this contact.")

            # Update frame3 (labels)
            if customer_details:
                name, address, contact = customer_details
                self.customer_name_label.config(text=f"Name: {name}")
                self.customer_address_label.config(text=f"Address: {address}")
                self.customer_contact_label.config(text=f"Contact: {contact}")
            else:
                self.customer_name_label.config(text="Name: N/A")
                self.customer_address_label.config(text="Address: N/A")
                self.customer_contact_label.config(text="Contact: N/A")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search customer: {e}")

    def search_product(self):
        PRODUCTID = self.var_PRODUCTID.get().strip()
        if not PRODUCTID:
            messagebox.showerror("Error", "Please enter a Product ID or scan the barcode!")
            return

        try:
            conn = sqlite3.connect(self.product_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT PRODUCTID, TYPE, SELLINGPRICE, QUANTITY FROM products WHERE PRODUCTID=?", (PRODUCTID,))
            product = cursor.fetchone()
            conn.close()

            if product:
                prod_id, name, price, stock_qty = product
                for item in self.cart:
                    if item[0] == prod_id:
                        if item[3] < stock_qty:
                            item[3] += 1
                            item[4] = item[3] * price
                            self.update_cart_display()
                            return
                        else:
                            messagebox.showerror("Stock Error", f"Cannot add more of {name}. Stock limit reached.")
                            return
                
                if stock_qty > 0:
                    self.cart.append([prod_id, name, price, 1, price])
                    self.update_cart_display()
                else:
                    messagebox.showerror("Stock Error", f"{name} is out of stock.")
            else:
                messagebox.showerror("Product Not Found", "No product found with this ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search product: {e}")

    def update_cart_display(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4]))
        
        self.total_amount = sum(item[4] for item in self.cart)
        self.total_label.config(text=f"Total: {self.total_amount:.2f}")

    def apply_discount(self):
        if self.discount_rate < 30:
            self.discount_rate += 5
        else:
            messagebox.showinfo("Maximum Discount", "Maximum discount of 30% has already been applied.")
            return

        discount_amount = self.total_amount * (self.discount_rate / 100)
        self.final_amount = self.total_amount - discount_amount
        self.discount_label.config(text=f"Discount: {self.discount_rate}% ({discount_amount:.2f})")
        self.total_label.config(text=f"Total: {self.final_amount:.2f}")

    def reset_discount(self):
        self.discount_rate = 0
        self.final_amount = self.total_amount
        self.discount_label.config(text="Discount: 0% (0.00)")
        self.total_label.config(text=f"Total: {self.total_amount:.2f}")

    def generate_pdf(self):
        if not self.cart:
            messagebox.showwarning("No Items", "No items in cart to generate a bill.")
            return 
       
        invoice_number = random.randint(100000, 999999)
        pdf_folder = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\invoicesPDF"
        os.makedirs(pdf_folder, exist_ok=True)
        pdf_file_path = os.path.join(pdf_folder, f"invoice-{invoice_number}.pdf")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add the JAI GURU JI heading
        pdf.set_font("Arial", style="B", size=27)
        pdf.cell(200, 10, txt="JAI GURU JI", ln=True, align="C")

        # Add the TARA HANDLOOMS heading
        pdf.set_font("Arial", style="", size=12)
        pdf.cell(200, 10, txt="TARA HANDLOOMS", ln=True, align="C")

        # Add the address
        pdf.set_font("Arial", style="", size=10)
        pdf.cell(200, 10, txt="1377 MAIN GURUDWARA ROAD, JAWAHAR COLONY, NIT- FARIDABAD", ln=True, align="C")
        pdf.ln(10)

        # Add customer details and invoice information
        current_time = datetime.now().strftime('%I:%M:%S %p, %d-%m-%Y')  # 12-hour format
        pdf.set_font("Arial", size=12)

        # Customer ID on the left
        pdf.cell(100, 10, txt=f"Customer ID: {self.customer_id if self.customer_id else 'N/A'}", ln=0)

        # Date and time on the right
        pdf.cell(0, 10, txt=f"Date & Time: {current_time}", ln=True, align="R")

        # Invoice number
        pdf.cell(100, 10, txt=f"Invoice Number: {invoice_number}", ln=True)

        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(40, 10, txt="Product ID", border=1, align="C")
        pdf.cell(60, 10, txt="Name", border=1, align="C")
        pdf.cell(30, 10, txt="Price", border=1, align="C")
        pdf.cell(30, 10, txt="Qty", border=1, align="C")
        pdf.cell(30, 10, txt="Total", border=1, align="C")
        pdf.ln()

        # Table Content
        pdf.set_font("Arial", size=12)
        for item in self.cart:
            pdf.cell(40, 10, txt=str(item[0]), border=1)
            pdf.cell(60, 10, txt=item[1], border=1)
            pdf.cell(30, 10, txt=f"{item[2]:.2f}", border=1)
            pdf.cell(30, 10, txt=str(item[3]), border=1)
            pdf.cell(30, 10, txt=f"{item[4]:.2f}", border=1)
            pdf.ln()

            # Update the quantity in the database
            try:
                conn = sqlite3.connect(r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\products.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET QUANTITY = QUANTITY - ? WHERE PRODUCTID = ?", (item[3], item[0]))
                conn.commit()
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product quantity in database: {e}")

            # Update the quantity in the Excel file
            try:
                df = pd.read_excel(r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\Excel\products.xlsx")
                df.loc[df['PRODUCTID'] == item[0], 'QUANTITY'] -= item[3]
                df.to_excel(r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\Excel\products.xlsx", index=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product quantity in Excel: {e}")

        # Total, Discount, and Payable Amount
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(160, 10, txt="Total", border=1, align="R")
        pdf.cell(30, 10, txt=f"{self.total_amount:.2f}", border=1, align="R")
        pdf.ln()

        discount_amount = self.total_amount * (self.discount_rate / 100)
        pdf.cell(160, 10, txt=f"Discount ({self.discount_rate}%)", border=1, align="R")
        pdf.cell(30, 10, txt=f"{discount_amount:.2f}", border=1, align="R")
        pdf.ln()

        self.final_amount = self.total_amount - discount_amount
        pdf.cell(160, 10, txt="Payable Amount", border=1, align="R")
        pdf.cell(30, 10, txt=f"{self.final_amount:.2f}", border=1, align="R")
        pdf.ln(20)

        # Billed By
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, txt="Billed By:", ln=True)
        pdf.cell(100, 10, txt=f"{self.selected_employee.get()}", ln=True)    
       
        # Save PDF
        pdf.output(pdf_file_path)
        messagebox.showinfo("PDF Generated", f"Invoice has been saved as: {pdf_file_path}")

        self.pdf_file_path = pdf_file_path  # Save the path of the generated PDF for further actions

        # Add bill details to the database
        try:
            conn = sqlite3.connect(r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/bill.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bills (bill_id, cust_id, total, discount, final_amount, date, employee_name, payment_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (invoice_number, self.customer_id, self.total_amount, self.discount_rate, self.final_amount, current_time, self.selected_employee.get(), self.payment_type.get())
            )
            conn.commit()
            conn.close()

            # Add product details to the bill_products table in the new database
            conn = sqlite3.connect(self.bill_products_db_path)
            cursor = conn.cursor()
            for item in self.cart:
                for _ in range(item[3]):  # Insert a row for each quantity of the product
                    cursor.execute(
                        "INSERT INTO bill_products (bill_id, product_id, product_name, quantity, price, employee_name, discount, date, payment_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (invoice_number, item[0], item[1], 1, self.final_amount, self.selected_employee.get(), self.discount_rate, current_time, self.payment_type.get())
                    )
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add bill details to database: {e}")

    def send_pdf(self):
        if not hasattr(self, 'pdf_file_path'):
            messagebox.showwarning("No PDF", "Generate a PDF first.")
            return
        
        contact = self.customer_contact_label.cget("text").split(":")[1].strip()
        if not contact:
            messagebox.showwarning("No Contact", "No customer contact found.")
            return

        try:
            # Convert PDF to images
            poppler_path = r"C:\Program Files (x86)\poppler-24.08.0\Library\bin"  # Update this path to where you extracted Poppler
            images = convert_from_path(self.pdf_file_path, poppler_path=poppler_path)
            invoice_number = os.path.basename(self.pdf_file_path).split('-')[1].split('.')[0]
            image_folder = r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/invoiceJPEG"
            os.makedirs(image_folder, exist_ok=True)
            image_paths = []

            for i, image in enumerate(images):
                image_path = os.path.join(image_folder, f"invoice-{invoice_number}-{i+1}.jpg")
                image.save(image_path, 'JPEG')
                image_paths.append(image_path)

            # Send images via WhatsApp
            message = "Here is your invoice."
            for image_path in image_paths:
                pywhatkit.sendwhats_image(f"+91{contact}", image_path, caption=message)
            
            messagebox.showinfo("Sent", "PDF images sent to the customer via WhatsApp.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send PDF via WhatsApp: {e}")

    def print_pdf(self):
        if not hasattr(self, 'pdf_file_path'):
            messagebox.showwarning("No PDF", "Generate a PDF first.")
            return

        try:
            printer_name = win32print.GetDefaultPrinter()
            os.startfile(self.pdf_file_path, "print")
            messagebox.showinfo("Printed", "PDF sent to printer.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print PDF: {e}")

    def clear_cart(self):
        self.cart = []
        self.total_amount = 0
        self.discount_rate = 0
        self.final_amount = 0
        self.update_cart_display()
        self.discount_label.config(text="Discount: 0% (0.00)")
        messagebox.showinfo("Cart Cleared", "All items have been removed from the cart.")

if __name__ == "__main__":
    root = Tk()
    app = BillingSystem(
        root,
        customer_db_path='C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/customers.db',
        product_db_path='C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/products.db',
        employee_db_path='C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employees.db',
        excel_path=r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/Excel/products.xlsx"
    )
    root.mainloop()