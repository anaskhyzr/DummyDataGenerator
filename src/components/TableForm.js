import React from 'react';
import FieldList from './FieldList';
import './TableForm.css';

function TableForm({
  tableName,
  numRows,
  format,
  fields,
  errors,
  setTableName,
  setNumRows,
  setFormat,
  handleFieldChange,
  handleAddField,
  handleRemoveField,
  generateInsertStatements,
  exportData
}) {
  return (
    <form className="table-form">
      <div className="input-group">
        <label>Table Name</label>
        <input
          type="text"
          name="tableName"
          value={tableName}
          onChange={(e) => setTableName(e.target.value)}
          placeholder="Enter table name"
          className="input-field"
        />
        {errors.tableName && <div className="error-message">{errors.tableName}</div>}
      </div>
      <div className="input-group">
        <label>Number of Rows</label>
        <input
          type="text"
          name="numRows"
          value={numRows}
          onChange={(e) => setNumRows(e.target.value)}
          placeholder="Enter number of rows"
          className="input-field"
        />
        {errors.numRows && <div className="error-message">{errors.numRows}</div>}
      </div>
      <div className="input-group">
        <label>Format</label>
        <select
          value={format}
          onChange={e => setFormat(e.target.value)}
          className="select-field"
        >
          <option value="SQL">SQL</option>
          <option value="JSON">JSON</option>
          <option value="CSV">CSV</option>
          <option value="EXCEL">EXCEL</option>
          <option value="XML">XML</option>
        </select>
      </div>
      <FieldList
        fields={fields}
        handleFieldChange={handleFieldChange}
        handleAddField={handleAddField}
        handleRemoveField={handleRemoveField}
        errors={errors}
      />
      <div className="button-group">
        <button type="button" className="generate-button" onClick={generateInsertStatements}>Generate Output</button>
        <button type="button" className="export-button" onClick={exportData}>Export Data</button>
      </div>
    </form>
  );
}

export default TableForm;
