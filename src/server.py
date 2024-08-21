from flask import Flask, request, jsonify, Response, send_file
from faker import Faker
import random
import csv
import json
import xml.etree.ElementTree as ET
import io
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

faker = Faker()

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

def generate_csv_data(num_rows, fields):
    data = generate_json_data(num_rows, fields)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[field['fieldName'] for field in fields])
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def generate_xml_data(num_rows, fields):
    data = generate_json_data(num_rows, fields)
    root = ET.Element("root")
    for row in data:
        item = ET.SubElement(root, "item")
        for field_name, value in row.items():
            field_element = ET.SubElement(item, field_name)
            field_element.text = str(value)
    return ET.tostring(root, encoding='unicode')

def generate_xlsx_data(num_rows, fields):
    data = generate_json_data(num_rows, fields)
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

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

    if format_type == 'SQL':
        sql_statements = generate_sql_statements(table_name, num_rows, fields)
        return jsonify({"data": sql_statements})
    elif format_type == 'JSON':
        json_data = generate_json_data(num_rows, fields)
        return jsonify({"data": json_data})
    elif format_type == 'CSV':
        csv_data = generate_csv_data(num_rows, fields)
        return Response(csv_data, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})
    elif format_type == 'XML':
        xml_data = generate_xml_data(num_rows, fields)
        return Response(xml_data, mimetype='application/xml', headers={"Content-Disposition": "attachment;filename=data.xml"})
    elif format_type == 'XLSX':
        xlsx_data = generate_xlsx_data(num_rows, fields)
        return Response(xlsx_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={"Content-Disposition": "attachment;filename=data.xlsx"})
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
