from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)



@router.get('/', response_model=List[schemas.Course])
def get_courses(db: Session = Depends(get_db), 
limit: int = 0, skip: int = 0, search: Optional[str] = ""):

    courses = db.query(models.Course).all()
    # .filter(models.Course.title.contains(search)).limit(limit).offset(skip)

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    # to make posts only shown if they belong to the logged in user add .filter(models.Post.owner_id  == current_user.id) before the .all()
    return courses

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Course)
def create_course(course: schemas.CreateCourse, db: Session = Depends(get_db)):
    
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("/{id}", response_model=schemas.Course)
def get_course(id: int, db: Session = Depends(get_db)):
    
    # results = db.query(models.Course, func.count(models.Vote.course_id).label("votes")).join(
    #     models.Vote, models.Vote.course_id == models.Course.id, isouter=True).group_by(models.Course.id).filter(models.Course.id == id).first()

    course = db.query(models.Course).filter(models.Course.id == id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return course



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    post = deleted_post.first()
    
    # db.refresh(deleted_post)

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: post with id: {id} not found")
    
    if post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return f"post with id: {id} has been deleted"



@router.put('/{id}', response_model=schemas.Course)
def update_post(id: int, updated_post: schemas.UpdateCourse, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,  
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    query_post = db.query(models.Post).filter(models.Post.id == id)

    post = query_post.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: post with id: {id} not found")

    if post.owner_id !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    query_post.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return query_post.first()

    
