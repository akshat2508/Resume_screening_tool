// src/App.js
import React from 'react';
import './App.css';
import UploadForm from './components/UploadForm'; // Import the UploadForm component

function App() {
  return (
    <div className="App">
      <h1>Resume Screening Tool</h1>
      <UploadForm /> {/* Render the UploadForm */}
    </div>
  );
}

export default App;
