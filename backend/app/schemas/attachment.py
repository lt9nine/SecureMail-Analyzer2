"""
Attachment Pydantic schemas for API validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AttachmentBase(BaseModel):
    """Base attachment schema"""
    filename: str = Field(..., max_length=500)
    content_type: str = Field(..., max_length=255)
    size_bytes: int = Field(..., ge=0)

class AttachmentResponse(AttachmentBase):
    """Schema for attachment responses"""
    id: int
    email_id: int
    sha256_hash: Optional[str] = None
    md5_hash: Optional[str] = None
    size_formatted: str
    file_path: Optional[str] = None
    is_stored: bool
    is_suspicious: bool
    analysis_score: Optional[float] = None
    risk_level: Optional[str] = None
    virustotal_results: Optional[Dict[str, Any]] = None
    content_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 