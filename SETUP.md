# DRM Benchmarking Tool - Setup Guide

## Quick Start Summary

This is a fully functional Python/FastAPI prototype with:
- ✅ SQLite database (zero dependencies)
- ✅ Pre-seeded Angola assessment data
- ✅ Interactive radar charts
- ✅ Working feedback system
- ✅ Admin dashboard with authentication
- ✅ REST API with full CRUD operations

## Step-by-Step Setup

### 1. Prerequisites Check

Make sure you have:
- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for cloning)

Verify Python version:
```powershell
python --version
```

### 2. Navigate to Project Directory

```powershell
cd "c:\Users\jqnmu\OneDrive\World_Bank_DRM\Cat DDO Benchmarking Tool"
```

### 3. Create Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
venv\Scripts\activate.bat
```

<!-- **Linux/Mac:**
```bash
source venv/bin/activate
``` -->

You should see `(venv)` prefix in your terminal.

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- Uvicorn (ASGI server)
- Jinja2 (templating)
- And all other dependencies

### 6. Set Up Environment Variables

```powershell
cp .env.example .env
```

The default `.env` file contains:
- SQLite database configuration
- Admin credentials: `admin@worldbank.org` / `demo-password-change-me`
- JWT secret (change in production!)

### 7. Initialize Database

```powershell
python scripts/init_db.py
```

This creates:
- SQLite database file (`drm_benchmark.db`)
- All tables (countries, assessments, pillars, indicators, feedback, admins)
- Uploads directory

### 8. Seed Angola Demo Data

```powershell
python scripts/seed_angola.py
```

This creates:
- Angola country record
- Assessment v1 with 6 pillars
- 12 indicator assessments
- Placeholder evidence PDF files
- Admin user account

You should see:
```
✅ Angola seed data loaded successfully!
   Country: Angola (AGO)
   Assessment: v1
   Overall Score: 38.5 (Emerging)
   Pillars: 6
   Indicators: 12
```

### 9. Start the Application

```powershell
python run.py
```

The server starts on `http://localhost:8000`

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 10. Access the Application

Open your web browser and visit:

**Homepage:**
http://localhost:8000

**Angola Assessment Page:**
http://localhost:8000/countries/AGO

**Admin Dashboard:**
http://localhost:8000/admin

**API Documentation (Swagger UI):**
http://localhost:8000/docs

## Testing the Features

### 1. View Angola Assessment

Navigate to: http://localhost:8000/countries/AGO

You should see:
- Country header with Angola info
- Radar chart showing 6 DRM pillars
- Pillar cards with scores and maturity levels
- Expandable indicator details with evidence

### 2. Submit Feedback

On the Angola page:
1. Click "Provide Feedback" under any pillar
2. Enter feedback text
3. (Optional) Add your name and email
4. Click "Submit Feedback"
5. Should see "✓ Feedback submitted!"

### 3. Login to Admin Dashboard

Navigate to: http://localhost:8000/admin

Login with:
- Email: `admin@worldbank.org`
- Password: `demo-password-change-me`

You should see:
- Feedback statistics
- List of all submitted feedback
- Ability to update feedback status

### 4. Test API Endpoints

**Get all countries:**
```powershell
curl http://localhost:8000/api/countries
```

**Get Angola assessment:**
```powershell
curl http://localhost:8000/api/countries/AGO/assessments/latest
```

**Export Angola data:**
```powershell
curl http://localhost:8000/api/countries/AGO/export -o angola_export.json
```

**Submit feedback via API:**
```powershell
$assessmentId = "YOUR_ASSESSMENT_ID"  # Get from export or API
$body = @{
    pillar_key = "legal"
    feedback_text = "Great assessment!"
    stakeholder_name = "Test User"
} | ConvertTo-Json

curl -X POST "http://localhost:8000/api/assessments/$assessmentId/feedback" `
     -H "Content-Type: application/json" `
     -d $body
```

## Running Tests

### Run all tests:
```powershell
pytest
```

### Run with coverage:
```powershell
pytest --cov=app tests/
```

### Run specific test:
```powershell
pytest tests/test_api.py::test_get_latest_assessment -v
```

## Optional: PostgreSQL Setup

### Using Docker Compose

1. Start PostgreSQL container:
```powershell
docker-compose up -d
```

2. Update `.env` file:
```
DATABASE_URL=postgresql://drm_user:drm_password@localhost:5432/drm_benchmarking
```

3. Re-initialize database:
```powershell
python scripts/init_db.py
python scripts/seed_angola.py
```

4. Start application:
```powershell
python run.py
```

## Troubleshooting

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python` on Mac/Linux

### Issue: PowerShell execution policy error
**Solution:** Run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port 8000 already in use
**Solution:** Change port in `.env`:
```
APP_PORT=8080
```

### Issue: Database locked error
**Solution:** Close any other processes accessing the database, or delete `drm_benchmark.db` and re-run init/seed scripts

### Issue: Module not found errors
**Solution:** Ensure virtual environment is activated and dependencies installed:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Admin login fails
**Solution:** Check that seed script ran successfully and admin user was created. Default credentials are in `.env` file.

## Project Structure

```
Cat DDO Benchmarking Tool/
├── app/
│   ├── api/              # API route handlers
│   │   ├── countries.py
│   │   ├── assessments.py
│   │   ├── feedback.py
│   │   ├── admin.py
│   │   └── pages.py
│   ├── templates/        # Jinja2 HTML templates
│   │   ├── index.html
│   │   ├── country.html
│   │   └── admin/
│   ├── static/           # CSS, JS, images
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database config
│   ├── auth.py           # Authentication
│   └── main.py           # FastAPI app
├── scripts/
│   ├── init_db.py        # Database initialization
│   └── seed_angola.py    # Seed Angola data
├── tests/
│   └── test_api.py       # API tests
├── fixtures/
│   └── angola.json       # Angola assessment fixture
├── seed_data/angola/     # Placeholder evidence files
├── uploads/              # User-uploaded files
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── docker-compose.yml    # PostgreSQL container
├── run.py                # Application entry point
└── README.md             # Main documentation
```

## Next Steps

After confirming the prototype works:

1. **Customize for your needs:**
   - Add more countries
   - Adjust pillar definitions
   - Customize maturity level criteria

2. **Enhance security:**
   - Review SECURITY.md
   - Change default credentials
   - Add rate limiting

3. **Deploy (if needed):**
   - Use PostgreSQL
   - Set up proper secrets management
   - Configure HTTPS
   - Add monitoring

## Support

This is a prototype for internal World Bank use. For questions or issues during demo, contact the development team.

---

**Prototype Version:** 0.1.0  
**Last Updated:** October 28, 2025
