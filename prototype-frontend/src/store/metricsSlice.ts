import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface NodeMetrics {
  [nodeId: string]: {
    degree_centrality: number;
    betweenness_centrality: number;
    closeness_centrality: number;
    eigenvector_centrality: number;
    pagerank: number;
    community_id: number;
    is_hub: boolean;
  };
}

interface MetricsState {
  byNetworkId: Record<string, NodeMetrics>;
  loading: false | string;  // false or network ID being loaded
  cache: Record<string, { timestamp: number }>;
}

const initialState: MetricsState = {
  byNetworkId: {},
  loading: false,
  cache: {},
};

export const metricsSlice = createSlice({
  name: 'metrics',
  initialState,
  reducers: {
    setMetricsLoading: (state, action: PayloadAction<string | false>) => {
      state.loading = action.payload;
    },
    
    setMetrics: (state, action: PayloadAction<{ networkId: string; metrics: NodeMetrics }>) => {
      state.byNetworkId[action.payload.networkId] = action.payload.metrics;
      state.cache[action.payload.networkId] = { timestamp: Date.now() };
      state.loading = false;
    },
    
    clearMetrics: (state, action: PayloadAction<string>) => {
      delete state.byNetworkId[action.payload];
      delete state.cache[action.payload];
    },
  },
});

export const { setMetricsLoading, setMetrics, clearMetrics } = metricsSlice.actions;
export default metricsSlice.reducer;
