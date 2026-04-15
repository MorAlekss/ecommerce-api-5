import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.users.profile import get_profile, update_profile, update_avatar, delete_account
from src.users.admin import list_users, get_user, suspend_user
from src.users.preferences import get_preferences, update_preferences, reset_preferences


def test_get_profile():
    with patch('src.users.profile.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "u1", "name": "Alice", "email": "alice@example.com"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_profile("u1", "token123")
        assert result["name"] == "Alice"

def test_update_profile():
    with patch('src.users.profile.requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "u1", "name": "Alice Updated"}
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response
        result = update_profile("u1", "token123", {"name": "Alice Updated"})
        assert result["name"] == "Alice Updated"

def test_list_users():
    with patch('src.users.admin.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"users": [{"id": "u1"}, {"id": "u2"}], "total": 2}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = list_users("admin_token")
        assert result["total"] == 2

@pytest.mark.asyncio
async def test_get_preferences():
    mock_response = MagicMock()
    mock_response.json.return_value = {"theme": "dark", "language": "en"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch('httpx.AsyncClient', return_value=mock_client):
        result = await get_preferences("u1", "token123")
        assert result["theme"] == "dark"

@pytest.mark.asyncio
async def test_update_preferences():
    mock_response = MagicMock()
    mock_response.json.return_value = {"theme": "light", "language": "en"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.put = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch('httpx.AsyncClient', return_value=mock_client):
        result = await update_preferences("u1", "token123", {"theme": "light"})
        assert result["theme"] == "light"

@pytest.mark.asyncio
async def test_reset_preferences():
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.delete = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch('httpx.AsyncClient', return_value=mock_client):
        result = await reset_preferences("u1", "token123")
        assert result == 204
