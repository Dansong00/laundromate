"""Email configuration for email service."""
from dataclasses import dataclass


@dataclass(frozen=True)
class EmailConfig:
    """
    Email service configuration.

    Contains only the configuration needed by EmailService,
    following the Interface Segregation Principle.
    """

    sendgrid_api_key: str
    from_email: str
    frontend_url: str
