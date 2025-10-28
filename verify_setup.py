"""
Verification script to check if the DRM Benchmarking Tool is set up correctly
Run this after initial setup to verify everything is working
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version is 3.10+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.10+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'jinja2',
        'jose',
        'passlib'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\nRun: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists"""
    env_path = Path('.env')
    if env_path.exists():
        print("✅ .env file exists")
        return True
    else:
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False

def check_database():
    """Check if database exists and has tables"""
    db_path = Path('drm_benchmark.db')
    if db_path.exists():
        print("✅ Database file exists")
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from app.database import SessionLocal
            from app.models import Country, Admin
            
            db = SessionLocal()
            
            # Check for Angola
            angola = db.query(Country).filter(Country.iso_code == 'AGO').first()
            if angola:
                print("✅ Angola country data found")
            else:
                print("⚠️  Angola not found - run: python scripts/seed_angola.py")
            
            # Check for admin
            admin = db.query(Admin).first()
            if admin:
                print("✅ Admin user exists")
            else:
                print("⚠️  No admin user - run: python scripts/seed_angola.py")
            
            db.close()
            return True
            
        except Exception as e:
            print(f"⚠️  Database exists but error querying: {e}")
            return True
    else:
        print("❌ Database not found")
        print("   Run: python scripts/init_db.py")
        return False

def check_directories():
    """Check required directories exist"""
    dirs = ['uploads', 'seed_data/angola', 'app/static', 'app/templates']
    all_exist = True
    
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/ exists")
        else:
            print(f"⚠️  {dir_path}/ not found (will be created on first run)")
    
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("DRM Benchmarking Tool - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Database", check_database),
        ("Directories", check_directories)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can start the application with:")
        print("   python run.py")
        print("\nThen visit: http://localhost:8000/countries/AGO")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above and run this script again.")
        print("\nQuick setup commands:")
        print("   pip install -r requirements.txt")
        print("   cp .env.example .env")
        print("   python scripts/init_db.py")
        print("   python scripts/seed_angola.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
