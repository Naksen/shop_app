from typing import AsyncGenerator
from fastapi.testclient import TestClient
import asyncio

from httpx import AsyncClient
from database import get_async_session
from src.main import app
import pytest


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
