from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

import auth.utils
from api_v1.demo_auth.crud import users_db
from api_v1.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth import utils as auth_utils
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/jwt/login')


def get_current_token_payload(  # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme)) -> dict:
    # token = credentials.credentials
    try:
        payload = auth.utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid token error: {e}')
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f'Invalid token type {current_token_type!r} expected {token_type!r}')


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid (user not found)")


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")


def validate_auth_user_login(username: str = Form(), password: str = Form()):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
    return user