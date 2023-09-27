from httpx import AsyncClient
from fastapi import status
from src.main import app
from database import get_async_session


class TestPostLogin:
    async def test_login(self, ac: AsyncClient):
        username = "string"
        password = "string"
        login_response = await ac.post(
            url="/users/token",
            headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"username": username, "password": password},
        )
        assert login_response.status_code == status.HTTP_200_OK
        access_token = login_response.json()["access_token"]

        user_response = await ac.get(
            url="/users/me",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        assert user_response.status_code == status.HTTP_200_OK
        user_data = user_response.json()
        assert user_data["username"] == "string"
        assert user_data["email"] == "user@example.com"
