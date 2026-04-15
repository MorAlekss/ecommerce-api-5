import sys
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.notifications.email import send_email, send_bulk_email, get_email_status
from src.notifications.sms import send_sms, send_bulk_sms


@pytest.mark.asyncio
async def test_send_email():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "msg_123", "status": "queued"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch('src.notifications.email.httpx.AsyncClient', return_value=mock_client):
        result = await send_email("token123", "user@example.com", "Hello", "Test body")
        assert result["status"] == "queued"

@pytest.mark.asyncio
async def test_send_bulk_email():
    mock_response = MagicMock()
    mock_response.json.return_value = {"batch_id": "batch_123", "count": 3}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch('src.notifications.email.httpx.AsyncClient', return_value=mock_client):
        result = await send_bulk_email("token123", ["a@example.com", "b@example.com"], "Subject", "Body")
        assert result["count"] == 3

def test_send_sms():
    with patch('src.notifications.sms.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "sms_123", "status": "sent"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = send_sms("+123****7890", "Your order is ready!")
        assert result["status"] == "sent"
