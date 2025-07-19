"""
Mail Account Pydantic schemas for API validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class MailAccountBase(BaseModel):
    """Base mail account schema"""
    email: EmailStr
    display_name: Optional[str] = Field(None, max_length=255)
    imap_host: str = Field(..., max_length=255)
    imap_port: int = Field(993, ge=1, le=65535)
    imap_username: str = Field(..., max_length=255)
    use_ssl: bool = True
    use_tls: bool = False

class MailAccountCreate(MailAccountBase):
    """Schema for mail account creation"""
    password: str = Field(..., min_length=1, max_length=128)

class MailAccountUpdate(BaseModel):
    """Schema for mail account updates"""
    display_name: Optional[str] = Field(None, max_length=255)
    imap_host: Optional[str] = Field(None, max_length=255)
    imap_port: Optional[int] = Field(None, ge=1, le=65535)
    imap_username: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=1, max_length=128)
    use_ssl: Optional[bool] = None
    use_tls: Optional[bool] = None
    is_active: Optional[bool] = None
    sync_enabled: Optional[bool] = None

class MailAccountResponse(MailAccountBase):
    """Schema for mail account responses"""
    id: int
    user_id: int
    is_active: bool
    sync_enabled: bool
    last_sync: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 