from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from datetime import timedelta, datetime

from models import AdminLogin, Token, AdminUser, AdminUserCreate, PasswordChange, AdminUpdate
from auth import authenticate_user, create_access_token, get_current_user, create_default_admin_user, get_password_hash

# Create auth router
auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/login", response_model=Token)
async def login(login_data: AdminLogin):
    """Login endpoint for admin users"""
    user = await authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login time
    from motor.motor_asyncio import AsyncIOMotorClient
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        await db.admin_users.update_one(
            {"id": user.id},
            {"$set": {"last_login": datetime.utcnow()}}
        )
    finally:
        client.close()
    
    # Create access token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=AdminUser)
async def read_users_me(current_user: AdminUser = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@auth_router.post("/create-admin", response_model=AdminUser)
async def create_admin_user(
    admin_data: AdminUserCreate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Create a new admin user (requires authentication)"""
    from motor.motor_asyncio import AsyncIOMotorClient
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        # Check if username already exists
        existing_user = await db.admin_users.find_one({"username": admin_data.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email already exists
        existing_email = await db.admin_users.find_one({"email": admin_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Create new admin user
        new_admin = AdminUser(
            username=admin_data.username,
            email=admin_data.email,
            hashed_password=get_password_hash(admin_data.password),
            is_active=True
        )
        
        await db.admin_users.insert_one(new_admin.dict())
        return new_admin
        
    finally:
        client.close()


@auth_router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: AdminUser = Depends(get_current_user)
):
    """Change current user's password"""
    from motor.motor_asyncio import AsyncIOMotorClient
    from auth import verify_password
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        new_hashed_password = get_password_hash(password_data.new_password)
        await db.admin_users.update_one(
            {"id": current_user.id},
            {"$set": {"hashed_password": new_hashed_password}}
        )
        
        return {"message": "Password changed successfully"}
        
    finally:
        client.close()


@auth_router.put("/update-profile", response_model=AdminUser)
async def update_admin_profile(
    profile_data: AdminUpdate,
    current_user: AdminUser = Depends(get_current_user)
):
    """Update current user's profile information"""
    from motor.motor_asyncio import AsyncIOMotorClient
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        update_data = {}
        
        # Check if username is being updated and if it's unique
        if profile_data.username and profile_data.username != current_user.username:
            existing_user = await db.admin_users.find_one({
                "username": profile_data.username,
                "id": {"$ne": current_user.id}
            })
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            update_data["username"] = profile_data.username
        
        # Check if email is being updated and if it's unique
        if profile_data.email and profile_data.email != current_user.email:
            existing_email = await db.admin_users.find_one({
                "email": profile_data.email,
                "id": {"$ne": current_user.id}
            })
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            update_data["email"] = profile_data.email
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No changes provided"
            )
        
        # Update user profile
        update_data["updated_at"] = datetime.utcnow()
        await db.admin_users.update_one(
            {"id": current_user.id},
            {"$set": update_data}
        )
        
        # Return updated user
        updated_user = await db.admin_users.find_one({"id": current_user.id})
        return AdminUser(**updated_user)
        
    finally:
        client.close()


@auth_router.post("/init-admin")
async def initialize_admin():
    """Initialize default admin user (public endpoint for first setup)"""
    await create_default_admin_user()
    return {"message": "Admin initialization completed"}