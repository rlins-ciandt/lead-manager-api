from os import getenv
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import  JWTError, jwt
from datetime import datetime, timedelta, timezone

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

class AuthService():

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    def get_access_token(self):
        to_encode = {
            "sub": "access_token",
            "iss": "https://localhost:8000",
        }
      
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, getenv("SECRET_AUTH_KEY"), algorithm=ALGORITHM)
        return encoded_jwt
    
    async def secure(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # just check if the token is valid
            jwt.decode(token, getenv("SECRET_AUTH_KEY"), algorithms=[ALGORITHM])
        except JWTError:
            raise credentials_exception
 