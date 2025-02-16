import React, { useState } from 'react';
import { uploadResume, uploadJobDescription, rankResumes } from '../services/api';

const UploadForm = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescFile, setJobDescFile] = useState(null);
  const [ranking, setRanking] = useState([]);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null); // For success messages

  // Handle resume file change
  const handleResumeChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  // Handle job description file change
  const handleJobDescChange = (e) => {
    setJobDescFile(e.target.files[0]);
  };

  // Upload resume to Flask API
  const handleUploadResume = async () => {
    if (!resumeFile) return;
    try {
      const response = await uploadResume(resumeFile);
      setMessage(response.data.message || 'Resume uploaded successfully'); // Show success message
      setError(null); // Clear previous error
    } catch (err) {
      console.error(err);
      setError('Failed to upload resume');
      setMessage(null); // Clear success message if error occurs
    }
  };

  // Upload job description to Flask API
  const handleUploadJobDescription = async () => {
    if (!jobDescFile) return;
    try {
      const response = await uploadJobDescription(jobDescFile);
      setMessage(response.data.message || 'Job description uploaded successfully'); // Show success message
      setError(null); // Clear previous error
    } catch (err) {
      console.error(err);
      setError('Failed to upload job description');
      setMessage(null); // Clear success message if error occurs
    }
  };

  // Rank resumes based on job description
  const handleRankResumes = async () => {
    try {
      const response = await rankResumes();
      setRanking(response.data); // Store ranking data in the state
      setError(null); // Clear previous error
    } catch (err) {
      console.error(err);
      setError('Failed to rank resumes');
      setMessage(null); // Clear success message if error occurs
    }
  };

  return (
    <div>
      <h1>Upload Resume and Job Description</h1>

      {/* Resume upload */}
      <div>
        <input type="file" onChange={handleResumeChange} />
        <button onClick={handleUploadResume}>Upload Resume</button>
      </div>

      {/* Job description upload */}
      <div>
        <input type="file" onChange={handleJobDescChange} />
        <button onClick={handleUploadJobDescription}>Upload Job Description</button>
      </div>

      {/* Rank resumes */}
      <div>
        <button onClick={handleRankResumes}>Rank Resumes</button>
      </div>

      {/* Display messages */}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Display ranked resumes */}
      <div>
        <h2>Ranked Resumes:</h2>
        <ul>
          {ranking.length > 0 ? (
            ranking.map((rank, index) => (
              <li key={index}>
                {rank.rank}. {rank.name} - {rank.similarity}% similarity
              </li>
            ))
          ) : (
            <p>No rankings available</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default UploadForm;
