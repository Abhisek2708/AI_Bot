import React, { useState } from 'react';
import axios from 'axios';

const UploadInformation = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.message);
      setError('');
    } catch (error) {
      setError('File upload failed.');
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Information</h2>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {message && <div className="message">{message}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default UploadInformation;
