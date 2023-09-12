from httpx import AsyncClient


async def test_add_item(ac: AsyncClient):
    response = await ac.post(
        "/item/add",
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

    assert response.status_code == 200
    assert response.json()["name"] == "Air Force"


async def test_count_item(ac: AsyncClient):
    response = await ac.get("/item/count")
    data = response.json()
    assert data == 1


async def test_get_item(ac: AsyncClient):
    response = await ac.get("/item/get", params={"item_id": 0})
    data = response.json()
    assert data["name"] == "Air Force"


async def test_delete_item(ac: AsyncClient):
    await ac.delete("item/delete", params={"item_id": 0})
    response = await ac.get("/item/count")
    data = response.json()
    assert data == 0
