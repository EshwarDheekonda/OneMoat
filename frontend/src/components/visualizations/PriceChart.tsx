import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useSelector } from 'react-redux';
import { selectPredictions } from '../../store/selectors';

interface PriceChartProps {
  ticker: string;
}

const PriceChart: React.FC<PriceChartProps> = ({ ticker }) => {
  const predictions = useSelector(selectPredictions(ticker));
  
  const chartData = predictions.map((prediction, index) => ({
    date: new Date(prediction.prediction_date).toLocaleDateString(),
    predictedChange: prediction.predicted_change,
    confidence: prediction.confidence * 100,
  }));

  return (
    <div className="price-chart">
      <h3>Price Prediction History</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="predictedChange"
            name="Predicted Change (%)"
            stroke="#8884d8"
          />
          <Line
            type="monotone"
            dataKey="confidence"
            name="Confidence (%)
            stroke="#82ca9d"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
