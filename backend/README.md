# Backend - SS Bags E-commerce API

FastAPI backend for the SS Bags e-commerce platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=ss_bags
DB_PORT=3306
SECRET_KEY=your-super-secret-key
FRONTEND_URL=http://localhost:3000
DEV_MODE=true
```

3. Run the application:
```bash
# Option 1: Using the launcher script (recommended)
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload

# Option 3: Using uvicorn with custom port
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

Import the provided SQL file:
```bash
mysql -u root -p ss_bags < combined_database.sql
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and connection
│   ├── models.py            # Pydantic models
│   ├── auth.py              # Authentication logic
│   ├── dependencies.py      # FastAPI dependencies
│   └── routers/
│       ├── users.py         # User authentication endpoints
│       ├── products.py      # Product management endpoints
│       ├── orders.py        # Order management endpoints
│       └── admin.py         # Admin-specific endpoints
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── combined_database.sql    # Database schema and sample data
├── hash.py                  # Password hashing utility
└── update_admin_password.py # Admin password update script
```
