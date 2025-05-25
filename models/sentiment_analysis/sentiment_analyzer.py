import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a given text
        Returns: Dictionary with sentiment scores
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
        outputs = self.model(**inputs)
        
        # Get probabilities for each class
        probabilities = torch.softmax(outputs.logits, dim=1).detach().cpu().numpy()[0]
        
        # Map probabilities to sentiment scores
        sentiment_scores = {
            "positive": probabilities[2],
            "negative": probabilities[0],
            "neutral": probabilities[1]
        }
        
        return sentiment_scores

    def analyze_filing(self, filing_text: str) -> Dict[str, float]:
        """
        Analyze an entire filing document
        Returns: Overall sentiment score and confidence
        """
        # Split filing into chunks
        chunks = self._split_text(filing_text, max_length=512)
        
        # Analyze each chunk
        chunk_scores = []
        for chunk in chunks:
            scores = self.analyze_text(chunk)
            chunk_scores.append(scores)
        
        # Calculate weighted average
        avg_scores = self._calculate_weighted_average(chunk_scores)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(avg_scores)
        
        return {
            "sentiment_score": avg_scores["positive"] - avg_scores["negative"],
            "confidence": confidence,
            "detailed_scores": avg_scores
        }

    def _split_text(self, text: str, max_length: int) -> List[str]:
        """Split text into chunks of max_length"""
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            if len(" ".join(current_chunk + [word])) <= max_length:
                current_chunk.append(word)
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def _calculate_weighted_average(self, scores: List[Dict[str, float]]) -> Dict[str, float]:
        """Calculate weighted average of sentiment scores"""
        total_scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for score in scores:
            for sentiment, value in score.items():
                total_scores[sentiment] += value
        
        num_chunks = len(scores)
        return {k: v/num_chunks for k, v in total_scores.items()}

    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence score based on sentiment distribution"""
        positive = scores["positive"]
        negative = scores["negative"]
        neutral = scores["neutral"]
        
        # Calculate confidence based on distribution
        max_score = max(positive, negative, neutral)
        confidence = (max_score - neutral) / (1 - neutral) if neutral < 1 else 1.0
        
        return confidence
