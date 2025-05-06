import axios from 'axios';
import { QueryResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to inject API key
api.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('apiKey');
  if (apiKey) {
    config.headers['Authorization'] = `Bearer ${apiKey}`;
  }
  return config;
});

export const ragApi = {
  async query(query: string, maxSections?: number, maxDocs?: number): Promise<QueryResponse> {
    const response = await api.post('/api/v1/rag/query', {
      query,
      max_sections: maxSections,
      max_docs: maxDocs,
    });
    return response.data;
  },

  async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
    const response = await api.get('/api/v1/rag/health');
    return response.data;
  },
}; 