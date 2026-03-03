#!/usr/bin/env python3
"""
Script to create a super admin user in the database.
Usage: python scripts/create_super_admin.py [phone] [email] [first_name] [last_name]
"""

import sys
from pathlib import Path

# Add parent directory to path so app imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.core.config.settings import settings  # noqa: E402
from app.core.models.user import User  # noqa: E402


def create_super_admin(
    phone: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
):
    """Create or update a super admin user."""
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.phone == phone).first()
        if existing_user:
            print(
                f"⚠️  User with phone {phone} already exists. "
                "Updating to super admin..."
            )
            existing_user.is_super_admin = True
            existing_user.is_admin = True
            existing_user.is_active = True
            if email and not existing_user.email:
                existing_user.email = email
            if first_name and not existing_user.first_name:
                existing_user.first_name = first_name
            if last_name and not existing_user.last_name:
                existing_user.last_name = last_name
            db.commit()
            db.refresh(existing_user)
            print("✅ Updated user to super admin!")
            print(f"   User ID: {existing_user.id}")
            print(f"   Phone: {existing_user.phone}")
            print(f"   Email: {existing_user.email}")
            print(f"   Name: {existing_user.first_name} {existing_user.last_name}")
            print(f"   Super Admin: {existing_user.is_super_admin}")
            return existing_user
        else:
            # Create new super admin user
            user = User(
                phone=phone,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_super_admin=True,
                is_admin=True,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("✅ Super admin user created successfully!")
            print(f"   User ID: {user.id}")
            print(f"   Phone: {user.phone}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Super Admin: {user.is_super_admin}")
            return user
    finally:
        db.close()


if __name__ == "__main__":
    # Get arguments or use defaults
    phone = sys.argv[1] if len(sys.argv) > 1 else "+1234567890"
    email = sys.argv[2] if len(sys.argv) > 2 else "superadmin@laundromate.com"
    first_name = sys.argv[3] if len(sys.argv) > 3 else "Super"
    last_name = sys.argv[4] if len(sys.argv) > 4 else "Admin"

    print("📱 Creating super admin user with:")
    print(f"   Phone: {phone}")
    print(f"   Email: {email}")
    print(f"   Name: {first_name} {last_name}")
    print()

    create_super_admin(phone, email, first_name, last_name)

    print()
    print("🎉 Super admin user created!")
    print()
    print("📱 Next steps:")
    print("   1. Sign in via the IdP (Auth0/Clerk/etc.) using the email above")
    print("   2. Ensure this user's email is linked in the IdP to get an access token")
    print("   3. Use the access token to access super admin routes (e.g. /auth/me)")
