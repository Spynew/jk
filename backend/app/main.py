from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from .database import get_db
from .routers import users, products, orders, admin

load_dotenv()

app = FastAPI(
    title="PK Shop API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
allowed_origins = [os.getenv('FRONTEND_URL', 'http://localhost:3000')]
if os.getenv('DEV_MODE', '').lower() == 'true':
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)

# Additional endpoints
@app.get("/api/categories")
async def get_categories():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, name FROM categories WHERE status = 'active' ORDER BY name")
        categories = cursor.fetchall()
        return {"categories": categories}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/health")
async def health_check():
    return {"status": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
