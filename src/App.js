import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [tableName, setTableName] = useState('');
  const [numRows, setNumRows] = useState('');
  const [fields, setFields] = useState([{ fieldName: '', dataType: '', enumValue: '' }]);
  const [output, setOutput] = useState('');
  const [format, setFormat] = useState('SQL');
  const [errors, setErrors] = useState({});

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
    const errors = {};
    if (!tableName.trim()) {
      errors.tableName = "Table name cannot be empty.";
    }
    if (!numRows.trim() || isNaN(numRows)) {
      errors.numRows = "Number of rows must be a valid integer.";
    }
    fields.forEach((field, index) => {
      if (!field.fieldName.trim()) {
        errors[`fieldName_${index}`] = "Field name cannot be empty.";
      }
      if (!field.dataType) {
        errors[`dataType_${index}`] = "Data type must be selected.";
      }
      if (field.dataType === 'ENUM' && !field.enumValue.trim()) {
        errors[`enumValue_${index}`] = "ENUM values cannot be empty.";
      }
    });

    setErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const generateInsertStatements = async () => {
    if (!validateInput()) return;

    const requestData = {
      tableName,
      numRows,
      fields,
      format
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/generate', requestData, {
        responseType: format === 'CSV' || format === 'XML' || format === 'XLSX' ? 'blob' : 'json'
      });

      if (format === 'SQL' || format === 'JSON') {
        setOutput(format === 'SQL' ? response.data.data.join('\n') : JSON.stringify(response.data.data, null, 2));
      } else {
        // For file formats (CSV, XML, XLSX), handle the download
        const url = window.URL.createObjectURL(new Blob([response.data], { type: response.headers['content-type'] }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `data.${format.toLowerCase()}`);
        document.body.appendChild(link);
        link.click();
      }
    } catch (error) {
      console.error("There was an error generating the data!", error);
      setErrors({ form: "There was an error generating the data." });
    }
  };

  const exportData = () => {
    if (!output) return;

    const fileContent = output;
    const fileType = format;
    const fileName = `data.${fileType.toLowerCase()}`;

    const blob = new Blob([fileContent], { type: getMimeType(fileType) });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const getMimeType = (fileType) => {
    switch (fileType) {
      case 'SQL':
        return 'text/plain';
      case 'JSON':
        return 'application/json';
      case 'CSV':
        return 'text/csv';
      case 'XML':
        return 'application/xml';
      case 'XLSX':
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      default:
        return 'text/plain';
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
        {errors.tableName && <div style={{ color: 'red' }}>{errors.tableName}</div>}
      </div>
      <div>
        <label>Number of Rows</label>
        <input 
          type="text" 
          name="numRows" 
          value={numRows}
          onChange={(e) => setNumRows(e.target.value)}
          placeholder="Value" 
        />
        {errors.numRows && <div style={{ color: 'red' }}>{errors.numRows}</div>}
      </div>
      <div>
        <label>Format</label>
        <select
          value={format}
          onChange={e => setFormat(e.target.value)}
        >
          <option value="SQL">SQL</option>
          <option value="JSON">JSON</option>
          <option value="CSV">CSV</option>
          <option value="XML">XML</option>
          <option value="XLSX">XLSX</option>
        </select>
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
          {errors[`fieldName_${index}`] && <div style={{ color: 'red' }}>{errors[`fieldName_${index}`]}</div>}
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
          {errors[`dataType_${index}`] && <div style={{ color: 'red' }}>{errors[`dataType_${index}`]}</div>}
          {field.dataType === 'ENUM' && (
            <input
              type="text"
              name="enumValue"
              value={field.enumValue}
              onChange={event => handleFieldChange(index, event)}
              placeholder="ENUM Value (comma-separated)"
            />
          )}
          {errors[`enumValue_${index}`] && <div style={{ color: 'red' }}>{errors[`enumValue_${index}`]}</div>}
          <button type="button" onClick={() => handleRemoveField(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={handleAddField}>Add Field</button>
      <p></p>
      <button type="button" onClick={generateInsertStatements}>Generate Output</button>
      <button type="button" onClick={exportData}>Export Data</button>
      {errors.form && <div style={{ color: 'red' }}>{errors.form}</div>}
      {(format === 'SQL' || format === 'JSON' || format === 'XML') && (
        <div>
          <textarea
            value={output}
            placeholder="Output"
            readOnly
            style={{ width: '100%', height: '150px', marginTop: '10px' }}
          />
        </div>
      )}
    </div>
  );
}

export default App;
