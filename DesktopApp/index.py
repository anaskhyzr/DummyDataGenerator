import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import csv
import json
import xml.etree.ElementTree as ET
import os
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Initialize global variables for fields and enums
fields = {}
enums = {}

# Function to get fake data based on data type and optional enum values
def get_fake_data(data_type, enum_values=None):
    if data_type == "VARCHAR":
        return fake.word()
    elif data_type == "INT":
        return fake.random_int(min=0, max=1000)
    elif data_type == "FLOAT":
        return round(fake.random_number(digits=5) / 100.0, 2)
    elif data_type == "DOUBLE":
        return round(fake.random_number(digits=7) / 100.0, 4)
    elif data_type == "DECIMAL":
        return round(fake.random_number(digits=10) / 100.0, 2)
    elif data_type == "DATE":
        return fake.date()
    elif data_type == "DATETIME":
        return fake.date_time().strftime('%Y-%m-%d %H:%M:%S')
    elif data_type == "TIMESTAMP":
        return fake.unix_time()
    elif data_type == "TIME":
        return fake.time()
    elif data_type == "YEAR":
        return fake.year()
    elif data_type == "CHAR":
        return fake.word()[:1]
    elif data_type == "TINYINT":
        return fake.random_int(min=0, max=127)
    elif data_type == "SMALLINT":
        return fake.random_int(min=0, max=32767)
    elif data_type == "MEDIUMINT":
        return fake.random_int(min=0, max=8388607)
    elif data_type == "BIGINT":
        return fake.random_int(min=0, max=9223372036854775807)
    elif data_type == "BOOLEAN":
        return fake.boolean()
    elif data_type == "BLOB":
        return fake.text(max_nb_chars=50).encode('utf-8')
    elif data_type == "TEXT":
        return fake.text()
    elif data_type == "ENUM" and enum_values:
        return fake.random_element(elements=enum_values)
    else:
        return "NULL"

# Function to generate SQL INSERT statements and fake data
def generate_insert_statements():
    global fields, enums
    
    table_name = table_name_entry.get().strip()  # Get table name from user input
    num_rows_str = num_rows_entry.get().strip()  # Get number of rows from user input
    
    # Validate table name and number of rows
    if not table_name:
        messagebox.showwarning("Input Error", "Table name cannot be empty.")
        return
    
    if not num_rows_str.isdigit():
        messagebox.showwarning("Input Error", "Number of rows must be a valid integer.")
        return
    
    num_rows = int(num_rows_str)
    
    # Collect field names and data types
    for field_entry, type_entry, enum_entry, _ in field_entries:
        field_name = field_entry.get()
        data_type = type_entry.get()
        enum_values = enum_entry.get().split(',') if enum_entry.get() and data_type == "ENUM" else None

        if field_name and data_type:
            fields[field_name] = data_type
            if data_type == "ENUM" and enum_values:
                enums[field_name] = [value.strip() for value in enum_values]
                
    sql_statements = []  # List to store SQL statements
    data = []  # List to store generated data

    # Generate fake data and SQL statements
    for _ in range(num_rows):
        record = {field: get_fake_data(fields[field], enums.get(field)) for field in fields}
        data.append(record)

        columns = ', '.join(fields.keys())
        values = ', '.join([f"'{get_fake_data(fields[field], enums.get(field))}'" for field in fields])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
        sql_statements.append(sql)

    return sql_statements, data

# Function to display generated SQL statements in the output area
def display_data():
    file_format = export_format.get()  # Get selected file format
    sql_statements, data = generate_insert_statements()
    
    if not sql_statements:
        return

    # Clear the text area
    sql_text_area.config(state=tk.NORMAL)
    sql_text_area.delete('1.0', tk.END)

    # Display content based on selected file format
    if file_format == "SQL":
        sql_text_area.insert(tk.END, '\n'.join(sql_statements))
    elif file_format == "CSV":
        csv_content = ", ".join(fields.keys()) + "\n"
        csv_content += "\n".join([", ".join([str(record[field]) for field in fields]) for record in data])
        sql_text_area.insert(tk.END, csv_content)
    elif file_format == "Excel":
        # Save data to a temporary Excel file
        temp_path = "temp_excel.xlsx"
        df = pd.DataFrame(data)
        df.to_excel(temp_path, index=False, engine='openpyxl')
        
        # Read and display the content
        excel_data = pd.read_excel(temp_path).to_string(index=False)
        sql_text_area.insert(tk.END, excel_data)
        os.remove(temp_path)  # Clean up temporary file
    elif file_format == "JSON":
        json_content = json.dumps(data, indent=4)
        sql_text_area.insert(tk.END, json_content)
    elif file_format == "XML":
        root = ET.Element("root")
        for record in data:
            item = ET.SubElement(root, "item")
            for key, value in record.items():
                child = ET.SubElement(item, key)
                child.text = str(value)
        xml_content = ET.tostring(root, encoding='unicode', method='xml')
        sql_text_area.insert(tk.END, xml_content)

    sql_text_area.config(state=tk.DISABLED)

