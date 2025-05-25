export interface Prediction {
  ticker: string;
  prediction_date: string;
  predicted_change: number;
  confidence: number;
  support_metrics: string[];
  timestamp: string;
}
