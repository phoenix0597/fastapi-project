from datetime import datetime, timezone

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import (
    ExpiredTokenException, TokenIsAbsentException, TokenIncorrectFormatException, UserNotFoundException
)
from app.users.dao import UsersDAO
from app.users.models import Users


async def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenIsAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise TokenIncorrectFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < int(datetime.now(timezone.utc).timestamp())):
        raise ExpiredTokenException
    user_id = payload.get("sub")
    if not user_id:
        raise UserNotFoundException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    
    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized as admin")
    return current_user
