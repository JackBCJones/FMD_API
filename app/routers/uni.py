from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from app import oauth2
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/unis",
    tags=['Unis']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UniOut)
def create_uni(uni: schemas.UniCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(uni.password)
    uni.password = hashed_password

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
def get_unis(db: Session = Depends(get_db)):
    
    all_unis = db.query(models.Uni).all()

    if not all_unis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"there are no universities available")
    return all_unis


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_uni(id: int, db: Session = Depends(get_db), current_uni: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    deleted_uni = db.query(models.Uni).filter(models.Uni.id == id)

    uni = deleted_uni.first()
    
    # db.refresh(deleted_post)

    if uni == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: course with id: {id} not found")
    
    if uni.id !=  current_uni.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    deleted_uni.delete(synchronize_session=False)
    db.commit()
    return f"uni with id: {id} has been deleted"


@router.put('/{id}', response_model=schemas.UniOut)
def update_post(id: int, updated_uni: schemas.UpdateUni, db: Session = Depends(get_db), current_uni: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,  
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    query_uni = db.query(models.Uni).filter(models.Uni.id == id)

    uni = query_uni.first()

    if uni == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: uni with id: {id} not found")

    if uni.id !=  current_uni.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    query_uni.update(updated_uni.dict(), synchronize_session=False)

    db.commit()

    return query_uni.first()