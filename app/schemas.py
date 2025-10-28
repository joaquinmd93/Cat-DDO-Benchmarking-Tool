"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Country schemas
class CountryBase(BaseModel):
    iso_code: str = Field(..., max_length=3)
    name: str
    region: str

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Pillar schemas
class PillarScoreBase(BaseModel):
    pillar_key: str
    pillar_name: str
    score: float
    maturity_level: str
    rationale: str

class PillarScore(PillarScoreBase):
    id: str
    assessment_id: str
    
    class Config:
        from_attributes = True

# Indicator schemas
class IndicatorAssessmentBase(BaseModel):
    pillar_key: str
    indicator_key: str
    indicator_name: str
    maturity_level: str
    explanation: str
    evidence_excerpt: Optional[str] = None
    evidence_link: Optional[str] = None

class IndicatorAssessment(IndicatorAssessmentBase):
    id: str
    assessment_id: str
    
    class Config:
        from_attributes = True

# Assessment schemas
class AssessmentBase(BaseModel):
    version: str
    created_by: str
    overall_score: float
    overall_maturity: str

class AssessmentCreate(AssessmentBase):
    country_id: str
    pillars: List[PillarScoreBase]
    indicators: List[IndicatorAssessmentBase]

class Assessment(AssessmentBase):
    id: str
    country_id: str
    created_at: datetime
    is_published: bool
    pillars: List[PillarScore]
    indicators: List[IndicatorAssessment]
    
    class Config:
        from_attributes = True

class AssessmentWithCountry(Assessment):
    country: Country

# Feedback schemas
class FeedbackCreate(BaseModel):
    pillar_key: Optional[str] = None
    indicator_key: Optional[str] = None
    feedback_text: str
    stakeholder_name: Optional[str] = None
    stakeholder_email: Optional[EmailStr] = None
    stakeholder_org: Optional[str] = None

class FeedbackUpdate(BaseModel):
    status: str
    admin_response: Optional[str] = None

class Feedback(BaseModel):
    id: str
    assessment_id: str
    pillar_key: Optional[str]
    indicator_key: Optional[str]
    feedback_text: str
    stakeholder_name: Optional[str]
    stakeholder_email: Optional[str]
    stakeholder_org: Optional[str]
    evidence_file: Optional[str]
    status: str
    admin_response: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Admin schemas
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AdminProfile(BaseModel):
    id: str
    email: str
    name: str
    
    class Config:
        from_attributes = True
