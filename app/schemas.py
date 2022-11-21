from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# by having these schemas you are regulating what can be changed or called when 
# using a get, post, delete, or update. by having these specific classes for each instance 
# you can have specific parameters in plavce. 
# for example, if I want you to only be able to update the title 
# I can only have the title available under the UpdatePost class
# Or if I want to make something manditory I will have it under that class

class CourseBase(BaseModel):
    title: str
    requirements: str
    created_at: datetime

class Course(CourseBase):
    id: int
    owner_id: int
    

    class Config:
        orm_mode = True


class UniOut(BaseModel):
    id: int
    name: str
    img: str
    nickname: str
    color: str
    text_color: str

    class Config:
        orm_mode = True

class CourseOut(CourseBase):
    id: int
    link: str
    owner_id: int
    owner: UniOut
    

    class Config:
        orm_mode = True



class CreateCourse(BaseModel):
    title: str
    requirements: str
    link : str

class UpdateCourse(BaseModel):
    title: str
    requirements: str
    link: str

# can also make use of inheritance 
# a class that inherites from another has all of its schemas 

class CreateCourses(BaseModel):
    Course: CreateCourse





class UniCreate(BaseModel):
    name: str
    img: str
    color: str
    text_color: str
    nickname: str
    password: str




class UniLogin(BaseModel):
    name: str
    password: str

class UpdateUni(BaseModel):
    name: str
    img: str
    color: str
    text_color: str
    nickname: str
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




