import React from 'react';
import FieldInput from './FieldInput';
import './FieldList.css';

function FieldList({ fields, handleFieldChange, handleAddField, handleRemoveField, errors }) {
  return (
    <div className="field-list">
      {fields.map((field, index) => (
        <FieldInput
          key={index}
          field={field}
          index={index}
          handleFieldChange={handleFieldChange}
          handleRemoveField={handleRemoveField}
          errors={errors}
        />
      ))}
      <button type="button" className="add-button" onClick={handleAddField}>Add Field</button>
    </div>
  );
}

export default FieldList;
