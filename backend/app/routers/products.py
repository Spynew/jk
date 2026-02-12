from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
import os
import uuid
from datetime import datetime
from ..database import get_db
from ..models import Product
from ..auth import verify_token
from ..dependencies import require_admin

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
async def get_products():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT p.id, p.name, p.description, p.price, p.stock, p.category, p.category_id, p.color, p.material, p.size, p.created_at, (SELECT GROUP_CONCAT(image_url) FROM product_images WHERE product_id = p.id) as image_urls FROM products p WHERE p.stock > 0"
        )
        products = cursor.fetchall()
        
        for product in products:
            if product['image_urls']:
                product['images'] = product['image_urls'].split(',')
            else:
                product['images'] = []
            del product['image_urls']
        
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("")
async def create_product(product: Product, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id FROM categories WHERE id = %s", (product.category_id,))
        category_exists = cursor.fetchone()
        if not category_exists:
            raise HTTPException(status_code=400, detail="Category does not exist")
        
        cursor.execute("SELECT name FROM categories WHERE id = %s", (product.category_id,))
        category_record = cursor.fetchone()
        category_name = category_record['name'] if category_record else product.category
        
        cursor.execute(
            "INSERT INTO products (name, description, price, stock, category, category_id, color, material, size, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (product.name, product.description, product.price, product.stock, category_name, product.category_id, product.color, product.material, product.size, datetime.now())
        )
        product_id = cursor.lastrowid
        conn.commit()
        return {"message": "Product created", "id": product_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/{product_id}")
async def update_product(product_id: int, product: Product, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id FROM categories WHERE id = %s", (product.category_id,))
        category_exists = cursor.fetchone()
        if not category_exists:
            raise HTTPException(status_code=400, detail="Category does not exist")
        
        cursor.execute("SELECT name FROM categories WHERE id = %s", (product.category_id,))
        category_record = cursor.fetchone()
        category_name = category_record['name'] if category_record else product.category
        
        cursor.execute(
            "UPDATE products SET name = %s, description = %s, price = %s, stock = %s, category = %s, category_id = %s, color = %s, material = %s, size = %s WHERE id = %s",
            (product.name, product.description, product.price, product.stock, category_name, product.category_id, product.color, product.material, product.size, product_id)
        )
        conn.commit()
        return {"message": "Product updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{product_id}")
async def delete_product(product_id: int, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return {"message": "Product deleted"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/{product_id}/images")
async def upload_product_images(product_id: int, files: List[UploadFile] = File(...), payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    finally:
        cursor.close()
        conn.close()
    
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 images allowed per upload")
    
    MAX_FILE_SIZE = 5 * 1024 * 1024
    for i, file in enumerate(files):
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {i+1} is too large. Maximum size is 5MB.")
    
    uploaded_images = []
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        for i, file in enumerate(files):
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail=f"File {i+1} is not an image")
            
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join("uploads", filename)
            
            contents = await file.read()
            with open(filepath, "wb") as f:
                f.write(contents)
            
            image_url = f"/uploads/{filename}"
            is_primary = (i == 0)
            
            cursor.execute(
                "INSERT INTO product_images (product_id, image_url, is_primary, sort_order) VALUES (%s, %s, %s, %s)",
                (product_id, image_url, is_primary, i)
            )
            uploaded_images.append(image_url)
        
        cursor.execute(
            "UPDATE products SET image_count = (SELECT COUNT(*) FROM product_images WHERE product_id = %s) WHERE id = %s",
            (product_id, product_id)
        )
        
        conn.commit()
        return {"message": f"{len(uploaded_images)} images uploaded successfully", "image_urls": uploaded_images}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/{product_id}/images")
async def get_product_images(product_id: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT id, image_url, is_primary, sort_order FROM product_images WHERE product_id = %s ORDER BY sort_order",
            (product_id,)
        )
        images = cursor.fetchall()
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{product_id}/images/{image_id}")
async def delete_product_image(product_id: int, image_id: int, payload=Depends(require_admin)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT image_url FROM product_images WHERE id = %s AND product_id = %s",
            (image_id, product_id)
        )
        image = cursor.fetchone()
        
        if not image:
            raise HTTPException(status_code=404, detail="Image not found for this product")
        
        image_path = os.path.join(os.getcwd(), image['image_url'][1:])
        if os.path.exists(image_path):
            os.remove(image_path)
        
        cursor.execute(
            "DELETE FROM product_images WHERE id = %s AND product_id = %s",
            (image_id, product_id)
        )
        
        cursor.execute(
            "UPDATE products SET image_count = (SELECT COUNT(*) FROM product_images WHERE product_id = %s) WHERE id = %s",
            (product_id, product_id)
        )
        
        conn.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
