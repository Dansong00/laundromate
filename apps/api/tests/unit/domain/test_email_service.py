"""Unit tests for email service."""
from unittest.mock import MagicMock, patch

import pytest
from sendgrid.helpers.mail import Mail

from app.core.models.organization import Organization
from app.core.models.store import Store


class TestEmailService:
    """Test email service functionality."""

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "test-api-key",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_success(
        self, mock_sendgrid_client_class: MagicMock, db_session
    ) -> None:
        """Test successfully sending an invitation email."""
        from app.core.services.email_service import send_invitation_email

        # Setup mock
        mock_sendgrid_client = MagicMock()
        mock_sendgrid_client_class.return_value = mock_sendgrid_client
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.send.return_value = mock_response

        # Create test data
        org = Organization(
            name="Email Org",
            billing_address="123 Email St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Email Store",
            street_address="456 Email Ave",
            city="New York",
            state="NY",
            postal_code="10002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        # Send email
        result = send_invitation_email(
            to_email="owner@example.com",
            store_name=store.name,
            organization_name=org.name,
            invitation_token="test-token-12345",
            expiration_days=7,
        )

        assert result is True
        mock_sendgrid_client.send.assert_called_once()
        call_args = mock_sendgrid_client.send.call_args[0][0]
        assert isinstance(call_args, Mail)
        assert call_args.to[0]["email"] == "owner@example.com"
        assert "Email Store" in call_args.subject
        assert "test-token-12345" in call_args.contents[0].value

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "test-api-key",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_includes_store_name(
        self, mock_sendgrid_client_class: MagicMock
    ) -> None:
        """Test that invitation email includes store name."""
        from app.core.services.email_service import send_invitation_email

        mock_sendgrid_client = MagicMock()
        mock_sendgrid_client_class.return_value = mock_sendgrid_client
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.send.return_value = mock_response

        send_invitation_email(
            to_email="owner@example.com",
            store_name="Test Store",
            organization_name="Test Org",
            invitation_token="token-123",
            expiration_days=7,
        )

        call_args = mock_sendgrid_client.send.call_args[0][0]
        assert "Test Store" in call_args.subject
        assert "Test Store" in call_args.contents[0].value

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "test-api-key",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_includes_invitation_link(
        self, mock_sendgrid_client_class: MagicMock
    ) -> None:
        """Test that invitation email includes invitation link."""
        from app.core.services.email_service import send_invitation_email

        mock_sendgrid_client = MagicMock()
        mock_sendgrid_client_class.return_value = mock_sendgrid_client
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.send.return_value = mock_response

        token = "test-token-abc123"
        send_invitation_email(
            to_email="owner@example.com",
            store_name="Test Store",
            organization_name="Test Org",
            invitation_token=token,
            expiration_days=7,
        )

        call_args = mock_sendgrid_client.send.call_args[0][0]
        email_content = call_args.contents[0].value
        assert token in email_content
        assert "https://app.laundromate.com/auth/accept-invitation" in email_content

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "test-api-key",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_includes_expiration_notice(
        self, mock_sendgrid_client_class: MagicMock
    ) -> None:
        """Test that invitation email includes expiration notice."""
        from app.core.services.email_service import send_invitation_email

        mock_sendgrid_client = MagicMock()
        mock_sendgrid_client_class.return_value = mock_sendgrid_client
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_sendgrid_client.send.return_value = mock_response

        send_invitation_email(
            to_email="owner@example.com",
            store_name="Test Store",
            organization_name="Test Org",
            invitation_token="token-123",
            expiration_days=7,
        )

        call_args = mock_sendgrid_client.send.call_args[0][0]
        email_content = call_args.contents[0].value
        assert "7 days" in email_content or "expires" in email_content.lower()

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "test-api-key",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_handles_sendgrid_error(
        self, mock_sendgrid_client_class: MagicMock
    ) -> None:
        """Test that email service handles SendGrid errors gracefully."""
        from app.core.services.email_service import send_invitation_email

        mock_sendgrid_client = MagicMock()
        mock_sendgrid_client_class.return_value = mock_sendgrid_client
        mock_sendgrid_client.send.side_effect = RuntimeError("SendGrid API error")

        # Should raise exception when SendGrid API fails
        with pytest.raises(RuntimeError):
            send_invitation_email(
                to_email="owner@example.com",
                store_name="Test Store",
                organization_name="Test Org",
                invitation_token="token-123",
                expiration_days=7,
            )

    @patch("app.core.services.email_service.SendGridAPIClient")
    @patch.dict(
        "os.environ",
        {
            "SENDGRID_API_KEY": "",
            "FROM_EMAIL": "noreply@laundromate.com",
            "FRONTEND_URL": "https://app.laundromate.com",
        },
    )
    def test_send_invitation_email_missing_api_key(
        self, mock_sendgrid_client_class: MagicMock
    ) -> None:
        """Test that email service handles missing API key."""
        from app.core.services.email_service import send_invitation_email

        # Should handle missing API key gracefully
        result = send_invitation_email(
            to_email="owner@example.com",
            store_name="Test Store",
            organization_name="Test Org",
            invitation_token="token-123",
            expiration_days=7,
        )

        # Should return False or raise appropriate error
        assert result is False or isinstance(result, Exception)

    def test_send_invitation_email_uses_html_template(self) -> None:
        """Test that email service uses HTML template."""
        # This test verifies that the email service loads and uses the HTML template
        # Implementation should read from
        # apps/api/app/core/templates/invitation_email.html
        pass  # Will be implemented when email service is created

    def test_send_invitation_email_uses_plain_text_template(self) -> None:
        """Test that email service uses plain text template."""
        # This test verifies that the email service loads and uses the
        # plain text template. Implementation should read from
        # apps/api/app/core/templates/invitation_email.txt
        pass  # Will be implemented when email service is created
