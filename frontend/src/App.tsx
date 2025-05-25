import React, { useState } from 'react';
import './App.css';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { filingsReducer } from './store/filingsSlice';
import { predictionsReducer } from './store/predictionsSlice';
import WebSocketClient from './components/WebSocketClient';
import Dashboard from './components/Dashboard';
import Analysis from './components/Analysis';
import Historical from './components/Historical';

// Configure Redux store
const store = configureStore({
  reducer: {
    filings: filingsReducer,
    predictions: predictionsReducer,
  },
});

function App() {
  const [ticker, setTicker] = useState('');

  return (
    <Provider store={store}>
      <Router>
        <div className="App">
          <header className="App-header">
            <h1>OneMoat</h1>
            <p>AI-Powered Stock Market Analysis</p>
            <div className="search-container">
              <input
                type="text"
                placeholder="Enter stock ticker..."
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
              />
              {ticker && (
                <WebSocketClient ticker={ticker} />
              )}
            </div>
          </header>
          <main className="App-main">
            <Routes>
              <Route path="/" element={<Navigate to={`/dashboard/${ticker}`} replace />} />
              <Route
                path="/dashboard/:ticker"
                element={<Dashboard />}
              />
              <Route
                path="/analysis/:ticker"
                element={<Analysis />}
              />
              <Route
                path="/historical/:ticker"
                element={<Historical />}
              />
            </Routes>
          </main>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
