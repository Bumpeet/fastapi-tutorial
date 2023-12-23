from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from ..schemas import Token
from ..models import User
from ..utils import hashing, verify
from ..oauth2 import create_access_token, get_current_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), 
          db: Session = Depends(get_db),):
    user_req = db.query(User).filter(user_credentials.username==User.email).first()
    if not (user_req):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail="invalid credentials")
        
    if not verify(user_credentials.password, user_req.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")
    
    #create a token
    #return a token

    acess_token = create_access_token(data={"user_name": user_credentials.username})
    return {"access_token": acess_token,
            "token_type":"bearer"}

        
    
