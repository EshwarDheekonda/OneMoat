from typing import Dict, List, Optional
from pydantic import BaseModel

class FilingAnalysis(BaseModel):
    ticker: str
    filing_date: str
    sentiment: Dict[str, float]
    key_metrics: Dict[str, List[Dict]]
    financial_values: Dict[str, List[str]]
    structure: Dict[str, List[str]]
    dates: List[str]
    confidence: float
    predicted_price_change: float
    key_points: List[str]

class PricePrediction(BaseModel):
    ticker: str
    filing_date: str
    predicted_change: float
    confidence: float
    support_metrics: List[str]

class AnalysisRequest(BaseModel):
    ticker: str
    filing_type: str
    filing_date: str
    content: str
    historical_data: Optional[List[Dict]] = None
