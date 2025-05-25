import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
import re
from datetime import datetime

class FilingAnalyzer:
    def __init__(self):
        self.key_metrics = {
            "revenue": ["revenue", "income", "sales"],
            "expenses": ["expense", "cost"],
            "profit": ["profit", "earnings"],
            "growth": ["growth", "increase", "decrease"],
            "forecast": ["forecast", "projection", "estimate"],
            "guidance": ["guidance", "outlook", "expectation"]
        }
        self.financial_patterns = {
            "currency": r"\$?\s?\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:million|billion)?",
            "percentage": r"\d+(?:\.\d+)?%",
            "date": r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+\d{4}\b"
        }

    def extract_key_metrics(self, filing_text: str) -> Dict[str, List[Dict]]:
        """
        Extract key financial metrics from filing text
        """
        metrics = {}
        
        for metric, keywords in self.key_metrics.items():
            matches = []
            for keyword in keywords:
                pattern = re.compile(keyword, re.IGNORECASE)
                for match in pattern.finditer(filing_text):
                    start = max(0, match.start() - 200)
                    end = min(len(filing_text), match.end() + 200)
                    context = filing_text[start:end]
                    matches.append({
                        "keyword": keyword,
                        "context": context,
                        "position": match.start()
                    })
            metrics[metric] = matches
        
        return metrics

    def extract_financial_values(self, filing_text: str) -> Dict[str, List[str]]:
        """
        Extract financial values (currency amounts, percentages) from text
        """
        values = {}
        
        for name, pattern in self.financial_patterns.items():
            matches = re.findall(pattern, filing_text)
            values[name] = matches
        
        return values

    def analyze_filing_structure(self, filing_text: str) -> Dict[str, List[str]]:
        """
        Analyze filing structure and extract sections
        """
        soup = BeautifulSoup(filing_text, 'html.parser')
        sections = {}
        
        # Extract headings and sections
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for heading in headings:
            section_name = heading.get_text().strip()
            section_content = []
            next_node = heading
            
            while next_node:
                next_node = next_node.find_next()
                if next_node.name in ['h1', 'h2', 'h3', 'h4']:
                    break
                if next_node.get_text().strip():
                    section_content.append(next_node.get_text().strip())
            
            sections[section_name] = section_content
        
        return sections

    def extract_dates(self, filing_text: str) -> List[str]:
        """
        Extract all dates mentioned in the filing
        """
        pattern = self.financial_patterns["date"]
        return re.findall(pattern, filing_text)

    def analyze_tone(self, filing_text: str) -> Dict[str, float]:
        """
        Analyze the overall tone of the filing
        """
        positive_words = [
            "increase", "growth", "improvement", "positive", "strong", "outperform",
            "exceed", "beat", "better", "improved", "enhanced"
        ]
        negative_words = [
            "decrease", "loss", "decline", "negative", "weak", "underperform",
            "miss", "worse", "reduced", "declined"
        ]
        
        positive_count = sum(filing_text.lower().count(word) for word in positive_words)
        negative_count = sum(filing_text.lower().count(word) for word in negative_words)
        
        total_words = len(filing_text.split())
        if total_words == 0:
            return {"positive": 0.5, "negative": 0.5}
        
        return {
            "positive": positive_count / total_words,
            "negative": negative_count / total_words
        }

    def analyze_filing(self, filing_text: str) -> Dict[str, any]:
        """
        Comprehensive filing analysis
        """
        return {
            "key_metrics": self.extract_key_metrics(filing_text),
            "financial_values": self.extract_financial_values(filing_text),
            "structure": self.analyze_filing_structure(filing_text),
            "dates": self.extract_dates(filing_text),
            "tone_analysis": self.analyze_tone(filing_text)
        }
