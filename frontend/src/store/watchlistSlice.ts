import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface WatchlistState {
  tickers: string[];
  loading: boolean;
  error: string | null;
}

const initialState: WatchlistState = {
  tickers: [],
  loading: false,
  error: null,
};

const watchlistSlice = createSlice({
  name: 'watchlist',
  initialState,
  reducers: {
    addTicker: (state, action: PayloadAction<string>) => {
      if (!state.tickers.includes(action.payload)) {
        state.tickers.push(action.payload);
      }
    },
    removeTicker: (state, action: PayloadAction<string>) => {
      state.tickers = state.tickers.filter(ticker => ticker !== action.payload);
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { addTicker, removeTicker, setLoading, setError } = watchlistSlice.actions;
export default watchlistSlice.reducer;
