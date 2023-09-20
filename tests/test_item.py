from httpx import AsyncClient
from fastapi import status
from src.main import app
from database import get_async_session

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


app.dependency_overrides[get_async_session] = override_get_async_session


async def test_item_get(ac: AsyncClient):
    response = await ac.get(url="/item/get", params={"item_id": 0})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Air Force"
    assert response.json()["size"] == "42EU"


async def test_item_add(ac: AsyncClient):
    response = await ac.post(
        url="/item/add",
        json={
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
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Air Force"
    assert response.json()["size"] == "42EU"


async def test_item_count(ac: AsyncClient):
    response = await ac.get(url="item/count")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 1


async def test_item_delete(ac: AsyncClient):
    response = await ac.delete(
        url="item/delete",
        params={
            "item_id": 0,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response

