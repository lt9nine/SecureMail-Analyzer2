"""
Pydantic Schemas Package
"""

from .user import UserCreate, UserUpdate, UserResponse, UserLogin, UserRegister
from .mail_account import MailAccountCreate, MailAccountUpdate, MailAccountResponse
from .email import EmailResponse, EmailPreview, EmailListResponse
from .attachment import AttachmentResponse
from .auth import TokenResponse, TokenData

__all__ = [
    'UserCreate', 'UserUpdate', 'UserResponse', 'UserLogin', 'UserRegister',
    'MailAccountCreate', 'MailAccountUpdate', 'MailAccountResponse',
    'EmailResponse', 'EmailPreview', 'EmailListResponse',
    'AttachmentResponse',
    'TokenResponse', 'TokenData'
] 