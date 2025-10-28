"""
Test suite for DRM Benchmarking Tool
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.database import Base, get_db
from app.models import Country, Assessment, PillarScore, IndicatorAssessment, Admin, Feedback
from app.auth import get_password_hash

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Get database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Get test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_country(db_session):
    """Create sample country"""
    country = Country(
        iso_code="AGO",
        name="Angola",
        region="Sub-Saharan Africa"
    )
    db_session.add(country)
    db_session.commit()
    db_session.refresh(country)
    return country

@pytest.fixture
def sample_assessment(db_session, sample_country):
    """Create sample assessment"""
    assessment = Assessment(
        country_id=sample_country.id,
        version="v1",
        created_by="test_user",
        is_published=True,
        overall_score=38.5,
        overall_maturity="Emerging"
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    
    # Add a pillar
    pillar = PillarScore(
        assessment_id=assessment.id,
        pillar_key="legal",
        pillar_name="Legal & Institutional Framework",
        score=66,
        maturity_level="Established",
        rationale="Test rationale"
    )
    db_session.add(pillar)
    db_session.commit()
    
    return assessment

@pytest.fixture
def admin_user(db_session):
    """Create admin user"""
    admin = Admin(
        email="test@admin.com",
        password_hash=get_password_hash("testpassword"),
        name="Test Admin"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def admin_token(client, admin_user):
    """Get admin JWT token"""
    response = client.post(
        "/api/admin/login",
        json={"email": "test@admin.com", "password": "testpassword"}
    )
    return response.json()["access_token"]

# Tests
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_countries(client, sample_country):
    """Test getting all countries"""
    response = client.get("/api/countries")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["iso_code"] == "AGO"

def test_get_country_by_iso(client, sample_country):
    """Test getting country by ISO code"""
    response = client.get("/api/countries/AGO")
    assert response.status_code == 200
    data = response.json()
    assert data["iso_code"] == "AGO"
    assert data["name"] == "Angola"

def test_get_latest_assessment(client, sample_assessment):
    """Test getting latest published assessment"""
    response = client.get("/api/countries/AGO/assessments/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v1"
    assert data["overall_score"] == 38.5
    assert len(data["pillars"]) > 0

def test_export_assessment(client, sample_assessment):
    """Test exporting assessment as JSON"""
    response = client.get("/api/countries/AGO/export")
    assert response.status_code == 200
    data = response.json()
    assert "country" in data
    assert "assessment" in data
    assert data["country"]["iso_code"] == "AGO"
    assert data["assessment"]["version"] == "v1"

def test_create_feedback(client, sample_assessment):
    """Test creating feedback"""
    response = client.post(
        f"/api/assessments/{sample_assessment.id}/feedback",
        json={
            "pillar_key": "legal",
            "feedback_text": "This is test feedback",
            "stakeholder_name": "Test User",
            "stakeholder_email": "test@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["feedback_text"] == "This is test feedback"
    assert data["status"] == "open"

def test_get_feedback(client, sample_assessment):
    """Test retrieving feedback"""
    # Create feedback first
    create_response = client.post(
        f"/api/assessments/{sample_assessment.id}/feedback",
        json={
            "feedback_text": "Test feedback",
        }
    )
    feedback_id = create_response.json()["id"]
    
    # Get feedback
    response = client.get(f"/api/feedback/{feedback_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feedback_id
    assert data["feedback_text"] == "Test feedback"

def test_admin_login(client, admin_user):
    """Test admin login"""
    response = client.post(
        "/api/admin/login",
        json={"email": "test@admin.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_admin_login_invalid(client, admin_user):
    """Test admin login with invalid credentials"""
    response = client.post(
        "/api/admin/login",
        json={"email": "test@admin.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_admin_get_feedback(client, sample_assessment, admin_token):
    """Test admin retrieving all feedback"""
    # Create some feedback
    client.post(
        f"/api/assessments/{sample_assessment.id}/feedback",
        json={"feedback_text": "Feedback 1"}
    )
    client.post(
        f"/api/assessments/{sample_assessment.id}/feedback",
        json={"feedback_text": "Feedback 2"}
    )
    
    # Get feedback as admin
    response = client.get(
        "/api/admin/feedback",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_admin_update_feedback(client, sample_assessment, admin_token):
    """Test admin updating feedback status"""
    # Create feedback
    create_response = client.post(
        f"/api/assessments/{sample_assessment.id}/feedback",
        json={"feedback_text": "Test feedback"}
    )
    feedback_id = create_response.json()["id"]
    
    # Update as admin
    response = client.patch(
        f"/api/admin/feedback/{feedback_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "status": "accepted",
            "admin_response": "Thank you for the feedback"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["admin_response"] == "Thank you for the feedback"

def test_publish_assessment(client, sample_assessment, admin_token):
    """Test admin publishing assessment"""
    # Unpublish first
    sample_assessment.is_published = False
    
    response = client.post(
        f"/api/admin/assessments/publish/{sample_assessment.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "published successfully" in data["message"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
