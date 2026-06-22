import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const interviewAPI = {
  // Start a new interview session
  startInterview: async (resume, jobDescription) => {
    const response = await api.post('/start-interview', {
      resume,
      job_description: jobDescription,
    });
    return response.data;
  },

  // Submit an answer
  submitAnswer: async (sessionId, answer) => {
    const response = await api.post('/submit-answer', {
      session_id: sessionId,
      answer,
    });
    return response.data;
  },

  // Get session status
  getSessionStatus: async (sessionId) => {
    const response = await api.get(`/session-status/${sessionId}`);
    return response.data;
  },

  // Load example data
  loadExampleData: async () => {
    const response = await api.get('/example-data');
    return response.data;
  },
};

export default api;

// Made with Bob
