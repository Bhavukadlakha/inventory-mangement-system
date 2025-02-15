import sqlite3
import pandas as pd

# Define paths
db_path = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\bill_products.db"
excel_path = r"C:\Users\badla\OneDrive\Desktop\ivntmgmt\bill_products.xlsx"

# Connect to SQLite database
conn = sqlite3.connect(db_path)

# Read data from the bill_products table
query = "SELECT * FROM bill_products"
df = pd.read_sql_query(query, conn)

# Close database connection
conn.close()

# Write to Excel file (overwrite if exists)
with pd.ExcelWriter(excel_path, engine="openpyxl", mode="w") as writer:
    df.to_excel(writer, sheet_name="bill_products", index=False)

print("Database exported to Excel successfully!")
