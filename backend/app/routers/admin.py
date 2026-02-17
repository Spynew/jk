from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
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
async def admin_login(admin: AdminLogin):
    print(f"Admin login attempt for: {admin.email}")
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, email, password, role FROM admins WHERE email = %s", (admin.email,))
        db_admin = cursor.fetchone()
        
        if not db_admin or not verify_password(admin.password, db_admin['password']):
            raise HTTPException(status_code=401, detail="Invalid admin credentials")
        
        token = create_token({"sub": str(db_admin['id']), "role": db_admin['role']})
        
        return {"token": token, "message": "Admin login successful"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in admin login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/stats/users")
async def get_users_stats(payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/stats/products")
async def get_products_stats(payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM products")
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/stats/orders")
async def get_orders_stats(payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total_sales FROM orders WHERE status IN ('confirmed', 'shipped', 'delivered')")
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/customers")
async def get_customers(payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT u.id, u.name, u.email, u.phone, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name, u.email, u.phone"
        )
        customers = cursor.fetchall()
        return {"customers": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/customers/{customer_id}")
async def deactivate_customer(customer_id: int, update: dict, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    admin_id = int(payload.get("sub"))
    
    try:
        cursor.execute("UPDATE users SET status = %s WHERE id = %s", (update.get("status"), customer_id))
        
        cursor.execute(
            "INSERT INTO activity_logs (admin_id, action, details) VALUES (%s, %s, %s)",
            (admin_id, f"Customer {customer_id} deactivated", f"Status: {update.get('status')}")
        )
        
        conn.commit()
        return {"message": "Customer updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/reports")
async def get_reports(period: str = "daily", payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if period == "monthly":
            query = """
                SELECT DATE_FORMAT(created_at, '%Y-%m-01') as date, 
                       COUNT(*) as orders, 
                       COALESCE(SUM(total_amount), 0) as revenue 
                FROM orders 
                WHERE status IN ('confirmed', 'shipped', 'delivered')
                AND created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
                GROUP BY DATE_FORMAT(created_at, '%Y-%m')
                ORDER BY date DESC
            """
        else:  # daily
            query = """
                SELECT DATE(created_at) as date, 
                       COUNT(*) as orders, 
                       COALESCE(SUM(total_amount), 0) as revenue 
                FROM orders 
                WHERE status IN ('confirmed', 'shipped', 'delivered')
                AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            """
        
        cursor.execute(query)
        report_data = cursor.fetchall()
        
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
    finally:
        cursor.close()
        conn.close()
