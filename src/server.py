from flask import Flask, request, jsonify
from faker import Faker
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

faker = Faker()

@app.route('/generate', methods=['POST'])
def generate_insert_statements():
    data = request.json
    table_name = data.get('tableName')
    num_rows = data.get('numRows')
    fields = data.get('fields')

    if not table_name or not num_rows.isdigit():
        return jsonify({"error": "Invalid table name or number of rows."}), 400

    num_rows = int(num_rows)
    collected_fields = {}
    enums = {}
    sql_statements = []

    for field in fields:
        field_name = field['fieldName']
        data_type = field['dataType']
        enum_values = field['enumValue'].split(',') if field['dataType'] == "ENUM" else None

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
            else:
                value = f'{field_name}_value{i + 1}'  # Fallback for other types
            
            values.append(f"'{value}'")

        sql = f"INSERT INTO {table_name} ({', '.join(collected_fields.keys())}) VALUES ({', '.join(values)});"
        sql_statements.append(sql)

    return jsonify({"sqlStatements": sql_statements})

if __name__ == '__main__':
    app.run(debug=True)
