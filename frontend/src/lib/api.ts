import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const feedbackAPI = {
  uploadCSV: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/feedback/upload-csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  list: async (params?: { platform?: string; sentiment?: string }) => {
    const response = await api.get('/feedback/', { params });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/feedback/stats');
    return response.data;
  },
};

export const analysisAPI = {
  cluster: async (days: number = 7) => {
    const response = await api.post('/analysis/cluster', null, {
      params: { days },
    });
    return response.data;
  },

  getPriorities: async (limit: number = 10) => {
    const response = await api.get('/analysis/priorities', {
      params: { limit },
    });
    return response.data;
  },

  getDashboard: async () => {
    const response = await api.get('/analysis/dashboard');
    return response.data;
  },

  getIssueDetails: async (issueId: number) => {
    const response = await api.get(`/analysis/issue/${issueId}`);
    return response.data;
  },
};

export const integrationsAPI = {
  connectPlayStore: async (config: any) => {
    const response = await api.post('/integrations/playstore/connect', config);
    return response.data;
  },

  syncPlayStore: async (days: number = 7) => {
    const response = await api.post('/integrations/playstore/sync', null, {
      params: { days },
    });
    return response.data;
  },
};