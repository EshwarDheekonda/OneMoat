import asyncio
import json
from datetime import datetime
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel
import aiohttp
import logging

router = APIRouter()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.filing_queue = asyncio.Queue()
        self.update_task = None

    async def connect(self, websocket: WebSocket, ticker: str):
        await websocket.accept()
        if ticker not in self.active_connections:
            self.active_connections[ticker] = set()
        self.active_connections[ticker].add(websocket)
        
        # Start update task if not running
        if not self.update_task:
            self.update_task = asyncio.create_task(self._update_filings())

    def disconnect(self, websocket: WebSocket, ticker: str):
        if ticker in self.active_connections:
            self.active_connections[ticker].remove(websocket)
            if not self.active_connections[ticker]:
                del self.active_connections[ticker]
        
        # Stop update task if no more connections
        if not self.active_connections and self.update_task:
            self.update_task.cancel()

    async def send_filing(self, ticker: str, filing: Dict):
        if ticker in self.active_connections:
            for connection in self.active_connections[ticker]:
                try:
                    await connection.send_json(filing)
                except Exception as e:
                    logger.error(f"Error sending filing to {ticker}: {str(e)}")
                    self.disconnect(connection, ticker)

    async def _update_filings(self):
        """
        Periodically check for new filings and notify connected clients
        """
        while True:
            try:
                # Check for new filings every 5 minutes
                await asyncio.sleep(300)
                
                # Get list of tickers with active connections
                tickers = list(self.active_connections.keys())
                
                if tickers:
                    # Fetch new filings for each ticker
                    async with aiohttp.ClientSession() as session:
                        for ticker in tickers:
                            try:
                                # Example: Get filings from SEC EDGAR API
                                # This would need to be replaced with actual SEC API integration
                                url = f"https://api.sec.gov/filings/{ticker}/recent"
                                async with session.get(url) as response:
                                    if response.status == 200:
                                        filings = await response.json()
                                        for filing in filings:
                                            # Process and analyze filing
                                            processed_filing = await self._process_filing(filing)
                                            if processed_filing:
                                                await self.send_filing(ticker, processed_filing)
                            except Exception as e:
                                logger.error(f"Error fetching filings for {ticker}: {str(e)}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in update task: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _process_filing(self, filing: Dict) -> Optional[Dict]:
        """
        Process and analyze a filing
        """
        try:
            # Extract key information
            filing_date = filing.get("filing_date")
            filing_type = filing.get("filing_type")
            content = filing.get("content")
            
            if not all([filing_date, filing_type, content]):
                return None
                
            # Analyze filing
            from models.filing_analysis.filing_analyzer import FilingAnalyzer
            from models.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer
            
            filing_analyzer = FilingAnalyzer()
            sentiment_analyzer = SentimentAnalyzer()
            
            filing_analysis = filing_analyzer.analyze_filing(content)
            sentiment = sentiment_analyzer.analyze_filing(content)
            
            # Create processed filing
            processed_filing = {
                "filing_date": filing_date,
                "filing_type": filing_type,
                "sentiment": sentiment,
                "key_metrics": filing_analysis["key_metrics"],
                "financial_values": filing_analysis["financial_values"],
                "confidence": sentiment["confidence"],
                "timestamp": datetime.now().isoformat()
            }
            
            return processed_filing
            
        except Exception as e:
            logger.error(f"Error processing filing: {str(e)}")
            return None

# Initialize connection manager
manager = ConnectionManager()

@router.websocket("/ws/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    await manager.connect(websocket, ticker)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, ticker)

@router.get("/ws-test/{ticker}")
async def ws_test(ticker: str):
    """
    Test endpoint to verify WebSocket connection
    """
    html = """
    <html>
        <body>
            <h1>WebSocket Test for {}</h1>
            <div id="messages"></div>
            <script>
                var ws = new WebSocket(`ws://${window.location.host}/ws/${ticker}`);
                
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('div');
                    message.innerHTML = event.data;
                    messages.appendChild(message);
                };
            </script>
        </body>
    </html>
    """.format(ticker)
    return HTMLResponse(html)
