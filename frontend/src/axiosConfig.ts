import axios from 'axios';

// Set the base URL for axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Optional: If you need to send credentials (e.g., cookies)
});

export default api;
