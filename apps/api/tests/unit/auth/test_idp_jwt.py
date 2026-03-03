"""Unit tests for IdP (Clerk) JWT decoding."""

import pytest

from app.auth import idp_jwt
from app.core.config.settings import settings


class TestDecodeIdpToken:
    """Test decode_idp_token behavior."""

    def test_returns_none_when_jwks_uri_not_configured(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When IDP_JWKS_URI is empty, decode_idp_token returns None for any token."""
        monkeypatch.setattr(settings, "IDP_JWKS_URI", "")
        monkeypatch.setattr(settings, "IDP_ISSUER", "")
        # Reset the cached client so the new config is used
        monkeypatch.setattr(idp_jwt, "_jwk_client", None)
        result = idp_jwt.decode_idp_token("any.token.here")
        assert result is None

    def test_returns_none_for_invalid_token_when_configured(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When IDP is configured but token is invalid, returns None."""
        monkeypatch.setattr(
            settings,
            "IDP_JWKS_URI",
            "https://example.clerk.accounts.dev/.well-known/jwks.json",
        )
        monkeypatch.setattr(
            settings, "IDP_ISSUER", "https://example.clerk.accounts.dev"
        )
        monkeypatch.setattr(idp_jwt, "_jwk_client", None)
        result = idp_jwt.decode_idp_token("not-a-valid-jwt")
        assert result is None
