import React, { useState, useRef } from 'react';
import TableForm from './components/TableForm';
import OutputDisplay from './components/OutputDisplay';
import Header from './components/Header';
import axios from 'axios';
import LoadingBar from 'react-top-loading-bar';
import * as XLSX from 'xlsx';
import './App.css';

function App() {
  const [tableName, setTableName] = useState('');
  const [numRows, setNumRows] = useState('');
  const [fields, setFields] = useState([{ fieldName: '', dataType: '', enumValue: '' }]);
  const [output, setOutput] = useState('');
  const [format, setFormat] = useState('SQL');
  const [errors, setErrors] = useState({});
  const [tableData, setTableData] = useState([]); // State for tableData
  const ref = useRef(null);

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
    if (!numRows.trim() || isNaN(numRows) || numRows <= 0) {
      errors.numRows = "Number of rows must be a positive integer.";
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

    ref.current.continuousStart(); // Start the loading bar

    const requestData = {
      tableName,
      numRows,
      fields,
      format
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/generate', requestData, {
        responseType: format === 'EXCEL' ? 'arraybuffer' : 'json'
      });

      if (format === 'SQL' || format === 'JSON') {
        setOutput(format === 'SQL' ? response.data.data.join('\n') : JSON.stringify(response.data.data, null, 2));
      } else if (format === 'CSV' || format === 'XML') {
        setOutput(response.data);
      } else if (format === 'EXCEL') {
        const data = response.data;
        const workbook = XLSX.read(data, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        setTableData(jsonData); // Set the table data
        setOutput(''); // Clear text output
      }
    } catch (error) {
      console.error("There was an error generating the data!", error);
      setErrors({ form: "There was an error generating the data." });
    } finally {
      ref.current.complete(); // Complete the loading bar
    }
  };

  const exportData = () => {
    if (!output && format !== 'EXCEL') return;
  
    const fileExtension = getFileExtension(format);
    const fileName = `data.${fileExtension}`;
    const mimeType = getMimeType(format);
  
    let blob;
    if (format === 'EXCEL') {
      const worksheet = XLSX.utils.json_to_sheet(tableData);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
      
      // Write workbook as binary string
      const binaryString = XLSX.write(workbook, { bookType: 'xlsx', type: 'binary' });
      
      // Convert binary string to array buffer
      const arrayBuffer = new ArrayBuffer(binaryString.length);
      const view = new Uint8Array(arrayBuffer);
      for (let i = 0; i < binaryString.length; i++) {
        view[i] = binaryString.charCodeAt(i) & 0xFF;
      }
  
      // Create Blob from array buffer
      blob = new Blob([arrayBuffer], { type: mimeType });
    } else {
      blob = new Blob([output], { type: mimeType });
    }
  
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  

  const getFileExtension = (format) => {
    switch (format) {
      case 'SQL':
        return 'sql';
      case 'JSON':
        return 'json';
      case 'CSV':
        return 'csv';
      case 'XML':
        return 'xml';
      case 'EXCEL':
        return 'xlsx';
      default:
        return 'txt';
    }
  };

  const getMimeType = (format) => {
    switch (format) {
      case 'SQL':
        return 'text/plain';
      case 'JSON':
        return 'application/json';
      case 'CSV':
        return 'text/csv';
      case 'XML':
        return 'application/xml';
      case 'EXCEL':
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      default:
        return 'text/plain';
    }
  };

  return (
    <div className="container">
      <LoadingBar color="#f11946" ref={ref} />  {/* Add the loading bar */}
      <Header />
      <TableForm
        tableName={tableName}
        numRows={numRows}
        fields={fields}
        errors={errors}
        setTableName={setTableName}
        setNumRows={setNumRows}
        setFormat={setFormat}
        handleFieldChange={handleFieldChange}
        handleAddField={handleAddField}
        handleRemoveField={handleRemoveField}
        generateInsertStatements={generateInsertStatements}
        exportData={exportData}
      />
      <OutputDisplay format={format} output={output} tableData={tableData} /> {/* Pass tableData to OutputDisplay */}
    </div>
  );
}

export default App;
