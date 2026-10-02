import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const chatService = {
  sendMessage: async (query, session_id = "default") => {
    const response = await api.post('/chat/', { query, session_id });
    return response.data;
  },
};

export const documentService = {
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  getDocuments: async () => {
    const response = await api.get('/documents/');
    return response.data;
  },
  deleteDocument: async (id) => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },
  summarizeDocument: async (id) => {
    const response = await api.post(`/documents/${id}/summarize`);
    return response.data;
  }
};

export const databaseService = {
  getSchema: async () => {
    const response = await api.get('/database/schema');
    return response.data;
  }
};
