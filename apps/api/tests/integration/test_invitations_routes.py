"""Integration tests for invitation routes."""
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.models.organization import Organization
from app.core.models.user import User
from app.core.models.user_organization import UserOrganization, UserOrganizationRole


class TestValidateInvitation:
    """Test GET /auth/invitations/{token}/validate endpoint."""

    def test_validate_invitation_success(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test successfully validating a valid invitation."""
        org = Organization(
            name="Validate Org",
            billing_address="123 Validate St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567890", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="valid-token-123",
            email="owner@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        response = client.get("/auth/invitations/valid-token-123/validate")

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["email"] == "owner@example.com"
        assert data["organization_id"] == str(org.id)
        assert data["organization_name"] == "Validate Org"
        assert data["organization_role"] == UserOrganizationRole.OWNER.value

    def test_validate_invitation_expired(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test validating an expired invitation."""
        org = Organization(
            name="Expired Org",
            billing_address="789 Expired St",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567891", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="expired-token-456",
            email="expired@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        response = client.get("/auth/invitations/expired-token-456/validate")

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "expired" in data["reason"].lower()

    def test_validate_invitation_already_accepted(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test validating an already accepted invitation."""
        org = Organization(
            name="Accepted Org",
            billing_address="555 Accepted St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567892", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="accepted-token-789",
            email="accepted@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.ACCEPTED,
            accepted_at=datetime.now(timezone.utc),
        )
        db_session.add(invitation)
        db_session.commit()

        response = client.get("/auth/invitations/accepted-token-789/validate")

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "accepted" in data["reason"].lower()

    def test_validate_invitation_invalid_token(self, client: TestClient) -> None:
        """Test validating with an invalid token (not found)."""
        # Use a valid format token that doesn't exist
        response = client.get(
            "/auth/invitations/AbCdEfGhIjKlMnOpQrStUvWxYz123456789012/validate"
        )

        assert response.status_code == 404

    def test_validate_invitation_invalid_token_format(self, client: TestClient) -> None:
        """Test validating with an invalid token format."""
        # Test with invalid format (spaces, special chars, etc.)
        invalid_tokens = [
            "invalid token with spaces",
            "invalid+token+with+plus",
            "short",
            "a" * 100,  # Too long
        ]
        for invalid_token in invalid_tokens:
            response = client.get(f"/auth/invitations/{invalid_token}/validate")
            assert response.status_code == 400
            assert "Invalid invitation token format" in response.json()["detail"]

    def test_validate_invitation_revoked(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test validating a revoked invitation."""
        org = Organization(
            name="Revoked Org",
            billing_address="777 Revoked St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567893", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="revoked-token-abc",
            email="revoked@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.REVOKED,
        )
        db_session.add(invitation)
        db_session.commit()

        response = client.get("/auth/invitations/revoked-token-abc/validate")

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "revoked" in data["reason"].lower()


class TestAcceptInvitation:
    """Test POST /auth/invitations/{token}/accept endpoint."""

    def test_accept_invitation_success(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test successfully accepting an invitation."""
        org = Organization(
            name="Accept Org",
            billing_address="999 Accept St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567894", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="accept-token-123",
            email="newowner@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {"password": "SecurePassword123!"}
        response = client.post(
            "/auth/invitations/accept-token-123/accept", json=payload
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "newowner@example.com"

        # Verify invitation was marked as accepted
        db_session.refresh(invitation)
        assert invitation.status == InvitationStatus.ACCEPTED
        assert invitation.accepted_at is not None

        # Verify user was created
        user = (
            db_session.query(User).filter(User.email == "newowner@example.com").first()
        )
        assert user is not None

        # Verify user-organization association was created
        user_org = (
            db_session.query(UserOrganization)
            .filter(
                UserOrganization.user_id == user.id,
                UserOrganization.organization_id == org.id,
            )
            .first()
        )
        assert user_org is not None
        assert user_org.role == UserOrganizationRole.OWNER

    def test_accept_invitation_existing_user(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test accepting invitation when user already exists."""
        org = Organization(
            name="Existing Org",
            billing_address="111 Existing St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        # Create existing user
        existing_user = User(
            email="existing@example.com",
            phone="+1234567895",
        )
        db_session.add(existing_user)
        db_session.commit()

        inviter = User(phone="+1234567896", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="existing-token-456",
            email="existing@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {"password": "NewPassword123!"}
        response = client.post(
            "/auth/invitations/existing-token-456/accept", json=payload
        )

        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "existing@example.com"
        assert data["user"]["id"] == str(existing_user.id)

        # Verify user-organization association was created
        user_org = (
            db_session.query(UserOrganization)
            .filter(
                UserOrganization.user_id == existing_user.id,
                UserOrganization.organization_id == org.id,
            )
            .first()
        )
        assert user_org is not None
        assert user_org.role == UserOrganizationRole.OWNER

    def test_accept_invitation_expired(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test accepting an expired invitation."""
        org = Organization(
            name="Expired Accept Org",
            billing_address="333 Expired St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567897", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="expired-accept-token",
            email="expired@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {"password": "Password123!"}
        response = client.post(
            "/auth/invitations/expired-accept-token/accept", json=payload
        )

        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower()

    def test_accept_invitation_already_accepted(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test accepting an already accepted invitation."""
        org = Organization(
            name="Already Accepted Org",
            billing_address="555 Already St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567898", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="already-accepted-token",
            email="already@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.ACCEPTED,
            accepted_at=datetime.now(timezone.utc),
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {"password": "Password123!"}
        response = client.post(
            "/auth/invitations/already-accepted-token/accept", json=payload
        )

        assert response.status_code == 400
        assert "accepted" in response.json()["detail"].lower()

    def test_accept_invitation_invalid_token(self, client: TestClient) -> None:
        """Test accepting with an invalid token (not found)."""
        # Use a valid format token that doesn't exist
        payload = {"password": "Password123!"}
        response = client.post(
            "/auth/invitations/AbCdEfGhIjKlMnOpQrStUvWxYz123456789012/accept",
            json=payload,
        )

        assert response.status_code == 404

    def test_accept_invitation_invalid_token_format(self, client: TestClient) -> None:
        """Test accepting with an invalid token format."""
        payload = {"password": "Password123!"}
        invalid_tokens = [
            "invalid token with spaces",
            "invalid+token+with+plus",
            "short",
            "a" * 100,  # Too long
        ]
        for invalid_token in invalid_tokens:
            response = client.post(
                f"/auth/invitations/{invalid_token}/accept", json=payload
            )
            assert response.status_code == 400
            assert "Invalid invitation token format" in response.json()["detail"]

    def test_accept_invitation_weak_password(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test accepting invitation with weak password."""
        org = Organization(
            name="Weak Password Org",
            billing_address="777 Weak St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567899", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="weak-password-token",
            email="weak@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        payload = {"password": "123"}  # Too weak
        response = client.post(
            "/auth/invitations/weak-password-token/accept", json=payload
        )

        assert response.status_code == 422
