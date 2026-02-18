import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env file load for local testing

# Leapcell pe env var se load hoga
DATABASE_URL = os.getenv("DATABASE_URL")

# Agar individual vars use kar rahe ho (fallback)
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "21578")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_mode=REQUIRED"

print(f"Using DATABASE_URL: {DATABASE_URL}")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        pool_recycle=3600,  # recycle connections to avoid timeout
        pool_pre_ping=True,  # check connection before use
        connect_args={"ssl": {"ssl_mode": "REQUIRED"}}  # Aiven ke liye SSL required
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("Database engine created successfully")
except Exception as e:
    print(f"Database connection failed: {str(e)}")
    raise  # ya raise mat karo agar crash nahi chahte