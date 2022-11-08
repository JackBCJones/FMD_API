from fastapi import FastAPI
# from . import models
# from .database import engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .routers import Course, uni, auth



# models.Base.metadata.create_all(bind=engine)
# not using anymore as we now have alembic 


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(Course.router)
app.include_router(uni.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "working!"}