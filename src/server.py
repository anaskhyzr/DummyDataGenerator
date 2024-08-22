from flask import Flask, request, jsonify, Response, send_file
from faker import Faker
import random
import csv
import json
import xml.etree.ElementTree as ET
import io
import pandas as pd
import xlsxwriter 
import xml.etree.ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

faker = Faker()

# Function to generate SQL data
def generate_sql_statements(table_name, num_rows, fields):
    collected_fields = {}
    enums = {}
    sql_statements = []

    for field in fields:
        field_name = field['fieldName']
        data_type = field['dataType']
        enum_values = field['enumValue'].split(',') if data_type == "ENUM" else None

        if field_name and data_type:
            collected_fields[field_name] = data_type
            if enum_values:
                enums[field_name] = [value.strip() for value in enum_values]

    for i in range(num_rows):
        values = []
        for field_name, data_type in collected_fields.items():
            if data_type == 'ENUM':
                value = random.choice(enums[field_name])
            elif data_type == 'VARCHAR':
                value = faker.word()
            elif data_type == 'INT':
                value = faker.random_int(min=0, max=100)
            elif data_type == 'FLOAT':
                value = round(faker.random_number(digits=5) * 0.01, 2)
            elif data_type == 'DOUBLE':
                value = round(faker.random_number(digits=10) * 0.01, 4)
            elif data_type == 'DECIMAL':
                value = round(faker.random_number(digits=5) * 0.01, 2)
            elif data_type == 'DATE':
                value = faker.date()
            elif data_type == 'DATETIME':
                value = faker.date_time()
            elif data_type == 'TIMESTAMP':
                value = faker.date_time().timestamp()
            elif data_type == 'YEAR':
                value = faker.year()
            elif data_type == 'CHAR':
                value = faker.word()
            elif data_type == 'TINYINT':
                value = faker.random_int(min=0, max=255)
            elif data_type == 'SMALLINT':
                value = faker.random_int(min=-32768, max=32767)
            elif data_type == 'BIGINT':
                value = faker.random_int(min=-9223372036854775808, max=9223372036854775807)
            elif data_type == 'MEDIUMINT':
                value = faker.random_int(min=-8388608, max=8388607)
            elif data_type == 'BOOLEAN':
                value = faker.boolean()
            elif data_type == 'BLOB':
                value = faker.binary()
            elif data_type == 'TEXT':
                value = faker.text()
            else:
                value = f'{field_name}_value{i + 1}'
            
            values.append(f"'{value}'")

        sql = f"INSERT INTO {table_name} ({', '.join(collected_fields.keys())}) VALUES ({', '.join(values)});"
        sql_statements.append(sql)

    return sql_statements

# Function to generate JSON data
def generate_json_data(num_rows, fields):
    data = []
    for _ in range(num_rows):
        row = {}
        for field in fields:
            field_name = field['fieldName']
            data_type = field['dataType']
            if data_type == 'ENUM':
                value = random.choice(field['enumValue'].split(','))
            elif data_type == 'VARCHAR':
                value = faker.word()
            elif data_type == 'INT':
                value = faker.random_int(min=0, max=100)
            elif data_type == 'FLOAT':
                value = round(faker.random_number(digits=5) * 0.01, 2)
            elif data_type == 'DOUBLE':
                value = round(faker.random_number(digits=10) * 0.01, 4)
            elif data_type == 'DECIMAL':
                value = round(faker.random_number(digits=5) * 0.01, 2)
            elif data_type == 'DATE':
                value = faker.date().isoformat()
            elif data_type == 'DATETIME':
                value = faker.date_time().isoformat()
            elif data_type == 'TIMESTAMP':
                value = faker.date_time().timestamp()
            elif data_type == 'YEAR':
                value = faker.year()
            elif data_type == 'CHAR':
                value = faker.word()
            elif data_type == 'TINYINT':
                value = faker.random_int(min=0, max=255)
            elif data_type == 'SMALLINT':
                value = faker.random_int(min=-32768, max=32767)
            elif data_type == 'BIGINT':
                value = faker.random_int(min=-9223372036854775808, max=9223372036854775807)
            elif data_type == 'MEDIUMINT':
                value = faker.random_int(min=-8388608, max=8388607)
            elif data_type == 'BOOLEAN':
                value = faker.boolean()
            elif data_type == 'BLOB':
                value = faker.binary().decode('latin1')  # Decode to string for JSON
            elif data_type == 'TEXT':
                value = faker.text()
            else:
                value = f'{field_name}_value'
            
            row[field_name] = value
        data.append(row)
    return data

# Function to generate CSV data
def generate_csv_data(num_rows, fields):
    csv_output = io.StringIO()
    columns = [f['fieldName'] for f in fields]
    rows = generate_json_data(num_rows, fields)
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(csv_output, index=False, sep=',')  # Ensure the separator is a comma
    return csv_output.getvalue()

