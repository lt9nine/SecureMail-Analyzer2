"""
MailAccount Model for IMAP account management
"""

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class MailAccount(BaseModel):
    """MailAccount model for IMAP account configuration"""
    
    # User relationship
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Account details
    email = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)
    
    # IMAP Configuration
    imap_host = Column(String(255), nullable=False)
    imap_port = Column(Integer, default=993, nullable=False)
    imap_username = Column(String(255), nullable=False)
    encrypted_password = Column(Text, nullable=False)  # AES-256-GCM encrypted
    
    # Connection settings
    use_ssl = Column(Boolean, default=True, nullable=False)
    use_tls = Column(Boolean, default=False, nullable=False)
    
    # Sync settings
    is_active = Column(Boolean, default=True, nullable=False)
    sync_enabled = Column(Boolean, default=True, nullable=False)
    last_sync = Column(String(50), nullable=True)  # Last UID for sync
    
    # Relationships
    user = relationship("User", back_populates="mail_accounts")
    emails = relationship("Email", back_populates="mail_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MailAccount(id={self.id}, email='{self.email}', user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses (without sensitive data)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.email,
            'display_name': self.display_name,
            'imap_host': self.imap_host,
            'imap_port': self.imap_port,
            'imap_username': self.imap_username,
            'use_ssl': self.use_ssl,
            'use_tls': self.use_tls,
            'is_active': self.is_active,
            'sync_enabled': self.sync_enabled,
            'last_sync': self.last_sync,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_password(self):
        """Convert to dictionary including encrypted password (for internal use)"""
        data = self.to_dict()
        data['encrypted_password'] = self.encrypted_password
        return data 