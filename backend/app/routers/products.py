from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
import os
import uuid
from datetime import datetime
from sqlalchemy import text
from ..database import get_db
from ..models import Product
from ..auth import verify_token
from ..dependencies import require_admin

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
async def get_products(db=Depends(get_db)):
    try:
        # SQLite doesn't support GROUP_CONCAT the same way, so we'll use a subquery
        result = db.execute(text("""
            SELECT p.id, p.name, p.description, p.price, p.stock, p.category, p.category_id, 
                   p.color, p.material, p.size, p.created_at,
                   (SELECT GROUP_CONCAT(image_url) FROM product_images WHERE product_id = p.id) as image_urls 
            FROM products p 
            WHERE p.stock > 0
        """))
        products = []
        for row in result:
            product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock": row[4],
                "category": row[5],
                "category_id": row[6],
                "color": row[7],
                "material": row[8],
                "size": row[9],
                "created_at": row[10],
                "images": row[11].split(',') if row[11] else []
            }
            products.append(product)
        
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def create_product(product: Product, payload=Depends(require_admin), db=Depends(get_db)):
    try:
        # Check if category exists
        result = db.execute(text("SELECT id FROM categories WHERE id = :category_id"), {"category_id": product.category_id})
        if not result.fetchone():
            raise HTTPException(status_code=400, detail="Category does not exist")
        
        # Get category name
        result = db.execute(text("SELECT name FROM categories WHERE id = :category_id"), {"category_id": product.category_id})
        category_record = result.fetchone()
        category_name = category_record[0] if category_record else product.category
        
        # Insert product
        result = db.execute(text("""
            INSERT INTO products (name, description, price, stock, category, category_id, color, material, size, created_at) 
            VALUES (:name, :description, :price, :stock, :category, :category_id, :color, :material, :size, :created_at)
        """), {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": category_name,
            "category_id": product.category_id,
            "color": product.color,
            "material": product.material,
            "size": product.size,
            "created_at": datetime.now()
        })
        product_id = result.lastrowid
        db.commit()
        return {"message": "Product created", "id": product_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}")
async def update_product(product_id: int, product: Product, payload=Depends(require_admin), db=Depends(get_db)):
    try:
        # Check if category exists
        result = db.execute(text("SELECT id FROM categories WHERE id = :category_id"), {"category_id": product.category_id})
        if not result.fetchone():
            raise HTTPException(status_code=400, detail="Category does not exist")
        
        # Get category name
        result = db.execute(text("SELECT name FROM categories WHERE id = :category_id"), {"category_id": product.category_id})
        category_record = result.fetchone()
        category_name = category_record[0] if category_record else product.category
        
        # Update product
        db.execute(text("""
            UPDATE products SET name = :name, description = :description, price = :price, stock = :stock, 
                           category = :category, category_id = :category_id, color = :color, material = :material, size = :size 
            WHERE id = :product_id
        """), {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": category_name,
            "category_id": product.category_id,
            "color": product.color,
            "material": product.material,
            "size": product.size,
            "product_id": product_id
        })
        db.commit()
        return {"message": "Product updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}")
async def delete_product(product_id: int, payload=Depends(require_admin), db=Depends(get_db)):
    try:
        db.execute(text("DELETE FROM products WHERE id = :product_id"), {"product_id": product_id})
        db.commit()
        return {"message": "Product deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{product_id}/images")
async def upload_product_images(product_id: int, files: List[UploadFile] = File(...), payload=Depends(require_admin), db=Depends(get_db)):
    # Check if product exists
    result = db.execute(text("SELECT id FROM products WHERE id = :product_id"), {"product_id": product_id})
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Product not found")
    
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
            
            db.execute(
                text("INSERT INTO product_images (product_id, image_url, created_at) VALUES (:product_id, :image_url, :created_at)"),
                {"product_id": product_id, "image_url": image_url, "created_at": datetime.now()}
            )
            uploaded_images.append(image_url)
        
        db.commit()
        return {"message": f"{len(uploaded_images)} images uploaded successfully", "image_urls": uploaded_images}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}/images")
async def get_product_images(product_id: int, db=Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT id, image_url, created_at 
            FROM product_images 
            WHERE product_id = :product_id 
            ORDER BY created_at
        """), {"product_id": product_id})
        
        images = []
        for row in result:
            images.append({
                "id": row[0],
                "image_url": row[1],
                "created_at": row[2]
            })
        
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}/images/{image_id}")
async def delete_product_image(product_id: int, image_id: int, payload=Depends(require_admin), db=Depends(get_db)):
    try:
        # Get image URL
        result = db.execute(
            text("SELECT image_url FROM product_images WHERE id = :image_id AND product_id = :product_id"),
            {"image_id": image_id, "product_id": product_id}
        )
        image = result.fetchone()
        
        if not image:
            raise HTTPException(status_code=404, detail="Image not found for this product")
        
        # Delete file from filesystem
        image_path = os.path.join(os.getcwd(), image[0][1:])
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Delete from database
        db.execute(
            text("DELETE FROM product_images WHERE id = :image_id AND product_id = :product_id"),
            {"image_id": image_id, "product_id": product_id}
        )
        
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
