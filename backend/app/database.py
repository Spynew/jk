import os
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'ss_bags'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Initialize connection pool
try:
    db_pool = MySQLConnectionPool(
        pool_name="mypool",
        pool_size=10,
        pool_reset_session=True,
        **DATABASE_CONFIG
    )
    print("Database connection pool created successfully")
except Error as e:
    print(f"Error creating connection pool: {e}")
    exit(1)

def get_db():
    try:
        conn = db_pool.get_connection()
        conn.autocommit = False
        return conn
    except Error as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
