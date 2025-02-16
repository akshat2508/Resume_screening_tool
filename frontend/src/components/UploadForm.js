

import React, { useState } from 'react';
import { uploadResume, uploadJobDescription, rankResumes } from '../services/api';
import '../App.css';

const UploadForm = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescFile, setJobDescFile] = useState(null);
  const [ranking, setRanking] = useState([]);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const handleResumeChange = (e) => setResumeFile(e.target.files[0]);
  const handleJobDescChange = (e) => setJobDescFile(e.target.files[0]);

  const handleUploadResume = async () => {
    if (!resumeFile) return;
    try {
      const response = await uploadResume(resumeFile);
      setMessage(response.data.message);
      setError(null);
    } catch (err) {
      console.error('Error uploading resume:', err); 
    }
  };

  const handleUploadJobDescription = async () => {
    if (!jobDescFile) return;
    try {
      const response = await uploadJobDescription(jobDescFile);
      setMessage(response.data.message);
      setError(null);
    } catch (err) {
      console.error('Error uploading job description:', err); 
    }
  };

  const handleRankResumes = async () => {
    try {
      const response = await rankResumes();
      setRanking(response.data.ranked_resumes);
      setError(null);
    } catch (err) {
      console.error('Error ranking resumes:', err); 
    }
  };

  // Function to assign special icons
  const getRankIcon = (rank) => {
    if (rank === 1) return '🏆'; // Gold trophy for #1
    if (rank === 2) return '🥈'; // Silver medal for #2
    if (rank === 3) return '🥉'; // Bronze medal for #3
    return '📄'; // Default icon for others
  };

  return (
    <div className="app-container">
      {/* Left Panel - Upload Section */}
      <div className="upload-section">
        <h1 className="header">RESUME SCREENING TOOL</h1>

        <div className="upload-box">
          <p>📄 Upload Job Description</p>
          <input type="file" id="jobDescUpload" onChange={handleJobDescChange} style={{ display: "none" }} />
          <label htmlFor="jobDescUpload" className="file-label">Choose File</label>
          {jobDescFile && <p className="file-name">📂 {jobDescFile.name}</p>}
          <button className="upload-btn" onClick={handleUploadJobDescription}>Upload</button>
        </div>

        <div className="upload-box">
          <p>📑 Upload Your Resume</p>
          <input type="file" id="resumeUpload" onChange={handleResumeChange} style={{ display: "none" }} />
          <label htmlFor="resumeUpload" className="file-label">Choose File</label>
          {resumeFile && <p className="file-name">📂 {resumeFile.name}</p>}
          <button className="upload-btn" onClick={handleUploadResume}>Upload</button>
        </div>

        <button className="rank-btn" onClick={handleRankResumes}>Rank Resumes</button>
      </div>

      {/* Right Panel - Ranking Section */}
      <div className="ranking-section">
        <h2>Ranked Resumes</h2>
        {ranking.length > 0 ? (
          ranking.map(({ rank, name, similarity }, index) => (
            <div key={index} className={`resume-card ${rank === 1 ? 'top-ranked' : ''}`}>
              <div className="resume-icon">{getRankIcon(rank)}</div> {/* Custom Icon */}
              <div className="resume-info">
                <p><strong>{name}</strong></p>
                <p>Rank: #{rank} | {similarity}% match</p>
              </div>
            </div>
          ))
        ) : (
          <p className="no-ranking">No rankings available</p>
        )}
      </div>

      {/* Message Display */}
      {message && <p className="message success">{message}</p>}
      {error && <p className="message error">{error}</p>}
    </div>
  );
};

export default UploadForm;
