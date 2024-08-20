import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [tableName, setTableName] = useState('');
  const [numRows, setNumRows] = useState('');
  const [fields, setFields] = useState([{ fieldName: '', dataType: '', enumValue: '' }]);
  const [output, setOutput] = useState('');

  const handleFieldChange = (index, event) => {
    const values = [...fields];
    values[index][event.target.name] = event.target.value;
    setFields(values);
  };

  const handleAddField = () => {
    setFields([...fields, { fieldName: '', dataType: '', enumValue: '' }]);
  };

  const handleRemoveField = (index) => {
    const values = [...fields];
    values.splice(index, 1);
    setFields(values);
  };

  const validateInput = () => {
    if (!tableName.trim()) {
      alert("Table name cannot be empty.");
      return false;
    }
    if (!numRows.trim() || isNaN(numRows)) {
      alert("Number of rows must be a valid integer.");
      return false;
    }
    return true;
  };

  const generateInsertStatements = async () => {
    if (!validateInput()) return;

    const requestData = {
      tableName,
      numRows,
      fields
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/generate', requestData);
      setOutput(response.data.sqlStatements.join('\n'));
    } catch (error) {
      console.error("There was an error generating the SQL statements!", error);
      alert("There was an error generating the SQL statements.");
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div>
        <label>Table Name</label>
        <input 
          type="text" 
          name="tableName" 
          value={tableName}
          onChange={(e) => setTableName(e.target.value)}
          placeholder="Value" 
        />
      </div>
      <div>
        <label>Numbers of Rows</label>
        <input 
          type="text" 
          name="numRows" 
          value={numRows}
          onChange={(e) => setNumRows(e.target.value)}
          placeholder="Value" 
        />
      </div><br/>
      {fields.map((field, index) => (
        <div key={index} style={{ display: 'flex', marginBottom: '10px' }}>
          <input
            type="text"
            name="fieldName"
            value={field.fieldName}
            onChange={event => handleFieldChange(index, event)}
            placeholder="Field Name"
          />
          <select
            name="dataType"
            value={field.dataType}
            onChange={event => handleFieldChange(index, event)}
          >
            <option value="">Data Type</option>
            <option value="VARCHAR">VARCHAR</option>
            <option value="INT">INT</option>
            <option value="FLOAT">FLOAT</option>
            <option value="DOUBLE">DOUBLE</option>
            <option value="DECIMAL">DECIMAL</option>
            <option value="DATE">DATE</option>
            <option value="DATETIME">DATETIME</option>
            <option value="TIMESTAMP">TIMESTAMP</option>
            <option value="YEAR">YEAR</option>
            <option value="CHAR">CHAR</option>
            <option value="TINYINT">TINYINT</option>
            <option value="SMALLINT">SMALLINT</option>
            <option value="BIGINT">BIGINT</option>
            <option value="MEDIUMINT">MEDIUMINT</option>
            <option value="BOOLEAN">BOOLEAN</option>
            <option value="BLOB">BLOB</option>
            <option value="TEXT">TEXT</option>
            <option value="ENUM">ENUM</option>
          </select>
          {field.dataType === 'ENUM' && (
            <input
              type="text"
              name="enumValue"
              value={field.enumValue}
              onChange={event => handleFieldChange(index, event)}
              placeholder="ENUM Value (comma-separated)"
            />
          )}
          <button type="button" onClick={() => handleRemoveField(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={handleAddField}>Add Field</button>
      <p></p>
      <button type="button" onClick={generateInsertStatements}>Generate Output</button>
      <div>
        <textarea
          value={output}
          placeholder="Output"
          readOnly
          style={{ width: '100%', height: '150px', marginTop: '10px' }}
        />
      </div>
    </div>
  );
}

export default App;
