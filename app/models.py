"""
SQLAlchemy models for DRM Benchmarking Tool
"""
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Country(Base):
    __tablename__ = "countries"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    iso_code = Column(String(3), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    region = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assessments = relationship("Assessment", back_populates="country", cascade="all, delete-orphan")


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    country_id = Column(String, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    version = Column(String(50), nullable=False)
    created_by = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    overall_score = Column(Float, nullable=False)
    overall_maturity = Column(String(50), nullable=False)
    
    country = relationship("Country", back_populates="assessments")
    pillars = relationship("PillarScore", back_populates="assessment", cascade="all, delete-orphan")
    indicators = relationship("IndicatorAssessment", back_populates="assessment", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="assessment", cascade="all, delete-orphan")


class PillarScore(Base):
    __tablename__ = "pillar_scores"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    assessment_id = Column(String, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    pillar_key = Column(String(50), nullable=False)
    pillar_name = Column(String(200), nullable=False)
    score = Column(Float, nullable=False)
    maturity_level = Column(String(50), nullable=False)
    rationale = Column(Text, nullable=False)
    
    assessment = relationship("Assessment", back_populates="pillars")


class IndicatorAssessment(Base):
    __tablename__ = "indicator_assessments"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    assessment_id = Column(String, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    pillar_key = Column(String(50), nullable=False)
    indicator_key = Column(String(100), nullable=False)
    indicator_name = Column(String(300), nullable=False)
    maturity_level = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    evidence_excerpt = Column(String(500), nullable=True)
    evidence_link = Column(String(500), nullable=True)
    
    assessment = relationship("Assessment", back_populates="indicators")


class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    assessment_id = Column(String, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    pillar_key = Column(String(50), nullable=True)
    indicator_key = Column(String(100), nullable=True)
    feedback_text = Column(Text, nullable=False)
    stakeholder_name = Column(String(200), nullable=True)
    stakeholder_email = Column(String(200), nullable=True)
    stakeholder_org = Column(String(200), nullable=True)
    evidence_file = Column(String(500), nullable=True)
    status = Column(String(20), default="open")  # open, triaged, accepted, rejected
    admin_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assessment = relationship("Assessment", back_populates="feedback")


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
