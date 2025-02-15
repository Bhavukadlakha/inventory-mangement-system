from tkinter import Tk, Label, Button, PhotoImage, Frame, LEFT, RIDGE, TOP, X, Toplevel
from PIL import Image, ImageTk
import time 
from employee import EmployeeClass 
from products import ProductManagement
from customer import CustomerClass 
from billing import BillingSystem  
from returns import ReturnProduct
from barcode_generator import BarcodeGenerator 
from sales import SalesTrackingApp 
from supplier import SupplierManagement

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System / JAIGURUJI")

        # Allow resizing
        self.root.resizable(True, True)

        # -----title------
        self.icon_title = PhotoImage(file='C:/Users/badla/OneDrive/Desktop/ivntmgmt/images/logo1.png')
        title = Label(self.root, text="Inventory Management System", image=self.icon_title,
                      compound=LEFT, font=("times new roman", 30, "bold"), 
                      bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ---button--- Logout functionality
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), 
                            bg="yellow", cursor="hand2", command=self.logout)
        btn_logout.place(x=1200, y=10, height=30, width=100)

        # ---clock---
        self.lbl_clock = Label(self.root, font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_clock()  # Call the clock update function

        # ---left menu---
        self.MenuLogo = Image.open('C:/Users/badla/OneDrive/Desktop/ivntmgmt/images/menu_im.png')
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE)
        LeftMenu.place(x=0, y=102, width=250, height=668)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        # ---icon for buttons---
        self.icon_side = PhotoImage(file='C:/Users/badla/OneDrive/Desktop/ivntmgmt/images/side.png')

        # ---menu buttons with function calls---
        btn_employee = Button(LeftMenu, text="Employee", image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                             bg="white", bd=3, cursor="hand2", command=self.employee)
        btn_employee.pack(side=TOP, fill=X)
        
        btn_sales = Button(LeftMenu, text="Sales", image=self.icon_side, compound=LEFT, 
                          padx=20, font=("times new roman", 15, "bold"), 
                          bg="white", bd=3, cursor="hand2", command=self.open_sales_window)
        btn_sales.pack(side=TOP, fill=X)
        
        btn_products = Button(LeftMenu, text="Products", image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                             bg="white", bd=3, cursor="hand2", command=self.product)
        btn_products.pack(side=TOP, fill=X)  
        btn_Barcode = Button(LeftMenu, text="Barcode", image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                             bg="white", bd=3, cursor="hand2", command=self.BarcodeGemerator)
        btn_Barcode.pack(side=TOP, fill=X) 
      
        btn_bill = Button(LeftMenu, text="Billing", image=self.icon_side, compound=LEFT,
                            padx=20, font=("times new roman", 15, "bold"), 
                            bg="white", bd=3, cursor="hand2", command=self.BillingSystem) 
        btn_bill.pack(side=TOP, fill=X)  

        btn_returns = Button(LeftMenu, text="Returns",image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                              bg="white", bd=3, cursor="hand2", command=self.returns) 
        btn_returns.pack(side=TOP, fill=X)

        # Added customer button
        btn_customer = Button(LeftMenu, text="New Customer", image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                             bg="white", bd=3, cursor="hand2", command=self.customer)
        btn_customer.pack(side=TOP, fill=X)  

        btn_supplier = Button(LeftMenu, text="New supplier", image=self.icon_side, compound=LEFT, 
                             padx=20, font=("times new roman", 15, "bold"), 
                             bg="white", bd=3, cursor="hand2", command=self.supplier)
        btn_supplier.pack(side=TOP, fill=X) 

        
        # added button for exit 
        btn_exit = Button(LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, 
                         padx=20, font=("times new roman", 15, "bold"), 
                         bg="white", bd=3, cursor="hand2", command=self.exit_application)
        btn_exit.pack(side=TOP, fill=X)   
    
    def update_clock(self):
        current_time = time.strftime("Welcome Staff\t\t Date: %d-%m-%Y\t\t Time: %I:%M:%S %p")
        self.lbl_clock.config(text=current_time)
        self.root.after(1000, self.update_clock)  # Update every 1 second

    def logout(self):
        self.root.quit()  # Logs out (exits the app)

    def exit_application(self):
        self.root.quit()  # Exits the application

    def employee(self): 
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win) 

    def BarcodeGemerator(self):
        self.new_win = Toplevel(self.root)
        BarcodeGenerator(self.new_win, 
                         products_file = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\Excel\products.xlsx",
                         barcode_file = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\Excel\barcode.xlsx",
                         barcode_photos_path = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\barcode photos")
                                        


    def open_sales_window(self):
       new_window = Toplevel(self.root) 
       self.new_obj = SalesTrackingApp(new_window) 

    def product(self): 
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductManagement(self.new_win)

    def open_attendance_window(self):
        print("Opening Attendance Window...")
        # Add functionality for the Attendance window here 

    def BillingSystem(self):
        new_window = Toplevel(self.root)
        BillingSystem(new_window, 
                      customer_db_path=r'C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\customers.db',
                      product_db_path=r'C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\products.db',
                      employee_db_path=r'C:\Users\badla\OneDrive\Desktop\ivntmgmt\database\employees.db',
                      excel_path=r"C:/Users/badla/OneDrive/Desktop/ivntmgmt/Excel/products.xlsx" 
        )  
        
    def supplier(self): 
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierManagement(self.new_win)
        
        

    def customer(self): 
        self.new_win = Toplevel(self.root)
        self.new_obj = CustomerClass(self.new_win) 

    
    def returns(self): 
        self.new_win = Toplevel(self.root)
        self.new_obj = ReturnProduct(self.new_win)    

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
