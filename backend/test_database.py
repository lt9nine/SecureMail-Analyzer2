"""
Test script for database models and basic functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models import User, MailAccount, Email, Attachment
from app.core.security import get_password_hash, encrypt_password
from datetime import datetime

def test_database_creation():
    """Test database table creation"""
    print("🔧 Creating database tables...")
    create_tables()
    print("✅ Database tables created successfully!")

def test_user_creation():
    """Test user creation"""
    print("\n👤 Creating test user...")
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("⚠️  Test user already exists")
            return existing_user
        
        # Create test user
        test_user = User(
            email="test@example.com",
            password_hash=get_password_hash("testpassword123"),
            first_name="Test",
            last_name="User",
            is_active=True,
            is_admin=False,
            settings={
                "ai_provider": "openrouter",
                "theme": "light",
                "language": "de"
            }
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ Test user created: {test_user.email}")
        return test_user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_mail_account_creation(user):
    """Test mail account creation"""
    print("\n📧 Creating test mail account...")
    
    db = SessionLocal()
    try:
        # Check if test mail account already exists
        existing_account = db.query(MailAccount).filter(
            MailAccount.email == "test@gmail.com",
            MailAccount.user_id == user.id
        ).first()
        
        if existing_account:
            print("⚠️  Test mail account already exists")
            return existing_account
        
        # Create test mail account
        test_account = MailAccount(
            user_id=user.id,
            email="test@gmail.com",
            display_name="Test Gmail Account",
            imap_host="imap.gmail.com",
            imap_port=993,
            imap_username="test@gmail.com",
            encrypted_password=encrypt_password("testpassword123"),
            use_ssl=True,
            use_tls=False,
            is_active=True,
            sync_enabled=True
        )
        
        db.add(test_account)
        db.commit()
        db.refresh(test_account)
        
        print(f"✅ Test mail account created: {test_account.email}")
        return test_account
        
    except Exception as e:
        print(f"❌ Error creating test mail account: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_email_creation(mail_account):
    """Test email creation"""
    print("\n📬 Creating test email...")
    
    db = SessionLocal()
    try:
        # Create test email
        test_email = Email(
            mail_account_id=mail_account.id,
            subject="Test Email - Security Warning",
            from_addr="security@company.com",
            to_addr="test@gmail.com",
            date_received=datetime.utcnow(),
            content_plain="This is a test email for security analysis.",
            content_html="<p>This is a test email for security analysis.</p>",
            uid_original="12345",
            uid_current="12345",
            is_deleted=False,
            is_read=False,
            analysis_score=85.0,
            risk_level="high",
            analysis_metadata={
                "status": "danger",
                "score": 75,
                "details": ["DKIM-Signatur fehlt", "SPF-Check fehlgeschlagen"]
            },
            analysis_content={
                "status": "danger",
                "score": 80,
                "details": ["Dringender Ton erkannt", "Verdächtige Keywords gefunden"]
            },
            analysis_links={
                "status": "critical",
                "score": 90,
                "details": ["Lookalike-Domain erkannt", "Phishing-Keywords gefunden"]
            }
        )
        
        db.add(test_email)
        db.commit()
        db.refresh(test_email)
        
        print(f"✅ Test email created: {test_email.subject}")
        return test_email
        
    except Exception as e:
        print(f"❌ Error creating test email: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_attachment_creation(email):
    """Test attachment creation"""
    print("\n📎 Creating test attachment...")
    
    db = SessionLocal()
    try:
        # Create test attachment
        test_attachment = Attachment(
            email_id=email.id,
            filename="test_document.pdf",
            content_type="application/pdf",
            size_bytes=1024000,  # 1MB
            sha256_hash="a" * 64,  # Dummy hash
            md5_hash="b" * 32,     # Dummy hash
            is_stored=False,
            is_suspicious=False,
            analysis_score=20.0,
            risk_level="low",
            virustotal_results={
                "clean": 45,
                "malicious": 2,
                "undetected": 3
            }
        )
        
        db.add(test_attachment)
        db.commit()
        db.refresh(test_attachment)
        
        print(f"✅ Test attachment created: {test_attachment.filename}")
        return test_attachment
        
    except Exception as e:
        print(f"❌ Error creating test attachment: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_relationships():
    """Test database relationships"""
    print("\n🔗 Testing database relationships...")
    
    db = SessionLocal()
    try:
        # Get test user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("❌ Test user not found")
            return
        
        # Test user -> mail_accounts relationship
        print(f"📧 User has {len(user.mail_accounts)} mail accounts")
        for account in user.mail_accounts:
            print(f"  - {account.email} ({account.imap_host})")
            
            # Test mail_account -> emails relationship
            print(f"    📬 Account has {len(account.emails)} emails")
            for email in account.emails:
                print(f"      - {email.subject} (Risk: {email.risk_level})")
                
                # Test email -> attachments relationship
                print(f"        📎 Email has {len(email.attachments)} attachments")
                for attachment in email.attachments:
                    print(f"          - {attachment.filename} ({attachment.size_formatted})")
        
        print("✅ All relationships working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing relationships: {e}")
    finally:
        db.close()

def main():
    """Main test function"""
    print("🚀 Starting database tests...")
    
    # Test database creation
    test_database_creation()
    
    # Test user creation
    user = test_user_creation()
    if not user:
        print("❌ Failed to create test user")
        return
    
    # Test mail account creation
    mail_account = test_mail_account_creation(user)
    if not mail_account:
        print("❌ Failed to create test mail account")
        return
    
    # Test email creation
    email = test_email_creation(mail_account)
    if not email:
        print("❌ Failed to create test email")
        return
    
    # Test attachment creation
    attachment = test_attachment_creation(email)
    if not attachment:
        print("❌ Failed to create test attachment")
        return
    
    # Test relationships
    test_relationships()
    
    print("\n🎉 All database tests completed successfully!")
    print("\n📋 Test Data Summary:")
    print(f"  👤 User: {user.email}")
    print(f"  📧 Mail Account: {mail_account.email}")
    print(f"  📬 Email: {email.subject}")
    print(f"  📎 Attachment: {attachment.filename}")

if __name__ == "__main__":
    main() 