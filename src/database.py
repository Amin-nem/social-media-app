from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#   try:
#     connection = psycopg2.connect(database=settings.DATABASE_NAME,user=settings.DATABASE_USERNAME,password=settings.DATABASE_PASSWORD,host=settings.DATABASE_HOSTNAME,cursor_factory=RealDictCursor)
#     cursor = connection.cursor()
#     print("--> database connection was successful")
#     break
#   except Exception as e:
#     print(e)
#     time.sleep(2)


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()