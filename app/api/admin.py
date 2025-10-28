"""
Admin API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Admin, Feedback, Assessment
from app.schemas import (
    AdminLogin,
    Token,
    AdminProfile,
    Feedback as FeedbackSchema,
    FeedbackUpdate,
    AssessmentCreate,
    Assessment as AssessmentSchema
)
from app.auth import (
    verify_password,
    create_access_token,
    get_current_admin
)

router = APIRouter()

@router.post("/login", response_model=Token)
def login(credentials: AdminLogin, db: Session = Depends(get_db)):
    """Admin login"""
    admin = db.query(Admin).filter(Admin.email == credentials.email).first()
    
    if not admin or not verify_password(credentials.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=AdminProfile)
def get_profile(current_admin: Admin = Depends(get_current_admin)):
    """Get current admin profile"""
    return current_admin

@router.get("/feedback", response_model=List[FeedbackSchema])
def admin_list_feedback(
    status_filter: str = None,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin: List all feedback"""
    query = db.query(Feedback)
    
    if status_filter:
        query = query.filter(Feedback.status == status_filter)
    
    feedback_list = query.order_by(Feedback.created_at.desc()).all()
    return feedback_list

@router.patch("/feedback/{feedback_id}", response_model=FeedbackSchema)
def update_feedback_status(
    feedback_id: str,
    update_data: FeedbackUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin: Update feedback status and response"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.status = update_data.status
    if update_data.admin_response:
        feedback.admin_response = update_data.admin_response
    
    db.commit()
    db.refresh(feedback)
    
    return feedback

@router.post("/assessments/publish/{assessment_id}")
def publish_assessment(
    assessment_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin: Publish an assessment"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    assessment.is_published = True
    db.commit()
    db.refresh(assessment)
    
    return {
        "message": "Assessment published successfully",
        "assessment_id": assessment.id,
        "version": assessment.version
    }

@router.post("/assessments/unpublish/{assessment_id}")
def unpublish_assessment(
    assessment_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin: Unpublish an assessment"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    assessment.is_published = False
    db.commit()
    db.refresh(assessment)
    
    return {
        "message": "Assessment unpublished successfully",
        "assessment_id": assessment.id,
        "version": assessment.version
    }
