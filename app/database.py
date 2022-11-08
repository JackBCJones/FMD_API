from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
# SQLALCHEMY_DATABASE_URL = 

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:

#     try:
#         conn = psycopg2.connect(host='{settings.DATABASE_HOSTNAME}', database='{settings.DATABASE_NAME}', user='{settings.DATABASE_USERNAME}', 
#         password='{settings.DATABASE_PASSWORD}', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print('connection to database failed')
#         print("Error: ",  error)
#         time.sleep(2)
