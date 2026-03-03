"""
Clerk / IdP JWT validation using JWKS.

When IDP_JWKS_URI is configured, verifies JWTs signed by Clerk (RS256)
and returns the payload. Used by get_current_user to support Clerk tokens.
"""

from typing import Any, Optional

from jwt import PyJWKClient, PyJWKClientError
from jwt.exceptions import InvalidTokenError

from app.core.config.settings import settings


def _get_jwk_client() -> Optional[PyJWKClient]:
    """Return a cached JWK client if IdP is configured."""
    if not settings.IDP_JWKS_URI or not settings.IDP_JWKS_URI.strip():
        return None
    return PyJWKClient(
        uri=settings.IDP_JWKS_URI.strip(),
        cache_jwk_set=True,
        cache_keys=True,
    )


_NOT_INITIALIZED = object()
_jwk_client: Optional[PyJWKClient] | object = _NOT_INITIALIZED


def get_jwk_client() -> Optional[PyJWKClient]:
    """Lazy-initialize and return the global JWK client."""
    global _jwk_client
    if _jwk_client is not _NOT_INITIALIZED:
        return _jwk_client  # type: ignore[return-value]
    _jwk_client = _get_jwk_client()
    return _jwk_client


def decode_idp_token(token: str) -> Optional[dict[str, Any]]:
    """
    Verify and decode a Clerk (or other IdP) JWT using JWKS.

    Returns the payload dict if valid (sub, email, etc.), or None if
    IdP is not configured, token is invalid, or verification fails.
    """
    client = get_jwk_client()
    if client is None:
        return None

    try:
        signing_key = client.get_signing_key_from_jwt(token)
    except (PyJWKClientError, InvalidTokenError):
        return None

    try:
        import jwt as pyjwt

        decoded = pyjwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_signature": True, "verify_exp": True},
        )
    except InvalidTokenError:
        return None

    # Optional: verify issuer and audience if configured
    if settings.IDP_ISSUER and settings.IDP_ISSUER.strip():
        iss = decoded.get("iss")
        if not iss or iss.rstrip("/") != settings.IDP_ISSUER.rstrip("/"):
            return None
    if settings.IDP_AUDIENCE and settings.IDP_AUDIENCE.strip():
        aud = decoded.get("aud")
        if aud != settings.IDP_AUDIENCE:
            return None

    return decoded
