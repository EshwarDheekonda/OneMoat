import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useSelector } from 'react-redux';
import { selectFilings } from '../../store/selectors';

interface SentimentChartProps {
  ticker: string;
}

const SentimentChart: React.FC<SentimentChartProps> = ({ ticker }) => {
  const filings = useSelector(selectFilings(ticker));
  
  const chartData = filings.map((filing, index) => ({
    date: new Date(filing.filing_date).toLocaleDateString(),
    positive: filing.sentiment.positive * 100,
    negative: filing.sentiment.negative * 100,
    neutral: filing.sentiment.neutral * 100,
  }));

  return (
    <div className="sentiment-chart">
      <h3>Sentiment Analysis</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="positive" name="Positive" fill="#8884d8" />
          <Bar dataKey="negative" name="Negative" fill="#82ca9d" />
          <Bar dataKey="neutral" name="Neutral" fill="#ffc658" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SentimentChart;
