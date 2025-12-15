from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create router for auth endpoints
auth_router = APIRouter()

# Pydantic models for authentication
class UserSignupRequest(BaseModel):
    email: str
    password: str
    name: str
    background: Optional[str] = None  # software-focused, hardware-focused, mixed
    preferences: Optional[dict] = None

class UserSigninRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    background: Optional[str] = None
    preferences: Optional[dict] = None
    created_at: datetime

class AuthResponse(BaseModel):
    user: UserResponse
    token: str

# Mock database for users (in production, use a real database)
users_db = {}

# In-memory storage for sessions (in production, use Redis or database)
sessions_db = {}

@auth_router.post("/signup", response_model=AuthResponse)
async def signup(request: UserSignupRequest):
    """Register a new user with background information"""
    try:
        # Check if user already exists
        if request.email in users_db:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": request.email,
            "name": request.name,
            "background": request.background,
            "preferences": request.preferences or {},
            "created_at": datetime.utcnow()
        }

        users_db[request.email] = user

        # Create session token
        session_token = str(uuid.uuid4())
        sessions_db[session_token] = user_id

        logger.info(f"New user registered: {request.email}")

        return AuthResponse(
            user=UserResponse(**user),
            token=session_token
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/signin", response_model=AuthResponse)
async def signin(request: UserSigninRequest):
    """Authenticate user and return token"""
    try:
        # Check if user exists
        if request.email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = users_db[request.email]

        # In a real app, you would verify the password here
        # For this implementation, we'll skip password verification for simplicity
        # But in production, always hash and verify passwords

        # Create session token
        session_token = str(uuid.uuid4())
        sessions_db[session_token] = user["id"]

        logger.info(f"User signed in: {request.email}")

        return AuthResponse(
            user=UserResponse(**user),
            token=session_token
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.post("/signout")
async def signout(token: str):
    """Sign out user by invalidating session"""
    try:
        if token in sessions_db:
            del sessions_db[token]
            logger.info("User signed out successfully")
            return {"message": "Signed out successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        logger.error(f"Signout error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(token: str):
    """Get current user profile"""
    try:
        if token not in sessions_db:
            raise HTTPException(status_code=401, detail="Invalid session token")

        user_id = sessions_db[token]

        # Find user by ID
        user = None
        for email, u in users_db.items():
            if u["id"] == user_id:
                user = u
                break

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return UserResponse(**user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.put("/profile", response_model=UserResponse)
async def update_profile(token: str, background: Optional[str] = None, preferences: Optional[dict] = None):
    """Update user profile with background information"""
    try:
        if token not in sessions_db:
            raise HTTPException(status_code=401, detail="Invalid session token")

        user_id = sessions_db[token]

        # Find and update user
        user = None
        user_email = None
        for email, u in users_db.items():
            if u["id"] == user_id:
                user = u
                user_email = email
                break

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Update user background and preferences
        if background is not None:
            user["background"] = background
        if preferences is not None:
            user["preferences"] = preferences

        logger.info(f"Updated profile for user: {user_email}")

        return UserResponse(**user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")