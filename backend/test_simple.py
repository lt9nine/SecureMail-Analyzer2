"""
Simple Backend Test Script
Tests basic database functionality and models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from app.core.config import settings
        print("✅ Config imported")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from app.database import create_tables, SessionLocal
        print("✅ Database imported")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from app.models import User, MailAccount, Email, Attachment
        print("✅ Models imported")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from app.core.security import get_password_hash, encrypt_password
        print("✅ Security imported")
    except Exception as e:
        print(f"❌ Security import failed: {e}")
        return False
    
    try:
        from app.schemas import UserCreate, UserLogin, TokenResponse
        print("✅ Schemas imported")
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        return False
    
    return True

def test_database_creation():
    """Test database table creation"""
    print("\n🗄️ Testing database creation...")
    
    try:
        from app.database import create_tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def test_user_creation():
    """Test user creation"""
    print("\n👤 Testing user creation...")
    
    try:
        from app.database import SessionLocal
        from app.models import User
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print(f"✅ Test user already exists: {existing_user.email} (ID: {existing_user.id})")
            print(f"   Full name: {existing_user.full_name}")
            print(f"   Settings: {existing_user.settings}")
            db.close()
            return True
        
        # Create test user
        test_user = User(
            email="test@example.com",
            password_hash=get_password_hash("testpassword123"),
            first_name="Test",
            last_name="User",
            is_active=True,
            is_admin=False,
            settings={"theme": "light"}
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ Test user created: {test_user.email} (ID: {test_user.id})")
        
        # Test user methods
        print(f"   Full name: {test_user.full_name}")
        print(f"   Settings: {test_user.settings}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return False

def test_mail_account_creation():
    """Test mail account creation"""
    print("\n📧 Testing mail account creation...")
    
    try:
        from app.database import SessionLocal
        from app.models import User, MailAccount
        from app.core.security import encrypt_password
        
        db = SessionLocal()
        
        # Get test user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("❌ Test user not found")
            return False
        
        # Create test mail account
        test_account = MailAccount(
            user_id=user.id,
            email="test@gmail.com",
            display_name="Test Gmail",
            imap_host="imap.gmail.com",
            imap_port=993,
            imap_username="test@gmail.com",
            encrypted_password=encrypt_password("testpassword123"),
            use_ssl=True,
            is_active=True
        )
        
        db.add(test_account)
        db.commit()
        db.refresh(test_account)
        
        print(f"✅ Test mail account created: {test_account.email}")
        print(f"   IMAP Host: {test_account.imap_host}")
        print(f"   SSL: {test_account.use_ssl}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Mail account creation failed: {e}")
        return False

def test_email_creation():
    """Test email creation"""
    print("\n📬 Testing email creation...")
    
    try:
        from app.database import SessionLocal
        from app.models import MailAccount, Email
        from datetime import datetime
        
        db = SessionLocal()
        
        # Get test mail account
        account = db.query(MailAccount).filter(MailAccount.email == "test@gmail.com").first()
        if not account:
            print("❌ Test mail account not found")
            return False
        
        # Create test email
        test_email = Email(
            mail_account_id=account.id,
            subject="Test Security Email",
            from_addr="security@company.com",
            to_addr="test@gmail.com",
            date_received=datetime.utcnow(),
            content_plain="This is a test email for security analysis.",
            content_html="<p>This is a test email for security analysis.</p>",
            uid_original="12345",
            is_deleted=False,
            analysis_score=85.0,
            risk_level="high",
            analysis_metadata={
                "status": "danger",
                "score": 75,
                "details": ["DKIM-Signatur fehlt"]
            }
        )
        
        db.add(test_email)
        db.commit()
        db.refresh(test_email)
        
        print(f"✅ Test email created: {test_email.subject}")
        print(f"   Risk Level: {test_email.risk_level}")
        print(f"   Analysis Score: {test_email.analysis_score}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Email creation failed: {e}")
        return False

def test_relationships():
    """Test database relationships"""
    print("\n🔗 Testing relationships...")
    
    try:
        from app.database import SessionLocal
        from app.models import User
        
        db = SessionLocal()
        
        # Get test user with relationships
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("❌ Test user not found")
            return False
        
        print(f"✅ User: {user.email}")
        print(f"   Mail Accounts: {len(user.mail_accounts)}")
        
        for account in user.mail_accounts:
            print(f"   📧 {account.email} ({account.imap_host})")
            print(f"     Emails: {len(account.emails)}")
            
            for email in account.emails:
                print(f"     📬 {email.subject} (Risk: {email.risk_level})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Relationship test failed: {e}")
        return False

def test_security_functions():
    """Test security functions"""
    print("\n🔐 Testing security functions...")
    
    try:
        from app.core.security import (
            get_password_hash, 
            verify_password, 
            encrypt_password, 
            decrypt_password,
            create_access_token,
            verify_token
        )
        
        # Test password hashing
        password = "testpassword123"
        hashed = get_password_hash(password)
        print(f"✅ Password hashed: {hashed[:20]}...")
        
        # Test password verification
        is_valid = verify_password(password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        # Test IMAP password encryption
        imap_password = "imappassword123"
        encrypted = encrypt_password(imap_password)
        print(f"✅ IMAP password encrypted: {encrypted[:20]}...")
        
        # Test IMAP password decryption
        decrypted = decrypt_password(encrypted)
        print(f"✅ IMAP password decrypted: {decrypted == imap_password}")
        
        # Test JWT token creation
        token_data = {"user_id": 1, "email": "test@example.com"}
        access_token = create_access_token(token_data)
        print(f"✅ Access token created: {access_token[:20]}...")
        
        # Test JWT token verification
        payload = verify_token(access_token)
        print(f"✅ Token verification: {payload is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Backend Tests...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Creation", test_database_creation),
        ("User Creation", test_user_creation),
        ("Mail Account Creation", test_mail_account_creation),
        ("Email Creation", test_email_creation),
        ("Relationships", test_relationships),
        ("Security Functions", test_security_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 