from httpx import AsyncClient


async def test_auth_registration(ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "fakeuser@example.com",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "role_id": 1,
            "username": "Boss",
            "registered_at": "2023-09-12T06:54:45.345",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "Boss"


async def test_auth_login(ac: AsyncClient):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "username": "fakeuser@example.com",
        "password": "password",
    }
    auth_response = await ac.post("/auth/login", headers=headers, data=data)
    assert auth_response.status_code == 204
