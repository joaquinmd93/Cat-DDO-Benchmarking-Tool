# Quick Reference - DRM Benchmarking Tool

## 🚀 Start the App (5 steps)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/init_db.py; python scripts/seed_angola.py
python run.py
```

**→ Open:** http://localhost:8000/countries/AGO

---

## 🔑 Login Credentials

**Admin Dashboard:** http://localhost:8000/admin

- Email: `admin@worldbank.org`
- Password: `demo-password-change-me`

---

## 📍 Key URLs

| Page | URL |
|------|-----|
| Homepage | http://localhost:8000 |
| Angola Assessment | http://localhost:8000/countries/AGO |
| Admin Dashboard | http://localhost:8000/admin |
| API Docs (Swagger) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 📊 Angola Assessment Data

- **Overall Score:** 38.5 (Emerging)
- **Pillars:** 6 (Legal, Risk ID, Risk Reduction, Preparedness, Financial, Reconstruction)
- **Indicators:** 12 detailed assessments
- **Evidence Files:** 12 placeholder PDFs

### Pillar Breakdown
- Legal & Institutional: **66** (Established)
- Risk Identification: **33** (Emerging)
- Risk Reduction: **33** (Emerging)
- Preparedness: **66** (Established)
- Financial Protection: **0** (Nascent)
- Resilient Reconstruction: **33** (Emerging)

---

## 🧪 Test the Features

### 1. View Assessment
- Go to http://localhost:8000/countries/AGO
- See radar chart and pillar cards
- Expand indicators to view evidence

### 2. Submit Feedback
- Click "Provide Feedback" under any pillar
- Fill form and submit
- Check admin dashboard to see it appear

### 3. Admin Actions
- Login at http://localhost:8000/admin
- View feedback list
- Click "Update" on any feedback
- Change status to "Accepted" or "Triaged"

### 4. Export Data
- Visit http://localhost:8000/api/countries/AGO/export
- See complete JSON export

---

## 🛠️ Common Commands

### Development
```powershell
python run.py              # Start server
python scripts/init_db.py  # Reset database
python scripts/seed_angola.py  # Re-seed data
```

### Testing
```powershell
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest --cov=app tests/    # With coverage
```

### Database
```powershell
# View database (install sqlite3 or use DB Browser)
sqlite3 drm_benchmark.db ".tables"
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Change `APP_PORT` in `.env` |
| Module not found | Activate venv: `.\venv\Scripts\Activate.ps1` |
| Database locked | Delete `drm_benchmark.db` and re-run init/seed |
| Login fails | Check `.env` has correct credentials |

---

## 📁 Project Files

```
Key Files:
├── app/main.py          # FastAPI application
├── app/models.py        # Database models
├── app/api/             # API endpoints
├── scripts/seed_angola.py  # Data seeding
├── fixtures/angola.json    # Angola data
├── requirements.txt     # Dependencies
└── .env                 # Configuration
```

---

## 🎯 What's Working

✅ SQLite database with Angola data  
✅ Radar chart visualization  
✅ Feedback submission & storage  
✅ Admin dashboard with JWT auth  
✅ File uploads  
✅ JSON export  
✅ 15+ passing tests  
✅ API documentation  

---

## 📖 More Info

- Full setup: `SETUP.md`
- Implementation details: `IMPLEMENTATION.md`
- Security notes: `SECURITY.md`
- Main docs: `README.md`

---

**Version:** 0.1.0 | **Date:** Oct 28, 2025
