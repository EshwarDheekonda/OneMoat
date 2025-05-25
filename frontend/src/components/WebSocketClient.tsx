import React from 'react';
import { useDispatch } from 'react-redux';
import { addFiling } from '../store/filingsSlice';
import { addPrediction } from '../store/predictionsSlice';
import { Filing, Prediction } from '../types';

interface WebSocketClientProps {
  ticker: string;
}

const WebSocketClient: React.FC<WebSocketClientProps> = ({ ticker }) => {
  const dispatch = useDispatch();
  const [ws, setWs] = React.useState<WebSocket | null>(null);
  const [connected, setConnected] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const connect = React.useCallback(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/${ticker}`);

    websocket.onopen = () => {
      setConnected(true);
      setError(null);
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleNewData(data);
      } catch (e) {
        console.error('Error parsing WebSocket data:', e);
      }
    };

    websocket.onerror = (error) => {
      setError('WebSocket error occurred');
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      setConnected(false);
      setError('WebSocket connection closed');
      // Attempt to reconnect after 5 seconds
      setTimeout(connect, 5000);
    };

    setWs(websocket);
  }, [ticker]);

  const handleNewData = React.useCallback((data: any) => {
    // Handle new filing data
    if (data.filing_date) {
      dispatch(addFiling({
        ticker,
        filing_date: data.filing_date,
        filing_type: data.filing_type,
        sentiment: data.sentiment,
        key_metrics: data.key_metrics,
        financial_values: data.financial_values,
        confidence: data.confidence,
        timestamp: data.timestamp
      }));

      // If there's a price prediction, dispatch it
      if (data.predicted_change) {
        dispatch(addPrediction({
          ticker,
          prediction_date: data.filing_date,
          predicted_change: data.predicted_change,
          confidence: data.confidence,
          support_metrics: data.support_metrics,
          timestamp: data.timestamp
        }));
      }
    }
  }, [dispatch, ticker]);

  React.useEffect(() => {
    connect();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [connect, ws]);

  return (
    <div className="websocket-status">
      <div className={`status-dot ${connected ? 'connected' : 'disconnected'}`} />
      <span>{connected ? 'Connected' : error || 'Disconnected'}</span>
    </div>
  );
};

export default WebSocketClient;