# Function to save data in the selected format
def save_file():
    file_format = export_format.get()  # Get selected file format
    sql_statements, data = generate_insert_statements()
    
    if not sql_statements:
        return

    # Prompt user for file save location and name
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_format.lower()}",
                                           filetypes=[(f"{file_format} files", f"*.{file_format.lower()}"),
                                                      ("All files", "*.*")])
    if not file_path:
        return

    # Ensure the file extension is correct
    if file_format == "Excel" and not file_path.endswith('.xlsx'):
        file_path += '.xlsx'

    # Save data based on selected file format
    if file_format == "SQL":
        with open(file_path, 'w') as f:
            f.write('\n'.join(sql_statements))
        sql_text_area.config(state=tk.NORMAL)
        sql_text_area.delete('1.0', tk.END)
        sql_text_area.insert(tk.END, f"SQL statements saved to {file_path}")
        sql_text_area.config(state=tk.DISABLED)
    elif file_format == "CSV":
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields.keys())
            for record in data:
                writer.writerow([record[field] for field in fields])
        sql_text_area.config(state=tk.NORMAL)
        sql_text_area.delete('1.0', tk.END)
        sql_text_area.insert(tk.END, f"CSV file saved to {file_path}")
        sql_text_area.config(state=tk.DISABLED)
    elif file_format == "Excel":
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            sql_text_area.config(state=tk.NORMAL)
            sql_text_area.delete('1.0', tk.END)
            sql_text_area.insert(tk.END, f"Excel file saved to {file_path}")
            sql_text_area.config(state=tk.DISABLED)
        except ImportError:
            messagebox.showerror("Error", "The `openpyxl` library is required to export Excel files.")
    elif file_format == "JSON":
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        sql_text_area.config(state=tk.NORMAL)
        sql_text_area.delete('1.0', tk.END)
        sql_text_area.insert(tk.END, f"JSON file saved to {file_path}")
        sql_text_area.config(state=tk.DISABLED)
    elif file_format == "XML":
        root = ET.Element("root")
        for record in data:
            item = ET.SubElement(root, "item")
            for key, value in record.items():
                child = ET.SubElement(item, key)
                child.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path)
        sql_text_area.config(state=tk.NORMAL)
        sql_text_area.delete('1.0', tk.END)
        sql_text_area.insert(tk.END, f"XML file saved to {file_path}")
        sql_text_area.config(state=tk.DISABLED)

# Function to add a new field input row
def add_field():
    # Track the data type selection for visibility control
    data_type_var = tk.StringVar()

    # Get the row index for placing widgets
    row_index = len(field_entries) + 1

    # Entry for field name
    field_entry = tk.Entry(fields_frame, font=('Arial', 10))
    field_entry.grid(row=row_index, column=0, padx=5, pady=5)

    # Combobox for selecting data type
    type_entry = ttk.Combobox(fields_frame, textvariable=data_type_var, values=[
        "VARCHAR", "INT", "FLOAT", "DOUBLE", "DECIMAL", "DATE", "DATETIME",
        "TIMESTAMP", "TIME", "YEAR", "CHAR", "TINYINT", "SMALLINT", 
        "MEDIUMINT", "BIGINT", "BOOLEAN", "BLOB", "TEXT", "ENUM"
    ],  style='TCombobox')
    type_entry.grid(row=row_index, column=1, padx=5, pady=5)
    type_entry.bind("<<ComboboxSelected>>", lambda event: toggle_enum_entry(type_entry, enum_entry))
    
    enum_entry = tk.Entry(fields_frame, bg='#BBDEFB', font=('Arial', 10), width=30)
    enum_entry.grid(row=row_index, column=2, padx=5, pady=5)
    enum_entry.grid_forget()  # Initially hidden
    
    # Button to remove the field entry row
    remove_button = tk.Button(fields_frame, text="Remove", command=lambda: remove_field(row_index))
    remove_button.grid(row=row_index, column=3, padx=5, pady=5)

    field_entries.append((field_entry, type_entry, enum_entry, remove_button))

