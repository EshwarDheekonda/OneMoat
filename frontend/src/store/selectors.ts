import { RootState } from './store';
import { Filing, Prediction } from '../types';

export const selectFilings = (ticker: string) => (state: RootState): Filing[] => {
  return state.filings.filings.filter(f => f.ticker === ticker);
};

export const selectPredictions = (ticker: string) => (state: RootState): Prediction[] => {
  return state.predictions.predictions.filter(p => p.ticker === ticker);
};

export const selectLatestFiling = (ticker: string) => (state: RootState): Filing | null => {
  const filings = selectFilings(ticker)(state);
  return filings.length > 0 ? filings[0] : null;
};

export const selectLatestPrediction = (ticker: string) => (state: RootState): Prediction | null => {
  const predictions = selectPredictions(ticker)(state);
  return predictions.length > 0 ? predictions[0] : null;
};
