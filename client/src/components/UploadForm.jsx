import React, { useState } from 'react';
import { uploadVideo } from '../services/api';

const UploadForm = ({ onUploadComplete }) => {
  const [videoFile, setVideoFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!videoFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      const response = await uploadVideo(formData);
      onUploadComplete(response.data.analysis);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button type="submit" disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Video'}
      </button>
    </form>
  );
};

export default UploadForm;
