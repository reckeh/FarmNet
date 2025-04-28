import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'api', // Proxy setup in Vite config
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Set to true if you need to send cookies or other credentials
});

export default apiClient;
