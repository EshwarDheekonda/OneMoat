import React from 'react';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { selectFilings, selectPredictions } from '../store/selectors';
import { Filing, Prediction } from '../types';

const Dashboard: React.FC = () => {
  const { ticker } = useParams();
  const filings = useSelector(selectFilings(ticker || ''));
  const predictions = useSelector(selectPredictions(ticker || ''));

  return (
    <div className="dashboard">
      <h2>{ticker} Dashboard</h2>
      
      <div className="predictions">
        <h3>Latest Predictions</h3>
        {predictions.length > 0 ? (
          predictions.map((prediction, index) => (
            <div key={index} className="prediction-card">
              <div className="prediction-date">
                {new Date(prediction.prediction_date).toLocaleDateString()}
              </div>
              <div className={`prediction-change ${prediction.predicted_change >= 0 ? 'positive' : 'negative'}`}>
                {prediction.predicted_change.toFixed(2)}%
              </div>
              <div className="confidence">Confidence: {prediction.confidence.toFixed(2)}</div>
              <div className="support-metrics">
                {prediction.support_metrics.map((metric, i) => (
                  <span key={i}>{metric}</span>
                ))}
              </div>
            </div>
          ))
        ) : (
          <div>No predictions available</div>
        )}
      </div>

      <div className="filings">
        <h3>Recent Filings</h3>
        {filings.length > 0 ? (
          filings.map((filing, index) => (
            <div key={index} className="filing-card">
              <div className="filing-date">
                {new Date(filing.filing_date).toLocaleDateString()}
              </div>
              <div className="filing-type">{filing.filing_type}</div>
              <div className="sentiment">
                Sentiment: {filing.sentiment.positive.toFixed(2)}
              </div>
              <div className="confidence">Confidence: {filing.confidence.toFixed(2)}</div>
            </div>
          ))
        ) : (
          <div>No filings available</div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
