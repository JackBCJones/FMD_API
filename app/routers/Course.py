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



@router.get('/', response_model=List[schemas.CourseOut])
def get_courses(db: Session = Depends(get_db), 
limit: int = 10, search: Optional[str] = ""):

    courses = db.query(models.Course).filter(models.Course.title.contains(search)).limit(limit).all()
    

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    # to make posts only shown if they belong to the logged in user add .filter(models.Post.owner_id  == current_user.id) before the .all()
    return courses


@router.get("/{id}", response_model=schemas.Course)
def get_course(id: int, db: Session = Depends(get_db)):
    
    # results = db.query(models.Course, func.count(models.Vote.course_id).label("votes")).join(
    #     models.Vote, models.Vote.course_id == models.Course.id, isouter=True).group_by(models.Course.id).filter(models.Course.id == id).first()

    course = db.query(models.Course).filter(models.Course.id == id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"course with id: {id} was not found")
    return course



@router.get('/owner_id/{id}', response_model=List[schemas.Course])
def get_course_by_owner_id(id: int, db: Session = Depends(get_db), 
limit: int = 10, search: Optional[str] = ""):

    courses = db.query(models.Course).filter(models.Course.owner_id == id).filter(models.Course.title.contains(search)).limit(limit).all()
    # filter(models.Course.title.contains(search)).limit(limit)
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with owner id: {id} not found")
    return courses



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Course)
def create_course(course: schemas.CreateCourse, db: Session = Depends(get_db), current_uni: int = Depends(oauth2.get_current_user)):
    

    # print(current_uni.id)
    new_course = models.Course(owner_id=current_uni.id, **course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_uni: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    deleted_course = db.query(models.Course).filter(models.Course.id == id)

    course = deleted_course.first()
    
    # db.refresh(deleted_post)

    if course == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: course with id: {id} not found")
    
    if course.owner_id !=  current_uni.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    deleted_course.delete(synchronize_session=False)
    db.commit()
    return f"course with id: {id} has been deleted"



@router.put('/{id}', response_model=schemas.Course)
def update_post(id: int, updated_course: schemas.UpdateCourse, db: Session = Depends(get_db), current_uni: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,  
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    query_course = db.query(models.Course).filter(models.Course.id == id)

    course = query_course.first()

    if course == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail=f"Error 404: course with id: {id} not found")

    if course.owner_id !=  current_uni.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    query_course.update(updated_course.dict(), synchronize_session=False)

    db.commit()

    return query_course.first()

    
