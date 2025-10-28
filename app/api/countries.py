"""
Countries API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.database import get_db
from app.models import Country, Assessment, PillarScore, IndicatorAssessment
from app.schemas import Country as CountrySchema, Assessment as AssessmentSchema, AssessmentWithCountry

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/countries", response_model=List[CountrySchema])
def get_countries(db: Session = Depends(get_db)):
    """Get all countries"""
    countries = db.query(Country).all()
    return countries

@router.get("/countries/{iso_code}", response_class=JSONResponse)
def get_country(iso_code: str, db: Session = Depends(get_db)):
    """Get country by ISO code"""
    country = db.query(Country).filter(Country.iso_code == iso_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return {
        "id": country.id,
        "iso_code": country.iso_code,
        "name": country.name,
        "region": country.region,
        "created_at": country.created_at.isoformat()
    }

@router.get("/countries/{iso_code}/assessments/latest", response_model=AssessmentWithCountry)
def get_latest_assessment(iso_code: str, db: Session = Depends(get_db)):
    """Get latest published assessment for a country"""
    country = db.query(Country).filter(Country.iso_code == iso_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    assessment = db.query(Assessment).filter(
        Assessment.country_id == country.id,
        Assessment.is_published == True
    ).order_by(Assessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No published assessment found")
    
    return assessment

@router.get("/countries/{iso_code}/export")
def export_assessment(iso_code: str, db: Session = Depends(get_db)):
    """Export country assessment as JSON"""
    country = db.query(Country).filter(Country.iso_code == iso_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    assessment = db.query(Assessment).filter(
        Assessment.country_id == country.id,
        Assessment.is_published == True
    ).order_by(Assessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No published assessment found")
    
    # Build export JSON
    export_data = {
        "country": {
            "iso_code": country.iso_code,
            "name": country.name,
            "region": country.region
        },
        "assessment": {
            "id": assessment.id,
            "version": assessment.version,
            "created_by": assessment.created_by,
            "created_at": assessment.created_at.isoformat(),
            "overall_score": assessment.overall_score,
            "overall_maturity": assessment.overall_maturity,
            "pillars": [
                {
                    "pillar_key": p.pillar_key,
                    "pillar_name": p.pillar_name,
                    "score": p.score,
                    "maturity_level": p.maturity_level,
                    "rationale": p.rationale
                }
                for p in assessment.pillars
            ],
            "indicators": [
                {
                    "pillar_key": i.pillar_key,
                    "indicator_key": i.indicator_key,
                    "indicator_name": i.indicator_name,
                    "maturity_level": i.maturity_level,
                    "explanation": i.explanation,
                    "evidence_excerpt": i.evidence_excerpt,
                    "evidence_link": i.evidence_link
                }
                for i in assessment.indicators
            ]
        }
    }
    
    return JSONResponse(content=export_data)
