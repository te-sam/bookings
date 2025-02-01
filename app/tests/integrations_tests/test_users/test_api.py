
import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("email, password, status_code", [
    ("lisiy_globus@planeta.com", "cherep228", 200),
    ("lisiy_globus@planeta.com", "chere29", 409),
    ("samogon@pervak.com", "70gradusov", 200),
    ("samogon", "70gradusov", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("pelmen@gmail.com", "myasistiy228", 200),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
