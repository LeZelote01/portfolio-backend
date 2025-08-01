#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur
Usage: python create_admin.py
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from passlib.context import CryptContext

# Add current directory to path to import models
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from models import AdminUser

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("🔄 Creating admin user...")
    
    # Check if admin already exists
    existing = await db.admin_users.find_one({"username": "admin"})
    if existing:
        print("ℹ️ Admin user already exists, skipping...")
        return
    
    # Hash password
    hashed_password = pwd_context.hash("admin123")
    
    # Create admin user
    admin_user = AdminUser(
        username="admin",
        email="admin@jeanyves.dev",
        hashed_password=hashed_password,
        is_active=True
    )
    
    await db.admin_users.insert_one(admin_user.dict())
    print("✅ Admin user created successfully")
    print("   Username: admin")
    print("   Password: admin123")

async def main():
    """Main function"""
    print("🚀 Creating admin user...")
    print(f"📍 MongoDB URL: {mongo_url}")
    print(f"📍 Database: {os.environ.get('DB_NAME', 'test_database')}")
    print()
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        print()
        
        # Create admin user
        await create_admin_user()
        
        print()
        print("🎉 Admin user creation completed!")
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {str(e)}")
        sys.exit(1)
    
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())