import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Prediction } from '../types/predictionTypes';

interface PredictionsState {
  predictions: Prediction[];
  loading: boolean;
  error: string | null;
}

const initialState: PredictionsState = {
  predictions: [],
  loading: false,
  error: null,
};

const predictionsSlice = createSlice({
  name: 'predictions',
  initialState,
  reducers: {
    addPrediction: (state, action: PayloadAction<Prediction>) => {
      state.predictions.push(action.payload);
      state.error = null;
    },
    updatePrediction: (state, action: PayloadAction<Prediction>) => {
      const index = state.predictions.findIndex(
        (p) => p.ticker === action.payload.ticker && p.prediction_date === action.payload.prediction_date
      );
      if (index !== -1) {
        state.predictions[index] = action.payload;
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

export const { addPrediction, updatePrediction, setLoading, setError } = predictionsSlice.actions;
export default predictionsSlice.reducer;
