from pydantic import BaseModel
from typing import List, Optional

class PatientBase(BaseModel):
    age_group: str
    gender: str
    education: str
    income_level: str
    location: str
    physical_env_score: float
    technical_quality_score: float
    interpersonal_score: float
    communication_score: float
    accessibility_score: float

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    no_show_probability: float
    preferred_contact: str

    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    patient_data: PatientBase

class PredictionResponse(BaseModel):
    no_show_probability: float
    risk_level: str
    recommended_actions: List[str]