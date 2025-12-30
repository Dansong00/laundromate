"""Unit tests for authentication decorators."""
from typing import Any

import pytest
from fastapi import HTTPException

from app.auth.decorators import (
    require_admin,
    require_auth,
    require_owner_or_admin,
    require_provisioning_specialist,
    require_super_admin,
    require_support_agent,
)
from app.core.models.user import User


class TestRequireAuth:
    """Test require_auth decorator."""

    @pytest.mark.asyncio
    async def test_require_auth_with_user(self) -> None:
        """Test that decorator allows request when user is present."""
        user = User(phone="+1234567890")

        @require_auth
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_auth_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""

        @require_auth
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        assert exc_info.value.status_code == 401
        assert "Authentication required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_auth_with_none_user(self) -> None:
        """Test that decorator raises exception when user is None."""

        @require_auth
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=None)
        assert exc_info.value.status_code == 401


class TestRequireAdmin:
    """Test require_admin decorator."""

    @pytest.mark.asyncio
    async def test_require_admin_with_admin_user(self) -> None:
        """Test that decorator allows request when user is admin."""
        admin_user = User(
            phone="+1234567890",
            is_admin=True,
            is_super_admin=False,
        )

        @require_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=admin_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_admin_with_super_admin(self) -> None:
        """Test that decorator allows request when user is super admin."""
        super_admin_user = User(
            phone="+1234567891",
            is_admin=False,
            is_super_admin=True,
        )

        @require_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=super_admin_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_admin_with_regular_user(self) -> None:
        """Test that decorator raises exception when user is not admin."""
        regular_user = User(
            phone="+1234567892",
            is_admin=False,
            is_super_admin=False,
        )

        @require_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=regular_user)
        assert exc_info.value.status_code == 403
        assert "Admin privileges required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_admin_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""

        @require_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        assert exc_info.value.status_code == 403


class TestRequireSuperAdmin:
    """Test require_super_admin decorator."""

    @pytest.mark.asyncio
    async def test_require_super_admin_with_super_admin(self) -> None:
        """Test that decorator allows request when user is super admin."""
        super_admin_user = User(
            phone="+1234567890",
            is_admin=False,
            is_super_admin=True,
        )

        @require_super_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=super_admin_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_super_admin_with_admin(self) -> None:
        """Test that decorator raises exception when user is only admin."""
        admin_user = User(
            phone="+1234567891",
            is_admin=True,
            is_super_admin=False,
        )

        @require_super_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=admin_user)
        assert exc_info.value.status_code == 403
        assert "Super admin privileges required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_super_admin_with_regular_user(self) -> None:
        """Test that decorator raises exception when user is regular."""
        regular_user = User(
            phone="+1234567892",
            is_admin=False,
            is_super_admin=False,
        )

        @require_super_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=regular_user)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_require_super_admin_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""

        @require_super_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        assert exc_info.value.status_code == 403


class TestRequireOwnerOrAdmin:
    """Test require_owner_or_admin decorator."""

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_with_owner(self) -> None:
        """Test that decorator allows request when user is owner."""
        from uuid import uuid4

        user_id = uuid4()
        owner_user = User(
            id=user_id,
            phone="+1234567890",
            is_admin=False,
            is_super_admin=False,
        )

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=owner_user, user_id=user_id)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_with_admin(self) -> None:
        """Test that decorator allows request when user is admin."""
        from uuid import uuid4

        user_id = uuid4()
        admin_user = User(
            id=uuid4(),
            phone="+1234567891",
            is_admin=True,
            is_super_admin=False,
        )

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=admin_user, user_id=user_id)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_with_super_admin(self) -> None:
        """Test that decorator allows request when user is super admin."""
        from uuid import uuid4

        user_id = uuid4()
        super_admin_user = User(
            id=uuid4(),
            phone="+1234567892",
            is_admin=False,
            is_super_admin=True,
        )

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=super_admin_user, user_id=user_id)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_with_different_user(self) -> None:
        """Test that decorator raises exception when user is not owner or admin."""
        from uuid import uuid4

        user_id = uuid4()
        other_user = User(
            id=uuid4(),
            phone="+1234567893",
            is_admin=False,
            is_super_admin=False,
        )

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=other_user, user_id=user_id)
        assert exc_info.value.status_code == 403
        assert "Not authorized to access this resource" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""
        from uuid import uuid4

        user_id = uuid4()

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(user_id=user_id)
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_with_customer_id(self) -> None:
        """Test that decorator works with customer_id parameter."""
        from uuid import uuid4

        user_id = uuid4()
        owner_user = User(
            id=user_id,
            phone="+1234567894",
            is_admin=False,
            is_super_admin=False,
        )

        @require_owner_or_admin
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=owner_user, customer_id=user_id)
        assert result == "success"


class TestRequireSupportAgent:
    """Test require_support_agent decorator."""

    @pytest.mark.asyncio
    async def test_require_support_agent_with_support_agent(self) -> None:
        """Test that decorator allows request when user is support agent."""
        support_agent_user = User(
            phone="+1234567890",
            is_admin=False,
            is_super_admin=False,
            is_support_agent=True,
            is_provisioning_specialist=False,
        )

        @require_support_agent
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=support_agent_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_support_agent_with_super_admin(self) -> None:
        """Test that decorator allows request when user is super admin."""
        super_admin_user = User(
            phone="+1234567891",
            is_admin=False,
            is_super_admin=True,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )

        @require_support_agent
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=super_admin_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_support_agent_with_regular_user(self) -> None:
        """Test that decorator raises exception when user is not support agent."""
        regular_user = User(
            phone="+1234567892",
            is_admin=False,
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )

        @require_support_agent
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=regular_user)
        assert exc_info.value.status_code == 403
        assert "Support agent privileges required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_support_agent_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""

        @require_support_agent
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        assert exc_info.value.status_code == 403


class TestRequireProvisioningSpecialist:
    """Test require_provisioning_specialist decorator."""

    @pytest.mark.asyncio
    async def test_require_provisioning_specialist_with_specialist(self) -> None:
        """Test that decorator allows request when user is provisioning specialist."""
        specialist_user = User(
            phone="+1234567890",
            is_admin=False,
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=True,
        )

        @require_provisioning_specialist
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=specialist_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_provisioning_specialist_with_super_admin(self) -> None:
        """Test that decorator allows request when user is super admin."""
        super_admin_user = User(
            phone="+1234567891",
            is_admin=False,
            is_super_admin=True,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )

        @require_provisioning_specialist
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        result = await test_endpoint(current_user=super_admin_user)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_require_provisioning_specialist_with_regular_user(self) -> None:
        """Test decorator raises exception when user is not provisioning specialist."""
        regular_user = User(
            phone="+1234567892",
            is_admin=False,
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )

        @require_provisioning_specialist
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=regular_user)
        assert exc_info.value.status_code == 403
        assert "Provisioning specialist privileges required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_provisioning_specialist_with_support_agent(self) -> None:
        """Test that decorator raises exception when user is only support agent."""
        support_agent_user = User(
            phone="+1234567893",
            is_admin=False,
            is_super_admin=False,
            is_support_agent=True,
            is_provisioning_specialist=False,
        )

        @require_provisioning_specialist
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint(current_user=support_agent_user)
        assert exc_info.value.status_code == 403
        assert "Provisioning specialist privileges required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_require_provisioning_specialist_without_user(self) -> None:
        """Test that decorator raises exception when user is not present."""

        @require_provisioning_specialist
        async def test_endpoint(*args: Any, **kwargs: Any) -> str:
            return "success"

        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        assert exc_info.value.status_code == 403
