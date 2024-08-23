import React from 'react';
import './OutputDisplay.css';

function OutputDisplay({ format, output, tableData }) {
  return (
    <div className="output-display">
      {format === 'EXCEL' ? (
        <table className="output-table">
          <thead>
            <tr>
              {tableData.length > 0 && Object.keys(tableData[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, idx) => (
                  <td key={idx}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <textarea
          value={output}
          placeholder="Generated output will appear here..."
          readOnly
          className="output-textarea"
        />
      )}
    </div>
  );
}

export default OutputDisplay;
