import { CensusDocument } from '@/components/CensusResults';

export interface SearchParams {
  year?: string;
  country?: string;
  state?: string;
  keyword?: string;
  max_results?: number;
}

export interface SearchResponse {
  results: CensusDocument[];
  total: number;
  searchTime: number;
  query: string;
}

export interface DownloadResponse {
  download_url: string;
  filename: string;
  size_mb: number;
}

export class CensusAPI {
  private baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async search(params: SearchParams): Promise<SearchResponse> {
    // Filter out "all-" values
    const cleanParams = {
      year: params.year === 'all-years' ? undefined : params.year,
      country: params.country === 'all-countries' ? undefined : params.country,
      state: params.state === 'all-states' ? undefined : params.state,
      keyword: params.keyword || undefined,
      max_results: params.max_results || 20,
    };

    return this.makeRequest<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify(cleanParams),
    });
  }

  async downloadDocument(documentId: string): Promise<DownloadResponse> {
    return this.makeRequest<DownloadResponse>(`/download/${documentId}`);
  }

  async downloadBulk(documentIds: string[]): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/download/bulk`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ document_ids: documentIds }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.blob();
  }

  async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
    return this.makeRequest('/health');
  }
}

// Create a singleton instance
export const censusAPI = new CensusAPI();
