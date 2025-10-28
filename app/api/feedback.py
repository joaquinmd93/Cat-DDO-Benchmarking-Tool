"""
Feedback API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import os
import uuid

from app.database import get_db
from app.models import Feedback, Assessment
from app.schemas import (
    Feedback as FeedbackSchema,
    FeedbackCreate,
    FeedbackUpdate
)

router = APIRouter()

@router.post("/assessments/{assessment_id}/feedback", response_model=FeedbackSchema)
async def create_feedback(
    assessment_id: str,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit feedback for an assessment"""
    # Verify assessment exists
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Create feedback
    feedback = Feedback(
        assessment_id=assessment_id,
        pillar_key=feedback_data.pillar_key,
        indicator_key=feedback_data.indicator_key,
        feedback_text=feedback_data.feedback_text,
        stakeholder_name=feedback_data.stakeholder_name,
        stakeholder_email=feedback_data.stakeholder_email,
        stakeholder_org=feedback_data.stakeholder_org,
        status="open"
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback

@router.post("/assessments/{assessment_id}/feedback-with-file")
async def create_feedback_with_file(
    assessment_id: str,
    feedback_text: str = Form(...),
    pillar_key: Optional[str] = Form(None),
    indicator_key: Optional[str] = Form(None),
    stakeholder_name: Optional[str] = Form(None),
    stakeholder_email: Optional[str] = Form(None),
    stakeholder_org: Optional[str] = Form(None),
    evidence_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Submit feedback with optional file upload"""
    # Verify assessment exists
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    evidence_filename = None
    if evidence_file:
        # Save uploaded file
        upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads")) / "feedback"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_ext = Path(evidence_file.filename).suffix
        evidence_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / evidence_filename
        
        # Save file
        with open(file_path, "wb") as f:
            content = await evidence_file.read()
            f.write(content)
        
        evidence_filename = f"feedback/{evidence_filename}"
    
    # Create feedback
    feedback = Feedback(
        assessment_id=assessment_id,
        pillar_key=pillar_key,
        indicator_key=indicator_key,
        feedback_text=feedback_text,
        stakeholder_name=stakeholder_name,
        stakeholder_email=stakeholder_email,
        stakeholder_org=stakeholder_org,
        evidence_file=evidence_filename,
        status="open"
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return {
        "id": feedback.id,
        "assessment_id": feedback.assessment_id,
        "feedback_text": feedback.feedback_text,
        "evidence_file": feedback.evidence_file,
        "status": feedback.status,
        "created_at": feedback.created_at.isoformat()
    }

@router.get("/feedback/{feedback_id}", response_model=FeedbackSchema)
def get_feedback(feedback_id: str, db: Session = Depends(get_db)):
    """Get feedback by ID"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.get("/feedback", response_model=List[FeedbackSchema])
def list_feedback(
    assessment_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List feedback with optional filters"""
    query = db.query(Feedback)
    
    if assessment_id:
        query = query.filter(Feedback.assessment_id == assessment_id)
    if status:
        query = query.filter(Feedback.status == status)
    
    feedback_list = query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    return feedback_list
