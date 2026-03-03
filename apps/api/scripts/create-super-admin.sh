#!/bin/bash

echo "🔧 Creating super admin user..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the apps/api directory"
    exit 1
fi

# Get phone number from user or use default
PHONE=${1:-"+1234567890"}
EMAIL=${2:-"superadmin@laundromate.com"}
FIRST_NAME=${3:-"Super"}
LAST_NAME=${4:-"Admin"}

echo "📱 Creating user with:"
echo "   Phone: $PHONE"
echo "   Email: $EMAIL"
echo "   Name: $FIRST_NAME $LAST_NAME"

# Run Python script to create super admin
python3 << EOF
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.models.user import User
from app.core.config.settings import settings

# Create database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Check if user already exists
    existing_user = db.query(User).filter(User.phone == "$PHONE").first()
    if existing_user:
        print(f"⚠️  User with phone $PHONE already exists. Updating to super admin...")
        existing_user.is_super_admin = True
        existing_user.is_admin = True
        existing_user.is_active = True
        if "$EMAIL" and not existing_user.email:
            existing_user.email = "$EMAIL"
        if "$FIRST_NAME" and not existing_user.first_name:
            existing_user.first_name = "$FIRST_NAME"
        if "$LAST_NAME" and not existing_user.last_name:
            existing_user.last_name = "$LAST_NAME"
        db.commit()
        db.refresh(existing_user)
        print(f"✅ Updated user to super admin!")
        print(f"   User ID: {existing_user.id}")
        print(f"   Phone: {existing_user.phone}")
        print(f"   Email: {existing_user.email}")
        print(f"   Super Admin: {existing_user.is_super_admin}")
    else:
        # Create new super admin user
        user = User(
            phone="$PHONE",
            email="$EMAIL" if "$EMAIL" else None,
            first_name="$FIRST_NAME",
            last_name="$LAST_NAME",
            is_super_admin=True,
            is_admin=True,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Super admin user created successfully!")
        print(f"   User ID: {user.id}")
        print(f"   Phone: {user.phone}")
        print(f"   Email: {user.email}")
        print(f"   Super Admin: {user.is_super_admin}")
finally:
    db.close()
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Super admin user created!"
    echo ""
    echo "📱 Next steps:"
    echo "   1. Request OTP at /auth/otp/request with phone: $PHONE"
    echo "   2. Verify OTP at /auth/otp/verify"
    echo "   3. Use the returned access_token to access super admin routes"
else
    echo "❌ Failed to create super admin user"
    exit 1
fi
