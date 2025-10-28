# DRM Institutional Benchmarking Tool - Prototype

A full-stack Python web application for assessing and benchmarking Disaster Risk Management (DRM) institutional frameworks across countries using the World Bank DRM framework.

## Features

- **Country Assessment Pages**: Interactive radar charts and pillar scorecards
- **Six DRM Pillars**: Legal/Institutional, Risk ID, Risk Reduction, Preparedness, Financial Protection, Resilient Reconstruction
- **Maturity Levels**: Nascent (0), Emerging (33), Established (66), Advanced (100)
- **Feedback System**: Stakeholders can provide feedback on assessments with evidence uploads
- **Admin Dashboard**: Review feedback, update assessment versions, manage content
- **Pre-seeded Demo**: Angola (AGO) fully populated with invented sample data

## Prerequisites

- Python 3.10+ and pip
- (Optional) Docker & Docker Compose for PostgreSQL mode

## Quick Start (SQLite - Zero Dependencies)

```bash
# Clone and navigate
cd "Cat DDO Benchmarking Tool"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Initialize database and seed Angola data
python scripts/init_db.py
python scripts/seed_angola.py

# Start development server
python run.py
```

Open http://localhost:8000 and navigate to http://localhost:8000/countries/AGO to see the seeded Angola assessment.

## Optional: Docker + PostgreSQL Mode

```bash
# Start PostgreSQL container
docker-compose up -d

# Update .env to use DATABASE_URL for postgres
# Then run migrations and seed
python scripts/init_db.py
python scripts/seed_angola.py

# Start server
python run.py
```

## Admin Access

Default admin credentials (dev only):
- Email: `admin@worldbank.org`
- Password: `demo-password-change-me`

Access admin dashboard at: http://localhost:8000/admin

## Example API Commands

```bash
# Get all countries
curl http://localhost:8000/api/countries

# Get latest Angola assessment
curl http://localhost:8000/api/countries/AGO/assessments/latest

# Export Angola assessment as JSON
curl http://localhost:8000/api/countries/AGO/export

# Submit feedback (replace {assessment-id} with actual UUID from the assessment)
curl -X POST http://localhost:8000/api/assessments/{assessment-id}/feedback \
  -H "Content-Type: application/json" \
  -d "{\"pillar_key\": \"legal\", \"feedback_text\": \"The 2019 law should reference subnational implementation.\", \"stakeholder_name\": \"Civil Society Org\", \"stakeholder_email\": \"feedback@example.org\"}"
```

## Project Structure

```
├── app/
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database connection
│   ├── schemas.py             # Pydantic schemas
│   ├── api/                   # API routes
│   │   ├── countries.py
│   │   ├── assessments.py
│   │   ├── feedback.py
│   │   └── admin.py
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── country.html
│   │   ├── admin/
│   │   └── index.html
│   └── static/                # CSS, JS, images
│       ├── css/
│       └── js/
├── scripts/
│   ├── init_db.py             # Database initialization
│   └── seed_angola.py         # Seed Angola data
├── uploads/                   # Evidence file storage (local)
├── seed_data/angola/          # Placeholder evidence files
├── fixtures/angola.json       # Angola assessment fixture
├── tests/                     # Pytest tests
├── run.py                     # Application entry point
└── requirements.txt           # Python dependencies
```

## Available Commands

- `python run.py` - Start development server (http://localhost:8000)
- `python scripts/init_db.py` - Initialize database
- `python scripts/seed_angola.py` - Seed Angola demo data
- `pytest` - Run tests
- `pytest --cov` - Run tests with coverage

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Key test scenarios:
# - GET /api/countries/AGO/assessments/latest returns seeded data
# - POST /api/assessments/{id}/feedback creates ticket
# - Feedback visible in admin dashboard
```

## Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Jinja2 templates + HTMX + Alpine.js
- **Charts**: Chart.js (radar charts)
- **Database**: SQLite (dev), PostgreSQL (optional)
- **ORM**: SQLAlchemy
- **Auth**: JWT tokens (dev mode)

## Security Notes

See [SECURITY.md](./SECURITY.md) for security guidelines. This is a **demo prototype** - do not use in production without proper security hardening.

## License

World Bank Internal Tool - Not for public distribution
