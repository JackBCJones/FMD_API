from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings

# we need a secret key, algorithm, expiration time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("uni_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail=f"Could not validate credentials", headers={"www-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    uni = db.query(models.Uni).filter(models.Uni.id == token.id).first()
    return uni
