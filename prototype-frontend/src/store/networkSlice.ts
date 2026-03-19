"""
Redux store configuration and slices for NetworkInsight frontend.
"""

/**
 * Network slice - manages loaded networks and metadata
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Network {
  id: string;
  name: string;
  format: string;
  nodes_count: number;
  edges_count: number;
  created_at: string;
  status: 'loading' | 'ready' | 'error';
}

interface NetworkState {
  networks: Record<string, Network>;
  currentNetworkId: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: NetworkState = {
  networks: {},
  currentNetworkId: null,
  loading: false,
  error: null,
};

export const networkSlice = createSlice({
  name: 'networks',
  initialState,
  reducers: {
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    
    addNetwork: (state, action: PayloadAction<Network>) => {
      state.networks[action.payload.id] = action.payload;
      state.currentNetworkId = action.payload.id;
      state.loading = false;
    },
    
    setCurrentNetwork: (state, action: PayloadAction<string>) => {
      state.currentNetworkId = action.payload;
    },
    
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.loading = false;
    },
    
    deleteNetwork: (state, action: PayloadAction<string>) => {
      delete state.networks[action.payload];
      if (state.currentNetworkId === action.payload) {
        state.currentNetworkId = null;
      }
    },
  },
});

export const { setLoading, addNetwork, setCurrentNetwork, setError, deleteNetwork } = networkSlice.actions;
export default networkSlice.reducer;
