from typing import AsyncGenerator
from fastapi.testclient import TestClient
import asyncio

from httpx import AsyncClient
from database import get_async_session
from src.main import app
import pytest


class MockScalarResult:
    @staticmethod
    def first():
        return {
            "id": 0,
            "name": "Air Force",
            "cost": 100,
            "brand": "Nike",
            "size": "42EU",
            "added_at": "2023-09-11T15:13:06.440",
            "description": "Best sneakers",
            "rating": 9.8,
            "amount": 4,
            "type": "sneakers",
        }


class MockResult:
    def scalars(self):
        return MockScalarResult()

    def scalar(self):
        return 1


class MockAsyncSession:
    async def commit(self):
        pass

    async def execute(self, statement):
        return MockResult()


async def override_get_async_session():
    return MockAsyncSession()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
