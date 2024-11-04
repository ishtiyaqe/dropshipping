import React from 'react';

function TimeComponent({ timestamp }) {
  const date = new Date(timestamp); // Assuming 'timestamp' is a string in the correct format
  
  

  const formattedDate = date.toLocaleString();

  return formattedDate;
}

export default TimeComponent;
