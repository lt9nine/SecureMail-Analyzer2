"""
Email Model for storing email data and analysis results
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class Email(BaseModel):
    """Email model for storing email data and analysis results"""
    
    # MailAccount relationship
    mail_account_id = Column(Integer, ForeignKey('mailaccount.id'), nullable=False)
    
    # Email metadata
    subject = Column(String(500), nullable=False)
    from_addr = Column(String(255), nullable=False)
    to_addr = Column(String(255), nullable=False)
    cc_addr = Column(Text, nullable=True)  # Comma-separated
    bcc_addr = Column(Text, nullable=True)  # Comma-separated
    date_received = Column(DateTime(timezone=True), nullable=False)
    
    # Email content
    content_plain = Column(Text, nullable=True)
    content_html = Column(Text, nullable=True)
    
    # IMAP UIDs
    uid_original = Column(String(50), nullable=False)  # Original UID from IMAP
    uid_current = Column(String(50), nullable=True)    # Current UID (may change)
    
    # Status flags
    is_deleted = Column(Boolean, default=False, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    
    # Deletion tracking
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Analysis results
    analysis_score = Column(Float, nullable=True)  # Overall risk score 0-100
    risk_level = Column(String(20), nullable=True)  # low, medium, high, critical
    
    # Detailed analysis (JSON)
    analysis_metadata = Column(JSON, nullable=True)    # DKIM, SPF, DMARC results
    analysis_headers = Column(JSON, nullable=True)     # Header analysis
    analysis_content = Column(JSON, nullable=True)     # Content analysis
    analysis_links = Column(JSON, nullable=True)       # Link analysis
    analysis_attachments = Column(JSON, nullable=True) # Attachment analysis
    analysis_ai = Column(JSON, nullable=True)          # AI analysis results
    
    # Relationships
    mail_account = relationship("MailAccount", back_populates="emails")
    attachments = relationship("Attachment", back_populates="email", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject[:50]}...', from_addr='{self.from_addr}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'mail_account_id': self.mail_account_id,
            'subject': self.subject,
            'from_addr': self.from_addr,
            'to_addr': self.to_addr,
            'cc_addr': self.cc_addr,
            'bcc_addr': self.bcc_addr,
            'date_received': self.date_received.isoformat() if self.date_received else None,
            'content_plain': self.content_plain,
            'content_html': self.content_html,
            'uid_original': self.uid_original,
            'uid_current': self.uid_current,
            'is_deleted': self.is_deleted,
            'is_read': self.is_read,
            'is_flagged': self.is_flagged,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'analysis_score': self.analysis_score,
            'risk_level': self.risk_level,
            'analysis_metadata': self.analysis_metadata,
            'analysis_headers': self.analysis_headers,
            'analysis_content': self.analysis_content,
            'analysis_links': self.analysis_links,
            'analysis_attachments': self.analysis_attachments,
            'analysis_ai': self.analysis_ai,
            'attachments_count': len(self.attachments) if self.attachments else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_preview(self):
        """Convert to dictionary for email list preview (without full content)"""
        return {
            'id': self.id,
            'mail_account_id': self.mail_account_id,
            'subject': self.subject,
            'from_addr': self.from_addr,
            'to_addr': self.to_addr,
            'date_received': self.date_received.isoformat() if self.date_received else None,
            'is_deleted': self.is_deleted,
            'is_read': self.is_read,
            'is_flagged': self.is_flagged,
            'analysis_score': self.analysis_score,
            'risk_level': self.risk_level,
            'attachments_count': len(self.attachments) if self.attachments else 0,
            'preview': self._generate_preview(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def _generate_preview(self):
        """Generate email preview text"""
        if self.content_plain:
            # Use plain text content for preview
            preview = self.content_plain.strip()
            if len(preview) > 200:
                preview = preview[:200] + "..."
            return preview
        elif self.content_html:
            # Strip HTML tags for preview
            import re
            clean_text = re.sub(r'<[^>]+>', '', self.content_html)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            if len(clean_text) > 200:
                clean_text = clean_text[:200] + "..."
            return clean_text
        else:
            return "Kein Inhalt verfügbar"
    
    @property
    def has_attachments(self):
        """Check if email has attachments"""
        return len(self.attachments) > 0 if self.attachments else False 