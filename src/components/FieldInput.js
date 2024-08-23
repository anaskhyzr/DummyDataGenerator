import React from "react";
import "./FieldInput.css";

function FieldInput({
  field,
  index,
  handleFieldChange,
  handleRemoveField,
  errors,
}) {
  return (
    <div className="field-input">
      <input
        type="text"
        name="fieldName"
        value={field.fieldName}
        onChange={(event) => handleFieldChange(index, event)}
        placeholder="Field Name"
        className="input-field"
      />
      {errors[`fieldName_${index}`] && (
        <div className="error-message">{errors[`fieldName_${index}`]}</div>
      )}
      <select
        name="dataType"
        value={field.dataType}
        onChange={(event) => handleFieldChange(index, event)}
        className="select-field"
      >
        <option value="">Data Type</option>
        <option value="VARCHAR">VARCHAR</option>
        <option value="INT">INT</option>
        <option value="NAME">NAME</option>
        <option value="FIRST NAME">FIRST NAME</option>
        <option value="LAST NAME">LAST NAME</option>
        <option value="USERNAME">USERNAME</option>
        <option value="EMAIL">EMAIL</option>
        <option value="PHONE">PHONE</option>
        <option value="ADDRESS">ADDRESS</option>
        <option value="ENUM">ENUM</option>
        <option value="AGE">AGE</option>
        <option value="DOB">DOB</option>
        <option value="CITY">CITY</option>
        <option value="COUNTRY">COUNTRY</option>
        <option value="FLOAT">FLOAT</option>
        <option value="DOUBLE">DOUBLE</option>
        <option value="DECIMAL">DECIMAL</option>
        <option value="DATE">DATE</option>
        <option value="DATETIME">DATETIME</option>
        <option value="TIMESTAMP">TIMESTAMP</option>
        <option value="YEAR">YEAR</option>
        <option value="TINYINT">TINYINT</option>
        <option value="SMALLINT">SMALLINT</option>
        <option value="BIGINT">BIGINT</option>
        <option value="MEDIUMINT">MEDIUMINT</option>
        <option value="BOOLEAN">BOOLEAN</option>
        <option value="BLOB">BLOB</option>
        <option value="TEXT">TEXT</option>
        {/* Add other options */}
      </select>
      {errors[`dataType_${index}`] && (
        <div className="error-message">{errors[`dataType_${index}`]}</div>
      )}
      {field.dataType === "ENUM" && (
        <input
          type="text"
          name="enumValue"
          value={field.enumValue}
          onChange={(event) => handleFieldChange(index, event)}
          placeholder="ENUM Value (comma-separated)"
          className="input-field"
        />
      )}
      {errors[`enumValue_${index}`] && (
        <div className="error-message">{errors[`enumValue_${index}`]}</div>
      )}
      <button
        type="button"
        className="remove-button"
        onClick={() => handleRemoveField(index)}
      >
        Remove
      </button>
    </div>
  );
}

export default FieldInput;