# Function to show or hide the ENUM entry based on the selected data type
def toggle_enum_entry(type_entry, enum_entry):
    if type_entry.get() == "ENUM":
        enum_entry.grid(row=type_entry.grid_info()["row"], column=2, padx=5, pady=5)
        enum_entry.insert(0, "ENUM Values (comma-separated)")
        enum_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, enum_entry))
        enum_entry.bind("<FocusOut>", lambda event: add_placeholder(event, enum_entry))
    else:
        enum_entry.grid_forget()

def clear_placeholder(event, entry):
    if entry.get() == "ENUM Values (comma-separated)":
        entry.delete(0, tk.END)

def add_placeholder(event, entry):
    if entry.get() == "":
        entry.insert(0, "ENUM Values (comma-separated)")

# Function to remove a field input row
def remove_field(row_index):
    # Find the widgets in the specified row and destroy them
    for widget in fields_frame.grid_slaves(row=row_index):
        widget.destroy()

    # Remove the entry from the field_entries list
    global field_entries
    field_entries = [entry for entry in field_entries if entry[0].grid_info()["row"] != row_index]

    # Update the remaining entries to fill the gap
    for i, entry in enumerate(field_entries):
        for widget in entry:
            widget.grid(row=i+1)

# Function to collect fields from user input
def collect_fields():
    global fields, enums
    fields = {}
    enums = {}

    for field_entry, type_entry, enum_entry, _ in field_entries:
        field_name = field_entry.get().strip()
        data_type = type_entry.get()
        enum_values = enum_entry.get().split(',') if enum_entry.get() and data_type == "ENUM" else None

        if field_name and data_type:
            fields[field_name] = data_type
            if data_type == "ENUM" and enum_values:
                enums[field_name] = [value.strip() for value in enum_values]  # Strip extra spaces

# Setup GUI
root = tk.Tk()
root.title("Dummy Data Generator")
root.geometry("1000x800")
root.minsize(1000, 800)

# Main frame to hold all components
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas and scrollbars for the main frame
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_x = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

scroll_y = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

# Frame to contain all content
content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor='nw')

content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Header frame for table name and number of rows
header_frame = tk.Frame(content_frame)
header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

tk.Label(header_frame, text="Table Name:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10)
table_name_entry = tk.Entry(header_frame)
table_name_entry.grid(row=0, column=1, padx=10)

tk.Label(header_frame, text="Number of Rows:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=10)
num_rows_entry = tk.Entry(header_frame)
num_rows_entry.grid(row=1, column=1, padx=10)

# Field management
fields_frame = tk.Frame(content_frame)
fields_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='W')
tk.Label(fields_frame, text="Field Name", font=('Arial', 12, 'bold')).grid(row=0, column=0)
tk.Label(fields_frame, text="Data Type", font=('Arial', 12, 'bold')).grid(row=0, column=1)
tk.Label(fields_frame, text="Enum Values (if any)", font=('Arial', 12, 'bold')).grid(row=0, column=2)
tk.Button(header_frame, text="Add Field", command=add_field).grid(row=2, column=0, columnspan=2, pady=10)

field_entries = []
add_field()  # Initialize with one field

# File format options
format_frame = tk.Frame(content_frame)
format_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

tk.Label(format_frame, text="Export Format:").grid(row=0, column=0, padx=10)

export_format = tk.StringVar(value="SQL")
formats = ["SQL", "CSV", "Excel", "JSON", "XML"]

for fmt in formats:
    tk.Radiobutton(format_frame, text=fmt, variable=export_format, value=fmt).grid(row=0, column=formats.index(fmt)+1, padx=5)

# Buttons
button_frame = tk.Frame(content_frame)
button_frame.grid(row=5, column=0, sticky='w', padx=20, pady=10)

generate_button = tk.Button(button_frame, text="Generate File", command=save_file)
generate_button.pack(side=tk.LEFT, padx=10)

display_button = tk.Button(button_frame, text="Display Statements", command=display_data)
display_button.pack(side=tk.LEFT, padx=10)

# SQL output area
sql_text_area_frame = tk.Frame(content_frame)
sql_text_area_frame.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

sql_text_area = scrolledtext.ScrolledText(sql_text_area_frame, height=15, width=80, wrap=tk.WORD)
sql_text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

sql_text_area_scroll_y = tk.Scrollbar(sql_text_area_frame, orient=tk.VERTICAL, command=sql_text_area.yview)
sql_text_area_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

sql_text_area.config(yscrollcommand=sql_text_area_scroll_y.set)

root.mainloop()
