from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from sqlalchemy import text
from ..database import get_db
from ..models import AdminLogin
from ..auth import hash_password, verify_password, create_token, verify_token
from ..dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.options("/login")
async def admin_login_options():
    from starlette.responses import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@router.post("/login")
async def admin_login(admin: AdminLogin, db=Depends(get_db)):
    print(f"Admin login attempt for: {admin.email}")
    
    try:
        result = db.execute(text("SELECT id, email, password, role FROM admins WHERE email = :email"), {"email": admin.email})
        db_admin = result.fetchone()
        
        if not db_admin or not verify_password(admin.password, db_admin[2]):
            raise HTTPException(status_code=401, detail="Invalid admin credentials")
        
        token = create_token({"sub": str(db_admin[0]), "role": db_admin[3]})
        
        return {"token": token, "message": "Admin login successful"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in admin login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/users")
async def get_users_stats(payload=Depends(require_admin), db=Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM users"))
        count = result.fetchone()
        return {"count": count[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/products")
async def get_products_stats(payload=Depends(require_admin), db=Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) as count FROM products"))
        count = result.fetchone()
        return {"count": count[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/orders")
async def get_orders_stats(payload=Depends(require_admin), db=Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total_sales FROM orders WHERE status IN ('confirmed', 'shipped', 'delivered')"))
        stats = result.fetchone()
        return {"count": stats[0], "total_sales": float(stats[1])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers")
async def get_customers(payload=Depends(require_admin), db=Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT u.id, u.name, u.email, u.phone, COUNT(o.id) as order_count 
            FROM users u 
            LEFT JOIN orders o ON u.id = o.user_id 
            GROUP BY u.id, u.name, u.email, u.phone
        """))
        
        customers = []
        for row in result:
            customers.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "order_count": row[4]
            })
        
        return {"customers": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/customers/{customer_id}")
async def deactivate_customer(customer_id: int, update: dict, payload=Depends(require_admin), db=Depends(get_db)):
    admin_id = int(payload.get("sub"))
    
    try:
        db.execute(text("UPDATE users SET status = :status WHERE id = :customer_id"), {
            "status": update.get("status"),
            "customer_id": customer_id
        })
        
        # Note: activity_logs table doesn't exist in our schema, so we'll skip this for now
        
        db.commit()
        return {"message": "Customer updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports")
async def get_reports(period: str = "daily", payload=Depends(require_admin), db=Depends(get_db)):
    try:
        if period == "monthly":
            # SQLite doesn't have DATE_FORMAT or DATE_SUB, so we'll use SQLite functions
            query = """
                SELECT strftime('%Y-%m-01', created_at) as date, 
                       COUNT(*) as orders, 
                       COALESCE(SUM(total_amount), 0) as revenue 
                FROM orders 
                WHERE status IN ('confirmed', 'shipped', 'delivered')
                AND created_at >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY date DESC
            """
        else:  # daily
            query = """
                SELECT date(created_at) as date, 
                       COUNT(*) as orders, 
                       COALESCE(SUM(total_amount), 0) as revenue 
                FROM orders 
                WHERE status IN ('confirmed', 'shipped', 'delivered')
                AND created_at >= date('now', '-7 days')
                GROUP BY date(created_at)
                ORDER BY date DESC
            """
        
        result = db.execute(text(query))
        report_data = []
        
        for row in result:
            report_data.append({
                "date": row[0],
                "orders": row[1],
                "revenue": float(row[2])
            })
        
        total_orders = sum(r['orders'] for r in report_data)
        total_revenue = sum(float(r['revenue']) for r in report_data)
        
        return {
            "report_data": report_data,
            "total_orders": total_orders,
            "total_revenue": total_revenue
        }
    except Exception as e:
        print(f"Report error: {str(e)}")
        return {"report_data": [], "total_orders": 0, "total_revenue": 0}
