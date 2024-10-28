from fastapi import FastAPI
import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import auth, post,user
# connect to db
# try:
#     connection = psycopg2.connect(database='fastapi',user='postgres',password='Amin1378',host='localhost',cursor_factory=RealDictCursor)
#     cursor = connection.cursor()
#     print("--> database connection was successful")
# except Exception as e:
#     print(e)


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)