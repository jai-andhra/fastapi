from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/login",
                    tags=['Authentication'])

@router.post("/", response_model=schemas.Token)
#def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #OAuth2PasswordRequestForm converts the data into key,value pair of 
    #{ "username": "assd", "password": "asasas"}
    print (user)
#    dbuser = db.query(models.User).filter(models.User.email == user.email).first()
    dbuser = db.query(models.User).filter(models.User.email == user.username).first()

    if not dbuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User Credentials!")

    if not utils.verifyPassword(user.password, dbuser.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User Credentials!")

    #Create a JWT token
    # Return the token
    access_token = oauth2.create_access_token(data={"userid": dbuser.id})

    return {"access_token": access_token, "token_type": "bearer"}