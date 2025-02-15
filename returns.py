import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox 

class ReturnProduct:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Search & Product Management")
        self.root.geometry("600x400")

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Enter Bill Number:").grid(row=0, column=0, padx=5, pady=5)
        self.bill_entry = tk.Entry(frame)
        self.bill_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="Search", command=self.search_bill).grid(row=0, column=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Product ID", "Product Name", "Quantity", "Price"), show="headings")
        for col in ("Product ID", "Product Name", "Quantity", "Price"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Return", command=self.return_product).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Damage", command=self.damage_product).grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)  

    def search_bill(self):
        bill_id = self.bill_entry.get()
        if not bill_id:
            messagebox.showwarning("Warning", "Please enter a bill number")
            return
        
        conn = sqlite3.connect(r'C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/bill_products.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT product_id, product_name, quantity, price FROM bill_products WHERE bill_id = ?", (bill_id,))
        rows = cursor.fetchall()
        conn.close()
        
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def return_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to return")
            return
        
        item = self.tree.item(selected_item, "values")
        product_id, product_name, quantity, price = item
        
        conn = sqlite3.connect(r'C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/bill_products.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM bill_products WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()
        
        conn = sqlite3.connect(r'C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/products.db')
        cursor = conn.cursor()
        
        cursor.execute("UPDATE products SET QUANTITY = QUANTITY + 1 WHERE PRODUCTID = ?", (product_id,))
        conn.commit()
        conn.close()
        
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", f"Product {product_name} returned and quantity updated.")

    def damage_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to mark as damaged")
            return
        
        item = self.tree.item(selected_item, "values")
        product_id, product_name, quantity, price = item
        
        conn = sqlite3.connect(r'C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/bill_products.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM bill_products WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()
        
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", f"Product {product_name} marked as damaged and removed from bill.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReturnProduct(root)
    root.mainloop()
