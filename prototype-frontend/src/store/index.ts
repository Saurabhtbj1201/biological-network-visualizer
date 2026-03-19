import { configureStore } from '@reduxjs/toolkit';
import networkReducer from './networkSlice';
import metricsReducer from './metricsSlice';
import filtersReducer from './filtersSlice';

export const store = configureStore({
  reducer: {
    networks: networkReducer,
    metrics: metricsReducer,
    filters: filtersReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
