from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    age_group = Column(String, index=True)
    gender = Column(String)
    education = Column(String)
    income_level = Column(String)
    location = Column(String)
    
    # Satisfaction scores from your research
    physical_env_score = Column(Float)
    technical_quality_score = Column(Float)
    interpersonal_score = Column(Float)
    communication_score = Column(Float)
    accessibility_score = Column(Float)
    
    no_show_probability = Column(Float)
    preferred_contact = Column(String)
    last_appointment = Column(String)
    next_appointment = Column(String)

Base.metadata.create_all(bind=engine)