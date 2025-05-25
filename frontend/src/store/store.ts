import { configureStore } from '@reduxjs/toolkit';
import filingsReducer from './filingsSlice';
import predictionsReducer from './predictionsSlice';
import watchlistReducer from './watchlistSlice';

export const store = configureStore({
  reducer: {
    filings: filingsReducer,
    predictions: predictionsReducer,
    watchlist: watchlistReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
