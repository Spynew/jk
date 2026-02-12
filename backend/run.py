#!/usr/bin/env python3
"""
Backend launcher script for S.S BAGS
Run this script to start the FastAPI server
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting S.S BAGS Backend Server...")
    print("📍 Server will run at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("⏹️ Press CTRL+C to stop the server")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
