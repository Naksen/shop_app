from httpx import AsyncClient
from fastapi import status

async def test_item_get(ac: AsyncClient):
    response = await ac.get(
        url="/item/get",
        params={
            "item_id": 0
        }
    )   
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