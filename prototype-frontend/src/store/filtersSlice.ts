import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface FilterState {
  degree: { min: number; max: number };
  centrality: { metric: string; threshold: number };
  communities: { selected: number[] };
  weight: { min: number; max: number };
  activeFilters: string[];
}

interface FiltersState {
  byNetworkId: Record<string, FilterState>;
}

const defaultFilters: FilterState = {
  degree: { min: 0, max: 100 },
  centrality: { metric: 'betweenness', threshold: 0 },
  communities: { selected: [] },
  weight: { min: 0, max: 1 },
  activeFilters: [],
};

const initialState: FiltersState = {
  byNetworkId: {},
};

export const filtersSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {
    initializeFilters: (state, action: PayloadAction<string>) => {
      if (!state.byNetworkId[action.payload]) {
        state.byNetworkId[action.payload] = { ...defaultFilters };
      }
    },
    
    setDegreeFilter: (state, action: PayloadAction<{ networkId: string; min: number; max: number }>) => {
      if (!state.byNetworkId[action.payload.networkId]) {
        state.byNetworkId[action.payload.networkId] = { ...defaultFilters };
      }
      state.byNetworkId[action.payload.networkId].degree = {
        min: action.payload.min,
        max: action.payload.max,
      };
      state.byNetworkId[action.payload.networkId].activeFilters.push('degree');
    },
    
    setCentralityFilter: (state, action: PayloadAction<{ networkId: string; metric: string; threshold: number }>) => {
      if (!state.byNetworkId[action.payload.networkId]) {
        state.byNetworkId[action.payload.networkId] = { ...defaultFilters };
      }
      state.byNetworkId[action.payload.networkId].centrality = {
        metric: action.payload.metric,
        threshold: action.payload.threshold,
      };
      state.byNetworkId[action.payload.networkId].activeFilters.push('centrality');
    },
    
    clearFilters: (state, action: PayloadAction<string>) => {
      state.byNetworkId[action.payload] = { ...defaultFilters };
    },
  },
});

export const { initializeFilters, setDegreeFilter, setCentralityFilter, clearFilters } = filtersSlice.actions;
export default filtersSlice.reducer;
