"""
Attachment Model for storing email attachment information and analysis results
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class Attachment(BaseModel):
    """Attachment model for storing email attachment information"""
    
    # Email relationship
    email_id = Column(Integer, ForeignKey('email.id'), nullable=False)
    
    # Attachment metadata
    filename = Column(String(500), nullable=False)
    content_type = Column(String(255), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    
    # File identification
    sha256_hash = Column(String(64), nullable=True)  # SHA256 hash for VirusTotal
    md5_hash = Column(String(32), nullable=True)     # MD5 hash
    
    # Storage
    file_path = Column(String(1000), nullable=True)  # Path to stored file (if saved)
    is_stored = Column(Boolean, default=False, nullable=False)  # Whether file is saved locally
    
    # Analysis results
    is_suspicious = Column(Boolean, default=False, nullable=False)
    analysis_score = Column(Float, nullable=True)  # Risk score 0-100
    risk_level = Column(String(20), nullable=True)  # low, medium, high, critical
    
    # VirusTotal results (JSON)
    virustotal_results = Column(JSON, nullable=True)
    
    # Content analysis (JSON)
    content_analysis = Column(JSON, nullable=True)  # File type, magic bytes, etc.
    
    # Relationships
    email = relationship("Email", back_populates="attachments")
    
    def __repr__(self):
        return f"<Attachment(id={self.id}, filename='{self.filename}', email_id={self.email_id})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'email_id': self.email_id,
            'filename': self.filename,
            'content_type': self.content_type,
            'size_bytes': self.size_bytes,
            'size_formatted': self._format_size(),
            'sha256_hash': self.sha256_hash,
            'md5_hash': self.md5_hash,
            'is_stored': self.is_stored,
            'is_suspicious': self.is_suspicious,
            'analysis_score': self.analysis_score,
            'risk_level': self.risk_level,
            'virustotal_results': self.virustotal_results,
            'content_analysis': self.content_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def _format_size(self):
        """Format file size in human readable format"""
        if self.size_bytes is None:
            return "Unbekannt"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.size_bytes < 1024.0:
                return f"{self.size_bytes:.1f} {unit}"
            self.size_bytes /= 1024.0
        return f"{self.size_bytes:.1f} TB"
    
    @property
    def is_executable(self):
        """Check if file is potentially executable"""
        executable_types = {
            'application/x-executable',
            'application/x-msdownload',
            'application/x-msi',
            'application/vnd.microsoft.portable-executable',
            'application/x-dosexec',
            'application/x-msdos-program'
        }
        return self.content_type in executable_types
    
    @property
    def is_archive(self):
        """Check if file is an archive"""
        archive_types = {
            'application/zip',
            'application/x-rar-compressed',
            'application/x-7z-compressed',
            'application/x-tar',
            'application/gzip',
            'application/x-bzip2'
        }
        return self.content_type in archive_types
    
    @property
    def is_document(self):
        """Check if file is a document"""
        document_types = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        }
        return self.content_type in document_types
    
    def get_virus_total_stats(self):
        """Get VirusTotal statistics if available"""
        if not self.virustotal_results:
            return None
        
        return {
            'clean': self.virustotal_results.get('clean', 0),
            'malicious': self.virustotal_results.get('malicious', 0),
            'undetected': self.virustotal_results.get('undetected', 0),
            'total': self.virustotal_results.get('total', 0)
        } 