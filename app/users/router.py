from fastapi import APIRouter, Depends, Response
from fastapi_versioning import version
from app.exceptions import IncorrectEmailPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users

from app.users.schemas import SUserAuth


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    #проверка, что пользователя не свуществует
    existng_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existng_user:
        raise UserAlreadyExistsException
    
    #хэширование пароля
    hashed_password = get_password_hash(user_data.password)
    #добавление в БД
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
@version(1)
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailPasswordException
    access_token = create_access_token({"sub": str(user.id)})  # sub -рекомендация JWT
    response.set_cookie("booking_access_token", access_token, httponly=True)  # помещение в куки
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")  # удаление coockies


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return current_user


