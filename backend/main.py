from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uvicorn
from typing import List, Dict, Optional
import os
import json
from datetime import datetime
from models import AnalysisRequest, FilingAnalysis, PricePrediction
from models.filing_analysis.filing_analyzer import FilingAnalyzer
from models.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
from models.price_prediction.price_predictor import PricePredictor
from realtime import router as realtime_router

app = FastAPI(title="OneMoat Stock Analysis API")

# Initialize models
filing_analyzer = FilingAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
price_predictor = PricePredictor()

# Include real-time routes
app.include_router(realtime_router)

def get_filing_analyzer():
    return filing_analyzer

def get_sentiment_analyzer():
    return sentiment_analyzer

def get_price_predictor():
    return price_predictor

@app.post("/analyze-filing/")
async def analyze_filing(
    request: AnalysisRequest,
    filing_analyzer: FilingAnalyzer = Depends(get_filing_analyzer),
    sentiment_analyzer: SentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Comprehensive analysis of company filing
    """
    try:
        # Analyze filing content
        filing_analysis = filing_analyzer.analyze_filing(request.content)
        
        # Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze_filing(request.content)
        
        # Extract key points
        key_points = []
        if filing_analysis["key_metrics"]["revenue"]:
            key_points.append("Revenue metrics identified in filing")
        if filing_analysis["key_metrics"]["profit"]:
            key_points.append("Profit metrics identified in filing")
        
        # Calculate predicted price change based on analysis
        sentiment_score = sentiment_result["sentiment_score"]
        confidence = sentiment_result["confidence"]
        
        # Simple prediction model (to be replaced with more sophisticated ML model)
        predicted_change = sentiment_score * 100  # Convert to percentage
        
        # Create response
        response = FilingAnalysis(
            ticker=request.ticker,
            filing_date=request.filing_date,
            sentiment=sentiment_result["detailed_scores"],
            key_metrics=filing_analysis["key_metrics"],
            financial_values=filing_analysis["financial_values"],
            structure=filing_analysis["structure"],
            dates=filing_analysis["dates"],
            confidence=confidence,
            predicted_price_change=predicted_change,
            key_points=key_points
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-price/")
async def predict_price(
    request: AnalysisRequest,
    price_predictor: PricePredictor = Depends(get_price_predictor)
):
    """
    Predict stock price change based on filing
    """
    try:
        # Get sentiment analysis
        sentiment_result = sentiment_analyzer.analyze_filing(request.content)
        
        # Extract key metrics for prediction
        support_metrics = []
        if sentiment_result["confidence"] > 0.8:
            support_metrics.append("High confidence in sentiment")
        
        # Get historical data for prediction
        historical_data = await get_historical_data(request.ticker)
        
        # Make prediction using the trained model
        predicted_change = price_predictor.predict(historical_data)
        
        # Get support metrics from prediction
        support_metrics = []
        if abs(predicted_change) > 2:  # Threshold for significant change
            support_metrics.append("Significant price movement predicted")
        if sentiment_result["confidence"] > 0.8:
            support_metrics.append("High confidence in sentiment")
        
        return PricePrediction(
            ticker=request.ticker,
            filing_date=request.filing_date,
            predicted_change=predicted_change,
            confidence=sentiment_result["confidence"],
            support_metrics=support_metrics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
