import axios, { AxiosError } from 'axios';
import type { DocumentConfig, Session, GenerateResponse, PreviewResponse, DocumentType, OutputFormat } from '../types';

// Use environment variable for API URL, fallback to relative path for local dev
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string }>) => {
    // Handle specific error cases
    if (error.response) {
      const status = error.response.status;
      const detail = error.response.data?.detail || 'An error occurred';

      if (status === 404) {
        console.error('Resource not found:', detail);
      } else if (status === 400) {
        console.error('Bad request:', detail);
      } else if (status === 500) {
        console.error('Server error:', detail);
      }
    } else if (error.request) {
      console.error('Network error: No response received');
    } else {
      console.error('Request error:', error.message);
    }

    return Promise.reject(error);
  }
);

// Session API
export const sessionApi = {
  create: async (): Promise<Session> => {
    const response = await api.post('/sessions');
    return response.data;
  },

  get: async (sessionId: string): Promise<Session> => {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data;
  },

  updateConfig: async (sessionId: string, config: Partial<DocumentConfig>): Promise<{ status: string; config: DocumentConfig }> => {
    const response = await api.patch(`/sessions/${sessionId}/config`, { config });
    return response.data;
  },

  reset: async (sessionId: string): Promise<{ status: string; config: DocumentConfig }> => {
    const response = await api.post(`/sessions/${sessionId}/reset`);
    return response.data;
  },
};

// Documents API
export const documentsApi = {
  generate: async (
    sessionId: string,
    docTypes: DocumentType[],
    outputFormat: OutputFormat = 'markdown'
  ): Promise<GenerateResponse> => {
    const response = await api.post('/documents/generate', {
      session_id: sessionId,
      doc_types: docTypes,
      output_format: outputFormat,
    });
    return response.data;
  },

  preview: async (
    sessionId: string,
    docType: DocumentType,
    format: OutputFormat = 'markdown'
  ): Promise<PreviewResponse> => {
    const response = await api.get(`/documents/preview/${sessionId}/${docType}`, {
      params: { format },
    });
    return response.data;
  },

  getDownloadUrl: (filename: string): string => {
    return `${API_BASE_URL}/documents/download/${filename}`;
  },

  download: async (filename: string): Promise<Blob> => {
    const response = await api.get(`/documents/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Config API
export const configApi = {
  getDefaults: async (): Promise<DocumentConfig> => {
    const response = await api.get('/config/defaults');
    return response.data;
  },
};

// Health check
export const healthApi = {
  check: async (): Promise<{ status: string; version: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
