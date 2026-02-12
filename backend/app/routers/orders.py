from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from ..database import get_db
from ..models import CreateOrder, UpdateOrderStatus
from ..auth import verify_token
from ..dependencies import require_admin

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("")
async def create_order(order: CreateOrder, payload=Depends(verify_token)):
    user_id = int(payload.get("sub"))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        for item in order.items:
            cursor.execute("SELECT stock FROM products WHERE id = %s FOR UPDATE", (item.product_id,))
            product = cursor.fetchone()
            if not product or product['stock'] < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}. Available: {product['stock'] if product else 0}, Requested: {item.quantity}")
        
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status, delivery_address, created_at) VALUES (%s, %s, %s, %s, %s)",
            (user_id, order.total_amount, order.status, "Pakistan", datetime.now())
        )
        order_id = cursor.lastrowid
        
        for item in order.items:
            cursor.execute("SELECT price FROM products WHERE id = %s", (item.product_id,))
            product = cursor.fetchone()
            
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (order_id, item.product_id, item.quantity, product['price'])
            )
            
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item.quantity, item.product_id)
            )
            
            cursor.execute("SELECT stock FROM products WHERE id = %s", (item.product_id,))
            new_stock = cursor.fetchone()['stock']
            old_stock = new_stock + item.quantity
            
            cursor.execute(
                "INSERT INTO inventory_logs (product_id, old_stock, new_stock, action) VALUES (%s, %s, %s, %s)",
                (item.product_id, old_stock, new_stock, "order_placed")
            )
        
        conn.commit()
        
        return {"message": "Order created successfully", "order_id": order_id}
    
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int, credentials=Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT id, user_id, total_amount, status, delivery_address, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        orders = cursor.fetchall()
        
        for order in orders:
            cursor.execute(
                "SELECT oi.product_id, p.name as product_name, oi.quantity, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = %s",
                (order['id'],)
            )
            order['items'] = cursor.fetchall()
        
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/admin/orders")
async def get_admin_orders(payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT o.id, o.user_id, u.name as customer_name, u.phone as customer_phone, o.total_amount, o.status, o.delivery_address, o.created_at FROM orders o JOIN users u ON o.user_id = u.id ORDER BY o.created_at DESC"
        )
        orders = cursor.fetchall()
        
        for order in orders:
            cursor.execute(
                "SELECT oi.product_id, p.name as product_name, oi.quantity, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = %s",
                (order['id'],)
            )
            order['items'] = cursor.fetchall()
        
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/admin/orders/{order_id}")
async def update_order_status(order_id: int, update: UpdateOrderStatus, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    admin_id = int(payload.get("sub"))
    
    try:
        cursor.execute("UPDATE orders SET status = %s, updated_at = %s WHERE id = %s", 
                      (update.status, datetime.now(), order_id))
        
        cursor.execute(
            "INSERT INTO activity_logs (admin_id, action, details) VALUES (%s, %s, %s)",
            (admin_id, f"Order {order_id} status updated", f"New status: {update.status}")
        )
        
        conn.commit()
        return {"message": "Order status updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
