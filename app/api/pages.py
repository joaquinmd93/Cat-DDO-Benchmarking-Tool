"""
Frontend page routes (HTML templates)
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db
from app.models import Country, Assessment

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/countries/{iso_code}", response_class=HTMLResponse)
async def country_page(iso_code: str, request: Request, db: Session = Depends(get_db)):
    """Render country assessment page"""
    country = db.query(Country).filter(Country.iso_code == iso_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    assessment = db.query(Assessment).filter(
        Assessment.country_id == country.id,
        Assessment.is_published == True
    ).order_by(Assessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No published assessment found")
    
    # Prepare pillar data for radar chart
    pillar_data = []
    for pillar in assessment.pillars:
        pillar_data.append({
            "key": pillar.pillar_key,
            "name": pillar.pillar_name,
            "score": pillar.score,
            "maturity": pillar.maturity_level,
            "rationale": pillar.rationale
        })
    
    # Prepare indicator data grouped by pillar
    indicators_by_pillar = {}
    for indicator in assessment.indicators:
        if indicator.pillar_key not in indicators_by_pillar:
            indicators_by_pillar[indicator.pillar_key] = []
        indicators_by_pillar[indicator.pillar_key].append(indicator)
    
    return templates.TemplateResponse("country.html", {
        "request": request,
        "country": country,
        "assessment": assessment,
        "pillars": pillar_data,
        "indicators_by_pillar": indicators_by_pillar
    })

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Render admin dashboard"""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})
