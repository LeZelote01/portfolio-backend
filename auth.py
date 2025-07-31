from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt  
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from models import AdminUser, Token, TokenData

# Security configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AdminUser:
    """Get the current authenticated user from JWT token"""
    from motor.motor_asyncio import AsyncIOMotorClient
    
    # MongoDB connection
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_token(credentials.credentials)
        user = await db.admin_users.find_one({"username": token_data.username})
        if user is None:
            raise credentials_exception
            
        # Check if user is active
        admin_user = AdminUser(**user)
        if not admin_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
            
        return admin_user
        
    except JWTError:
        raise credentials_exception
    finally:
        client.close()


async def authenticate_user(username: str, password: str) -> Optional[AdminUser]:
    """Authenticate a user with username and password"""
    from motor.motor_asyncio import AsyncIOMotorClient
    
    # MongoDB connection
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        user = await db.admin_users.find_one({"username": username})
        if not user:
            return None
            
        admin_user = AdminUser(**user)
        if not verify_password(password, admin_user.hashed_password):
            return None
            
        return admin_user
        
    finally:
        client.close()


async def create_default_admin_user():
    """Create a default admin user if none exists"""
    from motor.motor_asyncio import AsyncIOMotorClient
    
    # MongoDB connection
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    try:
        # Check if any admin user exists
        existing_admin = await db.admin_users.find_one()
        if existing_admin:
            print("ℹ️ Admin user already exists")
            return
        
        # Create default admin user
        default_admin = AdminUser(
            username="admin",
            email="admin@jeanyves.dev",
            hashed_password=get_password_hash("admin123"),  # Change this in production!
            is_active=True
        )
        
        await db.admin_users.insert_one(default_admin.dict())
        print("✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  Please change the password in production!")
        
    finally:
        client.close()