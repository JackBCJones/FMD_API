from ast import Try
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(
    prefix="/unis",
    tags=['Unis']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UniOut)
def create_uni(uni: schemas.UniCreate, db: Session = Depends(get_db)):

    new_uni = models.Uni(**uni.dict())
    db.add(new_uni)
    db.commit()
    db.refresh(new_uni)

    return new_uni

@router.get("/{id}", response_model=schemas.UniOut)
def get_uni(id: int, db: Session = Depends(get_db)):
    uni = db.query(models.Uni).filter(models.Uni.id == id).first()

    if not uni:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"uni with id: {id} was not found")
    return uni

@router.get("/", response_model=List[schemas.UniOut])
def get_uni(db: Session = Depends(get_db)):
    
    all_unis = db.query(models.Uni).all()

    if not all_unis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"uni with id: {id} was not found")
    return all_unis