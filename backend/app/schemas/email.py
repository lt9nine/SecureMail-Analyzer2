"""
Email Pydantic schemas for API validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class EmailBase(BaseModel):
    """Base email schema"""
    subject: str = Field(..., max_length=500)
    from_addr: str = Field(..., max_length=255)
    to_addr: str = Field(..., max_length=255)
    cc_addr: Optional[str] = None
    bcc_addr: Optional[str] = None
    date_received: datetime
    content_plain: Optional[str] = None
    content_html: Optional[str] = None

class EmailResponse(EmailBase):
    """Schema for email responses"""
    id: int
    mail_account_id: int
    uid_original: str
    uid_current: Optional[str] = None
    is_deleted: bool
    is_read: bool
    is_flagged: bool
    deleted_at: Optional[datetime] = None
    analysis_score: Optional[float] = None
    risk_level: Optional[str] = None
    analysis_metadata: Optional[Dict[str, Any]] = None
    analysis_headers: Optional[Dict[str, Any]] = None
    analysis_content: Optional[Dict[str, Any]] = None
    analysis_links: Optional[Dict[str, Any]] = None
    analysis_attachments: Optional[Dict[str, Any]] = None
    analysis_ai: Optional[Dict[str, Any]] = None
    attachments_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmailPreview(BaseModel):
    """Schema for email list preview"""
    id: int
    mail_account_id: int
    subject: str
    from_addr: str
    to_addr: str
    date_received: datetime
    is_deleted: bool
    is_read: bool
    is_flagged: bool
    analysis_score: Optional[float] = None
    risk_level: Optional[str] = None
    attachments_count: int
    preview: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmailListResponse(BaseModel):
    """Schema for email list responses"""
    emails: List[EmailPreview]
    total: int
    page: int
    per_page: int
    total_pages: int 