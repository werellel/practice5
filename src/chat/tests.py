import pytest
from channels.testing import HttpCommunicator
from chat.consumers import ChatConsumer

@pytest.mark.asyncio
async def test_my_consumer():
    communicator = HttpCommunicator(ChatConsumer, "GET", "/test/")
    response = await communicator.get_response()
    assert response["body"] == b"test response"
    assert response["status"] == 200