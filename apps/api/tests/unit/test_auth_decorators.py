"""
Unit tests for authentication decorators.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, Depends
from app.auth.decorators import require_auth, require_admin, require_owner_or_admin
from app.core.models.user import User
from sqlalchemy.orm import Session


class TestRequireAuthDecorator:
    """Test require_auth decorator."""

    @pytest.mark.asyncio
    async def test_require_auth_success(self):
        """Test require_auth with valid user."""
        # Mock current user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        
        # Create a mock function with the decorator
        @require_auth
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "success"}
        
        # Test the decorated function
        result = await test_endpoint()
        assert result["message"] == "success"

    @pytest.mark.asyncio
    async def test_require_auth_inactive_user(self):
        """Test require_auth with inactive user."""
        # Mock inactive user
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        
        # Create a mock function with the decorator
        @require_auth
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        
        assert exc_info.value.status_code == 401
        assert "Inactive user" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_require_auth_no_user(self):
        """Test require_auth with no user."""
        # Create a mock function with the decorator
        @require_auth
        async def test_endpoint(current_user: User = Depends(lambda: None)):
            return {"message": "success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        
        assert exc_info.value.status_code == 401
        assert "Not authenticated" in str(exc_info.value.detail)


class TestRequireAdminDecorator:
    """Test require_admin decorator."""

    @pytest.mark.asyncio
    async def test_require_admin_success(self):
        """Test require_admin with admin user."""
        # Mock admin user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = True
        
        # Create a mock function with the decorator
        @require_admin
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "admin success"}
        
        # Test the decorated function
        result = await test_endpoint()
        assert result["message"] == "admin success"

    @pytest.mark.asyncio
    async def test_require_admin_regular_user(self):
        """Test require_admin with regular user."""
        # Mock regular user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = False
        
        # Create a mock function with the decorator
        @require_admin
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "admin success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        
        assert exc_info.value.status_code == 403
        assert "Admin access required" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_require_admin_inactive_user(self):
        """Test require_admin with inactive user."""
        # Mock inactive user
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        mock_user.is_admin = True
        
        # Create a mock function with the decorator
        @require_admin
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "admin success"}
        
        # Test should raise HTTPException for inactive user first
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        
        assert exc_info.value.status_code == 401
        assert "Inactive user" in str(exc_info.value.detail)


class TestRequireOwnerOrAdminDecorator:
    """Test require_owner_or_admin decorator."""

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_owner_success(self):
        """Test require_owner_or_admin with owner user."""
        # Mock owner user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = False
        mock_user.id = "user-123"
        
        # Mock resource with same owner
        mock_resource = Mock()
        mock_resource.user_id = "user-123"
        
        # Create a mock function with the decorator
        @require_owner_or_admin
        async def test_endpoint(
            resource_id: str,
            current_user: User = Depends(lambda: mock_user),
            db: Session = Depends(lambda: Mock())
        ):
            return {"message": "owner success"}
        
        # Test the decorated function
        result = await test_endpoint("resource-123")
        assert result["message"] == "owner success"

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_admin_success(self):
        """Test require_owner_or_admin with admin user."""
        # Mock admin user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = True
        mock_user.id = "admin-123"
        
        # Mock resource with different owner
        mock_resource = Mock()
        mock_resource.user_id = "other-user-123"
        
        # Create a mock function with the decorator
        @require_owner_or_admin
        async def test_endpoint(
            resource_id: str,
            current_user: User = Depends(lambda: mock_user),
            db: Session = Depends(lambda: Mock())
        ):
            return {"message": "admin success"}
        
        # Test the decorated function
        result = await test_endpoint("resource-123")
        assert result["message"] == "admin success"

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_unauthorized_user(self):
        """Test require_owner_or_admin with unauthorized user."""
        # Mock unauthorized user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = False
        mock_user.id = "user-123"
        
        # Mock resource with different owner
        mock_resource = Mock()
        mock_resource.user_id = "other-user-456"
        
        # Create a mock function with the decorator
        @require_owner_or_admin
        async def test_endpoint(
            resource_id: str,
            current_user: User = Depends(lambda: mock_user),
            db: Session = Depends(lambda: Mock())
        ):
            return {"message": "unauthorized success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint("resource-123")
        
        assert exc_info.value.status_code == 403
        assert "Not authorized" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_inactive_user(self):
        """Test require_owner_or_admin with inactive user."""
        # Mock inactive user
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        mock_user.is_admin = False
        mock_user.id = "user-123"
        
        # Create a mock function with the decorator
        @require_owner_or_admin
        async def test_endpoint(
            resource_id: str,
            current_user: User = Depends(lambda: mock_user),
            db: Session = Depends(lambda: Mock())
        ):
            return {"message": "inactive success"}
        
        # Test should raise HTTPException for inactive user first
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint("resource-123")
        
        assert exc_info.value.status_code == 401
        assert "Inactive user" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_require_owner_or_admin_nonexistent_resource(self):
        """Test require_owner_or_admin with non-existent resource."""
        # Mock user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = False
        mock_user.id = "user-123"
        
        # Mock database that returns None for resource
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Create a mock function with the decorator
        @require_owner_or_admin
        async def test_endpoint(
            resource_id: str,
            current_user: User = Depends(lambda: mock_user),
            db: Session = Depends(lambda: mock_db)
        ):
            return {"message": "not found success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint("nonexistent-resource")
        
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value.detail).lower()


class TestDecoratorIntegration:
    """Test decorator integration scenarios."""

    @pytest.mark.asyncio
    async def test_multiple_decorators_admin(self):
        """Test using multiple decorators with admin user."""
        # Mock admin user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = True
        mock_user.id = "admin-123"
        
        # Create a mock function with multiple decorators
        @require_auth
        @require_admin
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "multi decorator success"}
        
        # Test the decorated function
        result = await test_endpoint()
        assert result["message"] == "multi decorator success"

    @pytest.mark.asyncio
    async def test_multiple_decorators_regular_user(self):
        """Test using multiple decorators with regular user."""
        # Mock regular user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = False
        mock_user.id = "user-123"
        
        # Create a mock function with multiple decorators
        @require_auth
        @require_admin
        async def test_endpoint(current_user: User = Depends(lambda: mock_user)):
            return {"message": "multi decorator success"}
        
        # Test should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await test_endpoint()
        
        assert exc_info.value.status_code == 403
        assert "Admin access required" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_decorator_with_async_function(self):
        """Test decorators work with async functions."""
        # Mock user
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.is_admin = True
        
        # Create an async function with decorator
        @require_auth
        @require_admin
        async def async_endpoint(current_user: User = Depends(lambda: mock_user)):
            # Simulate async work
            import asyncio
            await asyncio.sleep(0.001)
            return {"message": "async success"}
        
        # Test the decorated async function
        result = await async_endpoint()
        assert result["message"] == "async success"

    @pytest.mark.asyncio
    async def test_decorator_error_handling(self):
        """Test decorator error handling with various scenarios."""
        # Test with None user
        @require_auth
        async def test_none_user(current_user: User = Depends(lambda: None)):
            return {"message": "success"}
        
        with pytest.raises(HTTPException) as exc_info:
            await test_none_user()
        assert exc_info.value.status_code == 401
        
        # Test with inactive admin user
        mock_inactive_admin = Mock(spec=User)
        mock_inactive_admin.is_active = False
        mock_inactive_admin.is_admin = True
        
        @require_auth
        @require_admin
        async def test_inactive_admin(current_user: User = Depends(lambda: mock_inactive_admin)):
            return {"message": "success"}
        
        with pytest.raises(HTTPException) as exc_info:
            await test_inactive_admin()
        assert exc_info.value.status_code == 401  # Should fail on require_auth first