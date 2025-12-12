import axios from 'axios';

const API_BASE_URL = '/api';

export interface PredictRequest {
  text: string;
  clean?: boolean;
  mode?: string;
}

export interface PredictResponse {
  prediction: string;
  confidence: number;
  probability_fake: number;
  probability_real: number;
  proba: [number, number];
  individual_predictions: Record<string, any>;
  models_used: string[];
  rule_based_analysis?: {
    fake_score: number;
    real_score: number;
  };
  cached: boolean;
}

export interface BatchPredictRequest {
  texts: string[];
  clean?: boolean;
}

export interface BatchPredictResponse {
  predictions: string[];
  confidences: number[];
  probas: [number, number][];
}

export interface HealthResponse {
  ok: boolean;
  ensemble_loaded: boolean;
  models_available: string[];
  model_dir: string;
  cache_stats: any;
}

export interface ExplainRequest {
  text: string;
  model_name?: string;
}

export interface ExplainResponse {
  explanation: [string, number][];
  prediction: string;
  probability_fake: number;
  probability_real: number;
}

export const api = {
  async predict(data: PredictRequest): Promise<PredictResponse> {
    const response = await axios.post<PredictResponse>(`${API_BASE_URL}/predict`, data);
    return response.data;
  },

  async batchPredict(data: BatchPredictRequest): Promise<BatchPredictResponse> {
    const response = await axios.post<BatchPredictResponse>(`${API_BASE_URL}/batch`, data);
    return response.data;
  },

  async health(): Promise<HealthResponse> {
    const response = await axios.get<HealthResponse>(`${API_BASE_URL}/health`);
    return response.data;
  },

  async detectVisual(image: File, event?: string, location?: string, date?: string) {
    const formData = new FormData();
    formData.append('image', image);
    if (event) formData.append('event', event);
    if (location) formData.append('location', location);
    if (date) formData.append('date', date);

    const response = await axios.post(`${API_BASE_URL}/detect-visual`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async explain(data: ExplainRequest): Promise<ExplainResponse> {
    const response = await axios.post<ExplainResponse>(`${API_BASE_URL}/explain`, data);
    return response.data;
  },
};
