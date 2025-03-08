import axios from 'axios';
const API_URL = 'http://127.0.0.1:5000';
// const API_URL = 'http://localhost:5001/';
// const API_URL = "http://172.17.0.2:5000/";


export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post(`${API_URL}/upload-resume`, formData);
};

export const uploadJobDescription = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post(`${API_URL}/upload-job-description`, formData);
};

export const rankResumes = async () => {
  return axios.post(`${API_URL}/rank-resumes`);
};
