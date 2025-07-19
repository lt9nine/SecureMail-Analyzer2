"""
User Pydantic schemas for API validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

class UserRegister(UserCreate):
    """Schema for user registration"""
    pass

class UserUpdate(BaseModel):
    """Schema for user updates"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    settings: Optional[Dict[str, Any]] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Schema for user responses"""
    id: int
    is_active: bool
    is_admin: bool
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    """Schema for user profile (without sensitive data)"""
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    is_active: bool
    is_admin: bool
    settings: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True 