# Function to generate XML data
def generate_xml_data(num_rows, fields):
    # Create the root element
    root = ET.Element("data")
    
    # Generate data directly based on fields
    for _ in range(num_rows):
        record = ET.SubElement(root, "record")
        for field in fields:
            field_name = field['fieldName']
            data_type = field['dataType']
            
            # Generate field data based on its type
            if data_type == 'ENUM':
                value = random.choice(field['enumValue'].split(','))
            elif data_type == 'VARCHAR':
                value = faker.word()
            elif data_type == 'INT':
                value = str(faker.random_int(min=0, max=100))
            elif data_type == 'FLOAT':
                value = str(round(faker.random_number(digits=5) * 0.01, 2))
            elif data_type == 'DOUBLE':
                value = str(round(faker.random_number(digits=10) * 0.01, 4))
            elif data_type == 'DECIMAL':
                value = str(round(faker.random_number(digits=5) * 0.01, 2))
            elif data_type == 'DATE':
                value = faker.date().isoformat()
            elif data_type == 'DATETIME':
                value = faker.date_time().isoformat()
            elif data_type == 'TIMESTAMP':
                value = str(faker.date_time().timestamp())
            elif data_type == 'YEAR':
                value = faker.year()
            elif data_type == 'CHAR':
                value = faker.word()
            elif data_type == 'TINYINT':
                value = str(faker.random_int(min=0, max=255))
            elif data_type == 'SMALLINT':
                value = str(faker.random_int(min=-32768, max=32767))
            elif data_type == 'BIGINT':
                value = str(faker.random_int(min=-9223372036854775808, max=9223372036854775807))
            elif data_type == 'MEDIUMINT':
                value = str(faker.random_int(min=-8388608, max=8388607))
            elif data_type == 'BOOLEAN':
                value = str(faker.boolean()).lower()  # Convert to lowercase for XML boolean values
            elif data_type == 'BLOB':
                value = faker.binary().hex()  # Convert binary to a hexadecimal string
            elif data_type == 'TEXT':
                value = faker.text()
            else:
                value = f'{field_name}_value'
            
            # Create an XML element for each field
            field_element = ET.SubElement(record, field_name)
            field_element.text = value
    
    # Convert the XML tree to a string
    xml_string = ET.tostring(root, encoding='unicode')
    
    return xml_string



# Function to generate Excel data

def generate_excel_data(num_rows, fields):
    output = io.BytesIO()
    columns = [f['fieldName'] for f in fields]
    rows = generate_json_data(num_rows, fields)
    df = pd.DataFrame(rows, columns=columns)

    # Use the context manager to handle Excel file creation
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    output.seek(0)  # Move the pointer back to the beginning of the file
    return output.getvalue()  # Return the binary content of the Excel file





@app.route('/generate', methods=['POST'])
def generate_insert_statements():
    data = request.json
    table_name = data.get('tableName')
    num_rows = data.get('numRows')
    fields = data.get('fields')
    format_type = data.get('format')

    if not table_name or not num_rows or not fields:
        return jsonify({"error": "Missing required fields."}), 400

    if not num_rows.isdigit() or int(num_rows) <= 0:
        return jsonify({"error": "Invalid number of rows."}), 400

    num_rows = int(num_rows)

    # Generating data based on selected format
    if format_type == 'SQL':
        sql_statements = generate_sql_statements(table_name, num_rows, fields)
        return jsonify({"data": sql_statements})
    elif format_type == 'JSON':
        json_data = generate_json_data(num_rows, fields)
        return jsonify({"data": json_data})
    elif format_type == 'CSV':
        csv_data = generate_csv_data(num_rows, fields)
        return Response(csv_data, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})
    elif format_type == 'EXCEL':
        excel_data = generate_excel_data(num_rows, fields)
        return Response(excel_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={"Content-Disposition": "attachment;filename=data.xlsx"} )
    try:
        if format_type == 'XML':
            print(3)
            xml_data = generate_xml_data(num_rows, fields)
            print(f"Generated XML Data: {xml_data}")  # Debugging: Print XML Data
            if not xml_data.strip():  # Check if XML data is empty
                return "Error: No data generated", 500
            return Response(xml_data, mimetype='application/xml', headers={"Content-Disposition": "attachment;filename=data.xml"})
        # Handle other formats (CSV, EXCEL, etc.)
    except Exception as e:
        print(f"Error generating XML: {e}")
        return "Error generating XML", 500
    else:
        return jsonify({"error": "Invalid format type."}), 400
    


@app.route('/export', methods=['POST'])
def export_data():
    data = request.json  # Assuming the data is sent as JSON
    # Process the data (e.g., convert to the desired format)
    file_content = '\n'.join(data['output'])  # Assuming 'output' is a list of strings
    
    # Create a file-like object in memory
    file = io.BytesIO(file_content.encode('utf-8'))
    file.seek(0)
    
    # Return the file for download
    return send_file(file, as_attachment=True, attachment_filename='exported_data.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
