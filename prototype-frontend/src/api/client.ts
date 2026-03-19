import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export class NetworkInsightAPI {
  private client: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Network management
  async uploadNetwork(file: File, name?: string, metadata?: Record<string, any>): Promise<{ network_id: string; nodes_count: number; edges_count: number }> {
    const formData = new FormData();
    formData.append('file', file);
    if (name) formData.append('name', name);
    if (metadata) formData.append('metadata', JSON.stringify(metadata));

    const response = await this.client.post('/networks/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async getNetwork(networkId: string) {
    const response = await this.client.get(`/networks/${networkId}`);
    return response.data;
  }

  async deleteNetwork(networkId: string): Promise<void> {
    await this.client.delete(`/networks/${networkId}`);
  }

  async getNodes(networkId: string, options?: { limit?: number; offset?: number; min_degree?: number; max_degree?: number }) {
    const response = await this.client.get(`/networks/${networkId}/nodes`, { params: options });
    return response.data;
  }

  async getEdges(networkId: string, options?: { limit?: number; offset?: number }) {
    const response = await this.client.get(`/networks/${networkId}/edges`, { params: options });
    return response.data;
  }

  // Analysis
  async analyzeNetwork(networkId: string, options?: { metrics?: string[]; detect_communities?: boolean; cache?: boolean }) {
    const response = await this.client.post(`/networks/${networkId}/analyze`, options);
    return response.data;
  }

  async getCommunities(networkId: string) {
    const response = await this.client.get(`/networks/${networkId}/communities`);
    return response.data;
  }

  async getInsights(networkId: string) {
    const response = await this.client.get(`/networks/${networkId}/insights`);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new NetworkInsightAPI();
