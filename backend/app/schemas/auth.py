"""
Authentication Pydantic schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until expiration

class TokenData(BaseModel):
    """Schema for token data (JWT payload)"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = None
    exp: Optional[datetime] = None

class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str

class PasswordChangeRequest(BaseModel):
    """Schema for password change request"""
    current_password: str
    new_password: str
    confirm_new_password: str 