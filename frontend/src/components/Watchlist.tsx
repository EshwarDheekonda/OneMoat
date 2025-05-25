import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { selectFilings, selectPredictions } from '../store/selectors';
import { addTicker, removeTicker } from '../store/watchlistSlice';
import PriceChart from './visualizations/PriceChart';
import SentimentChart from './visualizations/SentimentChart';

const Watchlist: React.FC = () => {
  const dispatch = useDispatch();
  const tickers = useSelector((state: any) => state.watchlist.tickers);
  
  const handleAddTicker = (ticker: string) => {
    dispatch(addTicker(ticker.toUpperCase()));
  };

  const handleRemoveTicker = (ticker: string) => {
    dispatch(removeTicker(ticker));
  };

  return (
    <div className="watchlist">
      <h2>Watchlist</h2>
      
      <div className="add-ticker">
        <input
          type="text"
          placeholder="Add ticker..."
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              const ticker = e.currentTarget.value.trim();
              if (ticker) {
                handleAddTicker(ticker);
                e.currentTarget.value = '';
              }
            }
          }}
        />
      </div>

      <div className="ticker-grid">
        {tickers.map((ticker: string) => (
          <div key={ticker} className="ticker-card">
            <div className="ticker-header">
              <h3>{ticker}</h3>
              <button onClick={() => handleRemoveTicker(ticker)}>Remove</button>
            </div>
            
            <div className="ticker-content">
              <PriceChart ticker={ticker} />
              <SentimentChart ticker={ticker} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Watchlist;
