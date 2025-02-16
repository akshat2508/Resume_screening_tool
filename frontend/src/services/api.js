// // src/services/api.js
// import axios from 'axios';

// const API_BASE_URL = 'http://127.0.0.1:5000'; // Ensure this is set to your Flask backend URL
//  // Your Flask backend API URL

// // Function to upload a resume
// export const uploadResume = (file) => {
//   const formData = new FormData();
//   formData.append('file', file);

//   return axios.post(`${API_BASE_URL}/upload-resume`, formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   });
// };

// // Function to upload a job description
// export const uploadJobDescription = (file) => {
//   const formData = new FormData();
//   formData.append('file', file);

//   return axios.post(`${API_BASE_URL}/upload-job-description`, formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   });
// };

// // Function to rank resumes based on the uploaded job description
// export const rankResumes = () => {
//   return axios.get(`${API_BASE_URL}/rank-resumes`);
// };


import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'; // Flask API base URL

// Upload resume to Flask API
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const config = {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  };

  return axios.post(`${API_URL}/upload-resume`, formData, config);
};

// Upload job description to Flask API
export const uploadJobDescription = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const config = {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  };

  return axios.post(`${API_URL}/upload-job-description`, formData, config);
};

// Rank resumes based on the uploaded job description
export const rankResumes = async () => {
  return axios.get(`${API_URL}/rank-resumes`);
};
