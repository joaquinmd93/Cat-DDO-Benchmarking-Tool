"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from app.api import countries, assessments, feedback, admin, pages

# Create app instance
app = FastAPI(
    title="DRM Institutional Benchmarking Tool",
    description="World Bank DRM Framework Assessment Platform",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Mount uploads directory
upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads"))
upload_dir.mkdir(exist_ok=True, parents=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Include API routers
app.include_router(countries.router, prefix="/api", tags=["Countries"])
app.include_router(assessments.router, prefix="/api", tags=["Assessments"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(pages.router, tags=["Pages"])

# Root endpoint
@app.get("/")
async def root(request: Request):
    """Homepage"""
    return templates.TemplateResponse("index.html", {"request": request})

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DRM Benchmarking Tool"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
