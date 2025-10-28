"""
Initialize database - create all tables
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, Base
from app.models import Country, Assessment, PillarScore, IndicatorAssessment, Feedback, Admin

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    
    # Create uploads directory if it doesn't exist
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    print(f"Upload directory created: {upload_dir}")

if __name__ == "__main__":
    init_db()
