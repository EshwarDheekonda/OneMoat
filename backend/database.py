from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/onemoat")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)
    
    filings = relationship("Filing", back_populates="company")
    predictions = relationship("Prediction", back_populates="company")

class Filing(Base):
    __tablename__ = "filings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    filing_type = Column(String)
    filing_date = Column(DateTime)
    content = Column(String)
    sentiment_score = Column(Float)
    confidence = Column(Float)
    
    company = relationship("Company", back_populates="filings")
    metrics = relationship("FilingMetric", back_populates="filing")

class FilingMetric(Base):
    __tablename__ = "filing_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    filing_id = Column(Integer, ForeignKey("filings.id"))
    metric_type = Column(String)
    value = Column(Float)
    
    filing = relationship("Filing", back_populates="metrics")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    prediction_date = Column(DateTime)
    predicted_change = Column(Float)
    confidence = Column(Float)
    
    company = relationship("Company", back_populates="predictions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)
