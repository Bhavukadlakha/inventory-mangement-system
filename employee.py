import sqlite3
import cv2
import os
from tkinter import Toplevel, LabelFrame, Button, Label, CENTER, StringVar, Entry
from tkinter import ttk  # For Combobox and Treeview
from datetime import datetime
from tkinter.messagebox import showinfo, showerror
from tkinter import Tk
import pywhatkit as kit

class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x600+300+100")
        self.root.title("Employee Management & Attendance System")

        # Create the attendance table in the database
        self.create_attendance_table()

        # Database Initialization
        self.create_employee_table()

        # Variables
        self.name_var = StringVar()
        self.id_var = StringVar()
        self.contact_var = StringVar()
        self.email_var = StringVar()
        self.selected_employee = StringVar()
        self.selected_employee.set("Select Employee")
        self.timestamp_var = StringVar()
        self.photo_path = None  # To store the photo path

        # Frame for Adding Employee
        AddFrame = LabelFrame(self.root, text="Add Employee", font=("times new roman", 12, "bold"), bd=2, relief="ridge")
        AddFrame.place(x=10, y=10, width=500, height=150)

        Label(AddFrame, text="Name:", font=("times new roman", 12)).place(x=10, y=10)
        Entry(AddFrame, textvariable=self.name_var, font=("times new roman", 12)).place(x=150, y=10, width=200)

        Label(AddFrame, text="Employee ID:", font=("times new roman", 12)).place(x=10, y=40)
        Entry(AddFrame, textvariable=self.id_var, font=("times new roman", 12)).place(x=150, y=40, width=200)

        Label(AddFrame, text="Contact:", font=("times new roman", 12)).place(x=10, y=70)
        Entry(AddFrame, textvariable=self.contact_var, font=("times new roman", 12)).place(x=150, y=70, width=200)

        Label(AddFrame, text="Email:", font=("times new roman", 12)).place(x=10, y=100)
        Entry(AddFrame, textvariable=self.email_var, font=("times new roman", 12)).place(x=150, y=100, width=200)

        Button(AddFrame, text="Add Employee", font=("times new roman", 10), bg=("red") , command=self.add_employee).place(x=370, y=50, width=110)

        # Table Frame
        TableFrame = LabelFrame(self.root, text="Employee List", font=("times new roman", 12, "bold"), bd=2, relief="ridge")
        TableFrame.place(x=10, y=170, width=1080, height=200)

        self.employee_table = ttk.Treeview(
            TableFrame,
            columns=("id", "name", "contact", "email"),
            show="headings"
        )
        self.employee_table.heading("id", text="Employee ID")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("contact", text="Contact")
        self.employee_table.heading("email", text="Email")
        self.employee_table.pack(fill="both", expand=1)
        self.load_employees()

        # Attendance Frame
        AttendanceFrame = LabelFrame(self.root, text="Mark Attendance", font=("times new roman", 10, "bold"), bd=2, relief="ridge")
        AttendanceFrame.place(x=10, y=380, width=500, height=150)

        Label(AttendanceFrame, text="Employee:", font=("times new roman", 12)).place(x=10, y=10)
        self.attendance_dropdown = ttk.Combobox(AttendanceFrame, textvariable=self.selected_employee, font=("times new roman", 12), state="readonly")
        self.attendance_dropdown.place(x=150, y=10, width=200)
        self.load_employee_dropdown()

        Button(AttendanceFrame, text="Capture Photo", font=("times new roman", 10), bg=("lightblue"), command=self.capture_photo).place(x=370, y=10, width=110)

        # Share Button (Initially hidden)
        self.share_button = Button(self.root, text="Share on WhatsApp", font=("times new roman", 12, "bold"), fg=("black") , bg=("green"), command=self.share_photo, state="disabled")
        self.share_button.place(x=500, y=550, width=200)

    def create_attendance_table(self):
        """Initialize the attendance database table."""
        con = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employees.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name TEXT,
                timestamp TEXT,
                filename TEXT
            )
        """)
        con.commit()
        con.close()

    def create_employee_table(self):
        """Initialize the employee database."""
        con = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employees.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                email TEXT
            )
        """)
        con.commit()
        con.close()

    def add_employee(self):
        """Add a new employee to the database."""
        if not self.name_var.get() or not self.id_var.get():
            showerror("Error", "Employee Name and ID are required!")
            return
        con = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employee.db')
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO employees (id, name, contact, email) VALUES (?, ?, ?, ?)", (
                self.id_var.get(),
                self.name_var.get(),
                self.contact_var.get(),
                self.email_var.get()
            ))
            con.commit()
            showinfo("Success", "Employee added successfully!")
            self.load_employees()
            self.load_employee_dropdown()
            self.clear_fields()
        except sqlite3.IntegrityError:
            showerror("Error", "Employee ID already exists!")
        con.close()

    def load_employees(self):
        """Load all employees into the table."""
        self.employee_table.delete(*self.employee_table.get_children())
        con = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employees.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM employees")
        for row in cur.fetchall():
            self.employee_table.insert("", "end", values=row)
        con.close()

    def load_employee_dropdown(self):
        """Load employee names into the attendance dropdown."""
        self.attendance_dropdown["values"] = ("Select",)  # Initialize with "Select"
        con = sqlite3.connect('C:/Users/badla/OneDrive/Desktop/ivntmgmt/database/employees.db')
        cur = con.cursor()
        cur.execute("SELECT name FROM employees")
        employee_names = tuple(row[0] for row in cur.fetchall())
        self.attendance_dropdown["values"] += employee_names
        con.close()

    def clear_fields(self):
        """Clear input fields."""
        self.name_var.set("")
        self.id_var.set("")
        self.contact_var.set("")
        self.email_var.set("")

    def mark_attendance(self):
        """Mark attendance for the selected employee and capture a photo."""
        if self.selected_employee.get() == "Select":
            showerror("Error", "Please select an employee!")
            return
        self.capture_photo()

    def capture_photo(self):
        """Capture a photo using the webcam and save it to the specified folder."""
        if self.selected_employee.get() == "Select":
            showerror("Error", "Please select an employee!")
            return

        # Specify the directory where you want to save the photo
        save_directory = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\photos"

        # Ensure the directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Capture Photo")

        # Wait for space key to capture photo
        ret, frame = cam.read()
        if not ret:
            showerror("Error", "Failed to capture photo!")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %I-%M-%S %p")
        filename = f"Attendance_{self.selected_employee.get()}_{timestamp}.jpg"
        self.photo_path = os.path.join(save_directory, filename)  # Combine directory and filename

        # Save the photo to the specified folder
        cv2.imwrite(self.photo_path, frame)

        # Save attendance in the database with timestamp and file path
        con = sqlite3.connect("employees.db")
        cur = con.cursor()
        cur.execute("INSERT INTO attendance (employee_name, timestamp, filename) VALUES (?, ?, ?)", (
            self.selected_employee.get(),
            timestamp,
            self.photo_path
        ))
        con.commit()
        con.close()

        # Display the info box with employee details and timestamp
        showinfo("Photo Captured", f"Employee: {self.selected_employee.get()}\nTimestamp: {timestamp}\nSaved photo: {self.photo_path}")

        # Release the camera and close the window
        cam.release()
        cv2.destroyAllWindows()

        # Make the Share button visible and enabled
        self.share_button.config(state="normal")

    def share_photo(self):
        """Share the photo on WhatsApp."""
        if self.photo_path:
            # Get the most recently captured photo
            folder_path = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\photos"
            files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
            latest_image = files[0] if files else None

            if latest_image:
                latest_image_path = os.path.join(folder_path, latest_image)
                try: 
                    message = f"Photo file sent: {latest_image}"
                    # Share the photo via WhatsApp using pywhatkit
                    kit.sendwhats_image("+91" + "8851341067",  latest_image_path, message)
                    showinfo("Success", "Photo shared successfully!")
                except Exception as e:
                    showerror("Error", f"Failed to share photo: {e}")
            else:
                showerror("Error", "No photo available to share!")
        else:
            showerror("Error", "No photo captured yet!")

# Test the class with Tkinter root window
if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()  