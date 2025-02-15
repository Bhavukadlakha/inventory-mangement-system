import sqlite3
import pandas as pd
import os

# Define the path to the database file
db_file = "C:/Users/badla/OneDrive/Desktop/ivntmgmt/employees.db"
  # Replace with your .db file path'  # Replace with your .db file path

# Extract the name of the database without extension for the Excel file name
db_name = os.path.splitext(os.path.basename(db_file))[0]
excel_file = f"{db_name}.xlsx"

try:
    # Establish connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Get a list of all tables in the database
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(tables_query, conn)

    # Check if there are any tables in the database
    if not tables.empty:
        # If the Excel file already exists, delete it to avoid duplication
        if os.path.exists(excel_file):
            os.remove(excel_file)  # Remove the existing Excel file
            print(f"Deleted existing Excel file: {excel_file}")

        # Create a new Excel writer object with the same file name
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            for table in tables['name']:
                try:
                    # Query the table into a DataFrame
                    query = f"SELECT * FROM {table};"
                    df = pd.read_sql(query, conn)

                    # Add the table data to the Excel file
                    df.to_excel(writer, sheet_name=table, index=False)
                    print(f"Exported {table} to Excel.")
                except Exception as e:
                    print(f"Error exporting table {table}: {e}")
    else:
        print("No tables found in the database.")

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Ensure the connection is closed
    if conn:
        conn.close()
