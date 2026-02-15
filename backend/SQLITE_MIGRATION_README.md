# MySQL to SQLite Migration Guide

This document outlines the changes made to migrate the FastAPI backend from MySQL to SQLite.

## Changes Made

### 1. Dependencies Updated
- **File**: `requirements.txt`
- **Changes**: 
  - Removed: `mysql-connector-python==8.3.0`
  - Added: `sqlalchemy==2.0.25`

### 2. Database Configuration
- **File**: `app/database.py`
- **Changes**: 
  - Replaced MySQL connection pool with SQLAlchemy engine
  - Added SQLite configuration with `sqlite:///./app.db`
  - Added automatic table creation with `init_db()` function
  - Converted all MySQL-specific syntax to SQLite-compatible syntax

### 3. Router Files Updated
All router files have been updated to use SQLAlchemy instead of raw MySQL connections:

#### Users Router (`app/routers/users.py`)
- Replaced `cursor.execute()` with `db.execute(text())`
- Updated parameter binding from `%s` to `:parameter_name`
- Added proper SQLAlchemy session management with `db=Depends(get_db)`

#### Products Router (`app/routers/products.py`)
- Converted all CRUD operations to SQLAlchemy
- Updated image handling functions
- Maintained file upload functionality

#### Orders Router (`app/routers/orders.py`)
- Updated order creation and management
- Converted complex JOIN queries to SQLAlchemy
- Maintained stock management logic

#### Admin Router (`app/routers/admin.py`)
- Updated statistics functions
- Converted reporting queries to use SQLite date functions
- Replaced MySQL-specific functions with SQLite equivalents

### 4. Main Application
- **File**: `app/main.py`
- **Changes**: Updated categories endpoint to use SQLAlchemy

### 5. New Files Created
- **File**: `init_data.py`
- **Purpose**: Initialize database with basic categories and admin user
- **Features**:
  - Creates 18 bag categories
  - Sets up default admin account
  - Safe insertion with `INSERT OR IGNORE`

## Database Schema Differences

### MySQL → SQLite Changes
1. **AUTO_INCREMENT** → **AUTOINCREMENT**
2. **ENUM** → **VARCHAR with CHECK constraint**
3. **TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE** → **TIMESTAMP DEFAULT CURRENT_TIMESTAMP** (manual update needed)
4. **DATE_FORMAT()** → **strftime()**
5. **DATE_SUB()** → **date()**
6. **GROUP_CONCAT()** → **GROUP_CONCAT()** (supported in SQLite)

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_data.py
```
This will:
- Create `app.db` SQLite database file
- Create all necessary tables
- Insert basic categories
- Create admin user (email: admin@ssbags.com, password: admin123)

### 3. Start the Application
```bash
python run.py
```
or
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Important Notes

### Security
- **Change the default admin password** after first login
- The default admin credentials are:
  - Email: `admin@ssbags.com`
  - Password: `admin123`

### Data Migration
- This migration creates a fresh SQLite database
- To migrate existing MySQL data, you would need to:
  1. Export data from MySQL
  2. Transform data format if needed
  3. Import into SQLite using appropriate tools

### Environment Variables
- The `DATABASE_URL` environment variable can be set to override the default SQLite path
- Default: `sqlite:///./app.db`

### Features Maintained
- All CRUD operations
- File uploads for product images
- User authentication and authorization
- Order management
- Admin dashboard functionality
- Reporting and statistics

### Known Limitations
- Activity logging has been disabled (activity_logs table not included in schema)
- Some advanced MySQL features not available in SQLite
- Concurrent write performance may be lower than MySQL

## Testing
After migration, test the following endpoints:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/admin/login` - Admin login
- `GET /api/products` - Product listing
- `GET /api/categories` - Categories listing
- `POST /api/orders` - Order creation

## Troubleshooting

### Common Issues
1. **Database locked errors**: Ensure only one instance of the app is running
2. **Missing tables**: Run `python init_data.py` to recreate tables
3. **Import errors**: Ensure all dependencies are installed correctly

### File Locations
- SQLite database: `backend/app.db`
- Uploads directory: `backend/uploads/`
- Log files: Check console output for errors

## Backup Recommendations
- Regularly backup the `app.db` file
- Store backups in a secure location
- Test backup restoration process periodically
