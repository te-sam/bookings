import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, email, exists", [
    (1, "artem.sam@yandex.ru", True),
    (2, "govnovoz228@gmail.com", True),
    (13, "kon@gmail.com", False)
])
async def test_user_find_by_id(user_id, email, exists):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user