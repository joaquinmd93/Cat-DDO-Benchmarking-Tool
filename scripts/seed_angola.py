"""
Seed database with Angola assessment data
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models import Country, Assessment, PillarScore, IndicatorAssessment, Admin
from app.auth import get_password_hash

def load_angola_fixture():
    """Load Angola data from fixtures file"""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "angola.json"
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_placeholder_evidence_files():
    """Create placeholder PDF files for evidence"""
    seed_data_dir = Path(__file__).parent.parent / "seed_data" / "angola"
    seed_data_dir.mkdir(parents=True, exist_ok=True)
    
    evidence_files = [
        "legal_law_2019.pdf",
        "drm_strategy_2020.pdf",
        "hazard_map_2018.pdf",
        "data_access_policy.pdf",
        "luanda_master_plan.pdf",
        "investment_manual_2021.pdf",
        "early_warning_system.pdf",
        "contingency_plan_2024.pdf",
        "fiscal_risk_note.pdf",
        "budget_emergency_2024.pdf",
        "reconstruction_guidelines_2022.pdf",
        "pdna_cunene_2021.pdf"
    ]
    
    for filename in evidence_files:
        filepath = seed_data_dir / filename
        if not filepath.exists():
            # Create a simple placeholder PDF-like file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"%PDF-1.4\n% Placeholder evidence file: {filename}\n")
                f.write(f"% This is a demo file for the DRM Benchmarking Tool prototype\n")
                f.write(f"% Created: {datetime.now().isoformat()}\n")
    
    print(f"Created {len(evidence_files)} placeholder evidence files in {seed_data_dir}")

def seed_angola():
    """Seed Angola assessment data"""
    db = SessionLocal()
    
    try:
        # Create admin user from environment variables
        admin_email = os.getenv("ADMIN_EMAIL", "admin@worldbank.org")
        admin_password = os.getenv("ADMIN_PASSWORD", "demo-password-change-me")
        
        existing_admin = db.query(Admin).filter(Admin.email == admin_email).first()
        if not existing_admin:
            admin = Admin(
                email=admin_email,
                password_hash=get_password_hash(admin_password),
                name="System Administrator"
            )
            db.add(admin)
            db.commit()
            print(f"Created admin user: {admin_email}")
        else:
            print(f"Admin user already exists: {admin_email}")
        
        # Load Angola fixture
        data = load_angola_fixture()
        
        # Check if Angola already exists
        existing_country = db.query(Country).filter(
            Country.iso_code == data["country"]["iso_code"]
        ).first()
        
        if existing_country:
            print(f"Angola (AGO) already exists with ID: {existing_country.id}")
            country = existing_country
        else:
            # Create country
            country = Country(**data["country"])
            db.add(country)
            db.commit()
            db.refresh(country)
            print(f"Created country: {country.name} ({country.iso_code})")
        
        # Check if assessment already exists
        existing_assessment = db.query(Assessment).filter(
            Assessment.country_id == country.id,
            Assessment.version == data["assessment"]["version"]
        ).first()
        
        if existing_assessment:
            print(f"Assessment v{data['assessment']['version']} already exists for Angola")
            return
        
        # Create assessment
        assessment_data = data["assessment"]
        assessment = Assessment(
            country_id=country.id,
            version=assessment_data["version"],
            created_by=assessment_data["created_by"],
            created_at=datetime.fromisoformat(assessment_data["created_at"].replace('Z', '+00:00')),
            is_published=assessment_data["is_published"],
            overall_score=assessment_data["overall_score"],
            overall_maturity=assessment_data["overall_maturity"]
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        print(f"Created assessment v{assessment.version} for Angola")
        
        # Create pillar scores
        for pillar_data in assessment_data["pillars"]:
            pillar = PillarScore(
                assessment_id=assessment.id,
                **pillar_data
            )
            db.add(pillar)
        db.commit()
        print(f"Created {len(assessment_data['pillars'])} pillar scores")
        
        # Create indicator assessments
        for indicator_data in assessment_data["indicators"]:
            indicator = IndicatorAssessment(
                assessment_id=assessment.id,
                **indicator_data
            )
            db.add(indicator)
        db.commit()
        print(f"Created {len(assessment_data['indicators'])} indicator assessments")
        
        # Create placeholder evidence files
        create_placeholder_evidence_files()
        
        print("\n✅ Angola seed data loaded successfully!")
        print(f"   Country: {country.name} ({country.iso_code})")
        print(f"   Assessment: v{assessment.version}")
        print(f"   Overall Score: {assessment.overall_score} ({assessment.overall_maturity})")
        print(f"   Pillars: {len(assessment_data['pillars'])}")
        print(f"   Indicators: {len(assessment_data['indicators'])}")
        print(f"\n   View at: http://localhost:8000/countries/AGO")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_angola()
