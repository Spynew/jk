from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from sqlalchemy import text
from ..database import get_db
from ..models import CreateOrder, UpdateOrderStatus
from ..auth import verify_token
from ..dependencies import require_admin

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("")
async def create_order(order: CreateOrder, payload=Depends(verify_token), db=Depends(get_db)):
    user_id = int(payload.get("sub"))
    
    try:
        # Check if user exists
        result = db.execute(text("SELECT phone FROM users WHERE id = :user_id"), {"user_id": user_id})
        user = result.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check stock for all items
        for item in order.items:
            result = db.execute(text("SELECT stock FROM products WHERE id = :product_id"), {"product_id": item.product_id})
            product = result.fetchone()
            if not product or product[0] < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}. Available: {product[0] if product else 0}, Requested: {item.quantity}")
        
        # Create order
        result = db.execute(text("""
            INSERT INTO orders (user_id, total_amount, status, delivery_address, created_at) 
            VALUES (:user_id, :total_amount, :status, :delivery_address, :created_at)
        """), {
            "user_id": user_id,
            "total_amount": order.total_amount,
            "status": order.status,
            "delivery_address": "Pakistan",
            "created_at": datetime.now()
        })
        order_id = result.lastrowid
        
        # Add order items and update stock
        for item in order.items:
            # Get product price
            result = db.execute(text("SELECT price FROM products WHERE id = :product_id"), {"product_id": item.product_id})
            product = result.fetchone()
            
            # Add order item
            db.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, price, created_at) 
                VALUES (:order_id, :product_id, :quantity, :price, :created_at)
            """), {
                "order_id": order_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product[0],
                "created_at": datetime.now()
            })
            
            # Update product stock
            db.execute(text("UPDATE products SET stock = stock - :quantity WHERE id = :product_id"), {
                "quantity": item.quantity,
                "product_id": item.product_id
            })
        
        db.commit()
        return {"message": "Order created successfully", "order_id": order_id}
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int, credentials=Depends(verify_token), db=Depends(get_db)):
    try:
        # Get orders
        result = db.execute(text("""
            SELECT id, user_id, total_amount, status, delivery_address, created_at 
            FROM orders 
            WHERE user_id = :user_id 
            ORDER BY created_at DESC
        """), {"user_id": user_id})
        
        orders = []
        for row in result:
            order = {
                "id": row[0],
                "user_id": row[1],
                "total_amount": float(row[2]),
                "status": row[3],
                "delivery_address": row[4],
                "created_at": row[5],
                "items": []
            }
            
            # Get order items
            items_result = db.execute(text("""
                SELECT oi.product_id, p.name as product_name, oi.quantity, p.price 
                FROM order_items oi 
                JOIN products p ON oi.product_id = p.id 
                WHERE oi.order_id = :order_id
            """), {"order_id": order["id"]})
            
            for item_row in items_result:
                order["items"].append({
                    "product_id": item_row[0],
                    "product_name": item_row[1],
                    "quantity": item_row[2],
                    "price": float(item_row[3])
                })
            
            orders.append(order)
        
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/orders")
async def get_admin_orders(payload=Depends(require_admin), db=Depends(get_db)):
    try:
        # Get orders with user info
        result = db.execute(text("""
            SELECT o.id, o.user_id, u.name as customer_name, u.phone as customer_phone, 
                   o.total_amount, o.status, o.delivery_address, o.created_at 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            ORDER BY o.created_at DESC
        """))
        
        orders = []
        for row in result:
            order = {
                "id": row[0],
                "user_id": row[1],
                "customer_name": row[2],
                "customer_phone": row[3],
                "total_amount": float(row[4]),
                "status": row[5],
                "delivery_address": row[6],
                "created_at": row[7],
                "items": []
            }
            
            # Get order items
            items_result = db.execute(text("""
                SELECT oi.product_id, p.name as product_name, oi.quantity, p.price 
                FROM order_items oi 
                JOIN products p ON oi.product_id = p.id 
                WHERE oi.order_id = :order_id
            """), {"order_id": order["id"]})
            
            for item_row in items_result:
                order["items"].append({
                    "product_id": item_row[0],
                    "product_name": item_row[1],
                    "quantity": item_row[2],
                    "price": float(item_row[3])
                })
            
            orders.append(order)
        
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/orders/{order_id}")
async def update_order_status(order_id: int, update: UpdateOrderStatus, payload=Depends(require_admin), db=Depends(get_db)):
    admin_id = int(payload.get("sub"))
    
    try:
        # Update order status
        db.execute(text("UPDATE orders SET status = :status, updated_at = :updated_at WHERE id = :order_id"), {
            "status": update.status,
            "updated_at": datetime.now(),
            "order_id": order_id
        })
        
        # Note: activity_logs table doesn't exist in our schema, so we'll skip this for now
        # If you need activity logging, we can add that table later
        
        db.commit()
        return {"message": "Order status updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
