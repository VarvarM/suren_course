import secrets
import uuid
from time import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])

security = HTTPBasic()
usernames_to_passwords = {'qwe': 'admin', 'john': 'asd'}
static_auth_token_to_username = {'token333': 'admin',
                                 'dnf9fdsmsdkf4383nksdv8snrglsd': 'asd'}
cookies: dict[str, dict[str, Any]] = {}
cookie_session_key = "web-app-session-id"


@router.get('/basic-auth/')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"message": "Hi", "username": credentials.username, "password": credentials.password}


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password',
                                 headers={"WWW-Authenticate": "Basic"})
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
    if not secrets.compare_digest(credentials.password.encode("utf-8"), correct_password.encode("utf-8")):
        raise unauthed_exc
    return credentials.username


def get_username_by_static_auth_token(static_token: str = Header(alias="x-auth-token")) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.get('/basic-auth-username/')
def demo_basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {"message": "Hi", "username": auth_username}


@router.get('/some-http-header-auth/')
def demo_auth_some_http_header(username: str = Depends(get_username_by_static_auth_token)):
    return {"message": "Hi", "username": username}


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(session_id: str = Cookie(alias=cookie_session_key)):
    if session_id not in cookies:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return cookies[session_id]


@router.post('/login-cookie/')
def demo_auth_login_cookie(response: Response, username: str = Depends(get_username_by_static_auth_token)):
    session_id = generate_session_id()
    cookies[session_id] = {"username": username, "login_at": int(time())}
    response.set_cookie(cookie_session_key, session_id)
    print(cookies)
    return {"result": "OK", "cookie": session_id}


@router.get('/check-cookie/')
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    print(cookies)
    return {"message": f"Hello {username}", **user_session_data}


@router.get('/logout-cookie/')
def demo_auth_logout_cookie(response: Response, session_id: str = Cookie(alias=cookie_session_key),
                            user_session_data: dict = Depends(get_session_data)):
    cookies.pop(session_id)
    response.delete_cookie(cookie_session_key)
    username = user_session_data["username"]
    print(cookies)
    return {"message": f"Bye {username}"}
