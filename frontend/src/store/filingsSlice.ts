import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Filing } from '../types/filingTypes';

interface FilingsState {
  filings: Filing[];
  loading: boolean;
  error: string | null;
}

const initialState: FilingsState = {
  filings: [],
  loading: false,
  error: null,
};

const filingsSlice = createSlice({
  name: 'filings',
  initialState,
  reducers: {
    addFiling: (state, action: PayloadAction<Filing>) => {
      state.filings.push(action.payload);
      state.error = null;
    },
    updateFiling: (state, action: PayloadAction<Filing>) => {
      const index = state.filings.findIndex(
        (f) => f.ticker === action.payload.ticker && f.filing_date === action.payload.filing_date
      );
      if (index !== -1) {
        state.filings[index] = action.payload;
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { addFiling, updateFiling, setLoading, setError } = filingsSlice.actions;
export default filingsSlice.reducer;
