import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
from typing import Dict, List, Tuple
import joblib
import os
from datetime import datetime

class PricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = [
            "sentiment_score", "confidence", "revenue_growth", "profit_margin",
            "expense_ratio", "volume_change", "market_sentiment", "technical_indicators"
        ]
        self.lookback = 30  # Number of days to look back
        self.model_path = "models/price_prediction/model.h5"
        self.scaler_path = "models/price_prediction/scaler.pkl"

    def prepare_data(self, historical_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for training
        """
        df = pd.DataFrame(historical_data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        
        # Create features
        features = df[self.features].values
        
        # Create labels (next day's price change)
        labels = df["price_change"].shift(-1).values[:-1]
        
        # Create sequences
        X, y = [], []
        for i in range(len(features) - self.lookback):
            X.append(features[i:i + self.lookback])
            y.append(labels[i + self.lookback])
        
        return np.array(X), np.array(y)

    def build_model(self, input_shape: tuple) -> Sequential:
        """
        Build LSTM-based price prediction model
        """
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001),
                     loss='mse',
                     metrics=['mae'])
        
        return model

    def train(self, historical_data: List[Dict], epochs: int = 50, batch_size: int = 32):
        """
        Train the price prediction model
        """
        X, y = self.prepare_data(historical_data)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale data
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1]))
        X_train_scaled = X_train_scaled.reshape(X_train.shape)
        
        X_val_scaled = self.scaler.transform(X_val.reshape(-1, X_val.shape[-1]))
        X_val_scaled = X_val_scaled.reshape(X_val.shape)
        
        # Build and train model
        self.model = self.build_model((self.lookback, len(self.features)))
        self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_val_scaled, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        # Save model and scaler
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

    def predict(self, recent_data: List[Dict]) -> float:
        """
        Make price prediction based on recent data
        """
        if not self.model:
            self.load_model()
        
        df = pd.DataFrame(recent_data[-self.lookback:])
        features = df[self.features].values
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled.reshape(1, self.lookback, -1))
        return prediction[0][0]

    def load_model(self):
        """
        Load trained model and scaler
        """
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = tf.keras.models.load_model(self.model_path)
            self.scaler = joblib.load(self.scaler_path)

    def evaluate(self, test_data: List[Dict]) -> Dict[str, float]:
        """
        Evaluate model performance on test data
        """
        X, y = self.prepare_data(test_data)
        X_scaled = self.scaler.transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
        
        predictions = self.model.predict(X_scaled)
        
        # Calculate metrics
        mse = np.mean((predictions - y) ** 2)
        mae = np.mean(np.abs(predictions - y))
        rmse = np.sqrt(mse)
        
        return {
            "mse": mse,
            "mae": mae,
            "rmse": rmse,
            "accuracy": 1 - (mae / np.mean(np.abs(y)))
        }

    def update_model(self, new_data: List[Dict]):
        """
        Update model with new data
        """
        if not self.model:
            self.load_model()
            
        # Prepare new data
        X_new, y_new = self.prepare_data(new_data)
        
        if len(X_new) > 0:
            # Scale new data
            X_new_scaled = self.scaler.transform(X_new.reshape(-1, X_new.shape[-1])).reshape(X_new.shape)
            
            # Fine-tune model
            self.model.fit(
                X_new_scaled, y_new,
                epochs=5,
                batch_size=32,
                verbose=0
            )
            
            # Save updated model
            self.model.save(self.model_path)
