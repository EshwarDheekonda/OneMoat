# OneMoat - AI-Powered Stock Market Analysis Platform

OneMoat is an advanced stock market analysis platform that uses AI to analyze company filings and predict their impact on stock prices with high accuracy.

## Features

- Real-time company filing analysis
- AI-driven sentiment analysis and prediction
- Interactive visualization of filing impact
- Historical performance tracking
- Customizable watchlists
- Daily filing updates and alerts

## Tech Stack

- Frontend: React + TypeScript + TailwindCSS
- Backend: Python + FastAPI
- AI Models: TensorFlow + Transformers
- Data Processing: Pandas + NumPy

## Setup Instructions

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Run the development servers:
   ```bash
   # Backend
   uvicorn app.main:app --reload
   
   # Frontend
   cd frontend
   npm run dev
   ```

## Project Structure

```
OneMoat/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── models/           # AI models and training scripts
├── data/             # Data storage and processing
└── tests/            # Test files
```
