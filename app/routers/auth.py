from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentification'])

@router.post('/login', response_model=schemas.Token)
def login(uni_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # going to return username and password

    uni = db.query(models.Uni).filter(models.Uni.name == uni_credentials.username).first()

    if not uni:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail='Invalid Credentials')

    if not utils.verify(uni_credentials.password, uni.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail='Invalid Credentials')
    
    access_token = oauth2.create_access_token(data= {"uni_id": uni.id})
    return {"access_token": access_token, "token_type": "bearer"}
    