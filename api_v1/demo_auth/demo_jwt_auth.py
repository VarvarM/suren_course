from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from api_v1.demo_auth.helpers import create_access_token, \
    create_refresh_token
from api_v1.demo_auth.validation import get_current_token_payload, \
    get_current_auth_user_for_refresh, get_current_active_auth_user, validate_auth_user_login
from users.schemas import UserSchema


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/jwt', tags=['JWT'], dependencies=[Depends(http_bearer)])


@router.post('/login', response_model=TokenInfo)
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user_login)):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh/', response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    # def auth_refresh_jwt(user: UserSchema = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE))):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get('users/me/')
def auth_user_check_self_info(payload: dict = Depends(get_current_token_payload),
                              user: UserSchema = Depends(get_current_active_auth_user)):
    iat = payload.get('iat')
    return {'username': user.username, "email": user.email, 'logged in iat': iat}