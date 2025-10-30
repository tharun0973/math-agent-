// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  SOLVE: `${API_BASE_URL}/solve`,
  SOLVE_STREAM: `${API_BASE_URL}/solve/stream`,
  HEALTH: `${API_BASE_URL}/health`,
};

export default API_BASE_URL;

