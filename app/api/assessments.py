"""
Assessments API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Assessment
from app.schemas import Assessment as AssessmentSchema

router = APIRouter()

@router.get("/assessments/{assessment_id}", response_model=AssessmentSchema)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    """Get assessment by ID"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
