from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import database, schemas, models, config

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret_key
#algorithm
#expiration time

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})
    
    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)


def verify_acess_token(payload: str, credentials_excepiton) -> schemas.TokenData:
    try:
        payload_decoded = jwt.decode(token=payload, algorithms=[ALGORITHM], key=SECRET_KEY)
        uname = payload_decoded.get("user_name")
        if uname is None:
            raise credentials_excepiton
        token_data = schemas.TokenData(email=uname)
        print("verify_token_Data-->", token_data)

    except JWTError:
        raise credentials_excepiton

    return token_data

def get_current_user(token:str=Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_excepiton = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="not authorized",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_acess_token(token, credentials_excepiton)
    print("get_current_user -->", token_data)
    user = db.query(models.User).filter(token_data.email==models.User.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
    