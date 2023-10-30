// ImageUpload.js
import React, { useState } from 'react';

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [colorGrade, setColorGrade] = useState('');
  const [sizeGrade, setSizeGrade] = useState('');
  const [finalGrade, setFinalGrade] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('image', file);
  
    try {
      const response = await fetch('http://localhost:5003/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        setColorGrade(data.color_grade);
        setSizeGrade(data.size_grade);
        setFinalGrade(data.final_grade);
      } else {
        // Handle errors here
        console.error('Error uploading file:', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };
  

  return (
    <div className="container">
      <header>
        <h1>Coco Grading</h1>
      </header>
      <main>
      <section className="upload-section">
          <label className="upload-button">
            <input type="file" accept=".jpg, .jpeg, .png" onChange={handleFileChange} />
            Choose Image
          </label>
          <br></br>
          <button className="upload-image-button" onClick={handleUpload}>
            Upload Image
          </button>
        </section>
        <section className="results-section">
          {colorGrade && sizeGrade && finalGrade && (
            <div className="grading-results">
              <p>Color Grade: {colorGrade}</p>
              <p>Size Grade: {sizeGrade}</p>
              <br></br>
              <p style={{ fontWeight: 'bold' }}>Final Grade: {finalGrade}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default ImageUpload;
