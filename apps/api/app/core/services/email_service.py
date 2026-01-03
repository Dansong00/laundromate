"""Email service for sending emails via SendGrid."""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config.email_config import EmailConfig
from app.core.emails.invitation_templates import InvitationTemplateRendererProtocol


class EmailService:
    """Service for sending emails via SendGrid."""

    def __init__(
        self,
        config: EmailConfig,
        template_renderer: InvitationTemplateRendererProtocol,
    ) -> None:
        """
        Initialize email service with email configuration and template renderer.

        Args:
            config: Email configuration containing SendGrid API key,
                from email, and frontend URL
            template_renderer: Template renderer for generating email content
        """
        self.config = config
        self.template_renderer = template_renderer

    def send_invitation_email(
        self,
        to_email: str,
        store_name: str,
        organization_name: str,
        invitation_token: str,
        expiration_days: int = 7,
    ) -> bool:
        """
        Send an invitation email to a store owner.

        Args:
            to_email: Recipient email address
            store_name: Name of the store
            organization_name: Name of the organization
            invitation_token: Invitation token for the acceptance link
            expiration_days: Number of days until invitation expires

        Returns:
            bool: True if email was sent successfully

        Raises:
            RuntimeError: If SendGrid API key is missing or email sending fails
        """
        if not self.config.sendgrid_api_key:
            raise RuntimeError("SENDGRID_API_KEY is not configured")

        # Build invitation URL
        invitation_url = (
            f"{self.config.frontend_url}/auth/accept-invitation?"
            f"token={invitation_token}"
        )

        # Render email templates
        email_content = self.template_renderer.render_invitation_email(
            store_name=store_name,
            organization_name=organization_name,
            invitation_url=invitation_url,
            expiration_days=expiration_days,
        )

        # Create email message
        message = Mail(
            from_email=self.config.from_email,
            to_emails=to_email,
            subject=email_content.subject,
            html_content=email_content.html_content,
            plain_text_content=email_content.text_content,
        )

        # Send email via SendGrid
        try:
            sg = SendGridAPIClient(self.config.sendgrid_api_key)
            response = sg.send(message)
            if response.status_code in [200, 202]:
                return True
            else:
                raise RuntimeError(
                    f"SendGrid API returned status code {response.status_code}"
                )
        except Exception as e:
            raise RuntimeError(f"Failed to send invitation email: {str(e)}") from e
