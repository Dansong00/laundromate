"""Centralized dependency factories for FastAPI dependency injection."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config.email_config import EmailConfig
from app.core.config.settings import settings
from app.core.database.session import get_db
from app.core.emails.invitation_templates import InvitationTemplateRenderer
from app.core.repositories.invitation_repository import InvitationRepository
from app.core.repositories.organization_repository import OrganizationRepository
from app.core.repositories.user_organization_repository import (
    UserOrganizationRepository,
)
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.user_store_repository import UserStoreRepository
from app.core.services.email_service import EmailService
from app.core.services.invitation_service import InvitationService


def get_invitation_repository(
    db: Session = Depends(get_db),
) -> InvitationRepository:
    """Dependency factory for InvitationRepository."""
    return InvitationRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency factory for UserRepository."""
    return UserRepository(db)


def get_user_store_repository(
    db: Session = Depends(get_db),
) -> UserStoreRepository:
    """Dependency factory for UserStoreRepository."""
    return UserStoreRepository(db)


def get_user_organization_repository(
    db: Session = Depends(get_db),
) -> UserOrganizationRepository:
    """Dependency factory for UserOrganizationRepository."""
    return UserOrganizationRepository(db)


def get_organization_repository(
    db: Session = Depends(get_db),
) -> OrganizationRepository:
    """Dependency factory for OrganizationRepository."""
    return OrganizationRepository(db)


def get_invitation_service(
    invitation_repo: InvitationRepository = Depends(get_invitation_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    user_org_repo: UserOrganizationRepository = Depends(
        get_user_organization_repository
    ),
    user_store_repo: UserStoreRepository = Depends(get_user_store_repository),
    org_repo: OrganizationRepository = Depends(get_organization_repository),
) -> InvitationService:
    """Dependency factory for InvitationService."""
    return InvitationService(
        invitation_repo, user_repo, user_org_repo, user_store_repo, org_repo
    )


def get_invitation_template_renderer() -> InvitationTemplateRenderer:
    """Dependency factory for InvitationTemplateRenderer."""
    return InvitationTemplateRenderer()


def get_email_service(
    template_renderer: InvitationTemplateRenderer = Depends(
        get_invitation_template_renderer
    ),
) -> EmailService:
    """Dependency factory for EmailService."""
    email_config = EmailConfig(
        sendgrid_api_key=settings.SENDGRID_API_KEY,
        from_email=settings.FROM_EMAIL,
        frontend_url=settings.FRONTEND_URL,
    )
    return EmailService(email_config, template_renderer)
