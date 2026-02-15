#!/usr/bin/env python3
"""
Initialize SQLite database with basic data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, init_db
from sqlalchemy import text
from app.auth import hash_password

def init_basic_data():
    """Initialize database with basic categories and admin user"""
    
    # Initialize tables first
    init_db()
    
    with engine.connect() as conn:
        # Insert basic categories
        categories = [
            ("Handbags", "Fashionable handbags for all occasions"),
            ("Backpacks", "Durable backpacks for work and travel"),
            ("Wallets", "Stylish wallets for men and women"),
            ("Travel Bags", "Spacious bags for your travel needs"),
            ("Crossbody Bags", "Convenient crossbody bags for daily use"),
            ("Laptop Bags", "Protective bags for your laptops"),
            ("Duffel Bags", "Large duffel bags for gym and travel"),
            ("Clutch Bags", "Elegant clutch bags for special events"),
            ("Tote Bags", "Versatile tote bags for shopping and work"),
            ("Messenger Bags", "Professional messenger bags"),
            ("Sling Bags", "Compact sling bags for casual use"),
            ("Briefcases", "Professional briefcases for business"),
            ("School Bags", "Durable bags for students"),
            ("Sports Bags", "Specialized bags for sports activities"),
            ("Fashion Bags", "Trendy fashion bags"),
            ("Business Bags", "Professional business bags"),
            ("Casual Bags", "Comfortable casual bags"),
            ("Luxury Bags", "Premium luxury bags")
        ]
        
        for name, description in categories:
            try:
                conn.execute(text("""
                    INSERT OR IGNORE INTO categories (name, description) 
                    VALUES (:name, :description)
                """), {"name": name, "description": description})
            except Exception as e:
                print(f"Error inserting category {name}: {e}")
        
        # Insert default admin user
        admin_email = "admin@ssbags.com"
        admin_password = "admin123"  # Change this in production!
        hashed_password = hash_password(admin_password)
        
        try:
            conn.execute(text("""
                INSERT OR IGNORE INTO admins (name, email, password, role) 
                VALUES (:name, :email, :password, :role)
            """), {
                "name": "Admin User",
                "email": admin_email,
                "password": hashed_password,
                "role": "admin"
            })
        except Exception as e:
            print(f"Error inserting admin user: {e}")
        
        conn.commit()
        print("✅ Database initialized successfully!")
        print(f"📧 Admin email: {admin_email}")
        print(f"🔑 Admin password: {admin_password}")
        print("⚠️  Remember to change the admin password in production!")

if __name__ == "__main__":
    init_basic_data()
