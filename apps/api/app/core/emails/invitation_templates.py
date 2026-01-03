"""Email templates for invitation emails."""
from pathlib import Path
from typing import NamedTuple, Protocol

# Template file names
INVITATION_EMAIL_HTML_TEMPLATE = "invitation_email.html"
INVITATION_EMAIL_TEXT_TEMPLATE = "invitation_email.txt"


class InvitationEmailContent(NamedTuple):
    """Rendered email content for invitation emails."""

    html_content: str
    text_content: str
    subject: str


class InvitationTemplateRendererProtocol(Protocol):
    """Protocol for invitation template renderer operations used by EmailService."""

    def render_invitation_email(
        self,
        store_name: str,
        organization_name: str,
        invitation_url: str,
        expiration_days: int = 7,
    ) -> InvitationEmailContent:
        """Render invitation email templates with provided data."""
        ...


class InvitationTemplateRenderer:
    """Renderer for invitation email templates."""

    def __init__(self, template_dir: Path | None = None) -> None:
        """
        Initialize template renderer.

        Args:
            template_dir: Directory containing template files.
                If None, uses default location.
        """
        if template_dir is None:
            # Default to app/core/templates relative to this file
            template_dir = Path(__file__).parent.parent / "templates"
        self.template_dir = template_dir

    def render_invitation_email(
        self,
        store_name: str,
        organization_name: str,
        invitation_url: str,
        expiration_days: int = 7,
    ) -> InvitationEmailContent:
        """
        Render invitation email templates with provided data.

        Args:
            store_name: Name of the store
            organization_name: Name of the organization
            invitation_url: Full URL for accepting the invitation
            expiration_days: Number of days until invitation expires

        Returns:
            InvitationEmailContent with rendered HTML, text, and subject
        """
        html_template = self._load_template(INVITATION_EMAIL_HTML_TEMPLATE)
        text_template = self._load_template(INVITATION_EMAIL_TEXT_TEMPLATE)

        html_content = html_template.format(
            store_name=store_name,
            organization_name=organization_name,
            invitation_url=invitation_url,
            expiration_days=expiration_days,
        )
        text_content = text_template.format(
            store_name=store_name,
            organization_name=organization_name,
            invitation_url=invitation_url,
            expiration_days=expiration_days,
        )
        subject = f"You've been invited to manage {organization_name} on LaundroMate"

        return InvitationEmailContent(
            html_content=html_content,
            text_content=text_content,
            subject=subject,
        )

    def _load_template(self, template_name: str) -> str:
        """
        Load email template from filesystem.

        Args:
            template_name: Name of the template file

        Returns:
            str: Template content

        Raises:
            FileNotFoundError: If template file does not exist
        """
        template_path = self.template_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(
                f"Template file not found: {template_path}. "
                f"Expected template files: {INVITATION_EMAIL_HTML_TEMPLATE}, "
                f"{INVITATION_EMAIL_TEXT_TEMPLATE}"
            )

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
